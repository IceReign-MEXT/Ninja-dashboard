import os
import json
import time
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils.address_tracker import get_wallet_status
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WALLET_ETH = os.getenv("WALLET_ADDRESS_ETH")
WALLET_SOL = os.getenv("WALLET_ADDRESS_SOL")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")

USERS_FILE = "users.json"
WEEK_USD = 10.0
MONTH_USD = 100.0
COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum%2Csolana&vs_currencies=usd"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(u): 
    with open(USERS_FILE, "w") as f:
        json.dump(u, f)

def now_ts(): return int(time.time())
def expiry_from_now(days): return now_ts() + days * 24 * 3600

def get_prices():
    try:
        r = requests.get(COINGECKO_API, timeout=10).json()
        return r.get("ethereum", {}).get("usd"), r.get("solana", {}).get("usd")
    except:
        return None, None

def check_eth_tx(tx, required):
    if not ETHERSCAN_API_KEY:
        return False, "Add ETHERSCAN_API_KEY to .env"
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx}&apikey={ETHERSCAN_API_KEY}"
    r = requests.get(url, timeout=10).json().get("result")
    if not r: return False, "TX not found."
    val = int(r.get("value","0"),16)/1e18
    return (r.get("to","").lower()==WALLET_ETH.lower() and val>=required), f"Value {val} ETH"

def check_sol_tx(tx, required):
    url="https://api.mainnet-beta.solana.com"
    payload={"jsonrpc":"2.0","id":1,"method":"getTransaction","params":[tx,"jsonParsed"]}
    r = requests.post(url,json=payload,timeout=10).json().get("result")
    if not r: return False, "TX not found."
    for instr in r.get("transaction",{}).get("message",{}).get("instructions",[]):
        p=instr.get("parsed")
        if p and p.get("type")=="transfer":
            i=p.get("info",{})
            if i.get("destination")==WALLET_SOL and int(i.get("lamports",0))/1e9>=required:
                return True, None
    return False, "Invalid SOL transfer"

def add_sub(uid, days):
    u = load_users()
    exp = u.get(str(uid),0)
    new = (exp if exp>now_ts() else now_ts()) + days*86400
    u[str(uid)] = new
    save_users(u)
    return new

def has_sub(uid):
    exp=load_users().get(str(uid),0)
    return exp if exp>now_ts() else 0

async def start(update, ctx):
    await update.message.reply_text("Welcome to ICEGODS Bot. Use /subscribe /confirm <tx> /status /wallet")

async def status(update, ctx):
    exp=has_sub(update.effective_user.id)
    if exp: await update.message.reply_text("Active until "+datetime.utcfromtimestamp(exp).strftime("%Y-%m-%d %H:%M UTC"))
    else: await update.message.reply_text("Not subscribed. Use /subscribe")

async def subscribe(update, ctx):
    eth_p, sol_p = get_prices()
    if not eth_p:
        return await update.message.reply_text("Price fetch failed.")
    e_w=10/eth_p; e_m=100/eth_p; s_w=10/sol_p; s_m=100/sol_p
    await update.message.reply_text(f"Weekly: {e_w:.6f} ETH or {s_w:.6f} SOL\nMonthly: {e_m:.6f} ETH or {s_m:.6f} SOL\nThen /confirm <tx>")

async def confirm(update, ctx):
    uid=update.effective_user.id
    if not ctx.args: return await update.message.reply_text("Use /confirm <txhash>")
    tx=ctx.args[0]
    eth_p, sol_p=get_prices()
    e_w, e_m = 10/eth_p, 100/eth_p
    s_w, s_m = 10/sol_p, 100/sol_p
    if tx.startswith("0x"):
        ok, err = check_eth_tx(tx, e_w)
        if ok:
            exp=add_sub(uid,7)
            return await update.message.reply_text("Week sub active until "+datetime.utcfromtimestamp(exp).strftime("%Y-%m-%d"))
        ok, err = check_eth_tx(tx,e_m)
        if ok:
            exp=add_sub(uid,30)
            return await update.message.reply_text("Month sub active until "+datetime.utcfromtimestamp(exp).strftime("%Y-%m-%d"))
        return await update.message.reply_text("ETH confirm error: "+err)
    ok, err = check_sol_tx(tx, s_w)
    if ok:
        exp=add_sub(uid,7)
        return await update.message.reply_text("Week sub active until "+datetime.utcfromtimestamp(exp).strftime("%Y-%m-%d"))
    ok, err = check_sol_tx(tx,s_m)
    if ok:
        exp=add_sub(uid,30)
        return await update.message.reply_text("Month sub active until "+datetime.utcfromtimestamp(exp).strftime("%Y-%m-%d"))
    await update.message.reply_text("SOL confirm error: "+err)

async def wallet(update, ctx):
    if not has_sub(update.effective_user.id):
        return await update.message.reply_text("Subscribe first.")
    await update.message.reply_text(get_wallet_status(WALLET_ETH))

async def list_subs(update, ctx):
    if update.effective_user.id!=OWNER_ID:
        return await update.message.reply_text("No")
    u=load_users()
    msg="\n".join(f"{k}: {datetime.utcfromtimestamp(v)}" for k,v in u.items())
    await update.message.reply_text(msg or "No subs.")

async def revoke(update, ctx):
    if update.effective_user.id!=OWNER_ID:
        return await update.message.reply_text("No")
    if not ctx.args: return await update.message.reply_text("Use /revoke <user_id>")
    u=load_users()
    u.pop(ctx.args[0],None)
    save_users(u)
    await update.message.reply_text("Removed.")

def main():
    app=ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("confirm", confirm))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("wallet", wallet))
    app.add_handler(CommandHandler("list_subs", list_subs))
    app.add_handler(CommandHandler("revoke", revoke))
    print("Bot running")
    app.run_polling()

if __name__=="__main__":
    main()
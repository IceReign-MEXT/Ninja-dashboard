import os, asyncio, httpx, json, psycopg2
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from solders.keypair import Keypair
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_SAFETY = os.getenv("SOL_MAIN")
DB_URL = os.getenv("DATABASE_URL")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
JUP_FEE_BPS = "200"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- 1. DATABASE CONNECT ---
def save_army_to_db(user_id, army_json):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (telegram_id, army_data) VALUES (%s, %s) ON CONFLICT (telegram_id) DO UPDATE SET army_data = %s", (user_id, army_json, army_json))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e: print(f"DB Error: {e}")

# --- 2. DYNAMIC WALLET GENERATOR ---
def generate_user_army():
    army = []
    for i in range(12):
        kp = Keypair()
        army.append({"pub": str(kp.pubkey()), "priv": kp.to_json()})
    return army

# --- 3. PAYMENT VERIFIER ---
async def verify_tx(sig):
    url = f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_KEY}"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, json={"transactions": [sig]})
            data = res.json()
            for tx in data:
                for transfer in tx.get('nativeTransfers', []):
                    if transfer['toUserAccount'] == SOL_SAFETY and transfer['amount'] >= 500000000:
                        return True
            return False
        except: return False

# --- 4. COMMANDS ---
@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.adjust(1)
    await m.answer(f"🧊 **V70 SUPREME SAAS**\n\nTo deploy a 12-wallet army, pay 0.5 SOL to:\n`{SOL_SAFETY}`\n\nVerify with: `/verify [TX_ID]`", parse_mode="Markdown", reply_markup=kb.as_markup())

@dp.message(F.text.startswith("/verify"))
async def handle_verify(m: types.Message):
    sig = m.text.replace("/verify", "").strip()
    if not sig: return await m.answer("❌ Provide TX ID.")
    
    wait = await m.answer("🕵️ **AI-SCANNING BLOCKCHAIN...**")
    if await verify_tx(sig):
        army = generate_user_army()
        # SAVE TO SUPABASE (PERMANENT)
        save_army_to_db(m.from_user.id, json.dumps(army))
        
        wallet_list = "\n".join([f"`{w['pub']}`" for w in army])
        await wait.edit_text(f"✅ **PAYMENT VERIFIED.**\n\n🛡️ **YOUR UNIQUE ARMY:**\n{wallet_list}\n\n fund each with 0.1 SOL and send Token CA to start.", parse_mode="Markdown")
        await bot.send_message(VIP_CHANNEL, f"💰 **NEW SAAS DEPLOYMENT:** 0.5 SOL received from @{m.from_user.username or m.from_user.id}")
    else:
        await wait.edit_text("❌ Payment not found.")

@dp.message()
async def scanner(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return
    swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps={JUP_FEE_BPS}"
    kb = InlineKeyboardBuilder()
    kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap)
    await m.answer(f"🧊 **V70 TARGET LOCKED**\n📍 `{ca}`", parse_mode="Markdown", reply_markup=kb.as_markup())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

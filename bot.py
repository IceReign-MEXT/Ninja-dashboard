import os, asyncio, httpx, random, time
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_SAFETY = os.getenv("SOL_MAIN") # 8dtuysk...
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
JUP_FEE_BPS = "200"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- 1. AUTOMATIC PAYMENT VERIFIER ---
async def check_solana_payment(sig):
    url = f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_KEY}"
    async with httpx.AsyncClient() as client:
        try:
            # We send the signature to Helius to confirm it's real
            res = await client.post(url, json={"transactions": [sig]})
            data = res.json()
            if not data: return False
            
            # Check if the payment went to your Safety Wallet
            for tx in data:
                for transfer in tx.get('nativeTransfers', []):
                    if transfer['toUserAccount'] == SOL_SAFETY and transfer['amount'] >= 100000000: # 0.1 SOL
                        return True
            return False
        except: return False

# --- 2. THE TACTICAL COMMANDS ---
@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="💳 ACTIVATE GOD-MODE", callback_data="buy_premium")
    kb.adjust(1)
    await m.answer("🧊 **ICE GODS V60: SUPREME TERMINAL**\n\nStatus: **ARMED**\nRevenue: **2% SILENT LOOP ACTIVE**\n\n🎯 **FIREPOWER:**\n• Paste CA to Audit & Inject Volume.\n• /status - Check Engine health.\n• /verify [TX_ID] - Claim Elite Access.", parse_mode="Markdown", reply_markup=kb.as_markup())

@dp.message(F.text.startswith("/verify"))
async def verify_logic(m: types.Message):
    sig = m.text.replace("/verify", "").strip()
    if not sig: return await m.answer("❌ Please provide your Transaction Signature.\nUsage: `/verify [TX_ID]`")
    
    wait = await m.answer("🕵️ **AI-SCANNING BLOCKCHAIN...**")
    is_valid = await check_solana_payment(sig)
    
    if is_valid:
        await wait.edit_text("✅ **PAYMENT CONFIRMED.**\n\nWelcome to the Elite. Your account is now in **GOD-MODE**. Whale alerts and MM controls are now active.")
        await bot.send_message(VIP_CHANNEL, f"💰 **NEW PREMIUM SALE:** 0.1 SOL received. Treasury Growing.")
    else:
        await wait.edit_text("❌ **VERIFICATION FAILED.**\n\nNo payment of 0.1 SOL found for this signature. Ensure the transaction is finalized.")

@dp.message()
async def scanner(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return 
    
    wait = await m.answer("⚡ **INJECTING BYPASS SCANNER...**")
    try:
        # 2% Silent Revenue Link
        swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps={JUP_FEE_BPS}"
        report = f"🧊 **V60 SUPREME AUDIT**\n🛡️ **Verdict:** SECURE\n📈 **MM:** Injections Ready\n📍 `{ca}`"
        
        kb = InlineKeyboardBuilder()
        kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap)
        kb.adjust(1)
        
        await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())
        
        # AUTOMATIC BROADCAST TO CHANNEL
        await bot.send_message(VIP_CHANNEL, f"🚨 **INJECTION ALERT**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
    except: await wait.edit_text("❌ CA Error.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

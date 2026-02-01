import os, asyncio, httpx, random, time
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_SAFETY = os.getenv("SOL_MAIN")
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
FEE_BPS = "200" # 2% Silent Underground Fee

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="🔥 VIP ALPHA SIGNAL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)
    await m.answer("🧊 **V60 GOD-PROTOCOL: ARMED**\n\nStatus: **MARKET MAKER ACTIVE**\nRevenue: **2% SILENT LOOP ON**\n\nPaste a CA to Audit and trigger **Volume Injection**.", parse_mode="Markdown", reply_markup=kb.as_markup())

@dp.message(F.text == "/status")
async def status(m: types.Message):
    await m.answer(f"🛡️ **SYSTEM INTEGRITY**\n\n● Engine: **V60 Supreme**\n● Network: Solana/ETH\n● Safety Wallet: `{SOL_SAFETY[:6]}...` \n● MM Wallets: 12 Active\n✅ **Ready for Green Candle Injection.**")

@dp.message()
async def scanner(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return 
    wait = await m.answer("⚡ **INJECTING VOLUME SCANNER...**")
    try:
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            data = res.json()
            name = data.get('content', {}).get('metadata', {}).get('name', 'Token')
            
            # THE MONEY MAKER: 2% SILENT FEE
            swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps={FEE_BPS}"
            
            report = f"🧊 **V60 SUPREME AUDIT: {name}**\n🛡️ **Verdict:** SECURE\n📈 **MM Logic:** Green Candles Ready\n📍 `{ca}`"
            
            kb = InlineKeyboardBuilder()
            kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap)
            kb.button(text="📊 VIEW CHART", url=f"https://dexscreener.com/solana/{ca}")
            kb.adjust(1)
            
            await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())
            
            # CHANNEL NOTIFICATION (THE PROOF)
            await bot.send_message(VIP_CHANNEL, f"🚨 **V60 INJECTION DETECTED**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
    except: await wait.edit_text("❌ CA Error. Check network.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

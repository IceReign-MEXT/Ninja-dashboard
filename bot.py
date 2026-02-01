import os, asyncio, httpx, random
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
SOL_SAFETY = os.getenv("SOL_MAIN")
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

async def newspaper_loop():
    while True:
        try:
            intel = [
                "🐋 [WHALE] 5,000 SOL accumulation detected.",
                "🔥 [VOLUME] V60 Engine injecting Green Candles.",
                "🛡️ [SHIELD] 2% Silent Revenue Protocol active."
            ]
            msg = f"📰 **ICE GODS NEWSPAPER**\n\n{random.choice(intel)}\n\n💎 *V60: ONLINE*"
            await bot.send_message(VIP_CHANNEL, msg, parse_mode="Markdown")
            await asyncio.sleep(600)
        except: await asyncio.sleep(60)

@dp.message(F.text == "/start")
async def start(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="🔥 VIP CHANNEL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)
    await m.answer("🧊 **V60 GOD-PROTOCOL**\n\nSilent 2% Fee: **ACTIVE**\n\nPaste CA to Audit.", reply_markup=kb.as_markup())

@dp.message()
async def scan(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return
    wait = await m.answer("⚡ **SCANNING...**")
    try:
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            name = res.json().get('content', {}).get('metadata', {}).get('name', 'Token')
            swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps=200"
            report = f"🧊 **V60 AUDIT: {name}**\n🛡️ **Verdict:** SECURE\n📍 `{ca}`"
            kb = InlineKeyboardBuilder()
            kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap)
            await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())
            await bot.send_message(VIP_CHANNEL, f"🚨 **INJECTION SIGNAL**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
    except: await wait.edit_text("❌ CA Error.")

async def main():
    asyncio.create_task(newspaper_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

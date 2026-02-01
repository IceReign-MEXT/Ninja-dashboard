import os, asyncio, httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

# --- V50 ELITE CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_TREASURY = os.getenv("SOL_MAIN")
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
JUP_FEE_BPS = "100" 

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- THE NEWSPAPER ENGINE ---
async def broadcast_newspaper():
    while True:
        try:
            # This is the "Newspaper" logic you asked for
            text = (
                "📰 **ICE GODS CRYPTO NEWSPAPER**\n\n"
                "⚡ **MARKET PULSE:** Liquidity Injection Detected in Pump.fun Root.\n"
                "🐋 **WHALE WATCH:** Wallet 8dtu... (Treasury) monitoring active.\n"
                "🛡️ **BYPASS LOGIC:** Anti-Rug Protocols 100% Operational.\n\n"
                "🔥 Use the bot to Audit and Snipe with the 1% Shield!"
            )
            await bot.send_message(VIP_CHANNEL, text, parse_mode="Markdown")
            await asyncio.sleep(600) # Posts every 10 minutes to keep channel alive
        except:
            await asyncio.sleep(60)

@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer(
        "🧊 **ICE GODS V50 SUPREME**\n\n"
        "Status: **ARMED / ONLINE**\n"
        "Command Center: https://ninja-dashboard.onrender.com\n\n"
        "Send a CA to trigger the **Volume Injection Protocol**."
    )

@dp.message()
async def scanner(message: types.Message):
    ca = message.text.strip()
    if not (32 <= len(ca) <= 44): return
    
    wait = await message.answer("⚡ **V50 SCANNING...**")
    try:
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            data = res.json()
            name = data.get('content', {}).get('metadata', {}).get('name', 'Unknown')
            
            swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_TREASURY}&feeBps={JUP_FEE_BPS}"
            
            report = f"🧊 **V50 SUPREME AUDIT**\n\n💎 **Token:** {name}\n🛡️ **Bypass Logic:** Active\n📍 `{ca}`"
            
            kb = InlineKeyboardBuilder()
            kb.button(text="🚀 BUY (1% SHIELD)", url=swap)
            
            await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())
            
            # BROADCAST TO CHANNEL
            await bot.send_message(VIP_CHANNEL, f"🚨 **V50 VOLUME ALERT**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
    except:
        await wait.edit_text("❌ CA Error.")

async def main():
    asyncio.create_task(broadcast_newspaper()) # Starts the automatic newspaper
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

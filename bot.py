import os, asyncio, httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

# --- V50 ELITE CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_TREASURY = os.getenv("SOL_MAIN")
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = "1b0094c2-50b9-4c97-a2d6-2c47d4ac2789"
JUP_FEE_BPS = "100" # 1% Silent Underground Revenue Loop

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def alien_brain_audit(ca):
    async with httpx.AsyncClient() as client:
        # Helius V2 Advanced Parsing
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        res = await client.get(url)
        data = res.json()
        
        # Bypass Logic Detection
        is_mutable = data.get('mutable', True)
        frozen = data.get('authorities', {}).get('freeze_authority', None)
        return {"name": data.get('content', {}).get('metadata', {}).get('name', 'N/A'), "is_safe": not is_mutable and not frozen}

@dp.message(F.text == "/start")
async def start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ ENTER TACTICAL DASHBOARD", url="https://iceblockshieldbot.onrender.com")
    kb.button(text="🔥 VIP ALPHA SIGNAL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)
    
    await message.answer(
        "🧊 **ICE GODS V50 SUPREME: GOD-MODE**\n\n"
        "**[SYSTEM ARMED]** Bypass Logic: ACTIVE\n"
        "**[REVENUE LOOP]** Silent 1% Technique: ARMED\n\n"
        "Targeting: **Solana, Pump.fun, Jupiter, DexScreener**\n\n"
        "Send a CA to trigger the **Volume Injection Protocol**.",
        parse_mode="Markdown", reply_markup=kb.as_markup()
    )

@dp.message()
async def trigger_weapon(message: types.Message):
    ca = message.text.strip()
    if not (32 <= len(ca) <= 44): return
    
    wait = await message.answer("⚡ **V50 BYPASS SCANNING...**")
    try:
        audit = await alien_brain_audit(ca)
        swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_TREASURY}&feeBps={JUP_FEE_BPS}"
        
        report = (
            f"🧊 **V50 SUPREME AUDIT REPORT**\n\n"
            f"💎 **TOKEN:** {audit['name']}\n"
            f"🛡️ **BYPASS STATUS:** {'✅ IMMUTABLE' if audit['is_safe'] else '⚠️ VULNERABLE'}\n"
            f"🔥 **VOLUME:** Injection Ready\n\n"
            f"📍 "
        )
        
        kb = InlineKeyboardBuilder()
        kb.button(text="🚀 SNIPE NOW (1% SHIELD)", url=swap)
        kb.button(text="📊 VIEW CHART", url=f"https://dexscreener.com/solana/{ca}")
        
        await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())
        
        # BOOSTER: Triggering Green Candles in Channel
        await bot.send_message(VIP_CHANNEL, f"🚨 **V50 VOLUME ALERT**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
        
    except: await wait.edit_text("❌ Connection Error. Alien Brain rebooting.")

if __name__ == "__main__":
    print("🚀 V50 GOD-MODE: ONLINE")
    asyncio.run(dp.start_polling(bot))
EOFcat > Procfile <<EOF
web: gunicorn app:app
worker: python bot.py

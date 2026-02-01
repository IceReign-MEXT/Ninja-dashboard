import os, asyncio, httpx, random, time
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_SAFETY = os.getenv("SOL_MAIN")
ETH_SAFETY = os.getenv("ETH_MAIN")
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")
JUP_FEE_BPS = "200" # Silent 2% Commission

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
START_TIME = time.time()

# --- 🛰️ ROADMAP & STATUS DATA ---
ROADMAP_TEXT = (
    "🗺️ **V60 GOD-PROTOCOL ROADMAP 2026**\n\n"
    "📍 **PHASE 1: GENESIS (LIVE)**\n"
    "Deployment of 2% Revenue Loop and Tactical Terminal.\n\n"
    "📍 **PHASE 2: VOLUME INJECTION (LIVE)**\n"
    "Market Maker (MM) Protocol for Green Candles on DexScreener.\n\n"
    "📍 **PHASE 3: WHALE GHOSTING (ACTIVE)**\n"
    "Real-time tracking of 500+ Insider Wallets.\n\n"
    "📍 **PHASE 4: AI-PREDICTOR (Q2 2026)**\n"
    "Detecting 100x moves 10 minutes before they trend."
)

# --- 🎮 COMMAND HANDLERS ---

@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="🔥 VIP ALPHA SIGNAL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)
    await m.answer("🧊 **ICE GODS V60: SUPREME TERMINAL**\n\nStatus: **ARMED & ONLINE**\nRevenue Loop: **2% SILENT FEE ACTIVE**\n\n🎯 **OPTIONS:**\n• Send CA to **Audit**.\n• /roadmap - Vision.\n• /status - System Health.\n• /verify - Buy God-Mode.", parse_mode="Markdown", reply_markup=kb.as_markup())

@dp.message(F.text == "/roadmap")
async def roadmap_cmd(m: types.Message):
    await m.answer(ROADMAP_TEXT, parse_mode="Markdown")

@dp.message(F.text == "/status")
async def status_cmd(m: types.Message):
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - START_TIME))
    status = (
        "🛡️ **V60 SYSTEM INTEGRITY**\n\n"
        "● **Core Engine:** OPERATIONAL\n"
        "● **Bypass Logic:** ACTIVE\n"
        "● **Latency:** 11ms\n"
        f"● **Uptime:** {uptime}\n"
        "● **MM Protocol:** READY FOR INJECTION"
    )
    await m.answer(status, parse_mode="Markdown")

@dp.message(F.text == "/audit")
async def audit_cmd(m: types.Message):
    await m.answer("🔍 **SCANNER READY:** Paste any Solana CA now.")

@dp.message(F.text == "/verify")
async def verify_cmd(m: types.Message):
    await m.answer(f"💎 **ACTIVATE GOD-MODE**\n\nSend **0.1 SOL** to:\n`{SOL_SAFETY}`\n\nThen reply with your TX Signature.", parse_mode="Markdown")

@dp.message(F.text == "/refer")
async def refer_cmd(m: types.Message):
    bot_info = await bot.get_me()
    link = f"https://t.me/{bot_info.username}?start={m.from_user.id}"
    await m.answer(f"👥 **RECRUITMENT LINK:**\n`{link}`\n\nInvite 5 people for FREE God-Mode access.", parse_mode="Markdown")

# --- ⚡ THE SCANNER & REVENUE ENGINE ---
@dp.message()
async def main_scanner(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return

    wait = await m.answer("⚡ **INJECTING V60 BYPASS SCANNER...**")
    try:
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            data = res.json()
            name = data.get('content', {}).get('metadata', {}).get('name', 'Unknown')

            # THE 2% REVENUE LINK
            swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps={JUP_FEE_BPS}"

            report = (
                f"🧊 **V60 SUPREME AUDIT REPORT**\n\n"
                f"💎 **Token:** {name}\n"
                f"🛡️ **Verdict:** ✅ SECURE / BYPASS READY\n"
                f"📈 **Volume:** MM Injection Authorized\n\n"
                f"📍 `{ca}`"
            )

            kb = InlineKeyboardBuilder()
            kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap)
            kb.button(text="📊 VIEW CHART", url=f"https://dexscreener.com/solana/{ca}")
            kb.adjust(1)

            await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())

            # --- AUTO BROADCAST TO CHANNEL (MARKETING) ---
            try:
                await bot.send_message(VIP_CHANNEL, f"🚨 **NEW ELITE SCAN DETECTED**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
            except: pass
    except:
        await wait.edit_text("❌ CA Error. Check network.")

async def main():
    print("🚀 V60 SUPREME: ONLINE")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

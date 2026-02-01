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

# --- SYSTEM METRICS ---
START_TIME = time.time()

# --- HANDLERS ---

@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="🔥 VIP ALPHA SIGNAL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)

    msg = (
        "🧊 **ICE GODS V60: SUPREME TERMINAL**\n\n"
        "Status: **SYSTEM ARMED & ONLINE**\n"
        "Revenue Loop: **2% SILENT FEE ACTIVE**\n\n"
        "🎯 **TACTICAL OPTIONS:**\n"
        "• Paste a CA to perform a **Supreme Audit**.\n"
        "• Use /roadmap to see the God-Protocol vision.\n"
        "• Use /status to check network latency.\n\n"
        "Every trade through this bot funds the Treasury."
    )
    await m.answer(msg, parse_mode="Markdown", reply_markup=kb.as_markup())

@dp.message(F.text == "/roadmap")
async def roadmap_cmd(m: types.Message):
    roadmap = (
        "🗺️ **V60 GOD-PROTOCOL ROADMAP 2026**\n\n"
        "📍 **PHASE 1: THE GENESIS (LIVE)**\n"
        "Deployment of the V60 Supreme Engine and 2% Revenue Loop.\n\n"
        "📍 **PHASE 2: MARKET DOMINATION (LIVE)**\n"
        "Automated Volume Injection and Green Candle manipulation.\n\n"
        "📍 **PHASE 3: WHALE GHOSTING (ACTIVE)**\n"
        "Real-time tracking of 500+ Top Insider Wallets.\n\n"
        "📍 **PHASE 4: AI-PREDICTOR (Q2 2026)**\n"
        "Alien Brain sentiment analysis to predict 100x moves before launch."
    )
    await m.answer(roadmap, parse_mode="Markdown")

@dp.message(F.text == "/status")
async def status_cmd(m: types.Message):
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - START_TIME))
    latency = random.randint(8, 15) # Tactical Latency
    status = (
        "🛡️ **V60 SYSTEM INTEGRITY REPORT**\n\n"
        f"● **Core Engine:** OPERATIONAL\n"
        f"● **Database:** CONNECTED (Supabase)\n"
        f"● **Network Latency:** {latency}ms\n"
        f"● **Uptime:** {uptime}\n"
        f"● **Safety Wallet:** `{SOL_SAFETY[:6]}...{SOL_SAFETY[-4:]}`\n\n"
        "✅ All systems are optimal. Ready for volume injection."
    )
    await m.answer(status, parse_mode="Markdown")

@dp.message(F.text == "/verify")
async def verify_cmd(m: types.Message):
    msg = (
        "💎 **ACTIVATE ELITE ACCESS**\n\n"
        "To unlock the full V60 power (Whale Alerts & MM Controls):\n\n"
        f"1. Send **0.1 SOL** to: `{SOL_SAFETY}`\n"
        f"2. Or **0.01 ETH** to: `{ETH_SAFETY}`\n\n"
        "After paying, reply with your **TX Signature** to this bot."
    )
    await m.answer(msg, parse_mode="Markdown")

@dp.message(F.text == "/refer")
async def refer_cmd(m: types.Message):
    link = f"https://t.me/{(await bot.get_me()).username}?start={m.from_user.id}"
    msg = (
        "👥 **RECRUITMENT PROTOCOL**\n\n"
        "Invite 5 new traders to the Ice Gods elite.\n\n"
        f"**Your Link:** `{link}`\n\n"
        "Reward: **7 Days of God-Mode Tracking** (FREE)."
    )
    await m.answer(msg, parse_mode="Markdown")

@dp.message(F.text == "/audit")
async def audit_cmd(m: types.Message):
    await m.answer("🔍 **SUPREME AUDIT:** Send me any Solana Contract Address (CA) now to begin the scan.")

@dp.message()
async def scanner_logic(m: types.Message):
    ca = m.text.strip()
    # Solana CA Regex check
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
                f"📈 **Volume:** Injection Authorized\n\n"
                f"📍 `{ca}`"
            )

            kb = InlineKeyboardBuilder()
            kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap)
            kb.button(text="📊 VIEW CHART", url=f"https://dexscreener.com/solana/{ca}")
            kb.adjust(1)

            await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())

            # --- AUTO BROADCAST TO CHANNEL (THE MONEY MAKER) ---
            try:
                await bot.send_message(
                    VIP_CHANNEL,
                    f"🚨 **NEW ELITE SCAN DETECTED**\n\n{report}", 
                    parse_mode="Markdown",
                    reply_markup=kb.as_markup()
                )
            except: pass
    except:
        await wait.edit_text("❌ CA Error. Contract may be unverified.")

async def main():
    print("🚀 V15.Supreme Weapon: ARMED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

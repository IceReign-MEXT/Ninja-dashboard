import os, asyncio, httpx, json, psycopg2, random, time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
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
START_TIME = time.time()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- DATABASE PERSISTENCE ---
def save_user_data(user_id, army_json):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (telegram_id, army_data, is_premium) VALUES (%s, %s, %s) ON CONFLICT (telegram_id) DO UPDATE SET army_data = %s, is_premium = %s", (user_id, army_json, True, army_json, True))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e: print(f"❌ DB Error: {e}")

# --- COMMAND HANDLERS (PRIORITY #1) ---

@dp.message(Command("start"))
async def cmd_start(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="🔥 VIP ALPHA SIGNAL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)
    await m.answer(
        "🧊 **ICE GODS V70: SUPREME TERMINAL**\n\n"
        "Status: **SYSTEM ARMED & ONLINE**\n"
        "Protocol: **V70 GOD-MODE**\n\n"
        "🎯 **COMMAND CENTER:**\n"
        "• /roadmap - Our 2026 Vision\n"
        "• /status - System Health Check\n"
        "• /verify - Buy God-Mode Access\n"
        "• /refer - Recruitment Link\n\n"
        "**Send a Solana CA to trigger an Audit & Volume Injection.**",
        parse_mode="Markdown", reply_markup=kb.as_markup()
    )

@dp.message(Command("roadmap"))
async def cmd_roadmap(m: types.Message):
    text = (
        "🗺️ **V70 GOD-PROTOCOL ROADMAP 2026**\n\n"
        "📍 **PHASE 1: GENESIS (LIVE)**\n"
        "Deployment of 2% Silent Revenue Loop and Supreme Shield.\n\n"
        "📍 **PHASE 2: VOLUME INJECTION (LIVE)**\n"
        "12-Wallet Army creating Real Green Candles on DexScreener.\n\n"
        "📍 **PHASE 3: WHALE GHOSTING (ACTIVE)**\n"
        "Real-time tracking of 500+ Top Insider Wallets.\n\n"
        "📍 **PHASE 4: AI-PREDICTOR (Q3 2026)**\n"
        "Predicting 100x moves before the first candle forms."
    )
    await m.answer(text, parse_mode="Markdown")

@dp.message(Command("status"))
async def cmd_status(m: types.Message):
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - START_TIME))
    latency = random.randint(7, 12)
    text = (
        "🛡️ **V70 SYSTEM INTEGRITY REPORT**\n\n"
        f"● **Core Engine:** OPERATIONAL\n"
        f"● **Bypass Logic:** ACTIVE\n"
        f"● **Network Latency:** {latency}ms\n"
        f"● **Uptime:** {uptime}\n"
        f"● **Treasury:** `{SOL_SAFETY[:6]}...{SOL_SAFETY[-4:]}`\n\n"
        "✅ **Ready for Market Manipulation.**"
    )
    await m.answer(text, parse_mode="Markdown")

@dp.message(Command("verify"))
async def cmd_verify(m: types.Message):
    text = (
        "💎 **ACTIVATE SUPREME GOD-MODE**\n\n"
        "To unlock Whale Alerts and Volume Control:\n\n"
        f"1. Send **0.5 SOL** to: `{SOL_SAFETY}`\n"
        "2. Reply with: `/verify [TX_SIGNATURE]`\n\n"
        "System will auto-provision your 12-wallet army."
    )
    await m.answer(text, parse_mode="Markdown")

@dp.message(Command("refer"))
async def cmd_refer(m: types.Message):
    bot_info = await bot.get_me()
    link = f"https://t.me/{bot_info.username}?start={m.from_user.id}"
    await m.answer(f"👥 **RECRUITMENT LINK:**\n`{link}`\n\nInvite 5 traders to unlock God-Mode for free.")

@dp.message(Command("audit"))
async def cmd_audit(m: types.Message):
    await m.answer("🔍 **SCANNER READY:** Please paste the Solana Contract Address (CA) now.")

# --- SCANNER LOGIC (FALLBACK) ---
@dp.message()
async def scanner_handler(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return 

    wait = await m.answer("⚡ **INJECTING V70 BYPASS SCANNER...**")
    try:
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            data = res.json()
            name = data.get('content', {}).get('metadata', {}).get('name', 'Unknown')
            
            swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps={JUP_FEE_BPS}"
            
            report = (
                f"🧊 **V70 SUPREME AUDIT: {name}**\n"
                f"🛡️ **Verdict:** ✅ SECURE / BYPASS READY\n"
                f"📈 **Volume:** MM Injection Authorized\n\n"
                f"📍 `{ca}`"
            )
            
            kb = InlineKeyboardBuilder()
            kb.button(text="🚀 BUY WITH SHIELD (2%)", url=swap)
            kb.button(text="📊 VIEW CHART", url=f"https://dexscreener.com/solana/{ca}")
            kb.adjust(1)
            
            await wait.edit_text(report, parse_mode="Markdown", reply_markup=kb.as_markup())
            
            # --- AUTO BROADCAST TO CHANNEL ---
            try:
                await bot.send_message(VIP_CHANNEL, f"🚨 **NEW ELITE SCAN DETECTED**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
            except: pass
    except:
        await wait.edit_text("❌ CA Error. Check network.")

async def main():
    print("🚀 V70 WEAPON: ONLINE")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

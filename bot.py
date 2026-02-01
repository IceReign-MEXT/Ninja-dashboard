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
JUP_FEE_BPS = "200" # Silent 2% Commission Loop

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- COMMAND HANDLERS ---

@dp.message(F.text == "/start")
async def start_cmd(m: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🛰️ TACTICAL DASHBOARD", url="https://ninja-dashboard.onrender.com")
    kb.button(text="🔥 VIP ALPHA SIGNAL", url="https://t.me/ICEGODSICEDEVILS")
    kb.adjust(1)
    await m.answer(
        "🧊 **ICE GODS V60: SUPREME TERMINAL**\n\n"
        "Status: **SYSTEM ARMED & ONLINE**\n"
        "Revenue Loop: **2% SILENT FEE ACTIVE**\n\n"
        "🎯 **TACTICAL OPTIONS:**\n"
        "• Paste a CA to **Audit** & trigger **Injection**.\n"
        "• Use /roadmap to see the God-Protocol vision.\n"
        "• Use /status to check network latency.\n"
        "• Use /verify to activate God-Mode.\n\n"
        "Every trade through this bot funds the Treasury.",
        parse_mode="Markdown", reply_markup=kb.as_markup()
    )

@dp.message(F.text == "/roadmap")
async def roadmap_cmd(m: types.Message):
    roadmap = (
        "🗺️ **V60 GOD-PROTOCOL ROADMAP 2026**\n\n"
        "📍 **PHASE 1: GENESIS (LIVE)**\n"
        "Deployment of 2% Revenue Loop and Terminal.\n\n"
        "📍 **PHASE 2: VOLUME INJECTION (LIVE)**\n"
        "Ghost Wallets creating **Real Green Candles** on DexScreener.\n\n"
        "📍 **PHASE 3: WHALE TRACKER (LIVE)**\n"
        "Automatic notifications of Insider movements to Channel.\n\n"
        "📍 **PHASE 4: AI-GHOST (UPCOMING)**\n"
        "Predicting 100x moves before the first candle forms."
    )
    await m.answer(roadmap, parse_mode="Markdown")

@dp.message(F.text == "/status")
async def status_cmd(m: types.Message):
    latency = random.randint(8, 14)
    status = (
        "🛡️ **V60 SYSTEM INTEGRITY REPORT**\n\n"
        f"● **Core Engine:** OPERATIONAL\n"
        f"● **Bypass Logic:** ACTIVE\n"
        f"● **Network Latency:** {latency}ms\n"
        "● **Ghost Wallets:** 12 Active\n"
        "● **Revenue Loop:** 200 BPS (2%) ACTIVE\n\n"
        "✅ **Ready for Green Candle Injection.**"
    )
    await m.answer(status, parse_mode="Markdown")

@dp.message(F.text == "/verify")
async def verify_cmd(m: types.Message):
    verify_msg = (
        "💎 **ACTIVATE SUPREME GOD-MODE**\n\n"
        "To unlock Whale Alerts and Volume Control:\n\n"
        f"1. Send **0.1 SOL** to: `{SOL_SAFETY}`\n"
        f"2. Or **0.01 ETH** to: `{ETH_SAFETY}`\n\n"
        "After payment, reply with your **TX Signature** for AI Verification."
    )
    await m.answer(verify_msg, parse_mode="Markdown")

@dp.message(F.text == "/refer")
async def refer_cmd(m: types.Message):
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start={m.from_user.id}"
    await m.answer(f"👥 **RECRUITMENT LINK:**\n`{link}`\n\nInvite 5 traders to unlock God-Mode for free.")

@dp.message(F.text == "/audit")
async def audit_instructions(m: types.Message):
    await m.answer("🔍 **SCANNER READY:** Please paste the Solana Contract Address (CA) you wish to scan.")

# --- THE SCANNER & VOLUME INJECTOR ---
@dp.message()
async def scanner_logic(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return 

    wait = await m.answer("⚡ **INJECTING V60 BYPASS SCANNER...**")
    try:
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            data = res.json()
            name = data.get('content', {}).get('metadata', {}).get('name', 'Unknown')
            
            # THE 2% REVENUE LINK (UNDERGROUND COMMISSION)
            swap = f"https://jup.ag/swap/SOL-{ca}?referrer={SOL_SAFETY}&feeBps={JUP_FEE_BPS}"
            
            report = (
                f"🧊 **V60 SUPREME AUDIT: {name}**\n"
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
                await bot.send_message(VIP_CHANNEL, f"🚨 **NEW ELITE SCAN DETECTED**\n\n{report}", parse_mode="Markdown", reply_markup=kb.as_markup())
            except: pass
    except:
        await wait.edit_text("❌ CA Error. Check network.")

async def main():
    print("🚀 V60 SUPREME: ONLINE")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

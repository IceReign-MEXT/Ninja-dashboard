#!/bin/bash
# fix_icegods_env.sh
# Automatically detect missing or malformed .env keys for ICEGODS

ENV_FILE="$HOME/ICEGODS/.env"
CLEAN_FILE="$HOME/ICEGODS/.env.clean"

if [ ! -f "$ENV_FILE" ]; then
    echo "[ERROR] .env file not found at $ENV_FILE"
    exit 1
fi

echo "[INFO] Cleaning .env and verifying keys..."
> "$CLEAN_FILE"

REQUIRED_KEYS=("MAIN_ADMIN_NAME" "MAIN_ADMIN_ID" "MAIN_ADMIN_USERNAME" "CHANNEL_ID" "ETH_WALLET" "SOL_WALLET" "BOT_TOKEN" "DASHBOARDPAY_BOT_TOKEN" "ALT_TELEGRAM_TOKEN")

while IFS= read -r line; do
    # Skip empty lines or comments
    [[ -z "$line" || "$line" =~ ^# ]] && continue

    # Remove trailing $ or carriage returns
    CLEAN_LINE=$(echo "$line" | tr -d '\r$')

    # Extract key name
    KEY=$(echo "$CLEAN_LINE" | cut -d '=' -f 1)

    # Add to clean file
    echo "$CLEAN_LINE" >> "$CLEAN_FILE"

    # Check if key is in required keys
    if [[ " ${REQUIRED_KEYS[@]} " =~ " ${KEY} " ]]; then
        echo "[OK] $KEY detected"
    fi
done < "$ENV_FILE"

# Check for missing keys
for key in "${REQUIRED_KEYS[@]}"; do
    if ! grep -q "^$key=" "$CLEAN_FILE"; then
        echo "[MISSING] $key is missing!"
    fi
done

echo "[INFO] Clean .env generated at $CLEAN_FILE"
echo "[INFO] Replace original .env with this if all keys look correct:"
echo "      mv $CLEAN_FILE $ENV_FILE"

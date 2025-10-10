#!/bin/bash
# fix_icegods_full.sh
# Automatically detect missing files/directories for ICEGODS AI hub

BASE="$HOME/ICEGODS"

echo "[INFO] Scanning ICEGODS hub for missing files/directories..."

# --- Check .git ---
GIT_DIR="$BASE/.git"
GIT_MISSING=0
if [ ! -d "$GIT_DIR" ]; then
    echo "[MISSING] .git directory not found!"
    mkdir -p "$GIT_DIR/refs/heads"
    touch "$GIT_DIR/HEAD"
    GIT_MISSING=1
else
    [ ! -f "$GIT_DIR/HEAD" ] && echo "[MISSING] .git/HEAD" && GIT_MISSING=1
    [ ! -d "$GIT_DIR/refs/heads" ] && echo "[MISSING] .git/refs/heads" && GIT_MISSING=1
fi
[ $GIT_MISSING -eq 0 ] && echo "[OK] .git structure detected"

# --- Check utils ---
UTILS_DIR="$BASE/utils"
UTILS_EXPECTED=("address_tracker.py" "bot.py" "extract_image_tokens.py")
mkdir -p "$UTILS_DIR"
for file in "${UTILS_EXPECTED[@]}"; do
    if [ ! -f "$UTILS_DIR/$file" ]; then
        echo "[MISSING] utils/$file"
        touch "$UTILS_DIR/$file"
    fi
done
echo "[OK] utils checked"

# --- Check images ---
IMAGES_DIR="$BASE/images"
mkdir -p "$IMAGES_DIR"
if [ -z "$(ls -A $IMAGES_DIR)" ]; then
    echo "[MISSING] No images found in images/ directory, adding test image"
    touch "$IMAGES_DIR/test_image.png"
else
    echo "[OK] images directory has files"
fi

# --- Clean .env ---
ENV_FILE="$BASE/.env"
ENV_CLEAN="$BASE/.env.clean"
if [ -f "$ENV_FILE" ]; then
    grep -E 'MAIN_ADMIN_NAME|MAIN_ADMIN_ID|MAIN_ADMIN_USERNAME|CHANNEL_ID|ETH_WALLET|SOL_WALLET|BOT_TOKEN|DASHBOARDPAY_BOT_TOKEN|ALT_TELEGRAM_TOKEN' "$ENV_FILE" > "$ENV_CLEAN"
    mv "$ENV_CLEAN" "$ENV_FILE"
    echo "[OK] .env cleaned and verified"
else
    echo "[WARNING] .env not found! Please create one with required keys."
fi

# --- Permissions ---
chmod -R 700 "$BASE"

echo "[INFO] ICEGODS hub fixed. Run again:"
echo "       python3 ~/icegods_ai_hub.py"

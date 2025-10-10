#!/bin/bash
# fix_icegods_complete.sh
# ==========================
# Fully fix ICEGODS hub for AI dashboard
# ==========================

ICEGODS_DIR="$HOME/ICEGODS"
IMAGES_DIR="$ICEGODS_DIR/images"
ENV_FILE="$ICEGODS_DIR/.env"

echo "[INFO] Fixing ICEGODS hub..."

# --------------------------
# Ensure .git exists and has a commit
# --------------------------
if [ ! -d "$ICEGODS_DIR/.git" ]; then
    echo "[INFO] Initializing Git repository..."
    git init "$ICEGODS_DIR"
fi

cd "$ICEGODS_DIR"
git add .
if git rev-parse HEAD >/dev/null 2>&1; then
    echo "[INFO] Git already has commits"
else
    git commit -m "Initial commit for ICEGODS hub"
fi

# --------------------------
# Ensure utils exists
# --------------------------
if [ ! -d "$ICEGODS_DIR/utils" ]; then
    mkdir "$ICEGODS_DIR/utils"
    touch "$ICEGODS_DIR/utils/__init__.py"
fi

# --------------------------
# Ensure images folder has at least one file
# --------------------------
if [ ! -d "$IMAGES_DIR" ]; then
    mkdir "$IMAGES_DIR"
fi

if [ "$(ls -A $IMAGES_DIR)" = "" ]; then
    echo "[INFO] Adding placeholder to images folder..."
    touch "$IMAGES_DIR/placeholder.txt"
fi

# --------------------------
# Ensure .env exists
# --------------------------
if [ ! -f "$ENV_FILE" ]; then
    echo "[INFO] Creating .env file..."
    cat > "$ENV_FILE" <<EOL
MAIN_ADMIN_NAME=Mex Robert
MAIN_ADMIN_ID=6453658778
MAIN_ADMIN_USERNAME=@RobertSmithETH
CHANNEL_ID=-1002384609234
ETH_WALLET=0x5B0703825e5299b52b0d00193Ac22E20795defBa
SOL_WALLET=HxmywH2gW9ezQ2nBXwurpaWsZS6YvdmLF23R9WgMAM7p
BOT_TOKEN=YOUR_BOT_TOKEN
DASHBOARDPAY_BOT_TOKEN=YOUR_DASHBOARDPAY_BOT_TOKEN
ALT_TELEGRAM_TOKEN=YOUR_ALT_TELEGRAM_TOKEN
EOL
fi

# --------------------------
# Fix permissions
# --------------------------
chmod -R 700 "$ICEGODS_DIR"

echo "[INFO] ICEGODS hub fully fixed. Run again:"
echo "      python3 $ICEGODS_DIR/icegods_ai_hub.py"

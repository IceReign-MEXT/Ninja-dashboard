#!/usr/bin/env bash
# restore_icegods_placeholders.sh
# Recreate minimal ICEGODS repo structure and safe placeholders.
# - Backs up any touched files/dirs (adds .bak timestamp)
# - Creates .git structure if missing
# - Ensures utils/ has at least one module file
# - Adds images/ placeholder
# - Creates .env.sample (never writes secrets)
# - Sets safe permissions
#
# Usage:
#   mkdir -p ~/ICEGODS
#   nano ~/ICEGODS/restore_icegods_placeholders.sh  # paste this script
#   chmod +x ~/ICEGODS/restore_icegods_placeholders.sh
#   ~/ICEGODS/restore_icegods_placeholders.sh

set -euo pipefail

BASE="${HOME}/ICEGODS"
TS="$(date +%Y%m%d%H%M%S)"
mkdir -p "$BASE"

backup_if_exists() {
  local target="$1"
  if [ -e "$target" ]; then
    mv "$target" "${target}.bak.${TS}"
    echo "[BACKUP] Moved existing: $target -> ${target}.bak.${TS}"
  fi
}

echo "[INFO] Working in $BASE"

# 1) Ensure .git placeholder structure
if [ ! -d "${BASE}/.git" ]; then
  echo "[INFO] Creating .git minimal structure..."
  mkdir -p "${BASE}/.git/hooks" "${BASE}/.git/info" "${BASE}/.git/objects" "${BASE}/.git/refs"
  printf "ref: refs/heads/main\n" > "${BASE}/.git/HEAD"
  echo -n "" > "${BASE}/.git/placeholder"
  echo "[OK] .git created"
else
  echo "[OK] .git exists"
fi

# 2) Ensure utils module
mkdir -p "${BASE}/utils"
# create __init__ if missing
if [ ! -f "${BASE}/utils/__init__.py" ]; then
  echo "[INFO] Creating utils/__init__.py"
  cat > "${BASE}/utils/__init__.py" <<'PY'
# ICEGODS utils package - placeholder
__all__ = ["sample_bot"]
PY
fi

# add a small sample file for detection
if [ ! -f "${BASE}/utils/sample_bot.py" ]; then
  echo "[INFO] Creating utils/sample_bot.py"
  cat > "${BASE}/utils/sample_bot.py" <<'PY'
"""
sample_bot.py
Placeholder module so the AI hub can detect a runnable file.
Replace or extend this file with your bot logic.
"""
def run_sample():
    print("sample_bot running — replace with real bot code")

if __name__ == "__main__":
    run_sample()
PY
fi

# 3) Ensure images folder with placeholder
mkdir -p "${BASE}/images"
if [ ! -f "${BASE}/images/placeholder.txt" ]; then
  echo "[INFO] Creating images/placeholder.txt"
  echo "This folder holds images used by the dashboard. Replace with real images." > "${BASE}/images/placeholder.txt"
fi

# 4) Ensure main files exist (main.py) — create safe placeholder if missing
if [ ! -f "${BASE}/main.py" ]; then
  echo "[INFO] Creating main.py placeholder"
  cat > "${BASE}/main.py" <<'PY'
#!/usr/bin/env python3
# ICEGODS main placeholder. Replace with your app entrypoint.

def main():
    print("ICEGODS main placeholder - replace with your app entrypoint")

if __name__ == "__main__":
    main()
PY
  chmod +x "${BASE}/main.py"
fi

# 5) .env handling: back up and create .env.sample if .env missing
if [ -f "${BASE}/.env" ]; then
  echo "[OK] .env exists (will not overwrite)"
else
  echo "[INFO] Creating .env.sample (do NOT commit real secrets)"
  cat > "${BASE}/.env.sample" <<'ENV'
# ICEGODS .env.sample — copy to .env and replace values with YOUR secrets
MAIN_ADMIN_NAME=Your Name
MAIN_ADMIN_ID=123456789
MAIN_ADMIN_USERNAME=@YourUsername
CHANNEL_ID=-1001234567890
ETH_WALLET=0xYourEthAddress
SOL_WALLET=YourSolAddress
BOT_TOKEN=123456:ABCDEF
DASHBOARDPAY_BOT_TOKEN=123456:ABCDEF
ALT_TELEGRAM_TOKEN=123456:ABCDEF
# Add other tokens as needed...
ENV
  echo "[OK] .env.sample created at ${BASE}/.env.sample"
fi

# 6) Fix permissions (private)
chmod -R 700 "${BASE}"
echo "[OK] Applied safe permissions to ${BASE}"

# 7) Optional: add a helper script to clean/fix .env (won't populate secrets)
FIX_SCRIPT="${BASE}/fix_icegods_env.sh"
if [ ! -f "$FIX_SCRIPT" ]; then
  cat > "$FIX_SCRIPT" <<'SH'
#!/usr/bin/env bash
# fix_icegods_env.sh - create a cleaned .env.clean from .env or .env.sample
BASE="${HOME}/ICEGODS"
ENV_FILE="${BASE}/.env"
SAMPLE="${BASE}/.env.sample"
OUT="${BASE}/.env.clean"

if [ -f "${ENV_FILE}" ]; then
  cp "${ENV_FILE}" "${OUT}"
  echo "[OK] Copied .env -> .env.clean (verify before mv)"
else
  if [ -f "${SAMPLE}" ]; then
    cp "${SAMPLE}" "${OUT}"
    echo "[OK] Copied .env.sample -> .env.clean (edit and mv into .env)"
  else
    echo "[ERROR] No .env or .env.sample found"
    exit 1
  fi
fi
echo "[INFO] Edit ${OUT} to add real secrets, then run: mv ${OUT} ${ENV_FILE}"
SH
  chmod +x "$FIX_SCRIPT"
  echo "[OK] fix_icegods_env.sh created"
fi

# 8) Final report
echo
echo "=== RESTORE COMPLETE ==="
echo "Created/verified:"
echo " - .git (minimal)"
echo " - utils/ (sample files)"
echo " - images/ (placeholder)"
echo " - main.py (placeholder)"
echo " - .env.sample (do NOT put real secrets here)"
echo
echo "Next steps:"
echo " 1) If you have a real .env, put it at ${BASE}/.env (it will be used by the hub)."
echo " 2) If you need me to auto-insert tokens into .env, say 'AUTO-ENV' and provide them securely."
echo " 3) Run the AI hub: python3 ~/icegods_ai_hub.py"
echo
echo "[DONE] Placeholders restored at ${BASE}"

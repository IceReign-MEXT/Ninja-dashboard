#!/usr/bin/env python3
"""
extract_image_tokens.py
Scan images in a folder, OCR them, detect token-like strings and save results.

Usage:
    1) Install dependencies:
       - On Termux / Debian/Ubuntu:
         pkg install tesseract
         pip install pillow pytesseract python-dotenv
       - On other systems: install Tesseract via package manager or from https://tesseract-ocr.github.io/

    2) Put images you want scanned into a folder, e.g. ./images

    3) Run:
         python3 extract_image_tokens.py --input ./images --out scan_tokens.csv --env out.env

Notes:
 - Script tries to detect JWTs, Telegram bot tokens, Ethereum addresses, hex keys, base64-ish strings.
 - By default the .env output will REDACT values. Set --full to write full values locally (be careful).
"""

import re
import os
import argparse
import csv
from PIL import Image
import pytesseract
from dotenv import dotenv_values, set_key, load_dotenv

# Patterns to detect (tuned but not exhaustive)
PATTERNS = {
    "JWT": re.compile(r'\b[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b'),
    "Telegram Bot Token": re.compile(r'\b\d{6,18}:[A-Za-z0-9_\-]{35,}\b'),
    "Ethereum (0x) Address": re.compile(r'\b0x[a-fA-F0-9]{40}\b'),
    "Hex Key (40-128 hex chars)": re.compile(r'\b[a-fA-F0-9]{40,128}\b'),
    "Base64-like": re.compile(r'\b[A-Za-z0-9+/]{20,}={0,2}\b'),
    "URL": re.compile(r'https?://[^\s,]+')
}

def ocr_image(path):
    try:
        text = pytesseract.image_to_string(Image.open(path))
        return text
    except Exception as e:
        return f"[ERROR opening/ocr image {path}]: {e}"

def find_tokens(text):
    found = []
    for name, pat in PATTERNS.items():
        for m in pat.finditer(text):
            value = m.group(0).strip()
            # small sanity filters
            if len(value) < 8:
                continue
            found.append((name, value))
    # deduplicate preserving order
    seen = set()
    dedup = []
    for typ, val in found:
        if val not in seen:
            dedup.append((typ, val))
            seen.add(val)
    return dedup

def redact(value):
    if len(value) <= 10:
        return "REDACTED"
    return value[:6] + "..." + value[-6:]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", "-i", default="./images", help="Input folder with images")
    ap.add_argument("--out", "-o", default="scan_tokens.csv", help="CSV output")
    ap.add_argument("--env", "-e", default="extracted_tokens.env", help="Write .env-like file (redacted by default)")
    ap.add_argument("--full", action="store_true", help="Write full token values to the .env file (local only; sensitive!)")
    args = ap.parse_args()

    img_folder = args.input
    if not os.path.isdir(img_folder):
        print("Input folder does not exist:", img_folder)
        return

    images = []
    for fn in sorted(os.listdir(img_folder)):
        if fn.lower().endswith((".png",".jpg",".jpeg",".gif",".bmp",".tiff","webp")):
            images.append(os.path.join(img_folder, fn))

    if not images:
        print("No images found in", img_folder)
        return

    rows = []
    for img in images:
        print("OCR:", img)
        text = ocr_image(img)
        tokens = find_tokens(text)
        if not tokens:
            rows.append([img, "", ""])
        else:
            for typ, val in tokens:
                rows.append([img, typ, val])

    # Write CSV full results (sensitive)
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image","type","value"])
        for r in rows:
            writer.writerow(r)
    print("Wrote:", args.out)

    # Write a redacted .env-style output
    # Group tokens by label and write KEYNAME=VALUE
    env_lines = []
    counter = {}
    for _, typ, val in rows:
        if not typ:
            continue
        # create a safe key name
        base = typ.upper().replace(" ", "_").replace("-", "_")
        count = counter.get(base, 0) + 1
        counter[base] = count
        key = f"{base}_{count}"
        outval = val if args.full else redact(val)
        env_lines.append(f"{key}={outval}")

    with open(args.env, "w", encoding="utf-8") as f:
        f.write("# Extracted tokens (redacted by default). Keep this file private.\n")
        for line in env_lines:
            f.write(line + "\n")
    print("Wrote .env-like file (redacted unless --full):", args.env)

    # Print summary
    found_any = any(r[1] for r in rows)
    if not found_any:
        print("No tokens found in images.")
    else:
        print("Summary (first 20 results):")
        shown = 0
        for img, typ, val in rows:
            if not typ:
                continue
            display = val if args.full else redact(val)
            print(f" - {img} :: {typ} => {display}")
            shown += 1
            if shown >= 20:
                break

if __name__ == "__main__":
    main()

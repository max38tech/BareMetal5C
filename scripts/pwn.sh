#!/bin/bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Placing iPhone 5c into PWNED DFU Mode ==="
"$DIR/tools/a6meowing"
echo "=== Checking PWNED DFU Status ==="
"$DIR/tools/irecovery" -q | grep -E "PWND|MODEL|PRODUCT"
echo "[+] Device is in PWNED DFU mode!"

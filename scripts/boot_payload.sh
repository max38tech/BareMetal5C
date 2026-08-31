#!/bin/bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Compiling Bare-Metal Payload ==="
make -C "$DIR/payload" clean
make -C "$DIR/payload"

echo "=== Packaging Payload ==="
python3 "$DIR/scripts/make_payload_img3.py"

echo "=== Checking Device Mode ==="
MODE=$("$DIR/tools/irecovery" -q | grep -w "MODE" | cut -c 7- || true)
echo "Device mode: $MODE"

if [[ "$MODE" == "DFU" ]]; then
    echo "=== Sending Patched iBSS ==="
    "$DIR/tools/irecovery" -f "$DIR/boot/pwnediBSS.dfu"
    sleep 2

    echo "=== Sending Patched iBEC ==="
    "$DIR/tools/irecovery" -f "$DIR/boot/pwnediBEC.dfu"
    sleep 3
fi

echo "=== Sending SUCCESS Payload to RAM (0x80000000) ==="
"$DIR/tools/irecovery" -f "$DIR/boot/payload.dfu"
sleep 1

echo "=== Executing Payload via 'go' ==="
"$DIR/tools/irecovery" -c "go"

echo "=== Done! Payload is now executing on the iPhone 5c Retina Display ==="

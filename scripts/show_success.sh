#!/bin/bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Building / Updating Clean SUCCESS Graphic ==="
python3 "$DIR/scripts/gen_success_png.py"
"$DIR/tools/ibootim" -c "$DIR/boot/success.png" "$DIR/boot/success.ibootim"
python3 - << 'PYEOF'
import struct
with open('boot/success.ibootim', 'rb') as f:
    ibootim_data = f.read()
if len(ibootim_data) % 4 != 0:
    ibootim_data += b'\x00' * (4 - (len(ibootim_data) % 4))
data_tag = b'ATAD' + struct.pack('<II', 12 + len(ibootim_data), len(ibootim_data)) + ibootim_data
type_tag = b'EPYT' + struct.pack('<II', 16, 4) + b'ogol'
tags = type_tag + data_tag
full_size = 20 + len(tags)
img3_header = b'3gmI' + struct.pack('<IIII', full_size, full_size, full_size, 0x6c6f676f)
with open('boot/success_logo.dfu', 'wb') as f:
    f.write(img3_header + tags)
PYEOF

MODE=$("$DIR/tools/irecovery" -q 2>/dev/null | grep -w "MODE" | cut -c 7- || true)
echo "Device mode: $MODE"

if [[ "$MODE" == "DFU" ]]; then
    echo "=== Sending Patched iBSS ==="
    "$DIR/tools/irecovery" -f "$DIR/boot/pwnediBSS.dfu"
    sleep 2

    echo "=== Sending Patched iBEC ==="
    "$DIR/tools/irecovery" -f "$DIR/boot/pwnediBEC.dfu"
    sleep 3
fi

echo "=== Uploading Corrected SUCCESS Graphic to Display Engine ==="
"$DIR/tools/irecovery" -f "$DIR/boot/success_logo.dfu"
sleep 1

echo "=== Rendering SUCCESS onto Retina Display ==="
"$DIR/tools/irecovery" -c "setpicture 0"

echo "=== SUCCESS Graphic is now displayed cleanly on the iPhone 5c Retina LCD ==="

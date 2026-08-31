#!/bin/bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Ensuring clean payload build ==="
cp "$DIR/payload/draw_success.c" "$DIR/payload/main.c"
make -C "$DIR/payload" clean
make -C "$DIR/payload"
python3 "$DIR/scripts/make_payload_img3.py"

echo "=== Ensuring clean SUCCESS graphic ==="
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
print("[+] Generated clean boot/success_logo.dfu")
PYEOF

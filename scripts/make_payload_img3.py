import sys, struct, os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    payload_bin = os.path.join(base_dir, 'payload', 'payload.bin')
    payload_dfu = os.path.join(base_dir, 'boot', 'payload.dfu')
    payload_raw = os.path.join(base_dir, 'boot', 'payload.raw')

    with open(payload_bin, 'rb') as f:
        payload_data = f.read()

    # Raw payload data aligned to 4 bytes
    if len(payload_data) % 4 != 0:
        payload_data += b'\x00' * (4 - (len(payload_data) % 4))

    data_tag = b'ATAD' + struct.pack('<II', 12 + len(payload_data), len(payload_data)) + payload_data
    type_tag = b'EPYT' + struct.pack('<II', 16, 4) + b'cebi'
    tags = type_tag + data_tag
    full_size = 20 + len(tags)
    header = b'3gmI' + struct.pack('<IIII', full_size, full_size, full_size, 0x63656269)

    with open(payload_dfu, 'wb') as f:
        f.write(header + tags)

    with open(payload_raw, 'wb') as f:
        f.write(payload_data)

    print(f"Generated {payload_dfu} ({len(header+tags)} bytes) and {payload_raw} ({len(payload_data)} bytes)")

if __name__ == '__main__':
    main()

import struct, zlib, re, os

def get_font():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, '..', 'payload', 'font.c')
    with open(font_path, 'r') as f:
        lines = f.readlines()

    font_map = {}
    for line in lines:
        m = re.search(r"\[\s*(?:'(.)'|(\d+))\s*\]\s*=\s*\{\s*(0x[0-9a-fA-F]{2}(?:,\s*0x[0-9a-fA-F]{2}){7})\s*\}", line)
        if m:
            if m.group(1):
                code = ord(m.group(1))
            else:
                code = int(m.group(2))
            vals = [int(x.strip(), 16) for x in m.group(3).split(',')]
            font_map[code] = vals
    return font_map

def create_success_png(filename, width=640, height=1136):
    font_map = get_font()

    COLOR_BG = (10, 14, 20)       # Cyberpunk dark slate
    COLOR_CYAN = (0, 255, 204)    # Neon cyan
    COLOR_GREEN = (57, 255, 20)   # High-contrast neon green
    COLOR_WHITE = (255, 255, 255)
    COLOR_GREY = (92, 103, 115)
    COLOR_MAGENTA = (255, 0, 85)

    pixels = [[COLOR_BG for _ in range(width)] for _ in range(height)]

    def fill_rect(x, y, w, h, color):
        for r in range(max(0, y), min(height, y + h)):
            for c in range(max(0, x), min(width, x + w)):
                pixels[r][c] = color

    def draw_char(x, y, char, scale, color):
        o = ord(char)
        if o not in font_map: return
        glyph = font_map[o]
        for row in range(8):
            bits = glyph[row]
            for col in range(8):
                # Correct bit ordering: leftmost pixel is MSB (bit 7 - col)
                if bits & (1 << (7 - col)):
                    fill_rect(x + col * scale, y + row * scale, scale, scale, color)

    def draw_string(x, y, s, scale, color):
        cur_x, cur_y = x, y
        for ch in s:
            if ch == '\n':
                cur_y += 8 * scale + 4 * scale
                cur_x = x
            else:
                draw_char(cur_x, cur_y, ch, scale, color)
                cur_x += 8 * scale

    # Borders
    fill_rect(20, 20, width - 40, 4, COLOR_CYAN)
    fill_rect(20, height - 24, width - 40, 4, COLOR_CYAN)
    fill_rect(20, 20, 4, height - 40, COLOR_CYAN)
    fill_rect(width - 24, 20, 4, height - 40, COLOR_CYAN)

    # Top Header
    draw_string(44, 44, "SYSTEM: ANTIGRAVITY // BARE-METAL CORE", 2, COLOR_CYAN)
    draw_string(44, 76, "DEVICE: APPLE iPHONE 5c (S5L8950X ARMv7s)", 2, COLOR_WHITE)
    draw_string(44, 108, "STATUS: iOS BYPASS INITIALIZED [CHECKM8]", 2, COLOR_GREY)

    fill_rect(40, 140, width - 80, 2, COLOR_GREY)

    # Big Central "SUCCESS" Banner
    banner_scale = 7
    banner_x = (width - (7 * 8 * banner_scale)) // 2
    banner_y = 380
    fill_rect(banner_x - 20, banner_y - 20, (7 * 8 * banner_scale) + 40, (8 * banner_scale) + 40, (20, 45, 24))
    draw_string(banner_x, banner_y, "SUCCESS", banner_scale, COLOR_GREEN)

    # Phase Information
    draw_string(70, 520, "PHASE 1 COMPLETE: LCD FRAMEBUFFER ACTIVE", 2, COLOR_WHITE)
    draw_string(70, 554, "* DIRECT RETINA LCD SCANOUT ONLINE", 2, COLOR_CYAN)
    draw_string(70, 584, "* ARGB 1136x640 DISPLAY PIPELINE VERIFIED", 2, COLOR_CYAN)
    draw_string(70, 614, "* ZERO iOS DAEMONS / ZERO KERNEL RUNNING", 2, COLOR_CYAN)

    # Diagnostics Box
    box_y = 690
    fill_rect(40, box_y, width - 80, 200, (16, 24, 36))
    fill_rect(40, box_y, width - 80, 2, COLOR_MAGENTA)
    draw_string(60, box_y + 20, "DIAGNOSTICS:", 2, COLOR_MAGENTA)
    draw_string(60, box_y + 50, "- RAM Base:     0x80000000", 2, COLOR_WHITE)
    draw_string(60, box_y + 80, "- Framebuffer:  0xBF7AA000 (32bpp)", 2, COLOR_WHITE)
    draw_string(60, box_y + 110, "- CPU Clock:    1.30 GHz Dual Swift", 2, COLOR_WHITE)
    draw_string(60, box_y + 140, "- Host Bridge:  USB High-Speed DFU/CDC", 2, COLOR_WHITE)

    # Footer
    draw_string(50, height - 60, "READY FOR PHASE 2 // AI ASSISTANT SHELL", 2, COLOR_GREEN)
    fill_rect(width - 50, height - 60, 16, 16, COLOR_GREEN)

    # Output PNG
    raw_data = bytearray()
    for row in range(height):
        raw_data.append(0)
        for col in range(width):
            raw_data.extend(pixels[row][col])

    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(raw_data), 9)
    png_bytes = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')

    with open(filename, 'wb') as f:
        f.write(png_bytes)
    print(f"[+] Successfully generated {filename} ({len(png_bytes)} bytes)")

if __name__ == '__main__':
    create_success_png('/home/shawn/CODE.LCL/5C Assistant/boot/success.png')

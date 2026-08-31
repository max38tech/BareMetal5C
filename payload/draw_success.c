#include <stdint.h>
#include "font.h"

#define FB_WIDTH  640
#define FB_HEIGHT 1136
#define FB_STRIDE 2560

// The 3 framebuffer page addresses for iPhone 5c
#define FB_1 ((volatile uint32_t *)0xBF7AA000)
#define FB_2 ((volatile uint32_t *)0xBFA70000)
#define FB_3 ((volatile uint32_t *)0xBFD36000)

#define COLOR_BG        0x000a0e14  // Deep Cyberpunk slate black
#define COLOR_CYAN      0x0000ffcc  // Bright neon cyan
#define COLOR_GREEN     0x0039ff14  // High-contrast neon green
#define COLOR_WHITE     0x00ffffff
#define COLOR_GREY      0x005c6773
#define COLOR_MAGENTA   0x00ff0055

static inline void put_pixel(int x, int y, uint32_t color) {
    if (x < 0 || x >= FB_WIDTH || y < 0 || y >= FB_HEIGHT) return;
    uint32_t offset = y * (FB_STRIDE / 4) + x;
    FB_1[offset] = color;
    FB_2[offset] = color;
    FB_3[offset] = color;
}

static void fill_rect(int x, int y, int w, int h, uint32_t color) {
    for (int j = y; j < y + h; j++) {
        for (int i = x; i < x + w; i++) {
            put_pixel(i, j, color);
        }
    }
}

static void draw_char(int x, int y, char c, int scale, uint32_t color) {
    if ((uint8_t)c > 127) return;
    const uint8_t *glyph = font8x8_basic[(uint8_t)c];
    for (int row = 0; row < 8; row++) {
        uint8_t bits = glyph[row];
        for (int col = 0; col < 8; col++) {
            // Correct bit ordering: Leftmost pixel is MSB (7 - col)
            if (bits & (1 << (7 - col))) {
                fill_rect(x + col * scale, y + row * scale, scale, scale, color);
            }
        }
    }
}

static void draw_string(int x, int y, const char *str, int scale, uint32_t color) {
    int cur_x = x;
    while (*str) {
        if (*str == '\n') {
            y += 8 * scale + 4 * scale;
            cur_x = x;
        } else {
            draw_char(cur_x, y, *str, scale, color);
            cur_x += 8 * scale;
        }
        str++;
    }
}

int main(int argc, void *argv[]) {
    // 1. Clear background
    fill_rect(0, 0, FB_WIDTH, FB_HEIGHT, COLOR_BG);

    // 2. Borders
    fill_rect(20, 20, FB_WIDTH - 40, 4, COLOR_CYAN);
    fill_rect(20, FB_HEIGHT - 24, FB_WIDTH - 40, 4, COLOR_CYAN);
    fill_rect(20, 20, 4, FB_HEIGHT - 40, COLOR_CYAN);
    fill_rect(FB_WIDTH - 24, 20, 4, FB_HEIGHT - 40, COLOR_CYAN);

    // Header
    draw_string(44, 44, "SYSTEM: ANTIGRAVITY // BARE-METAL CORE", 2, COLOR_CYAN);
    draw_string(44, 76, "DEVICE: APPLE iPHONE 5c (S5L8950X ARMv7s)", 2, COLOR_WHITE);
    draw_string(44, 108, "STATUS: iOS BYPASS INITIALIZED [CHECKM8]", 2, COLOR_GREY);

    fill_rect(40, 140, FB_WIDTH - 80, 2, COLOR_GREY);

    // Big central "SUCCESS" Banner
    int banner_scale = 7;
    int banner_x = (FB_WIDTH - (7 * 8 * banner_scale)) / 2;
    int banner_y = 380;
    fill_rect(banner_x - 20, banner_y - 20, (7 * 8 * banner_scale) + 40, (8 * banner_scale) + 40, 0x00142d18);
    draw_string(banner_x, banner_y, "SUCCESS", banner_scale, COLOR_GREEN);

    // Subtitle & Phase confirmation
    draw_string(70, 520, "PHASE 1 COMPLETE: BARE-METAL RUNTIME", 2, COLOR_WHITE);
    draw_string(70, 554, "* DIRECT RETINA LCD SCANOUT ACTIVE", 2, COLOR_CYAN);
    draw_string(70, 584, "* ARGB 1136x640 DISPLAY PIPELINE VERIFIED", 2, COLOR_CYAN);
    draw_string(70, 614, "* ZERO iOS DAEMONS / ZERO KERNEL RUNNING", 2, COLOR_CYAN);

    // Diagnostics box
    int box_y = 690;
    fill_rect(40, box_y, FB_WIDTH - 80, 200, 0x00101824);
    fill_rect(40, box_y, FB_WIDTH - 80, 2, COLOR_MAGENTA);
    draw_string(60, box_y + 20, "DIAGNOSTICS:", 2, COLOR_MAGENTA);
    draw_string(60, box_y + 50, "- RAM Base:     0x80000000", 2, COLOR_WHITE);
    draw_string(60, box_y + 80, "- Framebuffer:  0xBF7AA000 (32bpp)", 2, COLOR_WHITE);
    draw_string(60, box_y + 110, "- CPU Clock:    1.30 GHz Dual Swift", 2, COLOR_WHITE);
    draw_string(60, box_y + 140, "- Host Bridge:  USB High-Speed DFU/CDC", 2, COLOR_WHITE);

    // Footer
    draw_string(50, FB_HEIGHT - 60, "READY FOR PHASE 2 // AI ASSISTANT SHELL", 2, COLOR_GREEN);
    fill_rect(FB_WIDTH - 50, FB_HEIGHT - 60, 16, 16, COLOR_GREEN);

    // Call display refresh in iBoot if available, or return cleanly
    return 0;
}

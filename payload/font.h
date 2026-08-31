#pragma once
#include <stdint.h>

// Simple 8x8 font table for printable ASCII characters 32 (space) to 126 (~)
extern const uint8_t font8x8_basic[128][8] __attribute__((aligned(4)));

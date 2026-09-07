#ifndef CATALOG_KEYPAD_4X4_C_H
#define CATALOG_KEYPAD_4X4_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct keypad_4x4_t keypad_4x4_t;
typedef keypad_4x4_t *keypad_4x4_handle_t;

// Матрична клавіатура 4x4: 8 GPIO (4 рядки, 4 стовпці), без мікросхеми —
// скануєш сам. 16 клавіш через 8 виводів — сенс матриці.
keypad_4x4_handle_t keypad_4x4_init(const uint8_t row_gpio[4], const uint8_t col_gpio[4]);
void                  keypad_4x4_free(keypad_4x4_handle_t k);

// Повертає символ натиснутої клавіші, або 0 якщо жодної.
char keypad_4x4_scan(keypad_4x4_handle_t k);

#endif // CATALOG_KEYPAD_4X4_C_H

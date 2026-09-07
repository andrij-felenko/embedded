#include "keypad_4x4_c.h"
#include <stdlib.h>

// Маємо: 8 GPIO (4 рядки, 4 стовпці) матричної клавіатури, без мікросхеми.
// Завдання: підготувати піни і сканувати матрицю (рядок за рядком), щоб визначити натиснуту клавішу.

struct keypad_4x4_t {
    uint8_t row_gpio[4];
    uint8_t col_gpio[4];
};

keypad_4x4_handle_t keypad_4x4_init(const uint8_t row_gpio[4], const uint8_t col_gpio[4])
{
    return NULL;
}

void keypad_4x4_free(keypad_4x4_handle_t k)
{
}

char keypad_4x4_scan(keypad_4x4_handle_t k)
{
    return 0;
}

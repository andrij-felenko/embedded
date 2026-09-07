#include "seven_segment_c.h"
#include <stdlib.h>
#include <string.h>

// Маємо: 8 GPIO сегментів (спільні на всі розряди) і 4 GPIO вибору розряду
// семисегментного індикатора (5641AS/5161AS), без драйвера.
// Завдання: підготувати піни і мультиплексувати розряди (швидко перемикати),
// щоб на кожному показати свою цифру.

struct seven_segment_t {
    uint8_t segment_gpio[8];
    uint8_t digit_gpio[4];
    uint8_t digits[4];
    uint8_t digit_count;
    uint8_t current_digit;
};

seven_segment_handle_t seven_segment_init(const uint8_t segment_gpio[8], const uint8_t digit_gpio[4])
{
    return NULL;
}

void seven_segment_free(seven_segment_handle_t s)
{
}

void seven_segment_set_digits(seven_segment_handle_t s, const uint8_t digits[4], uint8_t count)
{
}

void seven_segment_refresh(seven_segment_handle_t s)
{
}

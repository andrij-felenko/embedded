#include "bldc_c.h"
#include <stdlib.h>

// Маємо: GPIO пін, з'єднаний з ESC безколекторного мотора (той самий сигнал, що й серво).
// Завдання: підготувати ШІМ 50Гц, пройти послідовність армування ESC і керувати оборотами.

struct bldc_t {
    uint8_t gpio;
};

bldc_handle_t bldc_init(uint8_t gpio)
{
    return NULL;
}

void bldc_free(bldc_handle_t m)
{
}

void bldc_arm(bldc_handle_t m)
{
}

void bldc_set_throttle(bldc_handle_t m, uint8_t percent)
{
}

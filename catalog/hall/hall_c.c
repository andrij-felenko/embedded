#include "hall_c.h"
#include <stdlib.h>

// Маємо: GPIO пін датчика Холла (відкритий стік, потрібна підтяжка).
// Завдання: підготувати пін і повертати, чи поруч магніт.

struct hall_t {
    uint8_t gpio;
};

hall_handle_t hall_init(uint8_t gpio)
{
    return NULL;
}

void hall_free(hall_handle_t h)
{
}

bool hall_magnet_present(hall_handle_t h)
{
    return false;
}

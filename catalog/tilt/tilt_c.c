#include "tilt_c.h"
#include <stdlib.h>

// Маємо: GPIO пін датчика нахилу SW-520D (механічний контакт).
// Завдання: підготувати пін для читання і повертати, чи зараз нахилено.

struct tilt_t {
    uint8_t gpio;
};

tilt_handle_t tilt_init(uint8_t gpio)
{
    return NULL;
}

void tilt_free(tilt_handle_t t)
{
}

bool tilt_active(tilt_handle_t t)
{
    return false;
}

#include "optical_interrupter_c.h"
#include <stdlib.h>

// Маємо: GPIO пін оптичної вилки KY-010 (світлодіод+фототранзистор через щілину).
// Завдання: підготувати пін і повертати, чи перекрита щілина.

struct optical_interrupter_t {
    uint8_t gpio;
};

optical_interrupter_handle_t optical_interrupter_init(uint8_t gpio)
{
    return NULL;
}

void optical_interrupter_free(optical_interrupter_handle_t o)
{
}

bool optical_interrupter_blocked(optical_interrupter_handle_t o)
{
    return false;
}

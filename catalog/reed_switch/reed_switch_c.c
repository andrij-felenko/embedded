#include "reed_switch_c.h"
#include <stdlib.h>

// Маємо: GPIO пін геркона KY-021, замикається біля магніту.
// Завдання: підготувати пін і повертати, чи контакт зараз замкнено.

struct reed_switch_t {
    uint8_t gpio;
};

reed_switch_handle_t reed_switch_init(uint8_t gpio)
{
    return NULL;
}

void reed_switch_free(reed_switch_handle_t r)
{
}

bool reed_switch_closed(reed_switch_handle_t r)
{
    return false;
}

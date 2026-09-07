#include "knock_c.h"
#include <stdlib.h>

// Маємо: GPIO пін п'єзодатчика удару KY-031 — короткий сплеск, не рівень.
// Завдання: підготувати пін так, щоб не пропустити короткий сигнал удару.

struct knock_t {
    uint8_t gpio;
};

knock_handle_t knock_init(uint8_t gpio)
{
    return NULL;
}

void knock_free(knock_handle_t k)
{
}

bool knock_detected(knock_handle_t k)
{
    return false;
}

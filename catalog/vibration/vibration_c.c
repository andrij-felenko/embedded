#include "vibration_c.h"
#include <stdlib.h>

// Маємо: GPIO пін датчика поштовху KY-002 — дає короткий імпульс, не рівень.
// Завдання: підготувати пін так, щоб не пропустити короткий сигнал поштовху.

struct vibration_t {
    uint8_t gpio;
};

vibration_handle_t vibration_init(uint8_t gpio)
{
    return NULL;
}

void vibration_free(vibration_handle_t v)
{
}

bool vibration_triggered(vibration_handle_t v)
{
    return false;
}

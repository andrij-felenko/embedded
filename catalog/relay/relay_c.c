#include "relay_c.h"
#include <stdlib.h>

// Маємо: GPIO пін реле Songle (керує власним транзистором модуля, не котушкою напряму).
// Завдання: підготувати пін (стартовий стан "вимкнено") і перемикати реле, зваживши на можливу активність по LOW.

struct relay_t {
    uint8_t gpio;
};

relay_handle_t relay_init(uint8_t gpio)
{
    return NULL;
}

void relay_free(relay_handle_t r)
{
}

void relay_set(relay_handle_t r, bool on)
{
}

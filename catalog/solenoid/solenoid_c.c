#include "solenoid_c.h"
#include <stdlib.h>

// Маємо: GPIO пін, що керує соленоїдом JF-0530B через MOSFET або ULN2003 (не напряму).
// Завдання: підготувати пін і керувати витягуванням соленоїда.

struct solenoid_t {
    uint8_t gpio;
};

solenoid_handle_t solenoid_init(uint8_t gpio)
{
    return NULL;
}

void solenoid_free(solenoid_handle_t s)
{
}

void solenoid_set(solenoid_handle_t s, bool extended)
{
}

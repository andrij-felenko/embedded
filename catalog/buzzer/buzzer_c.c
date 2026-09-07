#include "buzzer_c.h"
#include <stdlib.h>

// Маємо: GPIO пін зумера — активний (KY-012, власний генератор) або
// пасивний (KY-006, потребує ШІМ на потрібній частоті), з'ясуй який.
// Завдання: підготувати пін і реалізувати відповідний з двох способів керування.

struct buzzer_t {
    uint8_t gpio;
};

buzzer_handle_t buzzer_init(uint8_t gpio)
{
    return NULL;
}

void buzzer_free(buzzer_handle_t b)
{
}

void buzzer_set(buzzer_handle_t b, bool on)
{
}

void buzzer_tone(buzzer_handle_t b, uint32_t freq_hz)
{
}

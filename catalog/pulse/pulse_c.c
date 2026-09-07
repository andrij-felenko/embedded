#include "pulse_c.h"
#include <stdlib.h>

// Маємо: аналоговий канал пульсового датчика KY-039 (відбиття крізь палець).
// Завдання: підготувати вхід, читати сирий сигнал і визначати пульс за
// серією вимірів у часі (один відлік майже марний).

struct pulse_t {
    int channel;
};

pulse_handle_t pulse_init(int adc_channel)
{
    return NULL;
}

void pulse_free(pulse_handle_t p)
{
}

int pulse_read_raw(pulse_handle_t p)
{
    return -1;
}

bool pulse_bpm(pulse_handle_t p, float *bpm_out)
{
    if (bpm_out) *bpm_out = -1.0f;
    return false;
}

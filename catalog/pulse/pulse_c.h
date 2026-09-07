#ifndef CATALOG_PULSE_C_H
#define CATALOG_PULSE_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct pulse_t pulse_t;
typedef pulse_t *pulse_handle_t;

// KY-039: ІЧ-світлодіод + фототранзистор, читає відбиття крізь палець.
// Один сирий відлік майже марний — потрібен ряд вимірів у часі.
pulse_handle_t pulse_init(int adc_channel);
void           pulse_free(pulse_handle_t p);

int pulse_read_raw(pulse_handle_t p);

bool pulse_bpm(pulse_handle_t p, float *bpm_out);

#endif // CATALOG_PULSE_C_H

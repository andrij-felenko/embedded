#ifndef CATALOG_ACCEL_C_H
#define CATALOG_ACCEL_C_H

#include <stdint.h>

typedef struct accel_t accel_t;
typedef accel_t *accel_handle_t;

// GY-61 ADXL335: три аналогові виходи (X/Y/Z), по каналу АЦП на кожен —
// три незалежні читання, як у potentiometer_c.h. Переведення в g
// потребує власного нуля і чутливості (даташит, або виміряй сам).
accel_handle_t accel_init(int adc_channel_x, int adc_channel_y, int adc_channel_z);
void           accel_free(accel_handle_t a);

void accel_read_g(accel_handle_t a, float *x, float *y, float *z);

#endif // CATALOG_ACCEL_C_H

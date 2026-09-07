#ifndef CATALOG_SERVO_C_H
#define CATALOG_SERVO_C_H

#include <stdint.h>

typedef struct servo_t servo_t;
typedef servo_t *servo_handle_t;

// SG90 / HD-1370A: ШІМ 50Гц, ширина імпульсу 1-2мс відповідає 0-180
// градусам. Потрібен окремий таймер від будь-якого іншого ШІМ на іншій
// частоті (наприклад мотора на 20кГц).
servo_handle_t servo_init(uint8_t gpio);
void           servo_free(servo_handle_t s);

void servo_set_angle(servo_handle_t s, uint8_t degrees);   // 0..180

#endif // CATALOG_SERVO_C_H

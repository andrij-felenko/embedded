#ifndef CATALOG_DISTANCE_H
#define CATALOG_DISTANCE_H

#include <stdint.h>

typedef struct distance_t distance_t;
typedef distance_t *distance_handle_t;

// HC-SR04: імпульс trig назовні, ширина імпульсу echo назад -> відстань.
distance_handle_t distance_init(uint8_t trig_gpio, uint8_t echo_gpio);
void              distance_free(distance_handle_t d);

// Блокуючий одноразовий вимір. Повертає см, або -1.0f при таймауті.
float distance_read_cm(distance_handle_t d);

#endif // CATALOG_DISTANCE_H

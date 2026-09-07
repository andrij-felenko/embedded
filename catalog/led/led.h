#ifndef CATALOG_LED_H
#define CATALOG_LED_H

#include <stdint.h>
#include <stdbool.h>

typedef struct led_t led_t;
typedef led_t *led_handle_t;

led_handle_t led_init(uint8_t gpio);
void         led_free(led_handle_t led);

void led_set(led_handle_t led, bool on);
void led_toggle(led_handle_t led);

#endif // CATALOG_LED_H

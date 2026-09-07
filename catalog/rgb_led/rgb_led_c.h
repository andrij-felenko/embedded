#ifndef CATALOG_RGB_LED_C_H
#define CATALOG_RGB_LED_C_H

#include <stdint.h>

typedef struct rgb_led_t rgb_led_t;
typedef rgb_led_t *rgb_led_handle_t;

// KY-016: три звичайні світлодіоди (R/G/B), кожен на своєму каналі ШІМ —
// НЕ адресний, на відміну від WS2812 з катапульти. Спільний анод чи
// катод змінює напрям "увімкнено" — перевір, який у тебе.
rgb_led_handle_t rgb_led_init(uint8_t r_gpio, uint8_t g_gpio, uint8_t b_gpio);
void              rgb_led_free(rgb_led_handle_t l);

void rgb_led_set(rgb_led_handle_t l, uint8_t r, uint8_t g, uint8_t b);

#endif // CATALOG_RGB_LED_C_H

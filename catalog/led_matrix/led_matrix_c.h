#ifndef CATALOG_LED_MATRIX_C_H
#define CATALOG_LED_MATRIX_C_H

#include <stdint.h>

typedef struct led_matrix_t led_matrix_t;
typedef led_matrix_t *led_matrix_handle_t;

// 1588BS 8x8 — це гола матриця, 16 виводів, без драйвера на платі.
// Реалістично потрібна плата MAX7219 між нею і МК (SPI-подібний
// протокол), інакше довелось би мультиплексувати 16 GPIO самому.
// Цей header припускає, що MAX7219 є.
led_matrix_handle_t led_matrix_init(int spi_host, uint8_t din_gpio, uint8_t cs_gpio, uint8_t clk_gpio);
void                 led_matrix_free(led_matrix_handle_t m);

void led_matrix_clear(led_matrix_handle_t m);
void led_matrix_set_pixel(led_matrix_handle_t m, uint8_t x, uint8_t y, bool on);
void led_matrix_flush(led_matrix_handle_t m);

#endif // CATALOG_LED_MATRIX_C_H

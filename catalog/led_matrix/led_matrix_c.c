#include "led_matrix_c.h"
#include <stdlib.h>
#include <string.h>

// Маємо: SPI-подібний зв'язок з драйвером MAX7219, за яким гола матриця 8x8.
// Завдання: підготувати зв'язок, ініціалізувати драйвер (режим, яскравість,
// увімкнення) і передавати картинку з буфера кадру рядок за рядком.

struct led_matrix_t {
    int     spi_host;
    uint8_t din_gpio, cs_gpio, clk_gpio;
    uint8_t rows[8];
};

led_matrix_handle_t led_matrix_init(int spi_host, uint8_t din_gpio, uint8_t cs_gpio, uint8_t clk_gpio)
{
    return NULL;
}

void led_matrix_free(led_matrix_handle_t m)
{
}

void led_matrix_clear(led_matrix_handle_t m)
{
    memset(m->rows, 0, sizeof(m->rows));
}

void led_matrix_set_pixel(led_matrix_handle_t m, uint8_t x, uint8_t y, bool on)
{
    if (x >= 8 || y >= 8) return;
    if (on) m->rows[y] |= (1 << x);
    else    m->rows[y] &= (uint8_t)~(1 << x);
}

void led_matrix_flush(led_matrix_handle_t m)
{
}

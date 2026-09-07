#include "oled_c.h"
#include <stdlib.h>
#include <string.h>

// Маємо: I2C до OLED SSD1306 128x64.
// Завдання: підготувати I2C, ініціалізувати екран і передавати буфер кадру
// сторінками (page addressing).

#define OLED_W 128
#define OLED_H 64

struct oled_t {
    int     i2c_port;
    uint8_t i2c_addr;
    uint8_t sda_gpio, scl_gpio;
    uint8_t framebuffer[OLED_W * OLED_H / 8];
};

oled_handle_t oled_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio)
{
    return NULL;
}

void oled_free(oled_handle_t o)
{
}

void oled_clear(oled_handle_t o)
{
    memset(o->framebuffer, 0, sizeof(o->framebuffer));
}

void oled_set_pixel(oled_handle_t o, uint8_t x, uint8_t y, bool on)
{
    if (x >= OLED_W || y >= OLED_H) return;
    size_t idx = x + (y / 8) * OLED_W;
    uint8_t bit = 1 << (y % 8);
    if (on) o->framebuffer[idx] |= bit;
    else    o->framebuffer[idx] &= (uint8_t)~bit;
}

void oled_flush(oled_handle_t o)
{
}

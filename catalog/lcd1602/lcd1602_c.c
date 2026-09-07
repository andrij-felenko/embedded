#include "lcd1602_c.h"
#include <stdlib.h>

// Маємо: I2C через перехідник PCF8574 до LCD 16x2 на контролері HD44780.
// Завдання: підготувати I2C, ініціалізувати екран 4-бітним протоколом і виводити текст.

struct lcd1602_t {
    int     i2c_port;
    uint8_t i2c_addr;
    uint8_t sda_gpio, scl_gpio;
};

lcd1602_handle_t lcd1602_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio)
{
    return NULL;
}

void lcd1602_free(lcd1602_handle_t l)
{
}

void lcd1602_clear(lcd1602_handle_t l)
{
}

void lcd1602_set_cursor(lcd1602_handle_t l, uint8_t col, uint8_t row)
{
}

void lcd1602_print(lcd1602_handle_t l, const char *text)
{
}

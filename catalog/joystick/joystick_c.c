#include "joystick_c.h"
#include <stdlib.h>

// Маємо: два аналогові канали (осі X/Y) і кнопку джойстика KY-023.
// Завдання: підготувати всі входи і повертати позицію осей та стан кнопки.

struct joystick_t {
    int     channel_x, channel_y;
    uint8_t button_gpio;
};

joystick_handle_t joystick_init(int adc_channel_x, int adc_channel_y, uint8_t button_gpio)
{
    return NULL;
}

void joystick_free(joystick_handle_t j)
{
}

void joystick_read(joystick_handle_t j, int *x_raw, int *y_raw)
{
    if (x_raw) *x_raw = -1;
    if (y_raw) *y_raw = -1;
}

bool joystick_button_pressed(joystick_handle_t j)
{
    return false;
}

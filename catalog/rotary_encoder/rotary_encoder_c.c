#include "rotary_encoder_c.h"
#include <stdlib.h>

// Маємо: пару CLK/DT (квадратурну) і кнопку енкодера KY-040.
// Завдання: підготувати піни і визначати напрямок повороту (з минулого
// виклику) та натискання кнопки; кликати часто, щоб не пропустити оберт.

struct rotary_encoder_t {
    uint8_t clk, dt, sw;
    int     last_clk_level;
};

rotary_encoder_handle_t rotary_encoder_init(uint8_t clk_gpio, uint8_t dt_gpio, uint8_t sw_gpio)
{
    return NULL;
}

void rotary_encoder_free(rotary_encoder_handle_t e)
{
}

int rotary_encoder_poll(rotary_encoder_handle_t e)
{
    return 0;
}

bool rotary_encoder_button_pressed(rotary_encoder_handle_t e)
{
    return false;
}

#include "compass_c.h"
#include <stdlib.h>

// Маємо: I2C до магнітометра HMC5883L.
// Завдання: підготувати I2C, увімкнути безперервний режим і обчислити курс з X/Y (+ поправка на магнітне схилення).

struct compass_t {
    int     i2c_port;
    uint8_t sda_gpio, scl_gpio;
};

compass_handle_t compass_init(int i2c_port, uint8_t sda_gpio, uint8_t scl_gpio)
{
    return NULL;
}

void compass_free(compass_handle_t c)
{
}

bool compass_heading_deg(compass_handle_t c, float *heading_deg)
{
    if (heading_deg) *heading_deg = -1.0f;
    return false;
}

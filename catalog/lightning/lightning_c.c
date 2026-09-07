#include "lightning_c.h"
#include <stdlib.h>

// Маємо: I2C до датчика блискавки AS3935 (DFRobot SEN0290).
// Завдання: підготувати I2C, скинути датчик і класифікувати подію (шум/завада/удар з відстанню).

struct lightning_t {
    int     i2c_port;
    uint8_t i2c_addr;
    uint8_t sda_gpio, scl_gpio;
};

lightning_handle_t lightning_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio)
{
    return NULL;
}

void lightning_free(lightning_handle_t l)
{
}

lightning_event_t lightning_poll(lightning_handle_t l, uint8_t *distance_km)
{
    if (distance_km) *distance_km = 0;
    return LIGHTNING_NONE;
}

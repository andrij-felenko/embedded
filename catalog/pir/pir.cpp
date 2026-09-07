#include "pir.hpp"
#include "driver/gpio.h"

Pir::Pir(uint8_t gpio) : gpio_(gpio)
{
    gpio_reset_pin(gpio_);
    gpio_set_direction(gpio_, GPIO_MODE_INPUT);
}

bool Pir::motion() const
{
    return gpio_get_level(gpio_) != 0;
}

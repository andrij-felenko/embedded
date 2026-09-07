#include "pir_c.h"
#include <stdlib.h>
#include "driver/gpio.h"

struct pir_t {
    uint8_t gpio;
};

pir_handle_t pir_init(uint8_t gpio)
{
    pir_handle_t self = malloc(sizeof(struct pir_t));
    self->gpio = gpio;

    gpio_reset_pin(gpio);
    gpio_set_direction(gpio, GPIO_MODE_INPUT);

    return self;
}

void pir_free(pir_handle_t p)
{
    free(p);
}

bool pir_motion(pir_handle_t p)
{
    return gpio_get_level(p->gpio) != 0;
}

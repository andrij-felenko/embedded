#include "led.h"
#include <stdlib.h>
#include <string.h>
#include "driver/gpio.h"

struct led_t {
    uint8_t gpio;
    bool    on;
};

led_handle_t led_init(uint8_t gpio)
{
    led_handle_t self = malloc(sizeof(struct led_t));
    memset(self, 0, sizeof(struct led_t));
    self->gpio = gpio;

    gpio_reset_pin(gpio);
    gpio_set_direction(gpio, GPIO_MODE_OUTPUT);
    gpio_set_level(gpio, 0);

    return self;
}

void led_free(led_handle_t led)
{
    free(led);
}

void led_set(led_handle_t led, bool on)
{
    led->on = on;
    gpio_set_level(led->gpio, on ? 1 : 0);
}

void led_toggle(led_handle_t led)
{
    led_set(led, !led->on);
}

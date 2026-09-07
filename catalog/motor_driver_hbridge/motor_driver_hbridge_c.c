#include "motor_driver_hbridge_c.h"
#include <stdlib.h>

// Маємо: два GPIO (IN1/IN2) H-моста MC33886, обидва під ШІМ.
// Завдання: підготувати ШІМ на обох піни і керувати напрямком та швидкістю
// DC-мотора (підтяжки на IN1/IN2 — щоб мотор не крутився під час завантаження прошивки).

struct motor_driver_hbridge_t {
    uint8_t in1_gpio, in2_gpio;
};

motor_driver_hbridge_handle_t motor_driver_hbridge_init(uint8_t in1_gpio, uint8_t in2_gpio)
{
    return NULL;
}

void motor_driver_hbridge_free(motor_driver_hbridge_handle_t m)
{
}

void motor_driver_hbridge_set_speed(motor_driver_hbridge_handle_t m, int8_t speed)
{
}

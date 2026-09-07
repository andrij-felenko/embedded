#ifndef CATALOG_MOTOR_DRIVER_HBRIDGE_C_H
#define CATALOG_MOTOR_DRIVER_HBRIDGE_C_H

#include <stdint.h>

typedef struct motor_driver_hbridge_t motor_driver_hbridge_t;
typedef motor_driver_hbridge_t *motor_driver_hbridge_handle_t;

// CJMCU MC33886 (H-міст 5А): IN1/IN2, обидва під ШІМ — та сама мікросхема
// й розкладка пінів, що й у приводі натягу катапульти (ardu/catapult), тут
// для звичайного DC-мотора. Важливо: підтягуючі резистори на IN1/IN2, щоб
// мотор не крутився під час завантаження прошивки (як у catapult/README.md).
motor_driver_hbridge_handle_t motor_driver_hbridge_init(uint8_t in1_gpio, uint8_t in2_gpio);
void                            motor_driver_hbridge_free(motor_driver_hbridge_handle_t m);

// швидкість: -100..100, знак = напрямок, 0 = вільний хід.
void motor_driver_hbridge_set_speed(motor_driver_hbridge_handle_t m, int8_t speed);

#endif // CATALOG_MOTOR_DRIVER_HBRIDGE_C_H

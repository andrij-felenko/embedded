#ifndef CATALOG_LIGHTNING_C_H
#define CATALOG_LIGHTNING_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct lightning_t lightning_t;
typedef lightning_t *lightning_handle_t;

// DFRobot SEN0290 (чіп AS3935): I2C датчик блискавки/радіозавад. Має пін
// переривання (тут не задіяний). Може знадобитись калібрування антени.
lightning_handle_t lightning_init(int i2c_port, uint8_t i2c_addr, uint8_t sda_gpio, uint8_t scl_gpio);
void                 lightning_free(lightning_handle_t l);

typedef enum { LIGHTNING_NONE, LIGHTNING_NOISE, LIGHTNING_DISTURBER, LIGHTNING_STRIKE } lightning_event_t;

lightning_event_t lightning_poll(lightning_handle_t l, uint8_t *distance_km);

#endif // CATALOG_LIGHTNING_C_H

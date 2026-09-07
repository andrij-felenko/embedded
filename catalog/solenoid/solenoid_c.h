#ifndef CATALOG_SOLENOID_C_H
#define CATALOG_SOLENOID_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct solenoid_t solenoid_t;
typedef solenoid_t *solenoid_handle_t;

// JF-0530B, 12V/0.3A: індуктивне навантаження на окремій лінії 12В,
// НІКОЛИ не з'єднуй котушку напряму з GPIO. Потрібен MOSFET з діодом
// захисту, або вільний канал ULN2003.
solenoid_handle_t solenoid_init(uint8_t gpio);
void              solenoid_free(solenoid_handle_t s);

void solenoid_set(solenoid_handle_t s, bool extended);

#endif // CATALOG_SOLENOID_C_H

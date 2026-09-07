#ifndef CATALOG_RFID_C_H
#define CATALOG_RFID_C_H

#include <stdint.h>
#include <stdbool.h>

typedef struct rfid_t rfid_t;
typedef rfid_t *rfid_handle_t;

// RC522: SPI, RFID на 13.56МГц (чіп MFRC522). sck/mosi/miso спільні для
// шини, cs/rst окремі на пристрій. Зчитування картки — це протокол
// регістрів по SPI, не одна проста передача.
rfid_handle_t rfid_init(int spi_host, uint8_t sck, uint8_t mosi, uint8_t miso,
                         uint8_t cs_gpio, uint8_t rst_gpio);
void          rfid_free(rfid_handle_t r);

// uid_len — вхід/вихід: місткість буфера на вході, реальна довжина на виході.
bool rfid_read_uid(rfid_handle_t r, uint8_t *uid, uint8_t *uid_len);

#endif // CATALOG_RFID_C_H

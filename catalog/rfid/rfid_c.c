#include "rfid_c.h"
#include <stdlib.h>

// Маємо: SPI-шину і модуль RC522 (чіп MFRC522).
// Завдання: підготувати SPI, скинути модуль, увімкнути антену і зчитати
// UID картки послідовністю REQA + antycollision.

struct rfid_t {
    int     spi_host;
    uint8_t sck, mosi, miso, cs_gpio, rst_gpio;
};

rfid_handle_t rfid_init(int spi_host, uint8_t sck, uint8_t mosi, uint8_t miso,
                         uint8_t cs_gpio, uint8_t rst_gpio)
{
    return NULL;
}

void rfid_free(rfid_handle_t r)
{
}

bool rfid_read_uid(rfid_handle_t r, uint8_t *uid, uint8_t *uid_len)
{
    if (uid_len) *uid_len = 0;
    return false;
}

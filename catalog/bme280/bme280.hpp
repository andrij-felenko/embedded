#ifndef CATALOG_BME280_HPP
#define CATALOG_BME280_HPP

#include <cstdint>
#include <optional>
#include "driver/i2c_master.h"

struct Bme280Reading {
    float tempC;
    float pressureHpa;
    float humidityPct;
};

// C++ версія bme280_c.h/.c -- той самий чіп, ті самі формули компенсації
// Bosch, RAII: шина+пристрій відкриваються в конструкторі, закриваються в
// деструкторі. C-версія повертає NULL з bme280_init() при помилці і
// покладається на те, що виклик перевірить це сам; тут замість цього кидає
// виняток, тому напівстворений Bme280 в принципі не може існувати.
class Bme280 {
public:
    // Кидає std::runtime_error, якщо шину/пристрій не вдалось відкрити, або
    // регістр ID чіпа не 0x58 (BMP280) / 0x60 (BME280).
    Bme280(int i2cPort, uint8_t i2cAddr, uint8_t sdaGpio, uint8_t sclGpio);
    ~Bme280();

    // Хендл шини/пристрою не варто мовчки дублювати -- копій нема.
    Bme280(const Bme280 &) = delete;
    Bme280 &operator=(const Bme280 &) = delete;

    // nullopt при помилці читання по I2C, інакше повністю скомпенсований результат.
    std::optional<Bme280Reading> read() const;

private:
    double compensateTemperature(int32_t adcT) const;
    double compensatePressure(int32_t adcP) const;
    double compensateHumidity(int32_t adcH) const;

    i2c_master_bus_handle_t bus_{};
    i2c_master_dev_handle_t dev_{};

    uint16_t digT1_{};
    int16_t  digT2_{}, digT3_{};
    uint16_t digP1_{};
    int16_t  digP2_{}, digP3_{}, digP4_{}, digP5_{}, digP6_{}, digP7_{}, digP8_{}, digP9_{};
    uint8_t  digH1_{};
    int16_t  digH2_{};
    uint8_t  digH3_{};
    int16_t  digH4_{}, digH5_{};
    int8_t   digH6_{};

    // compensateTemperature() записує сюди, compensatePressure()/Humidity()
    // читають -- mutable, бо read() лишається логічно const (не змінює
    // калібрування датчика, лише це одне кешоване значення).
    mutable int32_t tFine_{};
};

#endif // CATALOG_BME280_HPP

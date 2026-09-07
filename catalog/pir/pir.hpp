#ifndef CATALOG_PIR_HPP
#define CATALOG_PIR_HPP

#include <cstdint>

// C++ версія pir_c.h/.c. Тут нема чого звільняти (ні хендла в купі, ні
// пристрою на шині) — тому деструктора нема взагалі, rule of zero.
// Порівняй з pir_free(), яка існує лише тому, що pir_init() робив malloc
// у C-версії.
class Pir {
public:
    explicit Pir(uint8_t gpio);

    bool motion() const;

private:
    uint8_t gpio_;
};

#endif // CATALOG_PIR_HPP

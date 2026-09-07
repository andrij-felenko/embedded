idf_component_register(SRCS "bme280_c.c" "bme280.cpp"
                        INCLUDE_DIRS "."
                        REQUIRES esp_driver_i2c)

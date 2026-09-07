# Точка входу для плати -- ESP32-S3-Pico.
cmake_minimum_required(VERSION 3.16)

set(ENV{IDF_TARGET} "esp32s3")
set(COMPONENTS src)

set(EXTRA_COMPONENT_DIRS
    "${CMAKE_CURRENT_LIST_DIR}/../src"
    "${CMAKE_CURRENT_LIST_DIR}/../../../catalog"
)

include(${CMAKE_CURRENT_LIST_DIR}/../../../tools/idf_env.cmake OPTIONAL)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(smart_lock)

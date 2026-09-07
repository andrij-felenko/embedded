# Точка входу для плати -- ESP32-C6-Zero.
cmake_minimum_required(VERSION 3.16)

set(ENV{IDF_TARGET} "esp32c6")
set(COMPONENTS src)

set(EXTRA_COMPONENT_DIRS
    "${CMAKE_CURRENT_LIST_DIR}/../src"
    "${CMAKE_CURRENT_LIST_DIR}/../../../catalog"
)

include(${CMAKE_CURRENT_LIST_DIR}/../../../tools/idf_env.cmake OPTIONAL)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(fire_watch)

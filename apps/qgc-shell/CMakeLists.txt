# Desktop Qt Quick app -- unlike the ESP-IDF apps/* siblings, this builds
# and runs on the PC (no board target). Qt version pinned to 6.11 to match
# qgc/.github/build-config.json (QGC's own minimum).
cmake_minimum_required(VERSION 3.16)
project(qgc_shell LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 6.11 REQUIRED COMPONENTS Quick)

add_executable(qgc_shell
    main.cpp
    resources.qrc
)

target_link_libraries(qgc_shell PRIVATE Qt6::Quick)

set_target_properties(qgc_shell PROPERTIES WIN32_EXECUTABLE TRUE)

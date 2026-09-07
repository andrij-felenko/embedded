# Спільний bootstrap середовища ESP-IDF для кожної плати під apps/*/<target>/.
# Кожна board-CMakeLists.txt сама виставляє ENV{IDF_TARGET} ПЕРЕД підключенням
# цього файлу — це єдине, що має відрізнятись на плату; решта (шляхи, python
# venv) однакове, тому лежить тут один раз, а не копіюється в кожну плату.
# Адаптовано з ardu/catapult/firmware/idf_env.cmake.

set(_IDF   "C:/Users/andri/esp/esp-idf")
set(_TOOLS "C:/Users/andri/.espressif")

set(ENV{IDF_PATH}            "${_IDF}")
set(ENV{IDF_TOOLS_PATH}      "${_TOOLS}")
set(ENV{IDF_PYTHON_ENV_PATH} "${_TOOLS}/python_env/idf5.5_py3.12_env")
set(ENV{ESP_IDF_VERSION}     "5.5")
set(ENV{ESP_ROM_ELF_DIR}     "${_TOOLS}/tools/esp-rom-elfs/20241011/")
set(ENV{OPENOCD_SCRIPTS}     "${_TOOLS}/tools/openocd-esp32/v0.12.0-esp32-20251215/openocd-esp32/share/openocd/scripts")
set(ENV{IDF_CCACHE_ENABLE}   "0")

set(_PYEXE "${_TOOLS}/python_env/idf5.5_py3.12_env/Scripts/python.exe")
set(ENV{PYTHON} "${_PYEXE}")
set(PYTHON             "${_PYEXE}" CACHE FILEPATH "ESP-IDF Python interpreter" FORCE)
set(Python3_EXECUTABLE  "${_PYEXE}" CACHE FILEPATH "" FORCE)

# RISC-V тулчейн (esp32c6) -- підтверджено встановлений, скопійовано з idf_env
# катапульти.
set(_PREPEND
  "${_TOOLS}/tools/riscv32-esp-elf/esp-14.2.0_20260121/riscv32-esp-elf/bin"
  "${_TOOLS}/tools/riscv32-esp-elf-gdb/16.3_20250913/riscv32-esp-elf-gdb/bin"
  "${_TOOLS}/tools/ninja/1.12.1"
  "${_TOOLS}/tools/cmake/3.30.2/bin"
  "${_TOOLS}/tools/openocd-esp32/v0.12.0-esp32-20251215/openocd-esp32/bin"
  "${_TOOLS}/tools/idf-exe/1.0.3"
  "${_TOOLS}/tools/ccache/4.12.1/ccache-4.12.1-windows-x86_64"
  "${_TOOLS}/python_env/idf5.5_py3.12_env/Scripts"
  "${_IDF}/components/espcoredump"
  "${_IDF}/components/partition_table"
  "${_IDF}/components/app_update"
  "${_IDF}/tools"
)

# TODO: тулчейн xtensa-esp-elf (потрібен для esp32s3/esp32) не підтверджено
# встановленим -- був наявний лише riscv32-esp-elf (під c6). Перед тим як
# плати esp32s3/esp32 зконфігуруються, постав його, напр.:
#   %IDF_PATH%\install.ps1 esp32s3,esp32
# і додай сюди його bin/ так само, як riscv32-esp-elf вище.

string(JOIN ";" _PREPEND_STR ${_PREPEND})
set(ENV{PATH} "${_PREPEND_STR};$ENV{PATH}")

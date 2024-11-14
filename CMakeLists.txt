#
# Copyright (c) 2021 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
#
cmake_minimum_required(VERSION 3.21.0)

# Set the board to avoid deprecated warnings
set(BOARD "nrf52840dk/nrf52840")

# Set the correct path for CONF_FILE
set(MAIN_CONF_FILE "C:/ncs/projects/light_bulb/prj.conf")
message(STATUS "Main CONF FILE set to ${MAIN_CONF_FILE}")
set(MbedTLS_DIR "C:/ncs/v2.7.0/modules/crypto/mbedtls")
message(STATUS "MbedTLS_DIR: ${MbedTLS_DIR}")
add_library(psa_crypto_library_config INTERFACE)
add_library(psa_interface INTERFACE)
target_include_directories(psa_interface INTERFACE "")
set(CMAKE_BINARY_DIR "C:/ncs/projects/light_bulb")
include_directories(BEFORE ${CMAKE_BINARY_DIR}/modules/crypto/mbedtls/include/mbedtls)
include_directories(BEFORE ${CMAKE_SOURCE_DIR}/build/light_bulb/zephyr/include/generated)
message(STATUS "CMAKE_SOURCE_DIR set to ${CMAKE_SOURCE_DIR}")
message(STATUS "CMAKE_BINARY_DIR set to ${CMAKE_BINARY_DIR}")

# Find Zephyr
find_package(Zephyr HINTS $ENV{ZEPHYR_BASE})
message(STATUS "CMAKE_SOURCE_DIR is set to: ${CMAKE_SOURCE_DIR}")

# Enable GNU STD support and initialize the Matter Data Model.
include(${ZEPHYR_CONNECTEDHOMEIP_MODULE_DIR}/config/nrfconnect/app/enable-gnu-std.cmake)
message(STATUS "Included GNU STD support.")
include(${ZEPHYR_CONNECTEDHOMEIP_MODULE_DIR}/src/app/chip_data_model.cmake)
project(light_bulb)

# NORDIC SDK APP START

# Include all source files that are located in the Matter common directory.
include(${ZEPHYR_NRF_MODULE_DIR}/samples/matter/common/cmake/source_common.cmake)
message(STATUS "Included Matter common sources.")

target_include_directories(app PRIVATE
    src
)

if(CONFIG_AWS_IOT_INTEGRATION)
    add_subdirectory(src/aws_iot_integration)
    message(STATUS "AWS IoT integration included.")
endif()

target_sources(app PRIVATE
    src/app_task.cpp
    src/main.cpp
    src/zcl_callbacks.cpp
)

chip_configure_data_model(app
    INCLUDE_SERVER
    BYPASS_IDL
    GEN_DIR src/zap-generated
    ZAP_FILE ${CMAKE_CURRENT_SOURCE_DIR}/src/light_bulb.zap
)

# NORDIC SDK APP END

#
# Copyright (c) 2021 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: LicenseRef-Nordic-5-Clause
#

cmake_minimum_required(VERSION 3.21.0)

# Set the board to avoid deprecated warnings
set(BOARD "nrf52840dk/nrf52840")
message(STATUS "Board set to: ${BOARD}")
message(STATUS "ZEPHYR_BASE: $ENV{ZEPHYR_BASE}")

# Set the correct path for MbedTLS
set(MbedTLS_DIR "C:/ncs/v2.7.0/modules/crypto/mbedtls/cmake")
message(STATUS "MbedTLS_DIR: ${MbedTLS_DIR}")

# Set the correct path for CONF_FILE
set(CONF_FILE "C:/ncs/v2.7.0/bootloader/mcuboot/boot/zephyr/prj.conf")
message(STATUS "MCUBoot project configuration set to: ${CONF_FILE}")

# Matter configuration directory
set(ZEPHYR_CONNECTEDHOMEIP_MODULE_DIR "C:/ncs/v2.7.0/modules/lib/matter")
message(STATUS "ZEPHYR_CONNECTEDHOMEIP_MODULE_DIR: ${ZEPHYR_CONNECTEDHOMEIP_MODULE_DIR}")

# Find Zephyr
find_package(Zephyr HINTS $ENV{ZEPHYR_BASE})
include(${ZEPHYR_BASE}/cmake/modules/extensions.cmake)

# MBEDTLS Script Directory
set(MBEDTLS_SCRIPTS_DIR "C:/ncs/v2.7.0/modules/crypto/mbedtls/tests/scripts")

# MBEDTLS
add_subdirectory(${CMAKE_SOURCE_DIR}/modules/crypto/mbedtls)
target_include_directories(app PUBLIC ${CMAKE_SOURCE_DIR}/modules/crypto/mbedtls/include)
target_link_libraries(app PUBLIC mbedcrypto mbedtls mbedx509)
include(${ZEPHYR_BASE}/cmake/modules/extensions.cmake)  # Ensure this path is correct

# Enable GNU STD support and initialize the Matter Data Model.
include(${ZEPHYR_CONNECTEDHOMEIP_MODULE_DIR}/config/nrfconnect/app/enable-gnu-std.cmake)
message(STATUS "Included GNU STD support.")
include(${ZEPHYR_CONNECTEDHOMEIP_MODULE_DIR}/src/app/chip_data_model.cmake)
project(light_bulb)
message(STATUS "Project Name: ${PROJECT_NAME}")

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

# Install script for directory: /home/athanasios/gr-satellites/include/satellites

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/satellites" TYPE FILE FILES
    "/home/athanasios/gr-satellites/include/satellites/api.h"
    "/home/athanasios/gr-satellites/include/satellites/decode_rs.h"
    "/home/athanasios/gr-satellites/include/satellites/encode_rs.h"
    "/home/athanasios/gr-satellites/include/satellites/ao40_syncframe.h"
    "/home/athanasios/gr-satellites/include/satellites/ao40_deinterleaver.h"
    "/home/athanasios/gr-satellites/include/satellites/ao40_rs_decoder.h"
    "/home/athanasios/gr-satellites/include/satellites/ax100_decode.h"
    "/home/athanasios/gr-satellites/include/satellites/u482c_decode.h"
    "/home/athanasios/gr-satellites/include/satellites/lilacsat1_demux.h"
    "/home/athanasios/gr-satellites/include/satellites/varlen_packet_tagger.h"
    "/home/athanasios/gr-satellites/include/satellites/varlen_packet_framer.h"
    "/home/athanasios/gr-satellites/include/satellites/nusat_decoder.h"
    "/home/athanasios/gr-satellites/include/satellites/rscode_decoder.h"
    "/home/athanasios/gr-satellites/include/satellites/ao40_syncframe_soft.h"
    "/home/athanasios/gr-satellites/include/satellites/ao40_deinterleaver_soft.h"
    "/home/athanasios/gr-satellites/include/satellites/descrambler308.h"
    "/home/athanasios/gr-satellites/include/satellites/decode_rs_general.h"
    "/home/athanasios/gr-satellites/include/satellites/decode_rs_interleaved.h"
    )
endif()


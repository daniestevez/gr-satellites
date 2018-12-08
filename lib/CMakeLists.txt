# Copyright 2011,2012,2016 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

########################################################################
# Setup library
########################################################################
include(GrPlatform) #define LIB_SUFFIX

include_directories(${FEC_INCLUDE_DIRS} ${Boost_INCLUDE_DIR})
link_directories(${FEC_LIBRARY_DIRS} ${Boost_LIBRARY_DIRS})

list(APPEND satellites_sources
    decode_rs_impl.cc
    encode_rs_impl.cc
    ao40_syncframe_impl.cc
    ao40_deinterleaver_impl.cc
    ao40_rs_decoder_impl.cc
    ax100_decode_impl.cc
    u482c_decode_impl.cc
    randomizer.c
    golay24.c
    lilacsat1_demux_impl.cc
    varlen_packet_tagger_impl.cc
    varlen_packet_framer_impl.cc
    viterbi.c
    nusat_decoder_impl.cc
    rscode/berlekamp.c
    rscode/galois.c
    rscode/rs.c
    rscode_decoder_impl.cc
    ao40_syncframe_soft_impl.cc
    ao40_deinterleaver_soft_impl.cc
    descrambler308_impl.cc
    decode_rs_general_impl.cc
)

set(satellites_sources "${satellites_sources}" PARENT_SCOPE)
if(NOT satellites_sources)
	MESSAGE(STATUS "No C++ sources... skipping lib/")
	return()
endif(NOT satellites_sources)

add_library(gnuradio-satellites SHARED ${satellites_sources})
target_link_libraries(gnuradio-satellites ${FEC_LIBRARIES} ${Boost_LIBRARIES} ${GNURADIO_ALL_LIBRARIES})
set_target_properties(gnuradio-satellites PROPERTIES DEFINE_SYMBOL "gnuradio_satellites_EXPORTS")

if(APPLE)
    set_target_properties(gnuradio-satellites PROPERTIES
        INSTALL_NAME_DIR "${CMAKE_INSTALL_PREFIX}/lib"
    )
endif(APPLE)

########################################################################
# Install built library files
########################################################################
include(GrMiscUtils)
GR_LIBRARY_FOO(gnuradio-satellites RUNTIME_COMPONENT "satellites_runtime" DEVEL_COMPONENT "satellites_devel")

########################################################################
# Build and register unit test
########################################################################
#include(GrTest)
#
#include_directories(${CPPUNIT_INCLUDE_DIRS})
#
#list(APPEND test_satellites_sources
#    ${CMAKE_CURRENT_SOURCE_DIR}/test_satellites.cc
#    ${CMAKE_CURRENT_SOURCE_DIR}/qa_satellites.cc
#)
#
#add_executable(test-satellites ${test_satellites_sources})
#
#target_link_libraries(
#  test-satellites
#  ${GNURADIO_RUNTIME_LIBRARIES}
#  ${Boost_LIBRARIES}
#  ${CPPUNIT_LIBRARIES}
#  gnuradio-satellites
#)
#
#GR_ADD_TEST(test_satellites test-satellites)

########################################################################
# Print summary
########################################################################
message(STATUS "Using install prefix: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Building for version: ${VERSION} / ${LIBVER}")


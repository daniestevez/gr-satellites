# Copyright 2011 Free Software Foundation, Inc.
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
# Include python install macros
########################################################################
include(GrPython)
if(NOT PYTHONINTERP_FOUND)
    return()
endif()

########################################################################
# Install python sources
########################################################################
GR_PYTHON_INSTALL(
    FILES
    __init__.py
    kiss.py
    hdlc.py
    kiss_to_pdu.py
    pdu_to_kiss.py
    hdlc_framer.py
    nrzi_encode.py
    nrzi_decode.py
    hdlc_deframer.py
    check_address.py
    fixedlen_tagger.py
    csp_header.py
    print_header.py
    crc32c.py
    check_crc.py
    swap_crc.py
    swap_header.py
    submit.py
    print_timestamp.py
    sat3cat2_telemetry_parser.py
    DESTINATION ${GR_PYTHON_DIR}/satellites
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-satellites)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)

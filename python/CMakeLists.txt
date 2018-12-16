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
    funcube_telemetry.py
    funcube_telemetry_parser.py
    gomx3_beacon.py
    gomx1_beacon.py
    gomx3_beacon_parser.py
    adsb_kml.py
    gomx1_beacon_parser.py
    ks1q_header_remover.py
    by701_image_decoder.py
    by701_telemetry_parser.py
    by701_camera_telemetry_parser.py
    by701_telemetry.py
    kr01_telemetry.py
    kr01_telemetry_parser.py
    ao40_uncoded_crc.py
    check_ao40_uncoded_crc.py
    lilacsat1_gps_kml.py
    au03_telemetry_parser.py
    au03_telemetry.py
    check_tt64_crc.py
    append_crc32c.py
    dsat_image_decoder.py
    strip_ax25_header.py
    ccsds_telemetry.py
    picsat_telemetry.py
    picsat_telemetry_parser.py
    snet_telemetry.py
    snet_deframer.py
    bch15.py
    beesat_classifier.py
    snet_telemetry_parser.py
    adapters.py
    snet_classifier.py
    sat_1kuns_pf_telemetry.py
    sat_1kuns_pf_telemetry_parser.py
    sat_1kuns_pf_image_decoder.py
    k2sat_deframer.py
    k2sat_image_decoder.py
    feh.py
    cc11xx_packet_crop.py
    check_cc11xx_crc.py
    cc11xx_remove_length.py
    sat_3cat_1_telemetry.py
    sat_3cat_1_telemetry_parser.py
    suomi_100_telemetry.py
    suomi_100_telemetry_parser.py
    pwsat2_telemetry_parser.py
    pwsat2_submitter.py
    eseo_packet_crop.py
    eseo_line_decoder.py
    check_eseo_crc.py
    funcube_submit.py
    eseo_telemetry.py
    eseo_telemetry_parser.py
    DESTINATION ${GR_PYTHON_DIR}/satellites
)

########################################################################
# Handle the unit tests
########################################################################
include(GrTest)

set(GR_TEST_TARGET_DEPS gnuradio-satellites)
set(GR_TEST_PYTHON_DIRS ${CMAKE_BINARY_DIR}/swig)

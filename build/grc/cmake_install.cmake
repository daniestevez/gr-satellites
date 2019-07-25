# Install script for directory: /home/athanasios/gr-satellites/grc

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gnuradio/grc/blocks" TYPE FILE FILES
    "/home/athanasios/gr-satellites/grc/satellites_kiss_to_pdu.xml"
    "/home/athanasios/gr-satellites/grc/satellites_pdu_to_kiss.xml"
    "/home/athanasios/gr-satellites/grc/satellites_hdlc_framer.xml"
    "/home/athanasios/gr-satellites/grc/satellites_nrzi_encode.xml"
    "/home/athanasios/gr-satellites/grc/satellites_nrzi_decode.xml"
    "/home/athanasios/gr-satellites/grc/satellites_hdlc_deframer.xml"
    "/home/athanasios/gr-satellites/grc/satellites_check_address.xml"
    "/home/athanasios/gr-satellites/grc/satellites_fixedlen_tagger.xml"
    "/home/athanasios/gr-satellites/grc/satellites_print_header.xml"
    "/home/athanasios/gr-satellites/grc/satellites_check_crc.xml"
    "/home/athanasios/gr-satellites/grc/satellites_swap_crc.xml"
    "/home/athanasios/gr-satellites/grc/satellites_swap_header.xml"
    "/home/athanasios/gr-satellites/grc/satellites_submit.xml"
    "/home/athanasios/gr-satellites/grc/satellites_print_timestamp.xml"
    "/home/athanasios/gr-satellites/grc/satellites_sat3cat2_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_ao40_syncframe.xml"
    "/home/athanasios/gr-satellites/grc/satellites_ao40_deinterleaver.xml"
    "/home/athanasios/gr-satellites/grc/satellites_ao40_rs_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_funcube_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_gomx3_beacon_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_adsb_kml.xml"
    "/home/athanasios/gr-satellites/grc/satellites_ax100_decode.xml"
    "/home/athanasios/gr-satellites/grc/satellites_u482c_decode.xml"
    "/home/athanasios/gr-satellites/grc/satellites_gomx1_beacon_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_ks1q_header_remover.xml"
    "/home/athanasios/gr-satellites/grc/satellites_decode_rs.xml"
    "/home/athanasios/gr-satellites/grc/satellites_encode_rs.xml"
    "/home/athanasios/gr-satellites/grc/satellites_lilacsat1_demux.xml"
    "/home/athanasios/gr-satellites/grc/satellites_by701_image_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_by701_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_by701_camera_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_kr01_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_check_ao40_uncoded_crc.xml"
    "/home/athanasios/gr-satellites/grc/satellites_lilacsat1_gps_kml.xml"
    "/home/athanasios/gr-satellites/grc/satellites_au03_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_check_tt64_crc.xml"
    "/home/athanasios/gr-satellites/grc/satellites_varlen_packet_tagger.xml"
    "/home/athanasios/gr-satellites/grc/satellites_varlen_packet_framer.xml"
    "/home/athanasios/gr-satellites/grc/satellites_append_crc32c.xml"
    "/home/athanasios/gr-satellites/grc/satellites_dsat_image_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_nusat_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_rscode_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_strip_ax25_header.xml"
    "/home/athanasios/gr-satellites/grc/satellites_picsat_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_snet_deframer.xml"
    "/home/athanasios/gr-satellites/grc/satellites_ao40_syncframe_soft.xml"
    "/home/athanasios/gr-satellites/grc/satellites_ao40_deinterleaver_soft.xml"
    "/home/athanasios/gr-satellites/grc/satellites_beesat_classifier.xml"
    "/home/athanasios/gr-satellites/grc/satellites_snet_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_snet_classifier.xml"
    "/home/athanasios/gr-satellites/grc/satellites_sat_1kuns_pf_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_sat_1kuns_pf_image_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_k2sat_deframer.xml"
    "/home/athanasios/gr-satellites/grc/satellites_k2sat_image_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_descrambler308.xml"
    "/home/athanasios/gr-satellites/grc/satellites_cc11xx_packet_crop.xml"
    "/home/athanasios/gr-satellites/grc/satellites_check_cc11xx_crc.xml"
    "/home/athanasios/gr-satellites/grc/satellites_cc11xx_remove_length.xml"
    "/home/athanasios/gr-satellites/grc/satellites_sat_3cat_1_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_suomi_100_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_mysat1_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_pwsat2_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_pwsat2_submitter.xml"
    "/home/athanasios/gr-satellites/grc/satellites_eseo_packet_crop.xml"
    "/home/athanasios/gr-satellites/grc/satellites_eseo_line_decoder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_check_eseo_crc.xml"
    "/home/athanasios/gr-satellites/grc/satellites_decode_rs_general.xml"
    "/home/athanasios/gr-satellites/grc/satellites_funcube_submit.xml"
    "/home/athanasios/gr-satellites/grc/satellites_eseo_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_dstar_one_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_reflect_bytes.xml"
    "/home/athanasios/gr-satellites/grc/satellites_check_astrocast_crc.xml"
    "/home/athanasios/gr-satellites/grc/satellites_lume1_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_qo100_telemetry_print.xml"
    "/home/athanasios/gr-satellites/grc/satellites_decode_rs_interleaved.xml"
    "/home/athanasios/gr-satellites/grc/satellites_space_packet_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_telemetry_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_telecommand_parser.xml"
    "/home/athanasios/gr-satellites/grc/satellites_space_packet_primaryheader_adder.xml"
    "/home/athanasios/gr-satellites/grc/satellites_telemetry_primaryheader_adder.xml"
    )
endif()


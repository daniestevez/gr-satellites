#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020-2025 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

"""
GNU Radio gr-satellites out-of-tree module.

gr-satellites is a GNU Radio out-of-tree module encompassing a
collection of telemetry decoders that supports many different Amateur
satellites. It suports most popular protocols, such as AX.25, the
GOMspace NanoCom U482C and AX100 modems, an important part of the CCSDS
stack, the AO-40 protocol used in the FUNcube satellites, and several
ad-hoc protocols used in other satellites.
"""

__version__ = 'v5.8.0-git'
__author__ = 'Daniel Estevez'
__copyright__ = 'Copyright 2016-2025 Daniel Estevez'
__email__ = 'daniel@destevez.net'
__license__ = 'GPL-3.0-or-later'
__all__ = [
    'ccsds',
    'components',
    'core',
    'filereceiver',
    'hier',
    'satyaml',
    'telemetry',
    'usp',
    'utils',
    ]

# We need to import gnuradio.blocks so that the bindings for
# gnuradio.blocks.control_loop are imported, since the bindings for
# costas_loop_8apsk requiere control_loop to be imported.
import gnuradio.blocks

# Import bindings into the satellites namespace.
# The first try works when we are importing from the build dir
try:
    from .bindings.satellites_python import *
except ModuleNotFoundError:
    from .satellites_python import *

# Import any pure python here

from .aausat4_remove_fsm import aausat4_remove_fsm
from .adsb_kml import adsb_kml
from .append_crc32c import append_crc32c
from .autopolarization import autopolarization
from .beesat_classifier import beesat_classifier
from .bme_submitter import bme_submitter
from .bme_ws_submitter import bme_ws_submitter
from .cc11xx_packet_crop import cc11xx_packet_crop
from .check_address import check_address
from .check_ao40_uncoded_crc import check_ao40_uncoded_crc
from .check_astrocast_crc import check_astrocast_crc
from .check_cc11xx_crc import check_cc11xx_crc
from .check_crc16_ccitt import check_crc16_ccitt
from .check_crc16_ccitt_false import check_crc16_ccitt_false
from .check_crc import check_crc
from .check_eseo_crc import check_eseo_crc
from .check_hex_string import check_hex_string
from .check_swiatowid_crc import check_swiatowid_crc
from .check_tt64_crc import check_tt64_crc
from .eseo_line_decoder import eseo_line_decoder
from .eseo_packet_crop import eseo_packet_crop
from .fixedlen_tagger import fixedlen_tagger
from .funcube_submit import funcube_submit
from .hdlc_deframer import hdlc_deframer
from .hdlc_framer import hdlc_framer
from .k2sat_deframer import k2sat_deframer
from .kiss_to_pdu import kiss_to_pdu
from .ks1q_header_remover import ks1q_header_remover
from .lilacsat1_gps_kml import lilacsat1_gps_kml
from .ngham_check_crc import ngham_check_crc
from .ngham_packet_crop import ngham_packet_crop
from .ngham_remove_padding import ngham_remove_padding
from .pdu_to_kiss import pdu_to_kiss
from .print_header import print_header
from .print_timestamp import print_timestamp
from .pwsat2_submitter import pwsat2_submitter
from .pwsat2_telemetry_parser import pwsat2_telemetry_parser
from .reflect_bytes import reflect_bytes
from .snet_classifier import snet_classifier
from .snet_deframer import snet_deframer
from .submit import submit
from .swap_crc import swap_crc
from .swap_header import swap_header
from .swiatowid_packet_crop import swiatowid_packet_crop
from .swiatowid_packet_split import swiatowid_packet_split
from .sx12xx_check_crc import sx12xx_check_crc
from .sx12xx_packet_crop import sx12xx_packet_crop
from .mobitex_deframer import mobitex_deframer

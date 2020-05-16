#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# The presence of this file turns this directory into a Python package

'''
GNU Radio gr-satellites out-of-tree module.

gr-satellites is a GNU Radio out-of-tree module encompassing a
collection of telemetry decoders that supports many different Amateur
satellites. It suports most popular protocols, such as AX.25, the
GOMspace NanoCom U482C and AX100 modems, an important part of the CCSDS
stack, the AO-40 protocol used in the FUNcube satellites, and several
ad-hoc protocols used in other satellites.
'''


# import swig generated symbols into the satellites namespace
# this shouldn't fail, since the module is not python-only
from .satellites_swig import *

# import any pure python here
#

__all__ = ['ccsds', 'components', 'core', 'hier', 'filereceiver', 'satyaml', 'telemetry', 'utils']

from .kiss_to_pdu import kiss_to_pdu
from .pdu_to_kiss import pdu_to_kiss
from .hdlc_framer import hdlc_framer
from .nrzi_encode import nrzi_encode
from .nrzi_decode import nrzi_decode
from .hdlc_deframer import hdlc_deframer
from .check_address import check_address

from .fixedlen_tagger import fixedlen_tagger

from .print_header import print_header
from .check_crc import check_crc
from .swap_crc import swap_crc
from .swap_header import swap_header

from .submit import submit
from .print_timestamp import print_timestamp

from .adsb_kml import adsb_kml

from .ks1q_header_remover import ks1q_header_remover


from .check_ao40_uncoded_crc import check_ao40_uncoded_crc

from .lilacsat1_gps_kml import lilacsat1_gps_kml

from .check_tt64_crc import check_tt64_crc

from .append_crc32c import append_crc32c

from .strip_ax25_header import strip_ax25_header

from .snet_deframer import snet_deframer

from .beesat_classifier import beesat_classifier

from .snet_classifier import snet_classifier

from .k2sat_deframer import k2sat_deframer

from .cc11xx_packet_crop import cc11xx_packet_crop
from .check_cc11xx_crc import check_cc11xx_crc
from .cc11xx_remove_length import cc11xx_remove_length

from .pwsat2_telemetry_parser import pwsat2_telemetry_parser
from .pwsat2_submitter import pwsat2_submitter

from .eseo_packet_crop import eseo_packet_crop
from .eseo_line_decoder import eseo_line_decoder
from .check_eseo_crc import check_eseo_crc

from .funcube_submit import funcube_submit

from .dstar_one_telemetry_parser import dstar_one_telemetry_parser

from .reflect_bytes import reflect_bytes

from .check_astrocast_crc import check_astrocast_crc

from .swiatowid_packet_crop import swiatowid_packet_crop
from .check_swiatowid_crc import check_swiatowid_crc
from .swiatowid_packet_split import swiatowid_packet_split

from .manchester_sync import manchester_sync

from .header_remover import header_remover

from .smogp_packet_filter import smogp_packet_filter

from .aausat4_remove_fsm import aausat4_remove_fsm

from .ngham_packet_crop import ngham_packet_crop
from .ngham_remove_padding import ngham_remove_padding
from .ngham_check_crc import ngham_check_crc

from .bme_submitter import bme_submitter

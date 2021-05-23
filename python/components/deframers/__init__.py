#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

'''
gr-satellites deframer components

The deframers transform soft symbols into frames, detecting packet
boundaries and performing error correction and checking as needed.

The input to these hierarchical blocks is a stream of soft symbols
and the output are PDUs with the frames.
'''

from .aalto1_deframer import aalto1_deframer
from .aausat4_deframer import aausat4_deframer
from .aistechsat_2_deframer import aistechsat_2_deframer
from .ao40_fec_deframer import ao40_fec_deframer
from .ao40_uncoded_deframer import ao40_uncoded_deframer
from .astrocast_fx25_deframer import astrocast_fx25_deframer
from .ax100_deframer import ax100_deframer
from .ax25_deframer import ax25_deframer
from .ax5043_deframer import ax5043_deframer
from .ccsds_concatenated_deframer import ccsds_concatenated_deframer
from .ccsds_rs_deframer import ccsds_rs_deframer
from .diy1_deframer import diy1_deframer
from .eseo_deframer import eseo_deframer
from .fossasat_deframer import fossasat_deframer
from .grizu263a_deframer import grizu263a_deframer
from .ideassat_deframer import ideassat_deframer
from .k2sat_deframer import k2sat_deframer
from .lilacsat_1_deframer import lilacsat_1_deframer
from .lucky7_deframer import lucky7_deframer
from .mobitex_deframer import mobitex_deframer
from .ngham_deframer import ngham_deframer
from .nusat_deframer import nusat_deframer
from .ops_sat_deframer import ops_sat_deframer
from .reaktor_hello_world_deframer import reaktor_hello_world_deframer
from .sat_3cat_1_deframer import sat_3cat_1_deframer
from .smogp_ra_deframer import smogp_ra_deframer
from .smogp_signalling_deframer import smogp_signalling_deframer
from .snet_deframer import snet_deframer
from .swiatowid_deframer import swiatowid_deframer
from .tt64_deframer import tt64_deframer
from .u482c_deframer import u482c_deframer
from .ua01_deframer import ua01_deframer
from .usp_deframer import usp_deframer
from .yusat_deframer import yusat_deframer

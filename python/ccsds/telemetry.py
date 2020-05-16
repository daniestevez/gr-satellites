#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
# This was made under ESA Summer of Code in Space 2019
# by Athanasios Theocharis, mentored by Daniel Estevez
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

'''
Construct for the Primary Header of the CCSDS Telemetry Space Data Link Protocol
( CCSDS 132.0-B-2 )
'''

from construct import *

PrimaryHeader = BitStruct('transfer_frame_version_number' / BitsInteger(2),
                          'spacecraft_id' / BitsInteger(10),
                          'virtual_channel_id' / BitsInteger(3),
                          'ocf_flag' / Flag,
                          'master_channel_frame_count' / BitsInteger(8),
                          'virtual_channel_frame_count' / BitsInteger(8),
                          'transfer_frame_secondary_header_flag' / Flag,
                          'synch_flag' / Flag,
                          'packet_order_flag' / Flag,
                          'segment_length_id' / BitsInteger(2),
                          'first_header_pointer' / BitsInteger(11))

OCFTrailer = BitStruct('control_word_type' / Flag,
                       'clcw_version_number' / BitsInteger(2),
                       'status_field' / BitsInteger(3),
                       'cop_in_effect' / BitsInteger(2),
                       'virtual_channel_identification' / BitsInteger(6),
                       'rsvd_spare1' / BitsInteger(2),
                       'no_rf_avail' / Flag,
                       'no_bit_lock' / Flag,
                       'lockout' / Flag,
                       'wait' / Flag,
                       'retransmit' / Flag,
                       'farmb_counter' / BitsInteger(2),
                       'rsvd_spare2' / Flag,
                       'report_value' / BitsInteger(8))

FullPacket = Struct('primary' / PrimaryHeader,
                    'payload' / Byte[this._.size],
                    'ocftrailer' / If(this.primary.ocf_flag == 1, OCFTrailer))

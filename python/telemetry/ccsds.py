#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2019, 2024 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

import warnings

AOSPrimaryHeader = BitStruct(
    'transfer_frame_version_number' / BitsInteger(2),
    'spacecraft_id' / BitsInteger(8),
    'virtual_channel_id' / BitsInteger(6),
    'virtual_channel_frame_count' / BitsInteger(24),
    'replay_flag' / Flag,
    'vc_frame_count_usage_flag' / Flag,
    'rsvd_spare' / BitsInteger(2),
    'vc_framecount_cycle' / BitsInteger(4)
)

M_PDU_Header = BitStruct(
    'rsv_spare' / BitsInteger(5),
    'first_header_pointer' / BitsInteger(11)
)

SpacePacketPrimaryHeader = BitStruct(
    'ccsds_version' / BitsInteger(3),
    'packet_type' / BitsInteger(1),
    'secondary_header_flag' / Flag,
    'APID' / BitsInteger(11),
    'sequence_flags' / BitsInteger(2),
    'packet_sequence_count_or_name' / BitsInteger(14),
    'data_length' / BitsInteger(16)
)

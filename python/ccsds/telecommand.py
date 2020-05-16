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
Construct for the Transfer Frame Primary Header of Fig
the CCSDS TC Space Data Link Protocol ( CCSDS 232.0-B-3 )
'''

from construct import *

PrimaryHeader = BitStruct('transfer_frame_version' / BitsInteger(2),
                          'bypass' / Flag,
                          'control' / Flag,
                          'RSVD_spare' / BitsInteger(2),
                          'spacecraft_id' / BitsInteger(10),
                          'virtual_channel_id' / BitsInteger(6),
                          'frame_length' / BitsInteger(10),
                          'frame_sequence_number' / BitsInteger(8))

FullPacket = Struct('primary' / PrimaryHeader,
                    'pyaload' / Byte[this.primary.frame_length - 5])

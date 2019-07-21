#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
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

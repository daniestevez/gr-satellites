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
Construct for the Primary Header of the CCSDS Space Packet ( CCSDS 133.0-B-1 )
'''


from construct import *


PrimaryHeader = BitStruct('ccsds_version' / BitsInteger(3),
                          'packet_type' / Flag,
                          'secondary_header_flag' / Flag,
                          'process_id' / BitsInteger(4),
                          'level_flag' / Flag,
                          'payload_flag' / Flag,
                          'packet_category' / BitsInteger(5),
                          'sequence_flag' / BitsInteger(2),
                          'packet_sequence_count' / BitsInteger(14),
                          'data_length' / BitsInteger(16))

PayLoad = Struct('payload' / Bytes(this._.dataLength))

FullPacket = Struct('primary' / PrimaryHeader,
                    'payload' / BitsInteger(this.primary.data_length))



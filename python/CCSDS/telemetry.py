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
                          'transfer_frame_data_field_status' / BitsInteger(16))
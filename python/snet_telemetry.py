#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Daniel Estevez <daniel@destevez.net>
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

from construct import *

LTUFrameHeader = BitStruct(
    'SrcId' / BitsInteger(7),
    'DstId' / BitsInteger(7),
    'FrCntTx' / BitsInteger(4),
    'FrCntRx' / BitsInteger(4),
    'SNR' / BitsInteger(4),
    'AiTypeSrc' / BitsInteger(4),
    'AiTypeDst' / BitsInteger(4),
    'DfcId' / BitsInteger(2),
    'Caller' / Flag,
    'Arq' / Flag,
    'PduTypeId' / Flag,
    'BchRq' / Flag,
    'Hailing' / Flag,
    'UdFl1' / Flag,
    'PduLength' / BitsInteger(10),
    'CRC13' / BitsInteger(13),
    'CRC5' / BitsInteger(5),
    Padding(2)
    )

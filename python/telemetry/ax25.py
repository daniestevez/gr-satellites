#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 Daniel Estevez <daniel@destevez.net>
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

SSID = BitStruct(
    'ch' / Flag, # C / H bit
    Default(BitsInteger(2), 3), # reserved bits
    'ssid' / BitsInteger(4),
    'extension' / Flag # last address bit
    )

class CallsignAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return bytes([x << 1 for x in bytes((obj.upper() + ' '*6)[:6], encoding = 'ascii')])
    def _decode(self, obj, context, path = None):
        return str(bytes([x >> 1 for x in obj]), encoding = 'ascii').strip()

Callsign = CallsignAdapter(Bytes(6))

Address = Struct(
        'callsign' / Callsign,
        'ssid' / SSID
        )

Control = Hex(Int8ub)

PID = Hex(Int8ub)

Header = Struct(
    'addresses' / RepeatUntil(lambda x, lst, ctx: x.ssid.extension, Address),
    'control' / Control,
    'pid' / PID
    )

Frame = Struct(
    Embedded(Header),
    'info' / GreedyBytes
    )

ax25 = Frame

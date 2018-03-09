#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>
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

import datetime

from construct import *

class TimestampAdapter(Adapter):
    # TODO _encode()
    def _decode(self, obj, context, path = None):
        return datetime.datetime.utcfromtimestamp(obj)
Timestamp = TimestampAdapter(Int32sb)

class BatteryAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj - 4420) / 16.0)
    def _decode(self, obj, context, path = None):
        return obj * 16 + 4420
Battery = BatteryAdapter(Int8ub)

class CurrInAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj * 255.0 / 2700.0)
    def _decode(self, obj, context, path = None):
        return obj * 2700.0 / 255.0
CurrIn = CurrInAdapter(Int8ub)

class CurrOutAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj * 255.0 / 4000.0)
    def _decode(self, obj, context, path = None):
        return obj * 4000.0 / 255.0
CurrOut = CurrOutAdapter(Int8ub)

class Curr3Adapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj * 255.0 / 5500.0)
    def _decode(self, obj, context, path = None):
        return obj * 5500.0 / 255.0
Curr3 = Curr3Adapter(Int8ub)

class Curr5Adapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj * 255.0 / 4500.0)
    def _decode(self, obj, context, path = None):
        return obj * 4500.0 / 255.0
Curr5 = Curr5Adapter(Int8ub)
                      
Beacon = Struct(
        'timestamp' / Timestamp,
        'callsign' / String(6, encoding='utf8'),
        'flags' / Byte,
        'batt_voltage' / Battery,
        'current_in' / CurrIn,
        'current_out' / CurrOut,
        'rail3_current' / Curr3,
        'rail5_current' / Curr5,
        'com_temp' / Int8sb,
        'eps_temp' / Int8sb,
        'bat_temp' / Int8sb
        )

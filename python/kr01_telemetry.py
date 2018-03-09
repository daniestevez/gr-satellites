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

from construct import *

Mode = Enum(Int8ub,\
            Otherwise = 0,\
            MissionMode = 1)

class BatVoltageAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj - 3.0) * 20.0)
    def _decode(self, obj, context, path = None):
        return obj / 20.0 + 3.0
BatVoltage = BatVoltageAdapter(Int8ub)

class BatCurrentAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj + 1.0) * 127.0)
    def _decode(self, obj, context, path = None):
        return obj / 127.0 - 1.0
BatCurrent = BatCurrentAdapter(Int8ub)

class BusCurrentAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj * 40.0)
    def _decode(self, obj, context, path = None):
        return obj / 40.0
BusCurrent = BusCurrentAdapter(Int8ub)

class TempAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj + 15.0) * 4.0)
    def _decode(self, obj, context, path = None):
        return obj / 4.0 - 15.0
Temp = TempAdapter(Int8ub)

SpacecraftMode = Enum(Int8ub,\
                      GndDebug = 0,\
                      Initial = 1,\
                      Commissioning = 2,\
                      Mission = 3,\
                      Comm = 4,\
                      Powersafe = 17,\
                      Detumble = 18,\
                      Debug = 19,\
                      Standby = 32)

Beacon = Struct(
        'mode' / Mode,
        'batvoltage' / BatVoltage,
        'batcurrent' / BatCurrent,
        '3v3buscurrent' / BusCurrent,
        '5vbuscurrent' / BusCurrent,
        'tempcomm' / Temp,
        'tempeps' / Temp,
        'tempbattery' / Temp,
        'spacecraftmode' / SpacecraftMode
        )

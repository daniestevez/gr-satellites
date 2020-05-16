#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017,2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

kr01 = Struct(
        'header' / Bytes(0x23),
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

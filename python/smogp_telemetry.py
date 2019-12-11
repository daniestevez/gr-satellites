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
from .adapters import AffineAdapter, LinearAdapter, UNIXTimestampAdapter

Timestamp = UNIXTimestampAdapter(Int32sl)

Temperature = LinearAdapter(10.0, Int16sl)
Voltage = LinearAdapter(1000.0, Int16ul)

AntennaStatus = Enum(BitsInteger(2), closed = 0, open = 1, not_monitored = 2, invalid = 3)

PanelStatus = BitStruct(
    'panel_number' / BitsInteger(3),
    'antenna_status' / AntennaStatus,
    Padding(3)
    )

MPPT = Struct(
    'timestamp' / Timestamp,
    'temperature' / Temperature,
    'light_sensor' / Voltage,
    'input_current' / Int16ul,
    'input_voltage' / Voltage,
    'output_current' / Int16ul,
    'output_voltage' / Voltage,
    'panel_status' / PanelStatus
    )

AckInfo = Struct(
    'serial' / Int16sl,
    'rssi' / AffineAdapter(2.0, 2.0 * 131.0, Int8ul)
    )

Telemetry1 = Struct(
    'timestamp' / Timestamp,
    'mppts' / MPPT[6],
    'ack_info' / AckInfo
    )

Beacon = Struct(
    'type' / Int8ul,
    'payload' / Switch(this.type, {
        1 : Telemetry1
        }, default = GreedyBytes)
    )

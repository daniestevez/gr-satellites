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
from .adapters import LinearAdapter

EPS = Struct(
    'boot_count' / Int16ub,
    'uptime' / Int32ub,
    'rt_clock' / Int32ub,
    'ping_status' / Int8ub,
    'subsystem_status' / Int16ub,
    'battery_voltage' / LinearAdapter(1/40.0, Int8ub),
    'cell_diff' / LinearAdapter(1/4.0, Int8sb),
    'battery_current' / LinearAdapter(1/10.0, Int8sb),
    'solar_power' / LinearAdapter(1/20.0, Int8ub),
    'temp' / Int8sb,
    'pa_temp' / Int8sb,
    'main_voltage' / Int8sb
    )

COM = Struct(
    'boot_count' / Int16ub,
    'packets_received' / Int16ub,
    'packets_sent' / Int16ub,
    'latest_rssi' / Int16sb,
    'latest_bit_correction' / Int8ub,
    'latest_byte_correction' / Int8ub
    )

# Reverse-engineered

ADCS1 = Struct(
    'bdot' / Int16sb[3],
    'state' / Int8ub
    )

ADCS2 = Struct(
    'gyro' / Int16sb[3]
    )

AIS = Struct(
    'boot_count' / Int16ub,
    Padding(4), # unknown data
    'unique_mssi' / Int16ub,
    Padding(12) # unknown data
    )

Valid = BitStruct(
    Padding(2),
    'ais2' / Flag,
    'ais1' / Flag,
    'adcs2' / Flag,
    'adcs1' / Flag,
    'com' / Flag,
    'eps' / Flag
    )
Beacon = Struct(
    'valid' / Valid,
    'eps' / EPS,
    'com' / COM,
    'adcs1' / ADCS1,
    'adcs2' / ADCS2,
    'ais1' / AIS,
    'ais2' / AIS
    )

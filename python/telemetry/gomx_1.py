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
from .csp import CSPHeader
from ..adapters import UNIXTimestampAdapter, LinearAdapter

Timestamp = UNIXTimestampAdapter(Int32ub)
Temperature = LinearAdapter(4, Int16sb)

OBC = Struct(
    'boot_count' / Int16ub,
    'temp' / Temperature[2],
    'panel_temp' / Temperature[6]
    )

COM = Struct(
    'byte_corr_tot' / Int16ub, # Bytes corrected by RS
    'rx' / Int16ub, # RX packets
    'rx_err' / Int16ub,
    'tx' / Int16ub,
    'last_temp' / Int16sb[2],
    'last_rssi' / Int16sb, # dBm
    'last_rferr' / Int16sb, # Hz
    'last_batt_volt' / LinearAdapter(100.0, Int16ub), # V
    'last_tx_current' / Int16ub, # mA
    'boot_count' / Int16ub
    )

Battmode = Enum(Int8ub, normal = 0, undervoltage = 1, overvoltage = 2)

EPS = Struct(
    'vboost' / LinearAdapter(1000.0, Int16ub)[3],
    'vbatt' / LinearAdapter(1000.0, Int16ub),
    'curout' / Int16ub[6],
    'curin' / Int16ub[3],
    'cursun' / Int16ub, # Boost converter current mA
    'cursys' / Int16ub, # Battery current mA
    'temp' / Int16sb[6],
    'output' / Int8ub, # Output status
    'counter_boot' / Int16ub, # EPS reboots
    'counter_wdt_i2c' / Int16ub, # WDT I2C reboots
    'counter_wdt_gnd' / Int16ub, # WDT GND reboots
    'bootcause' / Int8ub,
    'latchup' / Int16ub[6],
    'battmode' / Battmode
    )

GATOSS = Struct(
    'average_fps_5min' / Int16ub,
    'average_fps_1min' / Int16ub,
    'average_fps_10sec' / Int16ub,
    'plane_count' / Int16ub,
    'frame_count' / Int32ub,
    'last_icao' / Hex(Int32ub),
    'last_timestamp' / Timestamp,
    'last_lat' / Float32b,
    'last_lon' / Float32b,
    'last_altitude' / Int32ub,
    'crc_corrected' / Int32ub,
    'boot_count' / Int16ub,
    'boot_cause' / Int16ub
    )

Hub = Struct(
    'temp' / Int8sb,
    'boot_count' / Int16ub,
    'reset_cause' / Int8ub,
    'switch_status' / Int8ub,
    'burns' / Int16ub[2] # burn tries
    )

ADCS = Struct(
    'tumblerate' / Float32b[3],
    'tumblenorm' / Float32b[2],
    'magnetometer' / Float32b[3],
    'status' / Int8ub,
    'torquerduty' / Float32b[3],
    'ads_state' / Int8ub,
    'acs_state' / Int8ub,
    'sunsensor' / Int8ub[8]
    )

beacon_a = Struct(
    'obc' / OBC,
    'com' / COM,
    'eps' / EPS,
    'gatoss' / GATOSS,
    'hub' / Hub,
    'adcs' / ADCS
    )

gomx_1 = Struct(
    'csp_header' / CSPHeader,
    'beacon_time' / Timestamp,
    'beacon_flags' / Int8ub,
    'beacon' / Optional(beacon_a), # there is also an unsupported beacon_b which is shorter
    )

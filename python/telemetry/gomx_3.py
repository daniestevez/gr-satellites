#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from .csp import CSPHeader
from ..adapters import UNIXTimestampAdapter, LinearAdapter


Voltage = LinearAdapter(1000.0, Int16ub)
Timestamp = UNIXTimestampAdapter(Int32ub)

EPS = Struct(
    'timestamp' / Timestamp,
    'vboost' / Voltage[3],
    'vbatt' / Voltage,
    'curout' / Int16ub[7],
    'curin' / Int16ub[3],
    'cursun' / Int16ub,
    'cursys' / Int16ub,
    'eps_temp' / Int16sb[6],
    'battmode' / Int8ub
    )

Temperature = LinearAdapter(10.0, Int16sb)
COM = Struct(
    'timestamp' / Timestamp,
    'temp_brd' / Temperature,
    'temp_pa' / Temperature,
    'last_rssi' / Int16sb,
    'last_rferr' / Int16sb,
    'bgnd_rssi' / Int16sb
    )

OBC = Struct(
    'timestamp' / Timestamp,
    'cur_gssb' / Int16ub[2],
    'cur_flash' / Int16ub,
    'temp' / Temperature[2]
    )

ADCS = Struct(
    'timestamp' / Timestamp,
    'cur_gssb' / Int16ub[2],
    'cur_flash' / Int16ub,
    'cur_pwm' / Int16ub,
    'cur_gps' / Int16ub,
    'cur_wde' / Int16ub,
    'temp' / Temperature[2]
    )

ADSB = Struct(
    'timestamp' / Timestamp,
    'cur5v0brd' / Int16ub,
    'cur3v3brd' / Int16ub,
    'cur3v3sd' / Int16ub,
    'cur1v2' / Int16ub,
    'cur2v5' / Int16ub,
    'cur3v3fpga' / Int16ub,
    'cur3v3adc' / Int16ub,
    'last_icao' / Hex(Int32ub),
    'last_lat' / Float32b,
    'last_lon' / Float32b,
    'last_alt' / Int32ub,
    'last_time' / Timestamp
    )

gomx_3 = Struct(
    'csp_header' / CSPHeader,
    'beacon_type' / Int8ub,
    'beacon' / If(
        ((this.csp_header.destination == 10)
         & (this.csp_header.destination_port == 30)
         & (this.csp_header.source == 1)
         & (this.beacon_type == 0)),
        Struct(
            'eps' / EPS,
            'com' / COM,
            'obc' / OBC,
            'adcs' / ADCS,
            'adsb' / ADSB
            )
        )
    )

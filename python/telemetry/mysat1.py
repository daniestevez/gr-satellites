#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

from construct import *
from ..adapters import *
from .ax25 import Header

Timestamp = UNIXTimestampAdapter(Int32ul)

Callsign = Struct(
    'callsign' /  Bytes(5))

OBC = Struct(
    'obc_mode' / Int8ul,
    'obc_reset_counter' / Int32ul,
    'obc_uptime' / Int32ul)

Gyro = Struct(
    'gyro_norm' / Int8ul)

EPS = Struct(
    'eps_counter_boot' / Int32ul,
    'eps_last_boot_cause' / Int8ul,
    'eps_battery_mode' / Int8ul)

Timestamp_Struct = Struct(
    'timestamp' / Timestamp)

OBC_Temp = Struct(
    'obc_temp' / AffineAdapter(1, 128, Int8ul),
    'obc_daughter_board_temp' / AffineAdapter(1, 128, Int8ul))

EPS_Temp = Struct(
    'eps_battery_temp' / AffineAdapter(1, 128, Int8ul),
    'eps_board_temp' / AffineAdapter(1, 128, Int8ul))

Ants = Struct(
    'ants_temp' / AffineAdapter(1, 128, Int8ul))

TRXVU_Temp = Struct(
    'trxvu_temp' / AffineAdapter(1, 128, Int8ul))

ADCS = Struct(
    'adcs_temp' / AffineAdapter(1, 128, Int8ul))

OBC_Voltages = Struct(
'obc_3v3_voltage' / LinearAdapter(10.0, Int8ul),
'obc_5v0_voltage' / LinearAdapter(10.0, Int8ul))

TRXVU_Voltage = Struct(
'trxvu_voltage' / LinearAdapter(10.0, Int8ul))

EPS_Batt_Voltage = Struct(
'eps_batt_voltage' / LinearAdapter(10.0, Int8ul))

OBC_Current = Struct(
'obc_5.0_current' / LinearAdapter(1000.0, Int16ul))

EPS_Currents = Struct(
'eps_total_pv_current' / LinearAdapter(1000.0, Int16ul),
'eps_total_system_current' / LinearAdapter(1000.0, Int16ul))

mysat1 = Struct(
    'header' / Header,
    'callsign' / Callsign,
    'obc' / OBC,
    'gyro' / Gyro,
    'eps' / EPS,
    'timestamp' / Timestamp_Struct,
    'obc_temp' / OBC_Temp,
    'eps_temp' / EPS_Temp,
    'ants' / Ants,
    'trxvu_temp' / TRXVU_Temp,
    'adcs' / ADCS,
    'obc_voltages' / OBC_Voltages,
    'trxvu_voltage' / TRXVU_Voltage,
    'eps_batt_voltage' / EPS_Batt_Voltage,
    'obc_current' / OBC_Current,
    'eps_currents' / EPS_Currents)

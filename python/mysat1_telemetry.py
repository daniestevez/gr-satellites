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
from adapters import UNIXTimestampAdapter

Timestamp = UNIXTimestampAdapter(Int32ub)

Header = Struct(
'header' / Int8ub[12])

Callsign = Struct(
    'callsign' /  Int8ub[5])

OBC = Struct(
    'obc_mode' / Int8ub,
    'obc_reset_counter' / Int32ub,
    'obc_uptime' / Int32ub)

Gyro = Struct(
    'gyro_norm' / Int8ub)

Timestamp_Struct = Struct(
    'timestamp' / Timestamp)

OBC_Temp = Struct(
    'obc_temp' / Int8ub,
    'obc_daughter_board_temp' / Int8ub)

EPS_Temp = Struct(
    'eps_battery_temp' / Int8ub,
    'eps_board_temp' / Int8ub)

Ants = Struct(
    'ants_temp' / Int8ub)

TRXVU_Temp = Struct(
    'trxvu_temp' / Int8ub)

ADCS = Struct(
    'adcs_temp' / Int8ub)

Solar_Panels = Struct(
    'solar_panels_temp' / Int8ub[6])

OBC_Voltages = Struct(
'obc_3v3_voltage' / Int8ub,
'obc_5v0_voltage' / Int8ub)

TRXVU_Voltage = Struct(
'trxvu_voltage' / Int8ub)

EPS_Batt_Voltage = Struct(
'eps_batt_voltage' / Int8ub)

OBC_Current = Struct(
'obc_5.0_current' / Int16ub)

EPS_Currents = Struct(
'eps_total_pv_current' / Int16ub,
'eps_total_system_current' / Int16ub)

Beacon0 = Struct(
    'header' / Header,
    'callsign' / Callsign,
    'obc' / OBC,
    'gyro' / Gyro,
    'timestamp' / Timestamp_Struct,
    'obc_temp' / OBC_Temp,
    'eps_temp' / EPS_Temp,
    'ants' / Ants,
    'trxvu_temp' / TRXVU_Temp,
    'adcs' / ADCS,
    'solar_panels' / Solar_Panels,
    'obc_voltages' / OBC_Voltages,
    'trxvu_voltage' / TRXVU_Voltage,
    'eps_batt_voltage' / EPS_Batt_Voltage,
    'obc_current' / OBC_Current,
    'eps_currents' / EPS_Currents)

Beacon = Select(Beacon0)
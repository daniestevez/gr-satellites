#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# This is based on the telemetry parser from
# https://github.com/danalvarez/gr-quetzal1/blob/master/apps/quetzal1_parse.py

from construct import *
from ..adapters import *
from .ax25 import Header as AX25Header
from .csp import CSPHeader

CDHS = Struct(
    'rtc_hour' / Int8ub,
	'rtc_min' / Int8ub,
	'rtc_sec' / Int8ub,
	'rtc_day' / Int8ub,
	'rtc_month' / Int8ub,
	'rtc_year' / Int8ub,
	'adm_status' / Hex(Int8ub),
	'eps_status' / Hex(Int8ub),
	'htr_status' / Hex(Int8ub),
	'adcs_status' / Hex(Int8ub),
	'pld_status' / Hex(Int8ub),
	'adm_reset_counter' / Int8ub,
	'eps_reset_counter' / Int8ub,
	'adcs_reset_counter1' / Int8ub, # software reset counter
	'adcs_reset_counter2' / Int8ub, # hardware reset counter
	'comm_reset_counter' / Int8ub,
	'reset_counter' / Int16ub
)

INA260 = Struct(
    'voltage' / LinearAdapter(1/0.01785, Int8ub),
    'current' / LinearAdapter(1/0.6109, Int16ub)
)

FaultFlags = BitStruct(
     #bits 0, 1, 2, 3  = overcurrent flags; bits 4, 5, 6, 7 =  short circuit flags.
     # bits 0,4 = ADCS
     # bits 1,5 = COMMS
	 # bits 2,6 = PLD
	 # bits 3,7 = HEATER
     'heater_short_circuit' / Flag,
     'pld_short_circuit' / Flag,
     'comms_short_circuit' / Flag,
     'adcs_short_circuit' / Flag,
     'heater_overcurrent' / Flag,
     'pld_overcurrent' / Flag,
     'comms_overcurrent' / Flag,
     'adcs_overcurrent' / Flag
)

CTFlags = BitStruct(
    Padding(3),
    # bit0 = INA260 1, bit1 = INA260 2, bit2 = INA260 3, bit3 = BQ27441, bit4 = TMP100
    'TMP100' / Flag,
    'BQ27441' / Flag,
    'INA260_3' / Flag,
    'INA260_2' / Flag,
    'INA260_1' / Flag
)

EPS = Struct(
    # TMP100
	'tmp' / AffineAdapter(1/0.377, 25/0.377, Int8ub),

    # BQ27441 No. 1
	'SoC' / Int8ub,
	'bat_voltage' / AffineAdapter(1/7.9681, -2492.0319/7.9681, Int8ub),
	'ave_current' / AffineAdapter(1/1.2219, 2500/1.2219, Int16ub),
	'remaining_capacity' / LinearAdapter(1/0.97752, Int16ub),
	'ave_power' / AffineAdapter(1/4.1544, 8500/4.1544, Int16ub),
	'SoH' / Int8ub,

	# INA260 No. 1
	'ina260' / INA260[3],

	# Subsystem Currents
	'ADCS_current' / Int16ub,
	'COMM_current' / Int16ub,
	'PLD_current' / Int16ub,
	'HTR_current' / Int16ub,
	
	# Overcurrent and Short Circuit Flags
	'fault_flags' / FaultFlags,
    
    # Communication and Transmission Flags
	'comm_flag' / CTFlags,
	'trans_flag' / CTFlags
)

ADCSFlags = BitStruct(
     # bit0 = BNO055, bit1 = ADC1, bit2 = ADC2, bit3 = TMP100
     Padding(4),
     'TMP100' / Flag,
     'ADC2' / Flag,
     'ADC1' / Flag,
     'BNO055' / Flag
)

ADCS = Struct(
    # BNO055 Gyroscope
	'gyr' / AffineAdapter(1.275, 127.5, Int8ub)[3],

	# BNO055 Magnetometer
	'mag_x' / AffineAdapter(8192.0/325, 65536.0/2, Int16ub),
    'mag_y' / AffineAdapter(8192.0/325, 65536.0/2, Int16ub),
    'mag_z' / AffineAdapter(8192.0/625, 65536.0/2, Int16ub),

	# ADC No. 1
	'adc' / LinearAdapter(77.27, Int8ub)[12],

	# Temperature Sensors
	'bno_temp' / Int8sb,
	'tmp100' / Int16sb,

	# Communication and Transmission Flags
	'flags' / ADCSFlags
)

Comm = Struct(
    'package_counter' / Int32ub
)

PLD = Struct(
    'operation' / Hex(Int8ub),
    'picture_counter' / Int16ub
)

RamParams = Struct(
    'cdhs_cycle_time' / Int8ub,
    'cdhs_wdt_time' / Int8ub,
    'adm_soc_lim' / Int8ub,
    'adcs_soc_lim' / Int8ub,
    'comm_soc_lim' / Int8ub,
    'pld_soc_lim' / Int8ub,
    'htr_cycle_time' / Int8ub,
    'htr_on_time' / Int8ub,
    'htr_off_time' / Int8ub,
    'adm_cycle_time' / Int8ub,
    'adm_burn_time' / Int8ub,
    'adm_max_cycles' / Int8ub,
    'adm_wait_time' / Int8ub[2],
    'adm_enable' / Int8ub,
    'comm_cycle_time' / Int8ub,
    'pld_cycle_time' / Int8ub,
    'pld_op_mode' / Int8ub,
    'cam_res' / Int8ub,
    'cam_expo' / Int8ub,
    'cam_pic_save_time' / Int8ub,
    'pay_enable' / Int8ub
)

telemetry = Struct(
    'identifier' / Bytes(8),
    'CDHS' / CDHS,
    'EPS' / EPS,
    'ADCS' / ADCS,
    'Comm' / Comm,
    'PLD' / PLD,
    'ram_params' / RamParams,
    'uvg_message' / Bytes(27)
)

ack = Struct(
    'ack' /  Int8ub[2]
    )

flash_params = Struct(
    'flash_params' / RamParams[2]
)

image_data = Struct(
    'image_data' / Bytes(232)
)

quetzal1 = Struct(
    'ax25_header' / AX25Header,
    'csp_header' / CSPHeader,
    'payload' / Select(image_data, telemetry, flash_params, ack)
)

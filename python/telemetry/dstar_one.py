#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018,2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

from construct import *
from ..adapters import LinearAdapter

Beacon = Struct(
    Const(b'\x6c'),
    Const(b'\xa3'),
    'time' / Int32ul,
    'reboots' / Int32ul,
    'rtc_val' / Int32ul,
    'bat_charge_in' / LinearAdapter(1/(2.5/(4096*20*0.05)), Int16ub),
    'bat_charge_out' / LinearAdapter(1/(2.5/(4096*20*0.033)), Int16ub),
    'bat_voltage' / LinearAdapter(1/(2.5/4096*((124+27.4)/27.4)), Int16ub),
    'supply_5V' / LinearAdapter(1/(2.5/4096*((30.1+18.2)/18.2)), Int16ub),
    'supply_3V3' / LinearAdapter(1/(2.5/4096*((18.2+18.2)/18.2)), Int16ub),
    'pcu_total_curr' / LinearAdapter(1/(2.5/(4096*20*1)), Int16ub),
    'solar_curr' / LinearAdapter(1/(2.5/(4096*20*0.1)), Int16ub)[6],
    'solar_total_v' / LinearAdapter(1/(2.5/4096*(30.1+18.2)/18.2), Int16ub),
    'vcc_curr' / LinearAdapter(1/(2.5/(4096*20*0.1)), Int16ub)[4],
    'vcc_curr2' / LinearAdapter(1/(2.5/(4096*20*0.05)), Int16ub)[4],
    'ss_total_curr' / LinearAdapter(1/(2.5/(4096*20*0.1)), Int16ub),
    'eeprom_curr1' / LinearAdapter(1/(2.5/(4096*20*0.2)), Int16ub),
    'eeprom_curr2' / LinearAdapter(1/(2.5/(4096*20*1)), Int16ub),
    'ext_adc_curr' / LinearAdapter(1/(2.5/(4096*20*1)), Int16ub)[4],
    'rtc_curr' / LinearAdapter(1/(2.5/(4096*20*1)), Int16ub),
    'charger_dcdc_v' / LinearAdapter(1/(2.5/(4096*20*0.1)), Int16ub),
    'system_v' / LinearAdapter(1/(2.5/(4096*20*0.1)), Int16ub),
    'obc_curr' / LinearAdapter(1/(2.5/(4096*20*0.1)), Int16ub),
    'switches' / Int8ub[3],
    'reserved1' / Int8ub,
    'battery_temp' / Int16sl,
    'schedule' / Int8ub,
    'reserved2' / Bytes(10),
    'mode' / Int8ub,
    'filler' / Bytes(10),
    'crc' / Int16ub)

dstar_one = Struct(
    'control' / Bytes(2),
    'beacon' / Beacon
    )

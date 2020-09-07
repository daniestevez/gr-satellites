#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

from construct import *

from .ax25 import Header as AX25Header
from ..adapters import LinearAdapter, AffineAdapter

import math

Header = Struct(
    'command_id' / Int8ub,
    'seq_number' / Int8ub,
    'length' / Int8ub
    )

OperatingMode = Enum(Int8ub, off = 0, test = 1, await_launch = 2, launch = 3,
                         latency = 4, initialization = 5, commissioning = 6, safe = 7,
                         beacon = 8, nominal = 9, experiment = 10)

BatteryWarning = Enum(BitsInteger(2), none = 0, low = 1, critical = 2, high = 3)

class TemperatureAdapter(Adapter):
    def __init__(self, *args, **kwargs):
        return Adapter.__init__(self, *args, **kwargs)
    def _decode(self, obj, context, path = None):
        return 0,336*(obj - 1708.1) if obj >= 1707.0 else \
          6.41 * (4.15 - math.sqrt(17.24 - 0.31 * (obj - 1712.2)))
# temporarily disabled since the formula above does not seem correct
#TemperatureAdapter(BitsInteger(12))
Temperature = BitsInteger(12)
          
class BatteryTempAdapter(Adapter):
    def __init__(self, *args, **kwargs):
        return Adapter.__init__(self, *args, **kwargs)
    def _decode(self, obj, context, path = None):
        return 1.2 * (60 - math.sqrt(3600 - 1.72 * (2333 - obj)))
BatteryTemp = BatteryTempAdapter(BitsInteger(12))

PSUCurrent = AffineAdapter(232.6, 0.42, BitsInteger(12))

AnalogData = BitStruct(
    'BATT_TBAT_TM' / BatteryTemp[3],
    'reserved' / BitsInteger(12),
    'BATT_VBAT_TM' / AffineAdapter(264.1, -4039.2, BitsInteger(12)),
    'PSU_T_TM' / BitsInteger(12),
    'p3V3_TM' / BitsInteger(12),
    'p5V_TM' / BitsInteger(12),
    'p15V_TM' / BitsInteger(12),
    'n15V_TM' / BitsInteger(12),
    'PSU_Ip5V_TM' / PSUCurrent,
    'PSU_Ip15V_TM' / PSUCurrent,
    'PSU_In15V_TM' / PSUCurrent,
    'PSU_Ip3V3_TM' / PSUCurrent,
    'PDU_IVBUS_TM' / PSUCurrent,
    'PV_TPSXp_TM'  / Temperature,
    'PV_TPSXn_TM'  / Temperature,
    'PV_TPSYp_TM'  / Temperature,
    'PV_TPSYn_TM'  / Temperature,
    'PV_TPSZp_TM'  / Temperature,
    'PV_ISPXp_TM'  / AffineAdapter(810.64, 1688.3, BitsInteger(12)),
    'PV_ISPXn_TM'  / AffineAdapter(656.02, 1622.3, BitsInteger(12)),
    'PV_ISPYp_TM'  / AffineAdapter(853.8, 1798.4, BitsInteger(12)),
    'PV_ISPYn_TM'  / AffineAdapter(810.64, 1688.3, BitsInteger(12)),
    'PV_ISPZp_TM'  / AffineAdapter(638.81, 1571.8, BitsInteger(12)),
    'OBC_T_TM'  / BitsInteger(12),
    'MGM_T_TM' / Temperature[3],
    'MGM_xyz_TM'  / BitsInteger(12)[9],
    'MGM_TX_TM'  / BitsInteger(12),
    'MODEM_T_TR_TM'  / Temperature,
    'EBOX_T_INT_TM'  / Temperature,
    'EBOX_T_EXT_TM'  / Temperature,
    'BATT_T_EXT_TM'  / Temperature,
    'BATT_T_INT_TM'  / Temperature,
    'SS6_XYZ_TM'  / AffineAdapter(17.7, -201.4, BitsInteger(12))[6],
    'RW_T_TM' / Temperature[2],
    'TP_TM' / Temperature[6],
    )

DigitalData = BitStruct(
    'battery_warning' / BatteryWarning,
    'DAS_p3V' / Flag,
    'DAS_p5V' / Flag,
    'DAS_p15V' / Flag,
    'DAS_n15V' / Flag,
    'DAS_p3V3' / Flag,
    'DAS_p5V_2' / Flag,
    'MGM1_p5V' / Flag,
    'MGM2_p5V' / Flag,
    'MGM3_p15V' / Flag,
    'MGM3_n15V' / Flag,
    'MGT_X_VBUS' / Flag,
    'TEMP_A_p5V' / Flag,
    'TEMP_B_p5V' / Flag,
    'MODEM_VBUS' / Flag,
    'RW_p5V' / Flag,
    'RW_VBUS' / Flag,
    'MTS_VBUS' / Flag,
    Padding(5)
    )

Time = LinearAdapter(4.0, Int32ub) 

HousekeepingData = Struct(
    'operating_mode' / OperatingMode,
    'snapshot_time' / Time,
    'analog_data' / AnalogData,
    'digital_data' / DigitalData
    )

Data = Struct(
    'sent_time' / Time,
    'housekeeping' / HousekeepingData
    )

upmsat_2 = Struct(
    'ax25_header' / AX25Header,
    'header' / Header,
    'data' / Data
    )

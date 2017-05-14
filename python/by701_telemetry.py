#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Daniel Estevez <daniel@destevez.net>
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
from math import log10

PayloadMode = BitStruct('open_telecommand' / Flag,\
                     'camera_task' / Flag,\
                     'valid_image_data' / Flag,\
                     'camera_power' / Flag,\
                     'rest' / Nibble)

class Iv3Adapter(Adapter):
    def _encode(self, obj, context):
        return int(obj * 10.0) & 0x1fff
    def _decode(self, obj, context):
        return (obj & 0x1fff) / 10.0
Iv3 = Iv3Adapter(Int16sl)

class IvbattAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj * 2.5) & 0x1fff
    def _decode(self, obj, context):
        return (obj & 0x1fff) / 2.5
Ivbatt = IvbattAdapter(Int16sl)

class VoltageAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj * 2000.0) & 0xfff8
    def _decode(self, obj, context):
        return (obj & 0xfff8) / 2000.0
Voltage = VoltageAdapter(Int16sl)

class TSTM32Adapter(Adapter):
    def _encode(self, obj, context):
        return int(4096.0*(2.5*(obj - 25.0) + 760.0)/3000.0)
    def _decode(self, obj, context):
        return (obj * 3000.0 / 4096.0 - 760.0) / 2.5 + 25.0
TSTM32 = TSTM32Adapter(Int16sl)

class TPAAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj*16.0) << 3
    def _decode(self, obj, context):
        return (obj >> 3) / 16.0
TPA = TPAAdapter(Int16sl)

class DCFMTCAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj*352.7)
    def _decode(self, obj, context):
        return obj/352.7
DCFMTC = DCFMTCAdapter(Int16sl)

class DCFMHamAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj*6864.0)
    def _decode(self, obj, context):
        return obj/6864.0
DCFMHam = DCFMHamAdapter(Int16sl)

class RSSIAdapter(Adapter):
    def _encode(self, obj, context):
        return int(10**((obj + 147.0)/10.0))
    def _decode(self, obj, context):
        return 10*log10(obj) - 147.0
RSSI = RSSIAdapter(Int32ul)

class RuntimeAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj * 1000.0)
    def _decode(self, obj, context):
        return obj / 1000.0
Runtime = RuntimeAdapter(Int32ul)

class CTCSSCountAdapter(Adapter):
    def _encode(self, obj, context):
        return int(obj / 0.04)
    def _decode(self, obj, context):
        return obj / 0.04
CTCSSCount = CTCSSCountAdapter(Int32ul)
             
Hk_STM32 = Struct(Const(b'\x1c\xa1'),\
                  'config' / Int8ul,\
                  'flag_direct_ins' / Int8ul,\
                  'payload_mode' / PayloadMode,\
                  'tx_mode' / Int8ul,\
                  'gain_tx' / Int16sl,\
                  'i_3v3' / Iv3,\
                  'u_3v3' / Voltage,\
                  'i_vbat_tx' / Ivbatt,\
                  'u_vbat_tx' / Voltage,\
                  'i_vbat_rx' / Ivbatt,\
                  'u_vbat_rx' / Voltage,\
                  't_stm32' / TSTM32,\
                  't_pa' / TPA,\
                  'n_tx_rf' / Int16ul,\
                  'n_rx_rf' / Int16ul,\
                  'n_tx_err_rf' / Int16ul,\
                  'n_tx_err_rf' / Int16ul,\
                  'n_tx_i2c' / Int16ul,\
                  'n_rx_i2c' / Int16ul,\
                  'n_tx_err_i2c' / Int16ul,\
                  'n_rx_err_i2c' / Int16ul,\
                  'n_tc' / Int32ul,\
                  'dc_fm_tc' / DCFMTC,\
                  'dc_fm_ham' / DCFMHam,\
                  'rssi_fm_tc' / RSSI,\
                  'rssi_fm_ham' / RSSI,\
                  'reset_flag' / Int8ul,\
                  'sys_flag' / Int8ul,\
                  'dma_overflow' / Int16ul,\
                  'runtime' / Runtime,\
                  'reset_count' / Int32ul,\
                  'ctcss_count' / CTCSSCount,\
                  'ctcss_det' / Float32l)

Cfg = Struct(Const(b'\x1c\xa2'),\
             'gain_tx_HI' / Int16sl,\
             'gain_tx_LO' / Int16sl,\
             'bias_I' / Int16sl,\
             'bias_Q' / Int16sl,\
             'threshold_u_vbat_rx_powerdown' / Int16sl,\
             'threshold_u_vbat_rx_repeateroff' / Int16sl,\
             'threshold_t_pa' / Int8sl,\
             'cam_ham_interval' / Int8ul,\
             'cam_ham_en' / Int8ul,\
             'ctcss_en' / Int8ul,\
             'ctcss_n_integration' / Int8ul,\
             'ctcss_n_tail' / Int8ul,\
             'ctcss_coeff' / Float32l,\
             'ctcss_threshold' / Float32l,\
             'gain_fmdm_ham' / Float32l,\
             'gain_fmdm_tc' / Float32l,\
             'interval_hk_OBC' / Int32ul,\
             'interval_hk_TLM' / Int32ul,\
             'interval_hk_BEACON' / Int32ul,\
             'message' / String(28),\
             'cam_delay' / Int32ul,\
             'crc' / Int32ul)

Hk_AVR = Struct(Const(b'\x1c\xa3'),\
                'adf7021_ld' / Int8ul,\
                'err_flag' / Int8ul,\
                'n_tx_i2c' / Int16ul,\
                'n_rx_i2c' / Int16ul,\
                'n_tx_232' / Int16ul,\
                'n_rx_232' / Int16ul,\
                'runtime' / Runtime,\
                'rssi_analog' / Int8ul,\
                'n_rssi_const' / Int8ul,\
                'unlock_count' / Int8ul,\
                'reset_flag' / Int8ul,\
                'reset_count' / Int32ul )

def beacon_parse(data):
    for beacon in [Hk_STM32, Cfg, Hk_AVR]:
        try:
            return beacon.parse(data)
        except Exception:
            pass
    return None

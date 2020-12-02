#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Stefano Speretta <s.speretta@tudelft.nl>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *
from .ax25 import Header
from ..adapters import LinearAdapter
from ..adapters import AffineAdapter
import math


partialBootCounter = 0
partialMeBoZpI = 0
partialMeBoZnI = 0
ComboI = 0
RAP1TXI = 0
RAP2RXI = 0
RAP2TXI = 0
RAP2FWDP = 0
RAP1REFP = 0
RAP2REFP = 0
RAP2RSSI = 0
RAP1Doppler = 0
RAP2Doppler = 0
RAP2T = 0


class ProcessFrameID(Adapter):
    def _decode(self, obj, context, path=None):
        global partialBootCounter
        partialBootCounter = (int(obj) >> 2) & 0x3F
        return int(obj) & 3


class ProcessBootCounter(Adapter):
    def _decode(self, obj, context, path=None):
        global partialBootCounter
        return ((int(obj) & 0x3F) << 6) + partialBootCounter


class ProcessFM430_I(Adapter):
    def _decode(self, obj, context, path=None):
        global partialMeBoZp
        partialMeBoZp = (int(obj) >> 2) & 0x3F
        return float((int(obj) >> 8) | ((int(obj) & 0x03) << 8)) * 0.395


class ProcessMeBoZp_I(Adapter):
    def _decode(self, obj, context, path=None):
        global partialMeBoZpI
        global partialMeBoZnI
        partialMeBoZnI = (int(obj) >> 4) & 0x0F
        return float(((int(obj) & 0x0F) << 6) + partialMeBoZp) * 0.395


class ProcessMeBoZn_I(Adapter):
    def _decode(self, obj, context, path=None):
        global partialMeBoZnI
        global ComboI
        ComboI = (int(obj) >> 6) & 0x03
        return float(((int(obj) & 0x3F) << 4) + partialMeBoZnI) * 0.395


class ProcessCombo_I(Adapter):
    def _decode(self, obj, context, path=None):
        global ComboI
        return float(((int(obj) & 0xFF) << 2) + ComboI) * 0.395


class ProcessRAP1Rx_I(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP1TXI
        RAP1TXI = (int(obj) >> 2) & 0x3F
        return float((int(obj) >> 8) | ((int(obj) & 0x03) << 8)) * 0.395


class ProcessRAP1Tx_I(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP1TXI
        global RAP2RXI
        RAP2RXI = (int(obj) >> 4) & 0x0F
        return float(((int(obj) & 0x0F) << 6) + RAP1TXI) * 0.395


class ProcessRAP2Rx_I(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2RXI
        global RAP2TXI
        RAP2TXI = (int(obj) >> 6) & 0x03
        return float(((int(obj) & 0x3F) << 4) + RAP2RXI) * 0.395


class ProcessRAP2Tx_I(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2TXI
        return float(((int(obj) & 0xFF) << 2) + RAP2TXI) * 0.395


class ProcessRAP1Fwd_P(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2FWDP
        RAP2FWDP = (int(obj) >> 2) & 0x3F
        return (
            float((int(obj) >> 8) | ((int(obj) & 0x03) << 8)) ** 2
            * 0.000478)


class ProcessRAP2Fwd_P(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2FWDP
        global RAP1REFP
        RAP1REFP = (int(obj) >> 4) & 0x0F
        return float(((int(obj) & 0x0F) << 6) + RAP2FWDP) ** 2 * 0.000478


class ProcessRAP1Ref_P(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP1REFP
        global RAP2REFP
        RAP2REFP = (int(obj) >> 6) & 0x03
        return float(((int(obj) & 0x3F) << 4) + RAP1REFP) ** 2 * 0.000478


class ProcessRAP2Ref_P(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2REFP
        return float(((int(obj) & 0xFF) << 2) + RAP2REFP) ** 2 * 0.000478


class ProcessRAP1RSSI_P(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2RSSI
        RAP2RSSI = (int(obj) >> 2) & 0x3F
        return float((int(obj) >> 8) | ((int(obj) & 0x03) << 8)) * 3.23


class ProcessRAP2RSSI_P(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2RSSI
        global RAP1Doppler
        RAP1Doppler = (int(obj) >> 4) & 0x0F
        return float(((int(obj) & 0x0F) << 6) + RAP2RSSI) * 3.23


class ProcessRAP1Doppler_V(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP1Doppler
        global RAP2Doppler
        RAP2Doppler = (int(obj) >> 6) & 0x03
        return float(((int(obj) & 0x3F) << 4) + RAP1Doppler) * 3.23


class ProcessRAP2Doppler_V(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2Doppler
        return float(((int(obj) & 0xFF) << 2) + RAP2Doppler) * 3.23


class ProcessRAP1_T(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2T
        RAP2T = (int(obj) >> 2) & 0x3F
        return float((int(obj) >> 8) | ((int(obj) & 0x03) << 8)) * 0.213 - 68.1


class ProcessRAP2_T(Adapter):
    def _decode(self, obj, context, path=None):
        global RAP2T
        return float(((int(obj) & 0x0F) << 6) + RAP2T) * 0.213 - 68.1


class BitArrayToByteArray(Adapter):
    def _decode(self, obj, context, path=None):
        sz = int(math.ceil(len(obj)/8))
        print("sie:  " + str(sz))
        out = bytearray(sz)
        for x in range(0, sz):
            for y in range(0, 7):
                out[sz - 1 - x] = out[sz - 1 - x] | (obj[x * 8 + y] << y)
        return out


OperationalMode = Enum(BitsInteger(4),
                       Idle=0,
                       Deployment=1,
                       Basic=2,
                       Science=3,
                       Transponder=4)

Housekeeping = BitStruct(
    'PICStatus_EMP' / BitsInteger(1),
    'RXcmd_ID' / BitsInteger(1),
    'SuccessfulBootCounter' / ProcessBootCounter(BitsInteger(6)),
    'PICStatus_CEP' / BitsInteger(1),
    'PICStatus_MDP1' / BitsInteger(1),
    'PICStatus_MDP2' / BitsInteger(1),
    'PICStatus_RBP1' / BitsInteger(1),
    'PICStatus_RBP2' / BitsInteger(1),
    'PICStatus_RCP1' / BitsInteger(1),
    'PICStatus_RCP2' / BitsInteger(1),
    'PICStatus_AWP' / BitsInteger(1),
    'PICStatus_ADP1' / BitsInteger(1),
    'PICStatus_ADP2' / BitsInteger(1),
    'PICStatus_ADP3' / BitsInteger(1),
    'PICStatus_ADP4' / BitsInteger(1),
    'PICStatus_MEP1' / BitsInteger(1),
    'PICStatus_MEP2' / BitsInteger(1),
    'PICStatus_REP1' / BitsInteger(1),
    'PICStatus_REP2' / BitsInteger(1),
    'MemoryStatus1' / BitArrayToByteArray(Bytes(64)),
    'MemoryStatus2' / BitArrayToByteArray(Bytes(64)),
    'deployStatusVector_SP_ZpXm' / BitsInteger(1),
    'deployStatusVector_SP_ZpXp' / BitsInteger(1),
    'deployStatusVector_MAB_ZmYp' / BitsInteger(1),
    'deployStatusVector_MAB_ZmXp' / BitsInteger(1),
    'deployStatusVector_MAB_ZmYm' / BitsInteger(1),
    'deployStatusVector_MAB_ZmXm' / BitsInteger(1),
    'deployStatusVector_SP_ZmYm' / BitsInteger(1),
    'deployStatusVector_SP_ZmYp' / BitsInteger(1),
    'operationalMode' / OperationalMode,
    'deployStatusVector_MAB_ZpXm' / BitsInteger(1),
    'deployStatusVector_MAB_ZpYp' / BitsInteger(1),
    'deployStatusVector_MAB_ZpXp' / BitsInteger(1),
    'deployStatusVector_MAB_ZpYm' / BitsInteger(1),
    'bus_V_sys' / LinearAdapter(1/0.049, BitsInteger(8)),  # V
    'bus_V_dep' / LinearAdapter(1/0.049, BitsInteger(8)),  # V
    'OBC_T' / AffineAdapter(1/0.6875, 80, BitsInteger(8)),  # degC
    'SP_I_ZpXp' / LinearAdapter(1/1.95, BitsInteger(8)),  # mA
    'SP_I_ZmYm' / LinearAdapter(1/1.95, BitsInteger(8)),  # mA
    'SP_I_ZpXm' / LinearAdapter(1/1.95, BitsInteger(8)),  # mA
    'SP_I_ZmYp' / LinearAdapter(1/1.95, BitsInteger(8)),  # mA
    'FM430_I' / ProcessFM430_I(BitsInteger(16)),  # mA
    'MeBo_Zp_I' / ProcessMeBoZp_I(BitsInteger(8)),  # mA
    'MeBo_Zn_I' / ProcessMeBoZn_I(BitsInteger(8)),  # mA
    'Combo_I' / ProcessCombo_I(BitsInteger(8)),  # mA
    'RAP1Rx_I' / ProcessRAP1Rx_I(BitsInteger(16)),  # mA
    'RAP1Tx_I' / ProcessRAP1Tx_I(BitsInteger(8)),  # mA
    'RAP2Rx_I' / ProcessRAP2Rx_I(BitsInteger(8)),  # mA
    'RAP2Tx_I' / ProcessRAP2Tx_I(BitsInteger(8)),  # mA
    'RAP1FwdPower' / ProcessRAP1Fwd_P(BitsInteger(16)),  # mW
    'RAP2FwdPower' / ProcessRAP2Fwd_P(BitsInteger(8)),  # mW
    'RAP1ReflPower' / ProcessRAP1Ref_P(BitsInteger(8)),  # mW
    'RAP2ReflPower' / ProcessRAP2Ref_P(BitsInteger(8)),  # mW
    'RAP1RSSI' / ProcessRAP1RSSI_P(BitsInteger(16)),  # mV
    'RAP2RSSI' / ProcessRAP2RSSI_P(BitsInteger(8)),  # mV
    'RAP1Doppler_V' / ProcessRAP1Doppler_V(BitsInteger(8)),  # V
    'RAP2Doppler_V' / ProcessRAP2Doppler_V(BitsInteger(8)),  # V
    'RAP1T' / ProcessRAP1_T(BitsInteger(16)),  # degC
    'RAP2T' / ProcessRAP2_T(BitsInteger(8)),  # degC
    'AWSS1' / BitArrayToByteArray(Bytes(168)),
    'AWSS2' / BitArrayToByteArray(Bytes(168)),

    # V
    'ReferenceDiode_Voltage_ZpXp' / LinearAdapter(1/0.002, BitsInteger(8)),
    # V
    'ReferenceDiode_Voltage_ZpXn' / LinearAdapter(1/0.002, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZpXp' / LinearAdapter(1/0.004, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZpXn' / LinearAdapter(1/0.004, BitsInteger(8)),
    # V
    'ReferenceDiode_Voltage_ZnYm' / LinearAdapter(1/0.002, BitsInteger(8)),
    # V
    'ReferenceDiode_Voltage_ZnYp' / LinearAdapter(1/0.002, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZnYm' / LinearAdapter(1/0.004, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZnYp' / LinearAdapter(1/0.004, BitsInteger(8))
    )

Payload = BitStruct(
    'TFSC_Current_ZpXp_0' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_0' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXp_1' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_1' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXp_2' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_2' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXp_3' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_3' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXp_4' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_4' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXp_5' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_5' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXp_6' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_6' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXp_7' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXp_7' / LinearAdapter(1/0.008, BitsInteger(8)),  # V

    'TFSC_Current_ZpXm_0' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_0' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXm_1' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_1' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXm_2' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_2' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXm_3' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_3' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXm_4' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_4' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXm_5' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_5' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXm_6' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_6' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZpXm_7' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZpXm_7' / LinearAdapter(1/0.008, BitsInteger(8)),  # V

    'TFSC_Current_ZmXp_0' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_0' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXp_1' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_1' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXp_2' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_2' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXp_3' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_3' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXp_4' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_4' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXp_5' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_5' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXp_6' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_6' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXp_7' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXp_7' / LinearAdapter(1/0.008, BitsInteger(8)),  # V

    'TFSC_Current_ZmXm_0' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_0' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXm_1' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_1' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXm_2' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_2' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXm_3' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_3' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXm_4' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_4' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXm_5' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_5' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXm_6' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_6' / LinearAdapter(1/0.008, BitsInteger(8)),  # V
    'TFSC_Current_ZmXm_7' / LinearAdapter(1/0.004, BitsInteger(8)),  # A
    'TFSC_Voltage_ZmXm_7' / LinearAdapter(1/0.008, BitsInteger(8)),  # V

    # degC
    'TFSC_Temperature_ZpXp' / AffineAdapter(1/1.492, -235.0, BitsInteger(8)),
    # degC
    'TFSC_Temperature_ZpXm' / AffineAdapter(1/1.389, -235.0, BitsInteger(8)),

    # degC
    'TFSC_Temperature_ZmXp' / AffineAdapter(1/1.445, -235.0, BitsInteger(8)),
    # degC
    'TFSC_Temperature_ZmXm' / AffineAdapter(1/1.345, -235.0, BitsInteger(8)),

    # V
    'ReferenceDiode_Voltage_ZpXp' / LinearAdapter(1/0.002, BitsInteger(8)),
    # V
    'ReferenceDiode_Voltage_ZpXn' / LinearAdapter(1/0.002, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZpXp' / LinearAdapter(1/0.004, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZpXn' / LinearAdapter(1/0.004, BitsInteger(8)),
    # V
    'ReferenceDiode_Voltage_ZnYm' / LinearAdapter(1/0.002, BitsInteger(8)),
    # V
    'ReferenceDiode_Voltage_ZnYp' / LinearAdapter(1/0.002, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZnYm' / LinearAdapter(1/0.004, BitsInteger(8)),
    # mA
    'ReferenceDiode_Current_ZnYp' / LinearAdapter(1/0.004, BitsInteger(8)),

    'AWSS' / BitArrayToByteArray(Bytes(168))
    )

Auxiliary = Struct(
    Padding(6)
    )

delfic3 = Struct(
    'ax25_header' / Header,
    'BootNumber' / BytesInteger(2, swapped=True),
    'FrameNumber' / BytesInteger(2, swapped=True),
    'FrameID' / ProcessFrameID(BytesInteger(1)),
    'packet' / Switch(lambda c: (c.FrameID), {
        1: Payload,
        2: Housekeeping})
    )

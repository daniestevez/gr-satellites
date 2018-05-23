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
import construct

import datetime
from distutils.version import LooseVersion

from adapters import LinearAdapter

LTUFrameHeader = BitStruct(
    'SrcId' / BitsInteger(7),
    'DstId' / BitsInteger(7),
    'FrCntTx' / BitsInteger(4),
    'FrCntRx' / BitsInteger(4),
    'SNR' / BitsInteger(4),
    'AiTypeSrc' / BitsInteger(4),
    'AiTypeDst' / BitsInteger(4),
    'DfcId' / BitsInteger(2),
    'Caller' / Flag,
    'Arq' / Flag,
    'PduTypeId' / Flag,
    'BchRq' / Flag,
    'Hailing' / Flag,
    'UdFl1' / Flag,
    'PduLength' / BitsInteger(10),
    'CRC13' / BitsInteger(13),
    'CRC5' / BitsInteger(5),
    Padding(2)
    )

class TimeAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        d = int((obj - datetime.datetime(2000, 1, 1))*2)
        return Container(days = d.days, milliseconds = d.seconds * 1000 + d.microseconds / 1000)
    def _decode(self, obj, context, path = None):
        return datetime.datetime(2000, 1, 1) + datetime.timedelta(seconds=float(obj)/2.0)

TimeStamp = TimeAdapter(BitsInteger(32, swapped=True))
    
SNETFrameHeader = BitStruct(
    Const(BitsInteger(18), 0b111100110101000000) if LooseVersion(construct.__version__) < LooseVersion('2.9') else Const(0b111100110101000000, BitsInteger(18)),
    'CRC' / BitsInteger(14),
    'FCIDMajor' / BitsInteger(6),
    'FCIDSub' / BitsInteger(10),
    'Urgent' / Flag,
    'FutureUse' / Flag,
    'CheckCRC' / Flag,
    'Multiframe' / Flag,
    'TimeTaggedSetting' / Flag,
    'TimeTagged' / Flag,
    'DataLength' / BitsInteger(10),
    'TimeTag' / If(lambda c: c.TimeTagged, TimeStamp)
    )

Battery = Struct(
    'V_BAT' / LinearAdapter(2, Int16sl),
    'A_IN_CHARGER' / LinearAdapter(12, Int16sl),
    'A_OUT_CHARGER' / LinearAdapter(6, Int16sl)
    )

BatteryCurrents = Struct(
    'A_IN' / LinearAdapter(12, Int16sl),
    'A_OUT' / LinearAdapter(12, Int16sl)
    )

EPSTelemetry = Struct(
    'CUR_SOL' / LinearAdapter(50, Int16sl)[6],
    'V_SOL' / Int16sl,
    'BATTERIES' / Battery[2],
    'V_SUM' / LinearAdapter(2, Int16sl),
    'V_3V3' / LinearAdapter(8, Int16sl),
    'V_5V' / LinearAdapter(5, Int16sl),
    'TEMP_BATT' / LinearAdapter(256, Int16sl)[2],
    'TEMP_OBC' / Int16sl,
    'A_OBC' / Int16ul,
    'V_OBC' / Int16ul,
    'BATT_CURRENTS' / BatteryCurrents[2]
    )

ADCSFlags = BitStruct(
    Padding(4),
    'AttDetTrackIGRFDeltaB' / Flag,
    'AttDetSuseAlbedoTracking' / Flag,
    'SUSE1AlbedoFlag' / Flag,
    'SUSE2AlbedoFlag' / Flag,
    'SUSE3AlbedoFlag' / Flag,
    'SUSE4AlbedoFlag' / Flag,
    'SUSE5AlbedoFlag' / Flag,
    'SUSE6AlbedoFlag' / Flag,
    'AttDetAutoVirtualizeMFSA' / Flag,
    'AttDetAutoVirtualizeSUSEA' / Flag,
    'AttDetNarrowVectors' / Flag,
    'AttDetMismatchingVectors' / Flag
)

ADCSTelemetry = Struct(
    'iModeChkListThisStepActive' / Int8sl,
    'iAttDetFinalState' / Int8ul,
    'iSensorArrayAvailStatusGA' / Int8ul,
    'iSensorArrayAvailStatusMFSA' / Int8ul,
    'iSensorArrayAvailStatusSUSEA' / Int8ul,
    'iActArrayAvailStatusRWA' / Int8ul,
    'iActArrayAvailStatusMATA' / Int8ul,
    'AttDetMfsDistCorrMode' / Int8ul,
    'AttDetSuseDistCorrMode' / Int8ul,
    'flags' / ADCSFlags,
    'omegaXOptimal_SAT' / LinearAdapter(260, Int16sl),
    'omegaYOptimal_SAT' / LinearAdapter(260, Int16sl),
    'omegaZOptimal_SAT' / LinearAdapter(260, Int16sl),
    'magXOptimal_SAT' / LinearAdapter(0.1, Int16sl),
    'magYOptimal_SAT' / LinearAdapter(0.1, Int16sl),  
    'magZOptimal_SAT' / LinearAdapter(0.1, Int16sl),
    'sunXOptimal_SAT' / LinearAdapter(32000, Int16sl),
    'sunYOptimal_SAT' / LinearAdapter(32000, Int16sl),
    'sunZOptimal_SAT' / LinearAdapter(32000, Int16sl),
    'dCtrlTorqueRWAx_SAT_lr' / LinearAdapter(38484, Int8ul),
    'dCtrlTorqueRWAy_SAT_lr' / LinearAdapter(38484, Int8ul),
    'dCtrlTorqueRWAz_SAT_lr' / LinearAdapter(38484, Int8ul),
    'dCtrlMagMomentMATAx_SAT_lr' / LinearAdapter(127, Int8ul),
    'dCtrlMagMomentMATAy_SAT_lr' / LinearAdapter(127, Int8ul),
    'dCtrlMagMomentMATAz_SAT_lr' / LinearAdapter(127, Int8ul),
    'iReadTorqueRWx_MFR' / LinearAdapter(9696969, Int16ul),
    'iReadTorqueRWy_MFR' / LinearAdapter(9696969, Int16ul),
    'iReadTorqueRWz_MFR' / LinearAdapter(9696969, Int16ul),
    'iReadRotSpeedRWx_MFR' / Int16ul,
    'iReadRotSpeedRWy_MFR' / Int16ul,
    'iReadRotSpeedRWz_MFR' / Int16ul,
    'SGP4LatXPEF' / LinearAdapter(355, Int16ul),
    'SGP4LongYPEF' / LinearAdapter(177, Int16ul),
    'SGP4AltPEF' / LinearAdapter(0.25, Int8ul),
    'AttitudeErrorAngle' / LinearAdapter(177, Int16ul),
    'TargetData_Distance' / Int16ul,
    'TargetData_ControlIsActive' / Int8ul # flag, really
    )


SNETFrame = Struct(
    'header' / SNETFrameHeader,
    'telemetry' / Switch(lambda c: (c.header.FCIDMajor, c.header.FCIDSub), {
        (0,0) : ADCSTelemetry,
        (9,0) : EPSTelemetry,
    }, default=Pass))

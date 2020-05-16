#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017, 2020 Daniel Estevez <daniel@destevez.net>
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

from construct import *

SatID = Enum(BitsInteger(2),\
                  FC1EM = 0,\
                  FC2 = 1,\
                  FC1FM = 2,\
                  extended = 3)

FrameType = Enum(BitsInteger(6),\
    WO1 = 0,\
    WO2 = 1,\
    WO3 = 2,\
    WO4 = 3,\
    WO5 = 4,\
    WO6 = 5,\
    WO7 = 6,\
    WO8 = 7,\
    WO9 = 8,\
    WO10 = 9,\
    WO11 = 10,\
    WO12 = 11,\
    HR1 = 12,\
    FM1 = 13,\
    FM2 = 14,\
    FM3 = 15,\
    HR2 = 16,\
    FM4 = 17,\
    FM5 = 18,\
    FM6 = 19,\
    HR3 = 20,\
    FM7 = 21,\
    FM8 = 22,\
    FM9 = 23)

FrameTypeNayif1 = Enum(BitsInteger(6),\
    WO1 = 0,\
    WO2 = 1,\
    WO3 = 2,\
    WO4 = 3,\
    WO5 = 4,\
    WO6 = 5,\
    WO7 = 6,\
    WO8 = 7,\
    WO9 = 8,\
    WO10 = 9,\
    WO11 = 10,\
    WO12 = 11,\
    HR1 = 12,\
    HR2 = 13,\
    HR3 = 14,\
    HR4 = 15,\
    HR5 = 16,\
    FM1 = 17,\
    FM2 = 18,\
    FM3 = 19,\
    FM4 = 20,\
    FM5 = 21,\
    FM6 = 22,\
    FM7 = 23)

class FrameTypeAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return obj.value
    def _decode(self, obj, context, path = None):
        return FrameType(obj)

FrameTypeField = FrameTypeAdapter(BitsInteger(6))

Header = BitStruct(
    'satid' / SatID,
    'frametype' / IfThenElse(lambda c: c.satid != 'extended', FrameType, FrameTypeNayif1),
    )

EPSFC1 = Struct(
    'photovoltage' / BitsInteger(16)[3],
    'photocurrent' / BitsInteger(16),
    'batteryvoltage' / BitsInteger(16),
    'systemcurrent' / BitsInteger(16),
    'rebootcount' / BitsInteger(16),
    'softwareerrors' / BitsInteger(16),
    'boostconvertertemp' / Octet[3],
    'batterytemp' / Octet,
    'latchupcount5v' / Octet,
    'latchupcount3v3' / Octet,
    'resetcause' / Octet,
    'MPPTmode' / Octet,
    )

EPSNayif1 = Struct(
    'photovoltage' / BitsInteger(14)[3],
    'batteryvoltage' / BitsInteger(14),
    'photocurrent' / BitsInteger(10)[3],
    'totalphotocurrent' / BitsInteger(10),
    'systemcurrent' / BitsInteger(10),
    'rebootcount' / Octet,
    'boostconvertertemp' / Octet[3],
    'batterytemp' / Octet,
    'latchupcount5v' / Octet,
    'channelcurrent5v' / Octet,
    'resetcause' / BitsInteger(4),
    'MPTTmode' / BitsInteger(4),
    )

iMTQMode = Enum(BitsInteger(2),\
                idle = 0,\
                selftest = 1,\
                detumble= 2)

iMTQ = Struct(
    'imtqmode' / iMTQMode,
    'imtqerrorcode' / BitsInteger(3),
    'imtqconfigurationset' / BitsInteger(1),
    'imtqmcutemperature' / Octet,
    )

class TempXpAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-158.239)/-0.2073)
    def _decode(self, obj, context, path = None):
        return -0.2073*obj + 158.239
TempXp = TempXpAdapter(BitsInteger(10))
class TempXmAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-159.227)/-0.2083)
    def _decode(self, obj, context, path = None):
        return -0.2083*obj + 159.227
TempXm = TempXmAdapter(BitsInteger(10))
class TempYpAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-158.656)/-0.2076)
    def _decode(self, obj, context, path = None):
        return -0.2076*obj + 158.656
TempYp = TempYpAdapter(BitsInteger(10))
class TempYmAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-159.045)/-0.2087)
    def _decode(self, obj, context, path = None):
        return -0.2087*obj + 159.045
TempYm = TempYmAdapter(BitsInteger(10))

class V3v3Adapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj/4.0)
    def _decode(self, obj, context, path = None):
        return 4*obj
V3v3 = V3v3Adapter(BitsInteger(10))

class V5vAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj/6.0)
    def _decode(self, obj, context, path = None):
        return 6*obj
V5v = V5vAdapter(BitsInteger(10))

# FC1
BOB = Struct(
    'sunsensor' / BitsInteger(10)[3],
    'paneltempX+' / TempXp,
    'paneltempX-' / TempXm,
    'paneltempY+' / TempYp,
    'paneltempY-' / TempYm,
    '3v3voltage' / V3v3,
    '3v3current' / BitsInteger(10),
    '5voltage' / V5v,
)

# Nayif-1
ASIB = Struct(
    'sunsensor' / BitsInteger(10)[6],
    '3v3voltage' / V3v3,
    'imtquptime' / BitsInteger(20),
    '5voltage' / V5v,
)

class RFTempAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-193.672)/-0.857)
    def _decode(self, obj, context, path = None):
        return -0.857*obj + 193.672
RFTemp = RFTempAdapter(Octet)

class RXCurrAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj/0.636)
    def _decode(self, obj, context, path = None):
        return 0.636*obj
RXCurr = RXCurrAdapter(Octet)

class TXCurrAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj/1.272)
    def _decode(self, obj, context, path = None):
        return 1.272*obj
TXCurr = TXCurrAdapter(Octet)

RF = Struct(
    'rxdoppler' / Octet,
    'rxrssi' / Octet,
    'temp' / RFTemp,
    'rxcurrent' / RXCurr,
    'tx3v3current' / RXCurr,
    'tx5vcurrent' / TXCurr,
    )

class PwrAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj/5e-3)**(1.0/2.0629))
    def _decode(self, obj, context, path = None):
        return 5e-3*obj**2.0629
Pwr = PwrAdapter(Octet)

class PACurrAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-2.5435)/0.5496)
    def _decode(self, obj, context, path = None):
        return 0.5496*obj + 2.5435
PACurr = PACurrAdapter(Octet)

PA = Struct(
    'revpwr' / Pwr,
    'fwdpwr' / Pwr,
    'boardtemp' / Octet, # TODO use lookup table
    'boardcurr' / PACurr,
    )

Ants = Struct(
    'temp' / Octet[2], # TODO use ISIS manual
    'deployment' / Flag[4],
    )

# Also valid for Nayif-1
SWFC1 = Struct(
    'seqnumber' / BitsInteger(24),
    'dtmfcmdcount' / BitsInteger(6),
    'dtmflastcmd' / BitsInteger(5),
    'dtmfcmdsuccess' / Flag,
    'datavalid' / Flag[7],
    'eclipse' / Flag,
    'safemode' / Flag,
    'hwabf' / Flag,
    'swabf' / Flag,
    'deploymentwait' / Flag,
    )

RealTimeFC1 = BitStruct(
    'eps' / EPSFC1,
    'bob' / BOB,
    'rf' / RF,
    'pa' / PA,
    'ants' / Ants,
    'sw' / SWFC1,
    )

HighResolution = BitStruct(
    'sunsensor' / BitsInteger(10)[5],
    'photocurrent' / BitsInteger(15),
    'batteryvoltage' / BitsInteger(15),
    )

HRPayload = HighResolution[20]

class TempBlackChassisAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-75.244)/-0.024)
    def _decode(self, obj, context, path = None):
        return -0.024*obj + 75.244
TempBlackChassis = TempBlackChassisAdapter(BitsInteger(12))
class TempSilverChassisAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-74.750)/-0.024)
    def _decode(self, obj, context, path = None):
        return -0.024*obj + 74.750
TempSilverChassis = TempSilverChassisAdapter(BitsInteger(12))
class TempBlackPanelAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-75.039)/-0.024)
    def _decode(self, obj, context, path = None):
        return -0.024*obj + 75.039
TempBlackPanel = TempBlackPanelAdapter(BitsInteger(12))
class TempSilverPanelAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int((obj-75.987)/-0.024)
    def _decode(self, obj, context, path = None):
        return -0.024*obj + 75.987
TempSilverPanel = TempSilverPanelAdapter(BitsInteger(12))

WholeOrbitFC1 = BitStruct(
    'tempblackchassis' / TempBlackChassis,
    'tempsilverchassis' / TempSilverChassis,
    'tempblackpanel' / TempBlackPanel,
    'tempsilverpanel' / TempSilverPanel,
    'paneltempX+' / TempXp,
    'paneltempX-' / TempXm,
    'paneltempY+' / TempYp,
    'paneltempY-' / TempYm,
    'photovoltage' / BitsInteger(16)[3],
    'photocurrent' / BitsInteger(16),
    'batteryvoltage' / BitsInteger(16),
    'systemcurrent' / BitsInteger(16),
)

Callsign = Bytes(8)

FC2Battery = Struct(
    'direction' / Flag,
    'current' / Octet,
    'voltage' / Octet,
    'temp' / Octet,
    )

EPSFC2 = Struct(
    'sunlight' / Flag,
    'solarcurrent' / BitsInteger(10)[12],
    'solartemp' / Octet,
    'batteries' / FC2Battery[3],
    'batteryheater' / Flag,
    )

SWFC2 = Struct(
    'seqnumber' / BitsInteger(24),
    'dtmfcmdcount' / BitsInteger(6),
    'dtmflastcmd' / BitsInteger(5),
    'dtmfcmdsuccess' / Flag,
    )

RealTimeFC2 = BitStruct(
    'eps' / EPSFC2,
    'antstimeout' / Octet,
    'antsstatus' / BitsInteger(12),
    'antstemp' / Octet,
    'rf' / RF,
    'pa' / PA,
    'amacmode' / BitsInteger(3),
    'magnetometer' / BitsInteger(12)[3],
    'funtrxenable' / Flag,
    'funtrxsampleenable' / Flag,
    'modemanagermode' / BitsInteger(3),
    'modemanagercommsnominal' / Flag,
    'modemanagercommsstate' / BitsInteger(2),
    'tmtcmanageridleenable' / Flag,
    'tmtceventforwarding' / Flag,
    'tcbufferreceiveenable' / BitsInteger(3),
    'tcbuffersendenable' / BitsInteger(3),
    'obcsoftresetcount' / Octet,
    'epshardresetcount' / Octet,
    Padding(20),
    'sw' / SWFC2,
    )

FC2Battery0 = Struct(
    'current' / Octet,
    'voltage' / Octet,
    'temp' / Octet,
    )

FC2Battery2 = Struct(
    'direction' / Flag,
    'current' / Octet,
    'voltage' / Octet,
    )

WholeOrbitFC2 = BitStruct(
    'tempthermistor' / BitsInteger(12)[4],
    'solartemps' / BitsInteger(8)[5],
    'battery0' / FC2Battery0,
    'battery1' / FC2Battery,
    'battery2' / FC2Battery2,
    Padding(6),
    )

RealTimeNayif1 = BitStruct(
    'eps' / EPSNayif1,
    'imtq' / iMTQ,
    'asib' / ASIB,
    'rf' / RF,
    'pa' / PA,
    'ants' / Ants,
    'sw' / SWFC1,
)

FitterMessage = Bytes(200)

Frame = Struct(
    'header' / Header,
    'extheader' / If(lambda c: c.header.satid == 'extended', Byte),
    'realtime' / Switch(lambda c: c.header.satid, {
        'FC1EM' : RealTimeFC1,
        'FC1FM' : RealTimeFC1,
        'FC2' : RealTimeFC2,
        'extended' : Switch(lambda c: c.extheader, {
            0x08 : RealTimeNayif1,
            }, default = Bytes(54)),
        }),
    'payload' / If(lambda c: hasattr(c.header.frametype, '__getitem__'),
                   Switch(lambda c: c.header.frametype[:2], {
                    'WO' : Bytes(200),
                    'HR' : HRPayload,
                    'FM' : FitterMessage,
                    })
                ),
    )

def WholeOrbit(satid):
    if satid == 'FC1EM' or satid == 'FC1FM':
        return WholeOrbitFC1
    if satid == 'FC2':
        return WholeOrbitFC2
    return Bytes(23)

WHOLEORBIT_SIZE = 23
PAYLOAD_SIZE = 200
WHOLEORBIT_MAX = 12

class Funcube:
    """Telemetry parser for FUNcube

    This is a stateful parser that reassembles Whole Orbit data
    from consecutive frames
    """
    def __init__(self):
        self.last_chunk = None
        self.last_seq = None

    def parse(self, packet):
        if len(packet) != 256:
            return

        data = Frame.parse(packet)

        if not data:
            return

        out = list()

        out.append(f'Frame type {data.header.frametype}')
        if not hasattr(data.header.frametype, '__getitem__'):
            print('Unknown frame type. Not processing frame.')
            return

        out.append('-'*40)
        out.append('Realtime telemetry:')
        out.append('-'*40)
        out.append(str(data.realtime))
        out.append('-'*40)
        if data.header.frametype[:2] == 'FM':
            out.append(f'Fitter Message {data.header.frametype[2]}')
            out.append('-'*40)
            out.append(str(data.payload))
        elif data.header.frametype[:2] == 'HR':
            out.append(f'High resolution {data.header.frametype[2]}')
            out.append('-'*40)
            out.append(str(data.payload))
        elif data.header.frametype[:2] == 'WO':
            chunk = int(data.header.frametype[2:])
            try:
                seq = data.realtime.search('seqnumber')
            except AttributeError:
                out.append('Unknown realtime format. Unable to get seqnumber.\n')
                return '\n'.join(out)
            remaining = (PAYLOAD_SIZE*chunk) % WHOLEORBIT_SIZE
            recover = True
            if chunk != 0:
                if self.last_chunk == chunk - 1 and self.last_seq == seq:
                    # can recover for last WO packet
                    wo = self.last_wo + data.payload[:-remaining]
                else:
                    recover = False
                    last_chunk_remaining = (PAYLOAD_SIZE*(chunk-1)) % WHOLEORBIT_SIZE
                    wo = data.payload[WHOLEORBIT_SIZE-last_chunk_remaining:-remaining]
            else:
                wo = data.payload[:-remaining]
            assert len(wo) % WHOLEORBIT_SIZE == 0
            wos = WholeOrbit(data.header.satid)[len(wo) // WHOLEORBIT_SIZE].parse(wo)
            self.last_chunk = chunk
            self.last_wo = data.payload[-remaining:]
            self.last_seq = seq
            out.append(f'Whole orbit {chunk}')
            if not recover:
                out.append('(could not recover data from previous beacon)')
            out.append('-'*40)
            out.append(str(wos))
            if chunk == WHOLEORBIT_MAX:
                out.append('-'*40)
                # callsign included
                out.append(f'Callsign: {Callsign.parse(self.last_wo)}')
        out.append('')

        return '\n'.join(out)

funcube = Funcube()

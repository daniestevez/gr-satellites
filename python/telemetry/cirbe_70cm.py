#!/usr/bin/env python3

# Copyright 2017, 2018, 2019, 2020 Daniel Estevez <daniel@destevez.net>
# Copyright 2022 The Regents of the University of Colorado
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import datetime

from construct import Adapter, BitsInteger, BitStruct, Container, Enum, \
                      Flag, GreedyBytes, If, Int8ub, Int16ub, Int32ub, \
                      Padding, RawCopy, Struct, Switch
from .ax25 import Header
from .cirbe_bct_soh import cirbe_bct_soh


PrimaryHeader = BitStruct(
    'ccsds_version' / BitsInteger(3),
    'packet_type' / Flag,
    'secondary_header_flag' / Flag,
    'is_stored_data' / Flag,
    'APID' / BitsInteger(10),
    'grouping_flag' / Enum(BitsInteger(2), GRP_MIDDLE=0, GRP_BEGIN=1,
                           GRP_END=2, GRP_FIRST_AND_LAST=3),
    'sequence_count' / BitsInteger(14),
    'packet_length' / BitsInteger(16)
)


SecondaryHeaderRaw = Struct(
    'time_stamp_seconds' / Int32ub,
    'sub_seconds' / Int8ub,
    Padding(1)
)


class TimeAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        return Container()

    def _decode(self, obj, context, path=None):
        t = datetime.datetime.fromtimestamp(
            obj.time_stamp_seconds,
            tz=datetime.timezone.utc
        )
        t = t.replace(tzinfo=None)
        offset = (
            datetime.datetime(2000, 1, 1, 12)
            - datetime.datetime(1970, 1, 1)
        )
        return (t + offset)


SecondaryHeader = TimeAdapter(
    SecondaryHeaderRaw
)


cirbe_70cm = Struct(
    'ax25_header' / Header,
    'primary_header' / PrimaryHeader,
    'secondary_header' / If(
        lambda c: c.primary_header.secondary_header_flag,
        SecondaryHeader
    ),
    'packet' / Switch(
        lambda c: c.primary_header.APID,
        {
            0x050: cirbe_bct_soh
        }
    )
)

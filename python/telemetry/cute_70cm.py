#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, 2018, 2019, 2020 Daniel Estevez <daniel@destevez.net>
# Copyright 2021 The Regents of the University of Colorado
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import copy
from datetime import datetime
from construct import Adapter, BitsInteger, BitStruct, Container, Enum, \
                      Flag, GreedyBytes, If, Int8ub, Int16ub, Int32ub, \
                      Padding, RawCopy, Struct, Switch
from .ax25 import Header
from .cute_bct_fsw import cute_bct_fsw
from .cute_bct_soh import cute_bct_soh
from .cute_pld import cute_pld_sw_stat

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


class TimeAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        return Container()

    def _decode(self, obj, context, path=None):
        offset = datetime(2000, 1, 1, 12) - datetime(1970, 1, 1)
        return (datetime.utcfromtimestamp(obj.time_stamp_seconds) + offset)


SecondaryHeaderRaw = Struct(
    'time_stamp_seconds' / Int32ub,
    'sub_seconds' / Int8ub,
    Padding(1)
)

SecondaryHeader = TimeAdapter(
    SecondaryHeaderRaw
)

cute_ax25_packet_header = RawCopy(Struct(
    'ax25_header' / Header,
    'primary_header' / PrimaryHeader,
    'secondary_header' / If(
        lambda c: c.primary_header.secondary_header_flag,
        SecondaryHeader
    )
))

cute_ax25_packet_fragment = Struct(
    'header' / cute_ax25_packet_header,
    'packet' / GreedyBytes
)

cute_ax25_packet_complete = Struct(
    'ax25_header' / Header,
    'primary_header' / PrimaryHeader,
    'secondary_header' / If(
        lambda c: c.primary_header.secondary_header_flag,
        SecondaryHeader
    ),
    'packet' / Switch(
        lambda c: (c.primary_header.APID),
        {
            (0x55): cute_bct_fsw,
            (0x56): cute_bct_soh,
            (0x1FF): cute_pld_sw_stat
        }
    )
)


class FswParserState(Enum):
    SEARCH_START = 0
    SEARCH_MIDDLE = 1


class CUTE:
    """Telemetry parser for the Colorado Ultraviolet Transit Experiment (CUTE)

    This is a stateful parser that reassembles flight software packets which
    span multiple AX.25 frames.
    """
    def __init__(self):
        self.frames = []
        self.state = FswParserState.SEARCH_START

    # Parses a reassembled frame
    def process(self):
        reassembled_packet = b''.join([self.frames[0].header.data] +
                                      [frame.packet for frame in self.frames])
        self.frames = []
        return cute_ax25_packet_complete.parse(reassembled_packet)

    def parse(self, packet):
        data = cute_ax25_packet_fragment.parse(packet)
        if data is None:
            return None
        primary_header = data.header.value.primary_header

        self.frames.append(data)

        if self.state == FswParserState.SEARCH_START:

            if primary_header.grouping_flag == 'GRP_MIDDLE':
                # This means we dropped/missed a frame
                self.frames = []
                return None

            elif primary_header.grouping_flag == 'GRP_BEGIN':
                self.state = FswParserState.SEARCH_MIDDLE
                return None

            elif primary_header.grouping_flag == 'GRP_END':
                # This means we dropped/missed a frame
                self.frames = []
                return None

            elif primary_header.grouping_flag == 'GRP_FIRST_AND_LAST':
                return self.process()

        elif self.state == FswParserState.SEARCH_MIDDLE:

            if primary_header.grouping_flag == 'GRP_BEGIN' or \
               primary_header.grouping_flag == 'GRP_FIRST_AND_LAST':
                # This means we dropped/missed a frame
                self.state = FswParserState.SEARCH_START
                self.frames = []
                return None

            prev_header = self.frames[-2].header.value.primary_header
            if primary_header.sequence_count != \
               (prev_header.sequence_count + 1) % (1 << 14):
                # A frame was dropped.
                self.state = FswParserState.SEARCH_START
                self.frames = []
                return None

            if primary_header.grouping_flag == 'GRP_MIDDLE':
                return None

            elif primary_header.grouping_flag == 'GRP_END':
                self.state = FswParserState.SEARCH_START
                return self.process()


cute_70cm = CUTE()

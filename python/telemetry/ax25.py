#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *


SSID = BitStruct(
    'ch' / Flag,  # C / H bit
    Default(BitsInteger(2), 3),  # reserved bits
    'ssid' / BitsInteger(4),
    'extension' / Flag  # last address bit
    )


class CallsignAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        return bytes([x << 1 for x in bytes(
            (obj.upper() + ' '*6)[:6], encoding='ascii')])

    def _decode(self, obj, context, path=None):
        return str(bytes([x >> 1 for x in obj]), encoding='ascii').strip()


Callsign = CallsignAdapter(Bytes(6))

Address = Struct(
        'callsign' / Callsign,
        'ssid' / SSID
        )

Control = Hex(Int8ub)
Control16 = Hex(Int16ub)

PID = Hex(Int8ub)

Header = Struct(
    'addresses' / RepeatUntil(lambda x, lst, ctx: x.ssid.extension, Address),
    'control' / Control,
    'pid' / PID
    )

Header16 = Struct(
    'addresses' / RepeatUntil(lambda x, lst, ctx: x.ssid.extension, Address),
    'control' / Control16,
    'pid' / PID
    )

Frame = Struct(
    'header' / Header,
    'info' / GreedyBytes
    )

ax25 = Frame

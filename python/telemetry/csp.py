#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *


Address = BitsInteger(5)
Port = BitsInteger(6)

CSPHeader = BitStruct(
    'priority' / BitsInteger(2),
    'source' / Address,
    'destination' / Address,
    'destination_port' / Port,
    'source_port' / Port,
    'reserved' / BitsInteger(3),
    'fragmentation' / Flag,
    'hmac' / Flag,
    'xtea' / Flag,
    'rdp' / Flag,
    'crc' / Flag
    )

Addressv2 = BitsInteger(14)

CSPHeaderv2 = BitStruct(
    'priority' / BitsInteger(2),
    'destination' / Addressv2,
    'source' / Addressv2,
    'destination_port' / Port,
    'source_port' / Port,
    'reserved' / BitsInteger(2),
    'hmac' / Flag,
    'xtea' / Flag,
    'rdp' / Flag,
    'crc' / Flag
    )

csp = Struct(
    'header' / CSPHeader,
    'payload' / GreedyBytes
    )

cspv2 = Struct(
    'header' / CSPHeaderv2,
    'payload' / GreedyBytes
    )

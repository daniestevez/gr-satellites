#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
"""
TUBiX20 Telemetry Format

# References
[1]: https://www.static.tu.berlin/fileadmin/www/10002275/
     Amateur_Radio/TechnoSat_Telemetry_Format.ods
"""

from construct import *


MessageType = Enum(
    BitsInteger(3),
    ack=0,
    regular=1,
    error_correction=7)

TargetAddress = Enum(
    BitsInteger(4),
    gs=0,
    broadcast=15,
)

TargetSubAddress = Enum(
    BitsInteger(2),
    primary_gs=0,
    secondary_gs=1,
    broadcast=3,
)

Baudrate = Enum(
    BitsInteger(1),
    baud_4k8=0,
    baud_9k6=1,
)

Control = BitStruct(
    'message_type' / MessageType,
    'num_blocks' / BitsInteger(5),
    'address' / TargetAddress,
    'sub_address' / TargetSubAddress,
    'ack' / Flag,
    'baud' / Baudrate,
    )

TransferFrameHeader = BitStruct(
    'scid' / BitsInteger(12),
    'version' / BitsInteger(4),
    'counter' / BitsInteger(16),
)

MasterFrame = Struct(
    'control' / Control,
    'callsign' / Bytes(6),
    'callsign_crc' / Hex(Int16ub),
    'transfer_frame' / Bytes(lambda ctx: 18 * (ctx.control.num_blocks + 1)),
    'reserved0' / Bytes(1),
    'error_marker' / Bytes(4),
    'reserved1' / Bytes(1),
    )

tubix20 = MasterFrame

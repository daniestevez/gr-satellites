#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# TODO: improve this computation.
# Probably bit reversal is not the best way to do it.

def crc(data):
    poly = 0x8408
    crc = 0xffff
    for byte in data:
        # reverse byte
        byte = (byte & 0x55) << 1 | (byte & 0xAA) >> 1
        byte = (byte & 0x33) << 2 | (byte & 0xCC) >> 2
        byte = (byte & 0x0F) << 4 | (byte & 0xF0) >> 4
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ poly if crc & 1 else crc >> 1
    crc = (crc & 0x5555) << 1 | (crc & 0xAAAA) >> 1
    crc = (crc & 0x3333) << 2 | (crc & 0xCCCC) >> 2
    crc = (crc & 0x0F0F) << 4 | (crc & 0xF0F0) >> 4
    crc = (crc & 0x00FF) << 8 | (crc & 0xFF00) >> 8
    return crc

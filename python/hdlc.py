#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy


flag = bytes([0] + 6*[1] + [0])


def crc_ccitt(data):
    # Implementation taken from
    # hdlc_framer_pb_impl.cc in gr-digital
    poly = 0x8408  # reflected 0x1021
    crc = 0xffff
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ poly if crc & 1 else crc >> 1
    return crc ^ 0xffff

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Daniel Estevez <daniel@destevez.net>.
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

# TODO improve this computation. probably bit reversal is not the best way to do it

def crc(data):
    poly = 0x8408
    crc = 0xffff
    for byte in data:
        # reverse byte
        byte = (byte & 0x55) <<  1 | (byte & 0xAA) >>  1
        byte = (byte & 0x33) <<  2 | (byte & 0xCC) >>  2
        byte = (byte & 0x0F) <<  4 | (byte & 0xF0) >>  4
        crc ^= byte
        for _ in range(8):
            if crc & 1: crc = (crc >> 1) ^ poly
            else: crc = crc >> 1
    crc = (crc & 0x5555) <<  1 | (crc & 0xAAAA) >>  1
    crc = (crc & 0x3333) <<  2 | (crc & 0xCCCC) >>  2
    crc = (crc & 0x0F0F) <<  4 | (crc & 0xF0F0) >>  4
    crc = (crc & 0x00FF) <<  8 | (crc & 0xFF00) >>  8
    return crc

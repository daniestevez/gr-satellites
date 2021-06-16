#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from construct import ConstructError

from .filereceiver import FileReceiver
from ..telemetry import ax25


class FileReceiverMirSat1(FileReceiver):
    def file_id(self, chunk):
        return struct.unpack('<I', chunk[1:5])[0]

    def chunk_offset(self, chunk):
        return struct.unpack('<I', chunk[6:9] + b'\x00')[0]

    def chunk_data(self, chunk):
        return chunk[9:-2]

    def is_last_chunk(self, chunk):
        return chunk[0] & 0x20

    def parse_chunk(self, chunk):
        try:
            frame = ax25.parse(chunk)
        except ConstructError:
            return None
        if frame.header.pid == 0xBB:
            # TODO check CRC-16
            return frame.info
        return None


mirsat1 = FileReceiverMirSat1

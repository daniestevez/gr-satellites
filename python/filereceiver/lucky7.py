#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# Based on the decoder by Xerbo
# https://github.com/Xerbo/Lucky7-Decoder

import struct

from .imagereceiver import ImageReceiver

class ImageReceiverLucky7(ImageReceiver):
    def chunk_sequence(self, chunk):
        return struct.unpack('>H', chunk[3:5])[0]

    def chunk_size(self):
        return 28
    
    def chunk_data(self, chunk):
        return chunk[7:]

    def file_size(self, chunk):
        return self.chunk_size() * struct.unpack('>H', chunk[5:7])[0]

    def parse_chunk(self, chunk):
        address = struct.unpack('>H', chunk[1:3])[0]
        if address < 0xC000 \
          or address >= 0xC000 + self.file_size(chunk)/self.chunk_size():
            return None
        return chunk    

lucky7 = ImageReceiverLucky7

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from .imagereceiver import ImageReceiver

class ImageReceiver1KUNSPF(ImageReceiver):
    def chunk_sequence(self, chunk):
        return struct.unpack('>H', chunk[4:6])[0]

    def chunk_data(self, chunk):
        return chunk[6:-4]

    def filename(self, fid):
        return f'{fid}.jpg'

    def parse_chunk(self, chunk):
        if len(chunk) != 138:
            return None
        else:
            return chunk

sat_1kuns_pf = ImageReceiver1KUNSPF

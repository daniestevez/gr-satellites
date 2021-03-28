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


class ImageReceiverK2SAT(ImageReceiver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_frame_count = None
        self._unwrap = 0
        self._first_header_frame_count = None

    def _first_header_pointer(self, chunk):
        return chunk[16 + 3]

    def _virtual_channel_frame_count(self, chunk):
        return chunk[16 + 2]

    def _unwrapped_frame_count(self, chunk):
        fc = self._virtual_channel_frame_count(chunk) + self._unwrap
        if self._last_frame_count is not None and fc < self._last_frame_count:
            self._unwrap += 256
            fc += 256
        self._last_frame_count = fc
        return fc

    def chunk_sequence(self, chunk):
        fh = self._first_header_pointer(chunk)
        if fh == 0x00:
            # First packet in image
            self._first_header_frame_count = self._unwrapped_frame_count(chunk)
            return 0
        return (self._unwrapped_frame_count(chunk)
                - self._first_header_frame_count
                if self._first_header_frame_count is not None
                else None)

    def is_last_chunk(self, chunk):
        # 0xff indicates last packet in image
        return self._first_header_pointer(chunk) == 0xff

    def chunk_data(self, chunk):
        return chunk[20:-1]

    def filename(self, fid):
        return f'{fid}.jpg'

    def parse_chunk(self, chunk):
        return chunk if len(chunk) > 16 + 4 + 1 else None


k2sat = ImageReceiverK2SAT

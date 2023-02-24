#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .imagereceiver import ImageReceiver

# Documentation:
# https://ukamsat.files.wordpress.com/2022/12/
# camsat-cas-5a-amateur-radio-satellite-users-manual-v2.0.pdf


class ImageReceiverCAS5A(ImageReceiver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_fid = -1
        self._first_chunk = None
        self._current_offset = 0
        self._current_chunk = None
        self._next_offset = 0

    def parse_chunk(self, chunk):
        # The AX.25 header occupies 16 bytes
        if len(chunk) <= 16:
            return None
        chunk = chunk[16:]
        if chunk.startswith(b'\x01\x00' * 3):
            # Telemetry frames start by 01 00 01 00 01 00.
            # The documentation says that they start by
            # 01 00 01 00 01 00 7E,
            # but they actually seem  to start by
            # 01 00 01 00 01 00 A7
            return None
        return chunk

    def chunk_data(self, chunk):
        return chunk

    def chunk_offset(self, chunk):
        # To determine the offset, we count how many bytes we've seen so far
        # (this assumes we don't lose any chunks).
        if self._current_chunk != chunk:
            self._current_chunk = chunk
            self._current_offset = self._next_offset
        offset = self._current_offset
        self._next_offset = offset + len(chunk)
        return offset

    def file_id(self, chunk):
        # A new JPEG file starts by ff d8
        if chunk.startswith(b'\xff\xd8') and chunk != self._first_chunk:
            self._current_fid += 1
            self._current_offset = 0
            self._first_chunk = chunk
            self._current_chunk = chunk
            self._next_offset = 0
        return self._current_fid


cas5a = ImageReceiverCAS5A

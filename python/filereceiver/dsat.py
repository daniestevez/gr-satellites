#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct
import datetime
import types

from .imagereceiver import ImageReceiver
from ..telemetry.csp import CSPHeader


class ImageReceiverDSAT(ImageReceiver):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dsat_reset_segments()

    def _dsat_reset_segments(self):
        self._dsat_old_offset = 0
        self._dsat_current_segment = 0
        self._dsat_current_segment_size = None

    def _dsat_segment_size(self, chunk):
        return struct.unpack('>I', chunk[-4:])[0]

    def chunk_offset(self, chunk):
        offset = struct.unpack('>I', chunk[-8:-4])[0]
        # handle offset rollover
        if self._dsat_old_offset > offset:
            self.log('D-SAT offset rollover')
            if self._dsat_current_segment_size is None:
                self.log('unknown last segment size, '
                         'taking from current chunk')
                self._dsat_current_segment_size = (
                    self._dsat_segment_size(chunk))
            self._dsat_current_segment += self._dsat_current_segment_size
            self.log(f'current segment now {self._dsat_current_segment}')
        self._dsat_old_offset = offset
        self._dsat_current_segment_size = self._dsat_segment_size(chunk)
        return self._dsat_current_segment + offset

    def chunk_data(self, chunk):
        return chunk[4:-8]

    def filename(self, fid):
        return f'{fid}.jpg'

    def parse_chunk(self, chunk):
        if len(chunk) <= 15+8:
            return None
        header = CSPHeader.parse(chunk)
        # destination port 30 is used for JPEG blocks
        if header.destination_port != 30:
            return None
        return chunk

    def _watch_file_announcements(self, chunk):
        if len(chunk) < 25:
            return
        header = CSPHeader.parse(chunk)
        # destination port 12 is used for announcements
        if header.destination_port != 12:
            return

        timestamp = datetime.datetime.fromtimestamp(
            struct.unpack('<i', chunk[4:8])[0],
            datetime.timezone.utc,
        )
        fid = struct.unpack('<I', chunk[8:12])[0]
        # next 12 bytes are for GPS position
        length = struct.unpack('<I', chunk[21:25])[0]

        self.log(f'image {fid} announced. Length {length}. '
                 f'Timestamp {timestamp}')

        # hook lambda functions for file id and size
        self.file_id = types.MethodType(lambda self, chunk: fid, self)
        self.file_size = types.MethodType(lambda self, chunk: length, self)

        self._dsat_reset_segments()

    def push_chunk(self, chunk):
        # hook the file announcement watch here
        self._watch_file_announcements(chunk)
        super().push_chunk(chunk)


dsat = ImageReceiverDSAT

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import zipfile

from .filereceiver import FileReceiver


class FileReceiverQO100Multimedia(FileReceiver):
    def frame_status(self, chunk):
        return (int(chunk[1]) >> 4) & 0x03

    def frame_type(self, chunk):
        frame_type = int(chunk[1]) & 0x0f
        self._current_frame_type = frame_type
        return frame_type

    def chunk_sequence(self, chunk):
        return int(chunk[0]) | ((int(chunk[1]) >> 6) << 8)

    def chunk_offset(self, chunk):
        seq = self.chunk_sequence(chunk)
        if seq == 0:
            return 0
        return (seq - 1) * 219 + 164

    def chunk_data(self, chunk):
        seq = self.chunk_sequence(chunk)
        if seq == 0:
            return chunk[57:]
        data = chunk[2:]
        if not self.is_last_chunk(chunk):
            return data
        # Trim if we are in the last chunk
        length = (self._files[self._current_file].size
                  - self.chunk_offset(chunk)
                  if self._current_file is not None
                  else len(data))
        return data[:length]

    def file_size(self, chunk):
        if self.chunk_sequence(chunk) != 0:
            return None
        return (int(chunk[54]) << 16) | (int(chunk[55]) << 8) | int(chunk[56])

    def is_last_chunk(self, chunk):
        return self.frame_status(chunk) in (2, 3)

    def parse_chunk(self, chunk):
        if self.frame_type(chunk) >= 8:
            return None
        return chunk

    def file_id(self, chunk):
        if self.chunk_sequence(chunk) != 0:
            return None
        return (str(chunk[2:52], encoding='ascii').rstrip('\x00')
                .replace('\x00', ' '))

    def on_completion(self, f):
        if self._current_frame_type not in [3, 4, 5]:
            return
        # ASCII, HTML and binary files are zipped
        f.f.close()
        del self._files[self._current_file]
        data = zipfile.ZipFile(f.path).read(f.path.name)
        with open(f.path, 'wb') as fdata:
            fdata.write(data)


qo100_multimedia = FileReceiverQO100Multimedia

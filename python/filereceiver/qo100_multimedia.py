#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import socket
import threading
import zipfile

from .filereceiver import FileReceiver


class FileReceiverQO100Multimedia(FileReceiver):
    def frame_status(self, chunk):
        return (int(chunk[1]) >> 4) & 0x03

    def frame_type(self, chunk):
        return int(chunk[1]) & 0x0f

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
        # Drop chunk if it's the last chunk and we do not have enough
        # information about the current file. This prevents self.chunk_data
        # from failing later on.
        if self.is_last_chunk(chunk):
            try:
                self.chunk_data(chunk)
            except Exception as e:
                print('Could not get file data for last chunk:', e)
                return None
        return chunk

    def file_id(self, chunk):
        if self.chunk_sequence(chunk) != 0:
            return None
        try:
            name = (str(chunk[2:52], encoding='ascii')
                    .rstrip('\x00')
                    .replace('\x00', ' '))
        except Exception as e:
            print('Could not obtain filename:', e)
            return None
        if self.frame_type(chunk) in [3, 4, 5]:
            # ASCII, HTML and binary files are zipped, so we add the .zip
            # extension
            name += '.zip'
        return name

    def on_completion(self, f):
        fname = f.path.name
        if not fname.endswith('.zip'):
            # Not a zip file. No need to unzip
            return
        f.f.flush()
        outname = fname[:-4]  # remove .zip
        try:
            data = zipfile.ZipFile(f.path).read(outname)
            with open(f.path.parent / outname, 'wb') as fdata:
                fdata.write(data)
                if fname.endswith('.blt.zip'):
                    threading.Thread(
                        target=send_to_websocket,
                        args=(data,)).run()
        except Exception as e:
            print('Could not unzip received file:', e)


# This is used in a new thread to send the file contents to the websocket
# server Python script (see examples/qo100-multimedia-beacon).
def send_to_websocket(data):
    port = 52002
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', port))
        s.send(data)
        s.close()
    except Exception as e:
        print('Could not send file to websocket server script:', e)


qo100_multimedia = FileReceiverQO100Multimedia

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Daniel Estevez <daniel@destevez.net>.
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

from construct import *

from .filereceiver import FileReceiver

block_size = 46

swiatowid_image_block = Struct(
    'sequence' / Int16ul,
    'data' / Bytes(block_size)
    )

class FileReceiverSwiatowid(FileReceiver):
    def filename(self, fid):
        return f'{fid}.jpg'

    def chunk_size(self):
        return block_size
    
    def parse_chunk(self, chunk):
        if len(chunk) != swiatowid_image_block.sizeof():
            return None
        try:
            frame = swiatowid_image_block.parse(chunk)
        except ConstructError:
            return None
        return frame

swiatowid = FileReceiverSwiatowid

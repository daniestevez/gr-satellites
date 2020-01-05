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

from construct.core import ConstructError

from .filereceiver import FileReceiver
from ..telemetry import smogp as tlm

class FileReceiverSMOGP(FileReceiver):
    def file_id(self, chunk):
        return f'spectrum_start_{chunk.startfreq}_step_{chunk.stepfreq}_rbw_{chunk.rbw}_measid_{chunk.measid}'

    def chunk_size(self):
        return 224

    def chunk_sequence(self, chunk):
        return chunk.pckt_index

    def chunk_data(self, chunk):
        return chunk.spectrum_data

    def file_size(self, chunk):
        return chunk.pckt_count * self.chunk_size()
    
    def parse_chunk(self, chunk):
        try:
            frame = tlm.parse(chunk)
        except ConstructError:
            return None
        return frame.payload if frame.type == 5 else None

smogp = FileReceiverSMOGP

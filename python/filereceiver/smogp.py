#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct.core import ConstructError

from .filereceiver import FileReceiver
from ..telemetry import smogp as tlm_smogp
from ..telemetry import smog1 as tlm_smog1

class FileReceiverSMOG(FileReceiver):
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
            frame = self._tlm.parse(chunk)
        except ConstructError:
            return None
        return frame.payload if frame.type == 5 else None

class FileReceiverSMOGP(FileReceiverSMOG):
    _tlm = tlm_smogp

class FileReceiverSMOG1(FileReceiverSMOG):
    _tlm = tlm_smog1

smogp = FileReceiverSMOGP
smog1 = FileReceiverSMOG1

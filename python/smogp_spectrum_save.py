#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 Daniel Estevez <daniel@destevez.net>
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
# 

import numpy
from gnuradio import gr
import pmt
import pathlib

from . import smogp_telemetry

class smogp_spectrum_save(gr.basic_block):
    """
    Saves spectrum data from SMOG-P/ATL-1 into files
    """
    def __init__(self, path):
        gr.basic_block.__init__(self,
            name="smogp_spectrum_save",
            in_sig=[],
            out_sig=[])
        self.path = pathlib.Path(path)
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        try:
            data = smogp_telemetry.Frame.parse(packet)
        except:
            return
        if data.type != 5:
            return

        filename = f'spectrum_start_{data.payload.startfreq}_step_{data.payload.stepfreq}_rbw_{data.payload.rbw}_measid_{data.payload.measid}'
        filepath = self.path / filename
        if not filepath.exists():
            with filepath.open('wb') as f:
                f.write(b'\x00' * data.payload.pckt_count * 224)
        with filepath.open('r+b') as f:
            f.seek(data.payload.pckt_index * 224)
            f.write(data.payload.spectrum_data)

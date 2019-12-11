#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Daniel Estevez <daniel@destevez.net>.
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

import numpy
from gnuradio import gr
import pmt

class smogp_packet_filter(gr.basic_block):
    """
    Filters out SMOG-P or ATL-1 packets not having a valid packet type

    The packet type is stored in the first byte
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="smogp_packet_filter",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    _valid_packet_types = [1, 2, 3, 4, 5, 6, 7, 33, 34, 129, 130, 131]
        
    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))
        packet_type = packet[0]

        if packet_type in self._valid_packet_types:
            self.message_port_pub(pmt.intern('out'), msg_pmt)

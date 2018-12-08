#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Daniel Estevez <daniel@destevez.net>.
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

import numpy as np
from gnuradio import gr
import pmt
import array

from eseo_line_decoder import reflect_bytes

class eseo_packet_crop(gr.basic_block):
    """
    docstring for block eseo_packet_crop
    """
    def __init__(self, drop_rs):
        gr.basic_block.__init__(self,
            name="eseo_packet_handler",
            in_sig=[],
            out_sig=[])

        self.drop_rs = drop_rs
        
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = array.array("B", pmt.u8vector_elements(msg))

        # find packet end marker
        idx = packet.tostring().find('\x7e\x7e')
        if idx == -1:
            return
        crop = idx if not self.drop_rs else idx - 16
        if crop < 0:
            return

        # reverse byte ordering
        packet = np.frombuffer(packet[:crop], dtype = 'uint8')
        packet = np.packbits(reflect_bytes(np.unpackbits(packet)))
        packet = array.array('B', packet)

        self.message_port_pub(pmt.intern('out'),  pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(len(packet), packet)))

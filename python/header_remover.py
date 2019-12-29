#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import numpy
from gnuradio import gr
import pmt

class header_remover(gr.basic_block):
    """
    Removes some bytes from the beginning of a PDU

    Args:
        length: Length to remove (int)
    """
    def __init__(self, length):
        gr.basic_block.__init__(self,
            name="header_remover",
            in_sig=[],
            out_sig=[])
        self.length = length
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        if len(packet) <= self.length:
            return

        data = packet[self.length:]
        self.message_port_pub(pmt.intern('out'),
                                  pmt.cons(pmt.car(msg_pmt),
                                           pmt.init_u8vector(len(data), data)))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Daniel Estevez <daniel@destevez.net>
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
import binascii

class ks1q_header_remover(gr.basic_block):
    """
    docstring for block ks1q_header_remover
    """
    def __init__(self, verbose):
        gr.basic_block.__init__(self,
            name="ks1q_header_remover",
            in_sig=[],
            out_sig=[])
        self.verbose = verbose
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))

        if len(packet) <= 3:
            return

        if self.verbose:
            print('Spacecraft ID', binascii.b2a_hex(packet[:2]))
            if packet[2] == 0x50:
                print('CSP downlink, protocol version 0')
            else:
                print('Unknown packet type')

        data = packet[3:]
        self.message_port_pub(pmt.intern('out'),
                                  pmt.cons(pmt.PMT_NIL,
                                           pmt.init_u8vector(len(data), data)))



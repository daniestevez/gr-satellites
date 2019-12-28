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

from gnuradio import gr
import pmt

# details of the NGHam protocol taken from
# https://github.com/skagmo/ngham/blob/master/ngham.c

ngham_rs_sizes = [47, 79, 111, 159, 191, 223, 255]
ngham_non_rs_sizes = [47-16, 79-16, 111-16, 159-32, 191-32, 223-32, 255-32]

class ngham_remove_padding(gr.basic_block):
    """
    Removes the padding on an NGHam packet

    Also it automatically detects if RS check bytes are
    still in the packet and removes them as well
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="ngham_remove_padding",
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        if len(packet) in ngham_rs_sizes:
            size_idx = ngham_rs_sizes.index(len(packet))
            packet = packet[:ngham_non_rs_sizes[size_idx]]

        if len(packet) not in ngham_non_rs_sizes:
            print('NGHam packet length invalid')
            return

        padding = packet[0] & 0x1f
        packet = packet[:-padding]
        self.message_port_pub(pmt.intern('out'),  pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(len(packet), packet)))

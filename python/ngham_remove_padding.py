#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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
        packet = pmt.u8vector_elements(msg)

        if len(packet) in ngham_rs_sizes:
            size_idx = ngham_rs_sizes.index(len(packet))
            packet = packet[:ngham_non_rs_sizes[size_idx]]

        if len(packet) not in ngham_non_rs_sizes:
            print('NGHam packet length invalid')
            return

        padding = packet[0] & 0x1f
        packet = packet[:-padding]
        self.message_port_pub(pmt.intern('out'),  pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(len(packet), packet)))

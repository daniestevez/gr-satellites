#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy as np
import pmt

from .eseo_line_decoder import reflect_bytes as reflect


class reflect_bytes(gr.basic_block):
    """docstring for block reflect_bytes"""
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='reflect_bytes',
            in_sig=[],
            out_sig=[])
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = np.array(pmt.u8vector_elements(msg), dtype='uint8')
        packet = np.unpackbits(packet)
        packet = reflect(packet)
        packet = bytes(np.packbits(packet))

        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))

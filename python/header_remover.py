#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

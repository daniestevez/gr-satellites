#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr
import numpy as np
import pmt


# This block is based on the Universal SPUNTIX Protocol (USP)
# Protocol Description revision 1.04
# https://sputnix.ru/tpl/docs/amateurs/USP%20protocol%20description%20v1.04.pdf

class usp_ax25_crop(gr.basic_block):
    """
    Crop a USP packet to obtain the encapsulated AX.25 frame
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='usp_ax25_crop',
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
        msg = pmt.u8vector_elements(msg)

        length_field = msg[2:4]
        length = struct.unpack('<H', bytes(length_field))[0]

        msg_out = msg[4:][:length]

        msg_out = pmt.init_u8vector(len(msg_out), msg_out)
        msg_out = pmt.cons(pmt.car(msg_pmt), msg_out)
        self.message_port_pub(pmt.intern('out'), msg_out)

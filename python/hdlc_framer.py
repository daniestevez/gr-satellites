#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import collections

from gnuradio import gr
import numpy
import pmt

from . import crc, hdlc


class hdlc_framer(gr.basic_block):
    """docstring for block hdlc_framer"""
    def __init__(self, preamble_bytes, postamble_bytes):
        gr.basic_block.__init__(
            self,
            name='hdlc_framer',
            in_sig=None,
            out_sig=None)

        self.crc_calc = crc(16, 0x1021, 0xFFFF, 0xFFFF, True, True)
        self.preamble_bytes = preamble_bytes
        self.postamble_bytes = postamble_bytes
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return

        data = list(pmt.u8vector_elements(msg))
        crc_val = self.crc_calc.compute(data)
        data.append(crc_val & 0xff)
        data.append((crc_val >> 8) & 0xff)

        buff = list(hdlc.flag * self.preamble_bytes)
        ones = 0  # number of consecutive ones
        for byte in data:
            for _ in range(8):
                # Transmit byte LSB first
                x = byte & 1
                buff.append(x)
                if x:
                    ones += 1
                else:
                    ones = 0
                if ones == 5:
                    # Bit-stuff
                    buff.append(0)
                    ones = 0
                byte >>= 1
        buff.extend(hdlc.flag * self.postamble_bytes)

        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(buff), buff)))

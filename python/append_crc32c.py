#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr
import pmt

from . import crc as _crc_module

_crc_fn = _crc_module(32, 0x1EDC6F41, 0xFFFFFFFF, 0xFFFFFFFF, True, True)


class append_crc32c(gr.basic_block):
    """docstring for block append_crc32c"""
    def __init__(self, include_header):
        gr.basic_block.__init__(
            self,
            name='append_crc32c',
            in_sig=[],
            out_sig=[])

        self.include_header = include_header

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))
        data = packet if self.include_header else packet[4:]
        crc = _crc_fn.compute(list(data))
        packet += struct.pack('>I', crc)
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import pmt

from . import crc as _crc_module

# CRC-16/CCITT-ZERO: poly=0x1021, init=0x0000, final_xor=0x0000,
# input_reflected=False, result_reflected=False
_crc_fn = _crc_module(16, 0x1021, 0x0000, 0x0000, False, False)


class check_eseo_crc(gr.basic_block):
    """docstring for block check_eseo_crc"""
    def __init__(self, verbose):
        gr.basic_block.__init__(
            self,
            name='check_eseo_crc',
            in_sig=[],
            out_sig=[])

        self.verbose = verbose

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = pmt.u8vector_elements(msg)

        if len(packet) < 3:
            return

        packet_out = packet[:-2]
        msg_out = pmt.cons(pmt.car(msg_pmt),
                           pmt.init_u8vector(len(packet_out), packet_out))
        if _crc_fn.compute(list(packet)) == 0:
            if self.verbose:
                print('CRC OK')
            self.message_port_pub(pmt.intern('ok'), msg_out)
        else:
            if self.verbose:
                print('CRC failed')
            self.message_port_pub(pmt.intern('fail'), msg_out)

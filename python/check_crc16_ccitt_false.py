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
import numpy
import pmt

from . import crc as _crc_module

# CRC-16/CCITT-FALSE: poly=0x1021, init=0xffff, final_xor=0x0,
# input_reflected=False, result_reflected=False
_crc_fn = _crc_module(16, 0x1021, 0xffff, 0x0, False, False)


def crc16_ccitt_false(data):
    return _crc_fn.compute(list(data))


class check_crc16_ccitt_false(gr.basic_block):
    """docstring for block check_crc16_ccitt_false"""
    def __init__(self, verbose):
        gr.basic_block.__init__(
            self,
            name='check_crc16_ccitt_false',
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
        crc = crc16_ccitt_false(packet_out)
        if crc == struct.unpack('<H', bytes(packet[-2:]))[0]:
            if self.verbose:
                print('CRC OK')
            self.message_port_pub(pmt.intern('ok'), msg_out)
        else:
            if self.verbose:
                print('CRC failed')
            self.message_port_pub(pmt.intern('fail'), msg_out)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
from gnuradio import gr
import numpy
import pmt

from . import crc as _crc_module

# CRC-16/X-25: poly=0x1021, init=0xffff, final_xor=0xffff,
# input_reflected=True, result_reflected=True
_crc_fn = _crc_module(16, 0x1021, 0xffff, 0xffff, True, True)


def crc16_x_25(data):
    return _crc_fn.compute(list(data))


class ngham_check_crc(gr.basic_block):
    """
    Checks the CRC-16 of an NGHam frame

    Input: An NGHam frame with a CRC-16 at the end
    Output: The NGHame frame with the CRC-16 dropped,
            classified according as to whether the CRC
            is correct.
    """
    def __init__(self, verbose):
        gr.basic_block.__init__(
            self,
            name='ngham_check_crc',
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
        crc = crc16_x_25(packet_out)
        if (crc >> 8) == packet[-2] and crc & 0xff == packet[-1]:
            if self.verbose:
                print('CRC OK')
            self.message_port_pub(pmt.intern('ok'), msg_out)
        else:
            if self.verbose:
                print('CRC failed')
            self.message_port_pub(pmt.intern('fail'), msg_out)

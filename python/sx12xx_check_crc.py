#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 jgromes <gromes.jan@gmail.com>
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


class sx12xx_check_crc(gr.basic_block):
    """Check SX12xx FSK packet CRC-16

    The CRC-16 is calculated from length field and payload.
    """
    def __init__(self, verbose, initial, final):
        gr.basic_block.__init__(
            self,
            name='sx12xx_check_crc',
            in_sig=[],
            out_sig=[])

        self.verbose = verbose
        self.initial = initial
        self.final = final
        self._crc_fn = _crc_module(16, 0x1021, initial, final, False, False)

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('ok'))
        self.message_port_register_out(pmt.intern('fail'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet_orig = pmt.u8vector_elements(msg)
        packet = bytes(packet_orig)

        if len(packet) < 3:
            return

        packet_out = packet_orig[:-2]
        packet_crc = int.from_bytes(packet[-2:], 'big')
        msg_out = pmt.cons(
            pmt.car(msg_pmt),
            pmt.init_u8vector(len(packet_out), packet_out))
        res = self._crc_fn.compute(list(packet[:-2]))
        if res == packet_crc:
            if self.verbose:
                print('CRC OK')
            self.message_port_pub(pmt.intern('ok'), msg_out)
        else:
            if self.verbose:
                print('CRC failed')
            self.message_port_pub(pmt.intern('fail'), msg_out)

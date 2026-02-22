#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy
import pmt

from . import crc as _crc_module

# CRC-16/ARC: poly=0x8005, init=0x0, final_xor=0x0, input_reflected=True,
# result_reflected=True
_crc_fn = _crc_module(16, 0x8005, 0x0, 0x0, True, True)


def crc16_arc(data):
    return _crc_fn.compute(list(data))


class check_tt64_crc(gr.basic_block):
    """docstring for block check_tt64_crc"""
    def __init__(self, verbose, packet_len=48, strip=True):
        gr.basic_block.__init__(
            self,
            name='check_tt64_crc',
            in_sig=[],
            out_sig=[])

        self.verbose = verbose
        self.packet_len = packet_len
        self.strip = strip

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

        if self.packet_len is not None:
            packet = packet[:self.packet_len]

        if ((self.packet_len is not None and len(packet) < self.packet_len)
                or (self.packet_len is None and len(packet) < 2)):
            if self.verbose:
                print('Packet too short')
            return

        packet_out = packet[:-2] if self.strip else packet
        msg_out = pmt.cons(pmt.PMT_NIL,
                           pmt.init_u8vector(len(packet_out), packet_out))
        if crc16_arc(packet) == 0:
            if self.verbose:
                print('CRC OK')
            self.message_port_pub(pmt.intern('ok'), msg_out)
        else:
            if self.verbose:
                print('CRC failed')
            self.message_port_pub(pmt.intern('fail'), msg_out)

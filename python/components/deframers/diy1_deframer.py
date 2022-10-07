#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021-2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr, digital
import numpy as np
import pmt

from ...crcs import crc16_ccitt_zero
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


# Syncword is 0x2dd4
_syncword = '0010110111010100'


class uart_decode(gr.basic_block):
    """
    Helper block to remove UART-like encoding

    The input is unpacked bits having 10 bits per byte consisting of a
    start bit (which should be 0 but we don't look at), an 8-bit byte
    in MSB-first order, and a stop bit (which should be 1 but we don't
    look at). The output consists of the 8-bit bytes as packed bytes.
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='uart_decode',
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
        if packet.size % 10 != 0:
            print('[ERROR] Packet size is not a multiple of 10 bits')
            return
        packet = np.packbits(packet.reshape((-1, 10))[:, 1:-1])
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))


class crop(gr.basic_block):
    """
    Helper block to crop DIY-1 packets according to packet length

    The format of DIY-1 packets is:
    - Header: 4 bytes
    - Length field: 1 byte (contains length of data field)
    - Data
    - CRC-16

    This crop block reads the length field and trims the PDU accordingly.
    Its is a PDU with all the fields listed above.
    """
    def __init__(self, verbose=False):
        gr.basic_block.__init__(
            self,
            name='crop',
            in_sig=[],
            out_sig=[])
        self.verbose = verbose
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = pmt.u8vector_elements(msg)
        if len(packet) < 7:
            # Packet is too short
            return
        length = packet[4]
        packet = packet[:5+length+2]
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet)))


class diy1_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe DIY-1 RFM22 frames

    The input is a float stream of soft symbols. The output are PDUs
    with DIY-1 frames.

    Args:
        options: Options from argparse
    """
    def __init__(self, options=None):
        gr.hier_block2.__init__(
            self,
            'diy1_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=262, sync=_syncword,
            threshold=self.options.syncword_threshold)
        self.crop = crop()
        self.crc = crc16_ccitt_zero()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 0

    @classmethod
    def add_options(cls, parser):
        """
        Adds DIY-1 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

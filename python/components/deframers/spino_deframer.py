#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import struct

from gnuradio import gr, digital
import pmt

from ...crcs import crc16_ccitt_zero
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


class spino_crop(gr.basic_block):
    """
    Helper block to crop SPINO frames to the correct length.
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='spino_crop',
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
        length = struct.unpack('<H', bytes(msg[16:18]))[0]
        # account for AX.25 headers (14 bytes) and CRC (2 bytes)
        length += 16
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(pmt.car(msg_pmt), pmt.init_u8vector(length, msg)))


_syncword = '00101110111111001001100000100111'


class spino_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe SPINO packets

    The input is a float stream of soft symbols. The output are PDUs
    with the decoded frames. This uses frames of a fixed size, a length
    field to determine the length of the payload (the remaining data in
    the frame is padding, and a CRC-16).

    https://code.electrolab.fr/spino/cubesat_cs/-/blob/master/
    SPECIFICATIONS/2023_04_01%20-%20Pr%C3%A9sentation%20Spino%20-%20CJ.pdf

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'spino_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=240, sync=_syncword, threshold=syncword_threshold)
        self.crop = spino_crop()
        self.crc_check = crc16_ccitt_zero(swap_endianness=True)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc_check, 'in'))
        self.msg_connect((self.crc_check, 'ok'), (self, 'out'))

    _default_sync_threshold = 0

    @classmethod
    def add_options(cls, parser):
        """
        Adds SPINO deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

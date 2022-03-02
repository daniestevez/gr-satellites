#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021-2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital
import pmt

from ... import pdu_head_tail
from ... import sx12xx_packet_crop
from ... import reflect_bytes

from ...crcs import crc16_cc11xx
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


_syncword = '0000000100100011010001010110011110001001101010111100110111101111'


class grizu263a_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe Grizu-263A custom framing

    This framing is based on Semtech SX1268 transceiver
    with PN9 scrambler, bit order swapping and a CRC-16.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'grizu263a_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.sync = sync_to_pdu_packed(
            packlen=255, sync=_syncword, threshold=syncword_threshold)
        self.reflect_1 = reflect_bytes()

        # The scrambler is like the PN9, but uses 0x100 instead of 0x1FF
        # as seed.
        self.scrambler = digital.additive_scrambler_bb(
            0x21, 0x100, 8, count=0, bits_per_byte=8,
            reset_tag_key='packet_len')
        self.stream2pdu = blocks.tagged_stream_to_pdu(blocks.byte_t,
                                                      'packet_len')
        self.pdu2stream = blocks.pdu_to_tagged_stream(blocks.byte_t,
                                                      'packet_len')

        self.reflect_2 = reflect_bytes()
        self.crop = sx12xx_packet_crop(crc_len=2)
        self.crc = crc16_cc11xx()
        self.remove_length = pdu_head_tail(3, 1)

        self.connect(self, self.slicer, self.sync)
        self.msg_connect((self.sync, 'out'), (self.reflect_1, 'in'))
        self.msg_connect((self.reflect_1, 'out'), (self.pdu2stream, 'pdus'))
        self.connect(self.pdu2stream, self.scrambler, self.stream2pdu)
        self.msg_connect((self.stream2pdu, 'pdus'), (self.reflect_2, 'in'))
        self.msg_connect((self.reflect_2, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.remove_length, 'in'))
        self.msg_connect((self.remove_length, 'out'), (self, 'out'))

    _default_sync_threshold = 8

    @classmethod
    def add_options(cls, parser):
        """
        Adds Grizu-263A deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

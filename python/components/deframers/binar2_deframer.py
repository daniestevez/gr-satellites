#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021-2022,2024 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital
import pmt

from ... import pdu_head_tail
from ... import sx12xx_packet_crop
from ...crcs import crc16_cc11xx
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


_syncword = '11010011100100011101001110010001'


class binar2_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe BINAR-2 custom framing

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'binar2_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.sync = sync_to_pdu_packed(
            packlen=250, sync=_syncword, threshold=syncword_threshold)
        self.crop = sx12xx_packet_crop(crc_len=2)
        self.crc = crc16_cc11xx()
        self.remove_length = pdu_head_tail(3, 1)

        self.connect(self, self.slicer, self.sync)
        self.msg_connect((self.sync, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.remove_length, 'in'))
        self.msg_connect((self.remove_length, 'out'), (self, 'out'))

    _default_sync_threshold = 0

    @classmethod
    def add_options(cls, parser):
        """
        Adds BINAR-2 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

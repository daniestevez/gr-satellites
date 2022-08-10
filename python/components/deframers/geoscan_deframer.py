#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital

from ...crcs import crc16_cc11xx
from ...hier.pn9_scrambler import pn9_scrambler
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


_syncword = '10010011000010110101000111011110'


class geoscan_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the GEOSCAN custom framing

    This framing is based in a TI CC1125 transceiver
    with a PN9 scrambler, and the built-in CRC.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'geoscan_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=66, sync=_syncword, threshold=syncword_threshold)
        self.scrambler = pn9_scrambler()
        self.crc = crc16_cc11xx()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds GEOSCAN deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

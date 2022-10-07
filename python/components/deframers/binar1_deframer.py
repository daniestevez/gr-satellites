#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021-2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital

from ... import cc11xx_packet_crop
from ...crcs import crc16_ccitt_false
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


# As syncword we use the last 0xAA from the preamble
# followed by the 0x7E synchronization marker
_syncword = '1010101001111110'


class binar1_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the BINAR-1 custom framing

    This framing uses a custom syncword, a 1-byte packet length
    field, no scrambling, and CRC-16 CCITT FALSE (as in CCSDS
    transfer frames). the packet length field was supposed to
    always have the value 0x56, but we have seen other values
    such as 0x4b being used.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'binar1_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=255+3, sync=_syncword, threshold=syncword_threshold)
        self.crop = cc11xx_packet_crop(use_crc16=True)
        self.crc = crc16_ccitt_false()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 0

    @classmethod
    def add_options(cls, parser):
        """
        Adds BINAR-1 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

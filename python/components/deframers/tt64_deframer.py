#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital

from ... import decode_rs
from ...crcs import crc16_arc
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


_syncword = '0010110111010100'


class tt64_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the TT-64 framing, used by QB50 AT04 Pegasus

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'tt64_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=64, sync=_syncword, threshold=syncword_threshold)
        self.rs = decode_rs(8, 0x11d, 1, 1, 16, 1)
        self.crc = crc16_arc()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.rs, 'in'))
        self.msg_connect((self.rs, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 1

    @classmethod
    def add_options(cls, parser):
        """
        Adds Astrocast 9k6 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')
        parser.add_argument(
            '--verbose_rs', action='store_true', help='Verbose RS decoder')

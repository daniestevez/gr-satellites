#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital

from ... import decode_rs, pdu_head_tail
from .ccsds_rs_deframer import _syncword
from ...hier.sync_to_pdu import sync_to_pdu
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...utils.options_block import options_block


class aistechsat_2_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe AISTECHSAT-2 custom frames

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'aistechast_2_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu(
            packlen=(93 + 32) * 8, sync=_syncword,
            threshold=syncword_threshold)
        self.scrambler = ccsds_descrambler()
        self.tail = pdu_head_tail(3, 10)
        self.fec = decode_rs(False, 1)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.tail, 'in'))
        self.msg_connect((self.tail, 'out'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self, 'out'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds AISTECHSAT-2 deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

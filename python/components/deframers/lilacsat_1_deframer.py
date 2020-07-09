#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital
from .ccsds_rs_deframer import _syncword
from ...hier.ccsds_viterbi import ccsds_viterbi
from ...utils.options_block import options_block
from ... import lilacsat1_demux

class lilacsat_1_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe LilacSat-1 frames

    The input is a float stream of soft symbols. The output are PDUs
    with chunks of a KISS stream. The additional output is codec2 data.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "lilacsat_1_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')
        self.message_port_register_hier_out('codec2')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.delay1 =  blocks.delay(gr.sizeof_float, 1)
        self.viterbi0 = ccsds_viterbi()
        self.viterbi1 = ccsds_viterbi()
        self.differential0 = digital.diff_decoder_bb(2)
        self.differential1 = digital.diff_decoder_bb(2)
        self.tag0 = digital.correlate_access_code_tag_bb(_syncword, syncword_threshold, 'syncword')
        self.tag1 = digital.correlate_access_code_tag_bb(_syncword, syncword_threshold, 'syncword')
        self.scrambler0 = digital.additive_scrambler_bb(0xA9, 0xFF, 7, count=0, bits_per_byte=1, reset_tag_key='syncword')
        self.scrambler1 = digital.additive_scrambler_bb(0xA9, 0xFF, 7, count=0, bits_per_byte=1, reset_tag_key='syncword')
        self.demux0 = lilacsat1_demux('syncword')
        self.demux1 = lilacsat1_demux('syncword')

        self.connect(self, self.viterbi0, self.differential0, self.tag0, self.scrambler0, self.demux0)
        self.connect(self, self.delay1, self.viterbi1, self.differential1, self.tag1, self.scrambler1, self.demux1)
        self.msg_connect((self.demux0, 'frame'), (self, 'out'))
        self.msg_connect((self.demux1, 'frame'), (self, 'out'))
        self.msg_connect((self.demux0, 'codec2'), (self, 'codec2'))
        self.msg_connect((self.demux1, 'codec2'), (self, 'codec2'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds LilacSat-1 deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')

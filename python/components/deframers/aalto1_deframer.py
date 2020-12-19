#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital
from ... import check_crc16_ccitt, cc11xx_packet_crop, pdu_head_tail
from ...hier.pn9_scrambler import pn9_scrambler
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block

_syncword = '00110101001011100011010100101110'

class aalto1_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the AALTO-1 custom framing

    This framing is based in a TI CC1125 transceiver
    with a PN9 scrambler, and a CRC-16 CCITT (as in AX.25).

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "aalto1_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(packlen = 255,\
                                           sync = _syncword,\
                                           threshold = syncword_threshold)
        self.scrambler = pn9_scrambler()
        self.crop = cc11xx_packet_crop(True)
        self.crc = check_crc16_ccitt(self.options.verbose_crc)
        self.crop2 = pdu_head_tail(3, 1)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.crop2, 'in'))
        self.msg_connect((self.crop2, 'out'), (self, 'out'))

    _default_sync_threshold = 4
    
    @classmethod
    def add_options(cls, parser):
        """
        Adds AALTO-1 deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_crc', action = 'store_true', help = 'Verbose CRC decoder')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital, fec, blocks
from ... import distributed_syncframe_soft, matrix_deinterleaver_soft, decode_rs,\
     check_tt64_crc
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...utils.options_block import options_block

_syncword = '11111110000111011110010110010010000001000100110001011101011011000'
_syncword_short = '1111111000011101111001011001001000000100010011000101'

class ao40_fec_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the AO-40 FEC protocol.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        short_frames: use short frames (used in SMOG-P) (bool)
        crc: use CRC-16 ARC (used in SMOG-P) (bool)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, short_frames = False,
                     crc = False, options = None):
        gr.hier_block2.__init__(self, "ao40_fec_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.deframer = distributed_syncframe_soft(syncword_threshold,\
                                                   _syncword_short if short_frames else _syncword,\
                                                   51 if short_frames else 80)
        self.deinterleaver = matrix_deinterleaver_soft(51 if short_frames else 80, 52 if short_frames else 65,
                                                       2572 if short_frames else 5132, 80 if short_frames else 65)
        self.viterbi = fec.cc_decoder.make(2572 if short_frames else 5132, 7, 2, [79,-109], 0, -1, fec.CC_TERMINATED, False)
        self.viterbi_decoder = fec.async_decoder(self.viterbi, False, False, 2572//8 if short_frames else 5132//8)
        self.scrambler = ccsds_descrambler()
        self.rs = decode_rs(False, 1 if short_frames else 2)

        if crc:
            # CRC-16 ARC
            self.crc = check_tt64_crc(verbose = self.options.verbose_crc,
                                      packet_len = None,
                                      strip = False)

        self.connect(self, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.deinterleaver, 'in'))
        self.msg_connect((self.deinterleaver, 'out'), (self.viterbi_decoder, 'in'))
        self.msg_connect((self.viterbi_decoder, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.rs, 'in'))
        if crc:
            self.msg_connect((self.rs, 'out'), (self.crc, 'in'))
            self.msg_connect((self.crc, 'ok'), (self, 'out'))
        else:
            self.msg_connect((self.rs, 'out'), (self, 'out'))

    _default_sync_threshold = 8
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds AO-40 FEC deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_rs', action = 'store_true', help = 'Verbose RS decoder')
        parser.add_argument('--verbose_crc', action = 'store_true', help = 'Verbose CRC decoder')

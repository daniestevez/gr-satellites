#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, digital, fec
from ... import decode_rs
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...hier.sync_to_pdu_soft import sync_to_pdu_soft
from ...usp import usp_pls_crop
from ...utils.options_block import options_block

_syncword = '0101000001110010111101100100101100101101100100001011000111110101'

class usp_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe the Unified SPUTNIX Protocol (USP)

    This framing is based on the CCSDS concatenated framing, but is
    optimized for variable frame size and borrows some ideas from
    DVB-S2.

    The description of the protocol can be found in
    https://sputnix.ru/tpl/docs/amateurs/USP%20protocol%20description%20v1.04.pdf

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "usp_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.deframer = sync_to_pdu_soft(packlen = 4144,\
                                         sync = _syncword,\
                                         threshold = syncword_threshold)
        self.pls = usp_pls_crop()
        self.viterbi = fec.cc_decoder.make(4080, 7, 2, [79, -109],
                                            0, -1, fec.CC_TRUNCATED, False)
        self.viterbi_decoder = fec.async_decoder(self.viterbi, False, False, 4080//8)
        self.scrambler = ccsds_descrambler()
        self.rs = decode_rs(True, 1)

        self.connect(self, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.pls, 'in'))
        self.msg_connect((self.pls, 'out'), (self.viterbi_decoder, 'in'))
        self.msg_connect((self.viterbi_decoder, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.rs, 'in'))
        self.msg_connect((self.rs, 'out'), (self, 'out'))

    _default_sync_threshold = 13
    
    @classmethod
    def add_options(cls, parser):
        """
        Adds AALTO-1 deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')

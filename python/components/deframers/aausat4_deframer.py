#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital, fec
from ... import decode_rs, aausat4_remove_fsm
from ...hier.sync_to_pdu_soft import sync_to_pdu_soft
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...utils.options_block import options_block

_syncword = '010011110101101000110100010000110101010101000010'

class aausat4_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe AAUSAT-4 frames

    These frames use a terminated CCSDS convolutional code, a
    CCSDS scrambler and CCSDS Reed-Solomon.

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold = None, options = None):
        gr.hier_block2.__init__(self, "aausat4_deframer",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)
        
        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.deframer = sync_to_pdu_soft(packlen = 1996 + 8,\
                                         sync = _syncword,\
                                         threshold = syncword_threshold)
        self.fsm = aausat4_remove_fsm()
        self.viterbi_short = fec.cc_decoder.make(1020, 7, 2, [79,-109], 0, -1, fec.CC_TERMINATED, False)
        self.viterbi_decoder_short = fec.async_decoder(self.viterbi_short, True, False, 1020//8)
        self.viterbi_long = fec.cc_decoder.make(1996, 7, 2, [79,-109], 0, -1, fec.CC_TERMINATED, False)
        self.viterbi_decoder_long = fec.async_decoder(self.viterbi_long, False, False, 1996//8)        

        # workaround for bug https://github.com/gnuradio/gnuradio/pull/2965
        # we use packed output for Viterbi short decoder and the we unpack the PDUs
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.unpack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.taglength = blocks.tagged_stream_multiply_length(gr.sizeof_char*1, 'packet_len', 8)
        self.tag2pdu = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')

        self.scrambler = ccsds_descrambler()
        self.rs = decode_rs(False, 1)

        self.connect(self, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.fsm, 'in'))
        self.msg_connect((self.fsm, 'short'), (self.viterbi_decoder_short, 'in'))
        self.msg_connect((self.fsm, 'long'), (self.viterbi_decoder_long, 'in'))

        # workaround
        self.msg_connect((self.viterbi_decoder_short, 'out'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.unpack, self.taglength, self.tag2pdu)
        self.msg_connect((self.tag2pdu, 'pdus'), (self.scrambler, 'in'))

        self.msg_connect((self.viterbi_decoder_long, 'out'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.rs, 'in'))
        self.msg_connect((self.rs, 'out'), (self, 'out'))

    _default_sync_threshold = 8
        
    @classmethod
    def add_options(cls, parser):
        """
        Adds AAUSAT-4 deframer specific options to the argparse parser
        """
        parser.add_argument('--syncword_threshold', type = int, default = cls._default_sync_threshold, help = 'Syncword bit errors [default=%(default)r]')
        parser.add_argument('--verbose_rs', action = 'store_true', help = 'Verbose RS decoder')

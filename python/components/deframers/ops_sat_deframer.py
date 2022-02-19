#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital

from ... import (
    nrzi_decode, hdlc_deframer, pdu_head_tail, decode_rs, pdu_length_filter)
from ...grpdu import pdu_to_tagged_stream, tagged_stream_to_pdu
from ...grtypes import byte_t
from ...utils.options_block import options_block


class ops_sat_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe OPS-SAT AX.25 + Reed-Solomon.

    The input is a float stream of soft symbols. The output are PDUs
    with Reed-Solomon decoded data.

    The input should be NRZ-I encoded and G3RUH scrambled.

    Args:
        options: Options from argparse
    """
    def __init__(self, options=None):
        gr.hier_block2.__init__(
            self,
            'ops_sat_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        self.slicer = digital.binary_slicer_fb()
        self.nrzi = nrzi_decode()
        self.descrambler = digital.descrambler_bb(0x21, 0, 16)
        self.deframer = hdlc_deframer(False, 10000)  # we skip CRC-16 check
        self.strip = pdu_head_tail(3, 16)

        # CCSDS descrambler
        self.pdu2tag = pdu_to_tagged_stream(byte_t, 'packet_len')
        self.unpack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.scramble = digital.additive_scrambler_bb(
            0xA9, 0xFF, 7, count=0, bits_per_byte=1,
            reset_tag_key='packet_len')
        self.pack = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.tag2pdu = tagged_stream_to_pdu(byte_t, 'packet_len')

        # Prevents passing codewords of incorrect size to the RS decoder
        self.length_filter = pdu_length_filter(33, 255)
        self.fec = decode_rs(False, 1)

        self.connect(self, self.slicer, self.nrzi, self.descrambler,
                     self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.strip, 'in'))
        self.msg_connect((self.strip, 'out'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.unpack, self.scramble, self.pack,
                     self.tag2pdu)
        self.msg_connect((self.tag2pdu, 'pdus'), (self.length_filter, 'in'))
        self.msg_connect((self.length_filter, 'out'), (self.fec, 'in'))
        self.msg_connect((self.fec, 'out'), (self, 'out'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds OPS-SAT deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--verbose_rs', action='store_true', help='Verbose RS decoder')

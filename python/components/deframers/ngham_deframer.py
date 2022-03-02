#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019, 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital

from ... import (
    decode_rs, ngham_packet_crop, ngham_remove_padding)
from ...crcs import crc16_ccitt_x25
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...utils.options_block import options_block


_syncword = '01011101111001100010101001111110'


class ngham_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe NGHam frames

    These use a CCSDS scrambler and CCSDS Reed-Solomon
    Reed-Solomon decoding is currently not implemented

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        decode_rs: use Reed-Solomon decoding (bool)
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, decode_rs=False, syncword_threshold=None,
                 options=None):
        gr.hier_block2.__init__(
            self,
            'ccsds_rs_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if decode_rs:
            raise ValueError('NGHam Reed-Solomon decoding not implemented yet')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            packlen=255 + 3, sync=_syncword, threshold=syncword_threshold)
        self.crop = ngham_packet_crop()
        self.pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.unpack = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.taglength = blocks.tagged_stream_multiply_length(
            gr.sizeof_char*1, 'packet_len', 8)
        self.tag2pdu = blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len')
        self.scrambler = ccsds_descrambler()
        self.padding = ngham_remove_padding()
        self.crc = crc16_ccitt_x25(swap_endianness=False)

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.crop, 'in'))
        self.msg_connect((self.crop, 'rs16'), (self.pdu2tag, 'pdus'))
        self.msg_connect((self.crop, 'rs32'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.unpack, self.taglength, self.tag2pdu)
        self.msg_connect((self.tag2pdu, 'pdus'), (self.scrambler, 'in'))
        self.msg_connect((self.scrambler, 'out'), (self.padding, 'in'))
        self.msg_connect((self.padding, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self, 'out'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds NGHam deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

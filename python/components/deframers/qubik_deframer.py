#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, digital

from ... import decode_rs
from ...grpdu import pdu_to_tagged_stream, tagged_stream_to_pdu
from ...grtypes import byte_t
from ...crcs import crc32c, crc16_ccitt_false
from ...hier.ccsds_descrambler import ccsds_descrambler
from ...hier.sync_to_pdu_packed import sync_to_pdu_packed
from ...utils.options_block import options_block


# 0x3C674952
_syncword = '00111100011001110100100101010010'


class qubik_deframer(gr.hier_block2, options_block):
    """
    Hierarchical block to deframe QUBIK custom frames

    QUBIK frames use a custom 32-bit syncword, CCSDS Reed-Solomon,
    CCSDS scrambling (unusually applied before Reed-Solomon encoding),
    and a CRC-32C and CRC-16-CCITT-FALSE.

    https://gitlab.com/amsat-dl/erminaz/erminaz-comms-sw/-/blob/master/test/flowgraphs/qubik_transceiver.grc?ref_type=heads
    https://gitlab.com/librespacefoundation/satnogs/gr-satnogs/-/blob/master/lib/ieee802_15_4_variant_decoder.cc?ref_type=heads

    The input is a float stream of soft symbols. The output are PDUs
    with frames.

    Args:
        syncword_threshold: number of bit errors allowed in syncword (int)
        options: Options from argparse
    """
    def __init__(self, syncword_threshold=None, options=None):
        gr.hier_block2.__init__(
            self,
            'qubik_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_out('out')

        if syncword_threshold is None:
            syncword_threshold = self.options.syncword_threshold

        self.slicer = digital.binary_slicer_fb()
        self.deframer = sync_to_pdu_packed(
            # +32 because of RS parity check bytes
            # +4 because of CRC-32C
            packlen=128+32+4, sync=_syncword,
            threshold=syncword_threshold)
        self.rs = decode_rs(False, 1)
        self.pdu2tag = pdu_to_tagged_stream(byte_t, 'packet_len')
        self.unpack = blocks.unpack_k_bits_bb(8)
        self.multiply_length = blocks.tagged_stream_multiply_length(
            gr.sizeof_char, 'packet_len', 8.0)
        self.tag2pdu = tagged_stream_to_pdu(byte_t, 'packet_len')
        self.descrambler = ccsds_descrambler()
        self.crc = crc32c()
        self.crc16 = crc16_ccitt_false()

        self.connect(self, self.slicer, self.deframer)
        self.msg_connect((self.deframer, 'out'), (self.rs, 'in'))
        self.msg_connect((self.rs, 'out'), (self.pdu2tag, 'pdus'))
        self.connect(self.pdu2tag, self.unpack, self.multiply_length,
                     self.tag2pdu)
        self.msg_connect((self.tag2pdu, 'pdus'), (self.descrambler, 'in'))
        self.msg_connect((self.descrambler, 'out'), (self.crc, 'in'))
        self.msg_connect((self.crc, 'ok'), (self.crc16, 'in'))
        self.msg_connect((self.crc16, 'ok'), (self, 'out'))

    _default_sync_threshold = 4

    @classmethod
    def add_options(cls, parser):
        """
        Adds QUBIK deframer specific options to the argparse parser
        """
        parser.add_argument(
            '--syncword_threshold', type=int,
            default=cls._default_sync_threshold,
            help='Syncword bit errors [default=%(default)r]')

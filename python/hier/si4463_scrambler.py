# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SI4463 scrambler
# Author: Daniel Estevez
# Description: SI4463 scrambler
# GNU Radio version: 3.8.0.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from ..grpdu import pdu_to_tagged_stream, tagged_stream_to_pdu
from ..grtypes import byte_t


class si4463_scrambler(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self,
            'SI4463 scrambler',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_in('in')
        self.message_port_register_hier_out('out')

        ##################################################
        # Blocks
        ##################################################
        self.digital_additive_scrambler_bb_0_0 = (
            digital.additive_scrambler_bb(
                0x21, 0x1e1, 8, count=0, bits_per_byte=1,
                reset_tag_key="packet_len"))
        self.blocks_tagged_stream_to_pdu_0_0 = (
            tagged_stream_to_pdu(byte_t, 'packet_len'))
        self.blocks_tagged_stream_multiply_length_0 = (
            blocks.tagged_stream_multiply_length(gr.sizeof_char*1,
                                                 'packet_len', 1.0/8))
        self.blocks_pdu_to_tagged_stream_0 = (
            pdu_to_tagged_stream(byte_t, 'packet_len'))
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect(
            (self.blocks_tagged_stream_to_pdu_0_0, 'pdus'), (self, 'out'))
        self.msg_connect(
            (self, 'in'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect(
            (self.blocks_pack_k_bits_bb_0, 0),
            (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect(
            (self.blocks_pdu_to_tagged_stream_0, 0),
            (self.digital_additive_scrambler_bb_0_0, 0))
        self.connect(
            (self.blocks_tagged_stream_multiply_length_0, 0),
            (self.blocks_tagged_stream_to_pdu_0_0, 0))
        self.connect(
            (self.digital_additive_scrambler_bb_0_0, 0),
            (self.blocks_pack_k_bits_bb_0, 0))

# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CCSDS descrambler
# Author: Daniel Estevez
# Description: CCSDS descrambler (input is unpacked, output is packed)
# GNU Radio version: 3.8.0.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes


class ccsds_descrambler(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self,
            'CCSDS descrambler',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_in("in")
        self.message_port_register_hier_out("out")

        ##################################################
        # Blocks
        ##################################################
        self.digital_additive_scrambler_bb_0_0 = digital.additive_scrambler_bb(
            0xA9, 0xFF, 7, count=0, bits_per_byte=1,
            reset_tag_key="packet_len")
        self.blocks_unpacked_to_packed_xx_0_0_0_0 = (
            blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST))
        self.blocks_tagged_stream_to_pdu_0_0_0_0_0 = (
            blocks.tagged_stream_to_pdu(blocks.byte_t, 'packet_len'))
        self.blocks_tagged_stream_multiply_length_0_0_0_0 = (
            blocks.tagged_stream_multiply_length(
                gr.sizeof_char*1, 'packet_len', 1/8.0))
        self.blocks_pdu_to_tagged_stream_0 = (
            blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len'))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect(
            (self.blocks_tagged_stream_to_pdu_0_0_0_0_0, 'pdus'),
            (self, 'out'))
        self.msg_connect(
            (self, 'in'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect(
            (self.blocks_pdu_to_tagged_stream_0, 0),
            (self.digital_additive_scrambler_bb_0_0, 0))
        self.connect(
            (self.blocks_tagged_stream_multiply_length_0_0_0_0, 0),
            (self.blocks_tagged_stream_to_pdu_0_0_0_0_0, 0))
        self.connect(
            (self.blocks_unpacked_to_packed_xx_0_0_0_0, 0),
            (self.blocks_tagged_stream_multiply_length_0_0_0_0, 0))
        self.connect(
            (self.digital_additive_scrambler_bb_0_0, 0),
            (self.blocks_unpacked_to_packed_xx_0_0_0_0, 0))

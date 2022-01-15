# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PN9 scrambler
# Author: Daniel Estevez
# Description: PN9 scrambler
# GNU Radio version: 3.8.0.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes

from ..grtypes import byte_t


class pn9_scrambler(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self,
            'PN9 scrambler',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_in('in')
        self.message_port_register_hier_out('out')

        ##################################################
        # Blocks
        ##################################################
        self.digital_additive_scrambler_bb_0 = (
            digital.additive_scrambler_bb(0x21, 0x1FF, 8, count=0,
                                          bits_per_byte=8,
                                          reset_tag_key='packet_len'))
        self.blocks_tagged_stream_to_pdu_0 = (
            blocks.tagged_stream_to_pdu(byte_t, 'packet_len'))
        self.blocks_pdu_to_tagged_stream_0 = (
            blocks.pdu_to_tagged_stream(byte_t, 'packet_len'))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect(
            (self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self, 'out'))
        self.msg_connect(
            (self, 'in'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.connect(
            (self.blocks_pdu_to_tagged_stream_0, 0),
            (self.digital_additive_scrambler_bb_0, 0))
        self.connect(
            (self.digital_additive_scrambler_bb_0, 0),
            (self.blocks_tagged_stream_to_pdu_0, 0))

# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Sync and create packed PDU
# Author: Daniel Estevez
# Description: Finds syncword and creates a PDU of fixed size and packed bytes
# GNU Radio version: 3.8.0.0

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import satellites
import numpy

from ..grtypes import byte_t


class sync_to_pdu_packed(gr.hier_block2):
    def __init__(self, packlen=0,
                 sync='00011010110011111111110000011101',
                 threshold=4):
        gr.hier_block2.__init__(
            self,
            'Sync and create packed PDU',
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_out('out')

        ##################################################
        # Parameters
        ##################################################
        self.packlen = packlen
        self.sync = sync
        self.threshold = threshold

        ##################################################
        # Blocks
        ##################################################
        self.satellites_fixedlen_tagger_0_0_0 = (
            satellites.fixedlen_tagger('syncword', 'packet_len',
                                       packlen*8, numpy.byte))
        self.digital_correlate_access_code_tag_bb_0_0_0 = (
            digital.correlate_access_code_tag_bb(sync, threshold, 'syncword'))
        self.blocks_unpacked_to_packed_xx_0 = (
            blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST))
        self.blocks_tagged_stream_to_pdu_0_0_0 = (
            blocks.tagged_stream_to_pdu(byte_t, 'packet_len'))
        self.blocks_tagged_stream_multiply_length_0 = (
            blocks.tagged_stream_multiply_length(gr.sizeof_char*1,
                                                 'packet_len', 1/8.0))

        ##################################################
        # Connections
        ##################################################
        self.msg_connect(
            (self.blocks_tagged_stream_to_pdu_0_0_0, 'pdus'), (self, 'out'))
        self.connect(
            (self.blocks_tagged_stream_multiply_length_0, 0),
            (self.blocks_tagged_stream_to_pdu_0_0_0, 0))
        self.connect(
            (self.blocks_unpacked_to_packed_xx_0, 0),
            (self.blocks_tagged_stream_multiply_length_0, 0))
        self.connect(
            (self.digital_correlate_access_code_tag_bb_0_0_0, 0),
            (self.satellites_fixedlen_tagger_0_0_0, 0))
        self.connect(
            (self, 0), (self.digital_correlate_access_code_tag_bb_0_0_0, 0))
        self.connect(
            (self.satellites_fixedlen_tagger_0_0_0, 0),
            (self.blocks_unpacked_to_packed_xx_0, 0))

    def get_packlen(self):
        return self.packlen

    def set_packlen(self, packlen):
        self.packlen = packlen
        self.satellites_fixedlen_tagger_0_0_0.set_packet_len(self.packlen)

    def get_sync(self):
        return self.sync

    def set_sync(self, sync):
        self.sync = sync
        (self.digital_correlate_access_code_tag_bb_0_0_0
             .set_access_code(self.sync))

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        (self.digital_correlate_access_code_tag_bb_0_0_0
             .set_threshold(self.threshold))

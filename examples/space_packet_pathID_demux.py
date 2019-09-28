#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Space Packet Pathid Demux
# GNU Radio version: 3.7.13.5
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt
import satellites


class space_packet_pathID_demux(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Space Packet Pathid Demux")

        ##################################################
        # Blocks
        ##################################################
        self.satellites_space_packet_primaryheader_adder_0_1 = satellites.space_packet_primaryheader_adder(0, 1, 3, 0, 0)
        self.satellites_space_packet_primaryheader_adder_0_0 = satellites.space_packet_primaryheader_adder(0, 1, 1, 0, 0)
        self.satellites_space_packet_primaryheader_adder_0 = satellites.space_packet_primaryheader_adder(0, 1, 10, 0, 0)
        self.satellites_space_packet_parser_0_2 = satellites.space_packet_parser(1, 0, 1, 'default_value')
        self.satellites_space_packet_parser_0_1 = satellites.space_packet_parser(1, 0, 1, 'default_value')
        self.satellites_space_packet_parser_0 = satellites.space_packet_parser(1, 0, 1, 'default_value')
        self.satellites_pathID_demultiplexer_0 = satellites.pathID_demultiplexer((0,1))
        self.blocks_random_pdu_0 = blocks.random_pdu(4, 4, chr(0xFF), 4)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("TEST"), 1000)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.satellites_space_packet_primaryheader_adder_0, 'in'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.satellites_space_packet_primaryheader_adder_0_0, 'in'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.satellites_space_packet_primaryheader_adder_0_1, 'in'))
        self.msg_connect((self.satellites_pathID_demultiplexer_0, 'out0'), (self.satellites_space_packet_parser_0, 'in'))
        self.msg_connect((self.satellites_pathID_demultiplexer_0, 'out1'), (self.satellites_space_packet_parser_0_1, 'in'))
        self.msg_connect((self.satellites_pathID_demultiplexer_0, 'discarded'), (self.satellites_space_packet_parser_0_2, 'in'))
        self.msg_connect((self.satellites_space_packet_primaryheader_adder_0, 'out'), (self.satellites_pathID_demultiplexer_0, 'in'))
        self.msg_connect((self.satellites_space_packet_primaryheader_adder_0_0, 'out'), (self.satellites_pathID_demultiplexer_0, 'in'))
        self.msg_connect((self.satellites_space_packet_primaryheader_adder_0_1, 'out'), (self.satellites_pathID_demultiplexer_0, 'in'))


def main(top_block_cls=space_packet_pathID_demux, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()

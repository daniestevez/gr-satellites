#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: KS-1Q decoder
# Author: Daniel Estevez
# Description: KS-1Q decoder
# Generated: Mon Jan 23 17:32:49 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from ccsds_descrambler import ccsds_descrambler  # grc-generated hier_block
from ccsds_viterbi import ccsds_viterbi  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from sync_to_pdu import sync_to_pdu  # grc-generated hier_block
import csp
import kiss
import ks1q
import libfec
import sids


class ks_1q(gr.top_block):

    def __init__(self, callsign='', invert=1, ip='::', latitude=0, longitude=0, port=7355, recstart=''):
        gr.top_block.__init__(self, "KS-1Q decoder")

        ##################################################
        # Parameters
        ##################################################
        self.callsign = callsign
        self.invert = invert
        self.ip = ip
        self.latitude = latitude
        self.longitude = longitude
        self.port = port
        self.recstart = recstart

        ##################################################
        # Variables
        ##################################################
        self.threshold = threshold = 4

        ##################################################
        # Blocks
        ##################################################
        self.sync_to_pdu_0_0 = sync_to_pdu(
            packlen=255*8,
            sync="00011010110011111111110000011101",
            threshold=threshold,
        )
        self.sync_to_pdu_0 = sync_to_pdu(
            packlen=255*8,
            sync="00011010110011111111110000011101",
            threshold=threshold,
        )
        self.sids_submit_0 = sids.submit('http://tlm.pe0sat.nl/tlmdb/frame_db.php', 41845, callsign, longitude, latitude, recstart)
        self.sids_print_timestamp_0 = sids.print_timestamp('%Y-%m-%d %H:%M:%S')
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, 48000, 11e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.libfec_decode_rs_0 = libfec.decode_rs(True, 1)
        self.ks1q_header_remover_0 = ks1q.header_remover(True)
        self.kiss_kiss_to_pdu_0_0 = kiss.kiss_to_pdu(True)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(2.4, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.csp_swap_header_0_0 = csp.swap_header()
        self.csp_check_crc_0_0 = csp.check_crc(False, False, True)
        self.ccsds_viterbi_0_0 = ccsds_viterbi()
        self.ccsds_viterbi_0 = ccsds_viterbi()
        self.ccsds_descrambler_0 = ccsds_descrambler()
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, ip, port, 1472, False)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767.0)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((invert*10, ))
        self.blocks_message_debug_0_0 = blocks.message_debug()
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ccsds_descrambler_0, 'out'), (self.libfec_decode_rs_0, 'in'))    
        self.msg_connect((self.csp_check_crc_0_0, 'ok'), (self.csp_swap_header_0_0, 'in'))    
        self.msg_connect((self.csp_swap_header_0_0, 'out'), (self.sids_print_timestamp_0, 'in'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0_0, 'out'), (self.csp_check_crc_0_0, 'in'))    
        self.msg_connect((self.ks1q_header_remover_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.libfec_decode_rs_0, 'out'), (self.ks1q_header_remover_0, 'in'))    
        self.msg_connect((self.libfec_decode_rs_0, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.sids_print_timestamp_0, 'out'), (self.blocks_message_debug_0_0, 'print_pdu'))    
        self.msg_connect((self.sync_to_pdu_0, 'out'), (self.ccsds_descrambler_0, 'in'))    
        self.msg_connect((self.sync_to_pdu_0_0, 'out'), (self.ccsds_descrambler_0, 'in'))    
        self.connect((self.blocks_delay_0, 0), (self.ccsds_viterbi_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.kiss_kiss_to_pdu_0_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.ccsds_viterbi_0, 0), (self.sync_to_pdu_0, 0))    
        self.connect((self.ccsds_viterbi_0_0, 0), (self.sync_to_pdu_0_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.ccsds_viterbi_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    

    def get_callsign(self):
        return self.callsign

    def set_callsign(self, callsign):
        self.callsign = callsign

    def get_invert(self):
        return self.invert

    def set_invert(self, invert):
        self.invert = invert
        self.blocks_multiply_const_vxx_0.set_k((self.invert*10, ))

    def get_ip(self):
        return self.ip

    def set_ip(self, ip):
        self.ip = ip

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_recstart(self):
        return self.recstart

    def set_recstart(self, recstart):
        self.recstart = recstart

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.sync_to_pdu_0_0.set_threshold(self.threshold)
        self.sync_to_pdu_0.set_threshold(self.threshold)


def argument_parser():
    description = 'KS-1Q decoder'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default='',
        help="Set your callsign [default=%default]")
    parser.add_option(
        "-i", "--invert", dest="invert", type="intx", default=1,
        help="Set invert the waveform (-1 to invert) [default=%default]")
    parser.add_option(
        "", "--ip", dest="ip", type="string", default='::',
        help="Set UDP listen IP [default=%default]")
    parser.add_option(
        "", "--latitude", dest="latitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set latitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--longitude", dest="longitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set longitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--port", dest="port", type="intx", default=7355,
        help="Set UDP port [default=%default]")
    parser.add_option(
        "", "--recstart", dest="recstart", type="string", default='',
        help="Set start of recording, if processing a recording (format YYYY-MM-DD HH:MM:SS) [default=%default]")
    return parser


def main(top_block_cls=ks_1q, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(callsign=options.callsign, invert=options.invert, ip=options.ip, latitude=options.latitude, longitude=options.longitude, port=options.port, recstart=options.recstart)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()

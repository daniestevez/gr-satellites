#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: BEESAT decoder
# Author: Daniel Estevez
# Description: BEESAT decoder
# Generated: Thu Sep 15 16:12:36 2016
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sids
import tnc_nx


class beesat(gr.top_block):

    def __init__(self, callsign="", invert=1, ip="::", latitude=0, longitude=0, port=7355, recstart=""):
        gr.top_block.__init__(self, "BEESAT decoder")

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
        # Blocks
        ##################################################
        self.tnc_nx_nx_decoder_1_0 = tnc_nx.nx_decoder()
        self.tnc_nx_beesat_classifier_0 = tnc_nx.beesat_classifier()
        self.sids_submit_0_0_0 = sids.submit("http://tlm.pe0sat.nl/tlmdb/frame_db.php", 41619, callsign, longitude, latitude, recstart)
        self.sids_submit_0_0 = sids.submit("http://tlm.pe0sat.nl/tlmdb/frame_db.php", 39136, callsign, longitude, latitude, recstart)
        self.sids_submit_0 = sids.submit("http://tlm.pe0sat.nl/tlmdb/frame_db.php", 35933, callsign, longitude, latitude, recstart)
        self.low_pass_filter_0 = filter.interp_fir_filter_fff(1, firdes.low_pass(
        	1, 48000, 3000, 100, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0_0 = digital.clock_recovery_mm_ff(10*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, ip, port, 1472, False)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767.0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((invert*10, ))
        self.blocks_message_debug_0 = blocks.message_debug()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.tnc_nx_beesat_classifier_0, 'BEESAT-1'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.tnc_nx_beesat_classifier_0, 'BEESAT-2'), (self.sids_submit_0_0, 'in'))    
        self.msg_connect((self.tnc_nx_beesat_classifier_0, 'BEESAT-4'), (self.sids_submit_0_0_0, 'in'))    
        self.msg_connect((self.tnc_nx_nx_decoder_1_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.tnc_nx_nx_decoder_1_0, 'out'), (self.tnc_nx_beesat_classifier_0, 'in'))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.tnc_nx_nx_decoder_1_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.digital_clock_recovery_mm_xx_0_0, 0))    

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


def argument_parser():
    description = 'BEESAT decoder'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default="",
        help="Set your callsign [default=%default]")
    parser.add_option(
        "-i", "--invert", dest="invert", type="intx", default=1,
        help="Set invert the waveform (-1 to invert) [default=%default]")
    parser.add_option(
        "", "--ip", dest="ip", type="string", default="::",
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
        "", "--recstart", dest="recstart", type="string", default="",
        help="Set start of recording, if processing a recording (format YYYY-MM-DD HH:MM:SS) [default=%default]")
    return parser


def main(top_block_cls=beesat, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(callsign=options.callsign, invert=options.invert, ip=options.ip, latitude=options.latitude, longitude=options.longitude, port=options.port, recstart=options.recstart)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()

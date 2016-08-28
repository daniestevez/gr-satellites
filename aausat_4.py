#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AAUSAT-4 decoder
# Author: Daniel Estevez
# Description: AAUSAT-4 decoder
# Generated: Sun Aug 28 23:05:33 2016
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import aausat
import numpy
import sids
import synctags


class aausat_4(gr.top_block):

    def __init__(self, callsign="", invert=1, ip="::", latitude=0, longitude=0, port=7355, recstart=""):
        gr.top_block.__init__(self, "AAUSAT-4 decoder")

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
        self.threshold = threshold = 8
        self.access_code = access_code = "010011110101101000110100010000110101010101000010"

        ##################################################
        # Blocks
        ##################################################
        self.synctags_fixedlen_tagger_0_0 = synctags.fixedlen_tagger("syncword", "packet_len", 2008, numpy.byte)
        self.synctags_fixedlen_tagger_0 = synctags.fixedlen_tagger("syncword", "packet_len", 2008, numpy.byte)
        self.sids_submit_0 = sids.submit("http://tlm.pe0sat.nl/tlmdb/frame_db.php", 41460, callsign, longitude, latitude, recstart)
        self.digital_correlate_access_code_tag_bb_0_0 = digital.correlate_access_code_tag_bb(access_code, threshold, "syncword")
        self.digital_correlate_access_code_tag_bb_0 = digital.correlate_access_code_tag_bb(access_code, threshold, "syncword")
        self.digital_clock_recovery_mm_xx_0_0 = digital.clock_recovery_mm_ff(5.0, 0.25*0.175*0.175, 0.005, 0.175, 0.005)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(20.0, 0.25*0.175*0.175, 0.005, 0.175, 0.005)
        self.digital_binary_slicer_fb_0_0 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_unpacked_to_packed_xx_0_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, ip, 7355, 1472, False)
        self.blocks_tagged_stream_to_pdu_0_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, "packet_len")
        self.blocks_tagged_stream_multiply_length_0_0 = blocks.tagged_stream_multiply_length(gr.sizeof_char*1, "packet_len", 1/8.0)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_char*1, "packet_len", 1/8.0)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767.0)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((invert*10, ))
        self.aausat_aausat4_fec_0 = aausat.aausat4_fec(False)
        self.aausat_aausat4_beacon_parser_0 = aausat.aausat4_beacon_parser()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.aausat_aausat4_fec_0, 'out'), (self.aausat_aausat4_beacon_parser_0, 'in'))    
        self.msg_connect((self.aausat_aausat4_fec_0, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.aausat_aausat4_fec_0, 'in'))    
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0_0, 'pdus'), (self.aausat_aausat4_fec_0, 'in'))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_clock_recovery_mm_xx_0_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))    
        self.connect((self.blocks_tagged_stream_multiply_length_0_0, 0), (self.blocks_tagged_stream_to_pdu_0_0, 0))    
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))    
        self.connect((self.blocks_unpacked_to_packed_xx_0_0, 0), (self.blocks_tagged_stream_multiply_length_0_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_correlate_access_code_tag_bb_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0_0, 0), (self.digital_correlate_access_code_tag_bb_0_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0_0, 0), (self.digital_binary_slicer_fb_0_0, 0))    
        self.connect((self.digital_correlate_access_code_tag_bb_0, 0), (self.synctags_fixedlen_tagger_0, 0))    
        self.connect((self.digital_correlate_access_code_tag_bb_0_0, 0), (self.synctags_fixedlen_tagger_0_0, 0))    
        self.connect((self.synctags_fixedlen_tagger_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))    
        self.connect((self.synctags_fixedlen_tagger_0_0, 0), (self.blocks_unpacked_to_packed_xx_0_0, 0))    

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

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code


def argument_parser():
    description = 'AAUSAT-4 decoder'
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


def main(top_block_cls=aausat_4, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(callsign=options.callsign, invert=options.invert, ip=options.ip, latitude=options.latitude, longitude=options.longitude, port=options.port, recstart=options.recstart)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()

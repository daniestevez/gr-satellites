#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: 3CAT-2 decoder
# Author: Daniel Estevez
# Description: Decodes 9k6 AX.25 BPSK telemetry from 3CAT-2
# Generated: Mon Aug 29 19:09:53 2016
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import kiss
import sat3cat2
import sids


class sat_3cat_2(gr.top_block):

    def __init__(self, bfo=12000, callsign="", ip="::", latitude=0, longitude=0, port=7355, recstart=""):
        gr.top_block.__init__(self, "3CAT-2 decoder")

        ##################################################
        # Parameters
        ##################################################
        self.bfo = bfo
        self.callsign = callsign
        self.ip = ip
        self.latitude = latitude
        self.longitude = longitude
        self.port = port
        self.recstart = recstart

        ##################################################
        # Variables
        ##################################################
        self.samp_per_sym = samp_per_sym = 5
        self.nfilts = nfilts = 16
        
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()
        
        self.samp_rate = samp_rate = 48000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(samp_per_sym), 0.35, 11*samp_per_sym*nfilts)

        ##################################################
        # Blocks
        ##################################################
        self.sids_submit_0 = sids.submit("http://tlm.pe0sat.nl/tlmdb/frame_db.php", 41732, callsign, longitude, latitude, recstart)
        self.sat3cat2_telemetry_parser_0 = sat3cat2.telemetry_parser()
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 7500, 500, firdes.WIN_HAMMING, 6.76))
        self.kiss_pdu_to_kiss_0 = kiss.pdu_to_kiss()
        self.kiss_nrzi_decode_0 = kiss.nrzi_decode()
        self.kiss_hdlc_deframer_0 = kiss.hdlc_deframer(check_fcs=True, max_length=10000)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcf(1, (firdes.low_pass(1, samp_rate, 10000, 1000)), bfo, samp_rate)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(samp_per_sym, 0.1, (rrc_taps), nfilts, nfilts/2, 1.5, 2)
        self.digital_lms_dd_equalizer_cc_0_0 = digital.lms_dd_equalizer_cc(2, 0.03, 2, variable_constellation_0)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(samp_per_sym, 0.350, 100, 0.020)
        self.digital_costas_loop_cc_0_0_0_0 = digital.costas_loop_cc(0.04, 2, False)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, ip, port, 1472, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", "", "52001", 10000, True)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024*4, 2)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.kiss_pdu_to_kiss_0, 'in'))    
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.sat3cat2_telemetry_parser_0, 'in'))    
        self.msg_connect((self.kiss_hdlc_deframer_0, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.kiss_pdu_to_kiss_0, 'out'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.digital_fll_band_edge_cc_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.kiss_nrzi_decode_0, 0))    
        self.connect((self.digital_costas_loop_cc_0_0_0_0, 0), (self.digital_lms_dd_equalizer_cc_0_0, 0))    
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.digital_lms_dd_equalizer_cc_0_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_feedforward_agc_cc_0, 0))    
        self.connect((self.kiss_nrzi_decode_0, 0), (self.kiss_hdlc_deframer_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    

    def get_bfo(self):
        return self.bfo

    def set_bfo(self, bfo):
        self.bfo = bfo
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.bfo)

    def get_callsign(self):
        return self.callsign

    def set_callsign(self, callsign):
        self.callsign = callsign

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

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.samp_per_sym), 0.35, 11*self.samp_per_sym*self.nfilts))

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 7500, 500, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1, self.samp_rate, 10000, 1000)))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.rrc_taps))


def argument_parser():
    description = 'Decodes 9k6 AX.25 BPSK telemetry from 3CAT-2'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--bfo", dest="bfo", type="eng_float", default=eng_notation.num_to_str(12000),
        help="Set carrier frequency of the BPSK signal [default=%default]")
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default="",
        help="Set your callsign [default=%default]")
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


def main(top_block_cls=sat_3cat_2, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(bfo=options.bfo, callsign=options.callsign, ip=options.ip, latitude=options.latitude, longitude=options.longitude, port=options.port, recstart=options.recstart)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()

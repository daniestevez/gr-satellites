#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: LilacSat-2 decoder for FUNcube Dongle Pro+
# Author: Daniel Estevez
# Description: LilacSat-2 decoder for FUNcube Dongle Pro+
# Generated: Wed Jan  4 11:12:28 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from ccsds_descrambler import ccsds_descrambler  # grc-generated hier_block
from ccsds_viterbi import ccsds_viterbi  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from sync_to_pdu import sync_to_pdu  # grc-generated hier_block
import fcdproplus
import gpredict
import kiss
import libfec
import math
import sids


class lilacsat2_fcdpp(gr.top_block):

    def __init__(self, callsign='', gpredict_port=4532, latitude=0, longitude=0):
        gr.top_block.__init__(self, "LilacSat-2 decoder for FUNcube Dongle Pro+")

        ##################################################
        # Parameters
        ##################################################
        self.callsign = callsign
        self.gpredict_port = gpredict_port
        self.latitude = latitude
        self.longitude = longitude

        ##################################################
        # Variables
        ##################################################
        self.sub_sps = sub_sps = 32
        self.sub_nfilts = sub_nfilts = 16
        self.sub_alpha = sub_alpha = 0.35
        self.sps = sps = 5
        self.nfilts = nfilts = 16
        self.freq = freq = 437.2e6
        self.alpha = alpha = 0.35
        
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist(([-1, 1]), ([0, 1]), 2, 1).base()
        
        self.threshold = threshold = 4
        self.sub_rrc_taps = sub_rrc_taps = firdes.root_raised_cosine(sub_nfilts, sub_nfilts, 1.0/float(sub_sps), sub_alpha, 11*sub_sps*sub_nfilts)
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), alpha, 11*sps*nfilts)
        self.rf_samp_rate = rf_samp_rate = 192000
        self.offset = offset = 30e3
        self.if_samp_rate = if_samp_rate = 48000
        self.doppler_freq = doppler_freq = freq
        self.af_samp_rate = af_samp_rate = 9600

        ##################################################
        # Blocks
        ##################################################
        self.sync_to_pdu_0_1_0 = sync_to_pdu(
            packlen=(114+32)*8,
            sync="00011010110011111111110000011101",
            threshold=threshold,
        )
        self.sync_to_pdu_0_1 = sync_to_pdu(
            packlen=(114+32)*8,
            sync="00011010110011111111110000011101",
            threshold=threshold,
        )
        self.sync_to_pdu_0_0_0 = sync_to_pdu(
            packlen=(114+32)*8,
            sync="00011010110011111111110000011101",
            threshold=threshold,
        )
        self.sync_to_pdu_0_0 = sync_to_pdu(
            packlen=(114+32)*8,
            sync="00011010110011111111110000011101",
            threshold=threshold,
        )
        self.sync_to_pdu_0 = sync_to_pdu(
            packlen=(114+32)*8,
            sync="00011010110011111111110000011101",
            threshold=threshold,
        )
        self.sids_submit_0 = sids.submit('http://tlm.pe0sat.nl/tlmdb/frame_db.php', 40908, callsign, longitude, latitude, '')
        self.low_pass_filter_3_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, if_samp_rate, 8e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, af_samp_rate, 200, 50, firdes.WIN_HAMMING, 6.76))
        self.libfec_decode_rs_0_0_0 = libfec.decode_rs(True, 0)
        self.libfec_decode_rs_0_0 = libfec.decode_rs(True, 0)
        self.libfec_decode_rs_0 = libfec.decode_rs(True, 0)
        self.kiss_kiss_to_pdu_0_1 = kiss.kiss_to_pdu(False)
        self.kiss_kiss_to_pdu_0_0 = kiss.kiss_to_pdu(False)
        self.kiss_kiss_to_pdu_0 = kiss.kiss_to_pdu(False)
        self.gpredict_doppler_0 = gpredict.doppler(self.set_doppler_freq, "localhost", 4532, False)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(rf_samp_rate/if_samp_rate, (filter.firdes.low_pass(1,rf_samp_rate,10000,2000)), doppler_freq - freq + offset, rf_samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(rf_samp_rate/if_samp_rate, (filter.firdes.low_pass(1,rf_samp_rate,5000,2000)), doppler_freq - freq + offset + 25e3, rf_samp_rate)
        self.fcdproplus_fcdproplus_0 = fcdproplus.fcdproplus('',1)
        self.fcdproplus_fcdproplus_0.set_lna(0)
        self.fcdproplus_fcdproplus_0.set_mixer_gain(0)
        self.fcdproplus_fcdproplus_0.set_if_gain(0)
        self.fcdproplus_fcdproplus_0.set_freq_corr(0)
        self.fcdproplus_fcdproplus_0.set_freq(freq-offset)
          
        self.digital_pfb_clock_sync_xxx_0_0 = digital.pfb_clock_sync_fff(sub_sps, 0.0628, (sub_rrc_taps), sub_nfilts, sub_nfilts/2, 0.01, 1)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 0.100, (rrc_taps), nfilts, nfilts/2, 1.5, 2)
        self.digital_lms_dd_equalizer_cc_0_0 = digital.lms_dd_equalizer_cc(2, 0.3, 2, variable_constellation_0)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, 0.350, 100, 0.1)
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(2)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc(0.4, 2, False)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(10, 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_1 = digital.binary_slicer_fb()
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(1024, True)
        self.ccsds_viterbi_0_1 = ccsds_viterbi()
        self.ccsds_viterbi_0_0_0 = ccsds_viterbi()
        self.ccsds_viterbi_0_0 = ccsds_viterbi()
        self.ccsds_viterbi_0 = ccsds_viterbi()
        self.ccsds_descrambler_0_0_0 = ccsds_descrambler()
        self.ccsds_descrambler_0_0 = ccsds_descrambler()
        self.ccsds_descrambler_0 = ccsds_descrambler()
        self.blocks_pdu_to_tagged_stream_0_1 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_delay_0_0_0 = blocks.delay(gr.sizeof_float*1, 1)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_float*1, 1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(0.5)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=af_samp_rate,
        	quad_rate=if_samp_rate,
        	tau=75e-6,
        	max_dev=3.5e3,
          )
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 1)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ccsds_descrambler_0, 'out'), (self.libfec_decode_rs_0, 'in'))    
        self.msg_connect((self.ccsds_descrambler_0_0, 'out'), (self.libfec_decode_rs_0_0, 'in'))    
        self.msg_connect((self.ccsds_descrambler_0_0_0, 'out'), (self.libfec_decode_rs_0_0_0, 'in'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0_0, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0_1, 'out'), (self.blocks_message_debug_0, 'print_pdu'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0_1, 'out'), (self.sids_submit_0, 'in'))    
        self.msg_connect((self.libfec_decode_rs_0, 'out'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.libfec_decode_rs_0_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))    
        self.msg_connect((self.libfec_decode_rs_0_0_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_1, 'pdus'))    
        self.msg_connect((self.sync_to_pdu_0, 'out'), (self.ccsds_descrambler_0, 'in'))    
        self.msg_connect((self.sync_to_pdu_0_0, 'out'), (self.ccsds_descrambler_0_0, 'in'))    
        self.msg_connect((self.sync_to_pdu_0_0_0, 'out'), (self.ccsds_descrambler_0_0_0, 'in'))    
        self.msg_connect((self.sync_to_pdu_0_1, 'out'), (self.ccsds_descrambler_0_0, 'in'))    
        self.msg_connect((self.sync_to_pdu_0_1_0, 'out'), (self.ccsds_descrambler_0_0_0, 'in'))    
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.digital_fll_band_edge_cc_0, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_delay_0_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.ccsds_viterbi_0_1, 0))    
        self.connect((self.blocks_delay_0_0, 0), (self.ccsds_viterbi_0_0_0, 0))    
        self.connect((self.blocks_delay_0_0_0, 0), (self.ccsds_viterbi_0_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.kiss_kiss_to_pdu_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.kiss_kiss_to_pdu_0_0, 0))    
        self.connect((self.blocks_pdu_to_tagged_stream_0_1, 0), (self.kiss_kiss_to_pdu_0_1, 0))    
        self.connect((self.ccsds_viterbi_0, 0), (self.sync_to_pdu_0_1_0, 0))    
        self.connect((self.ccsds_viterbi_0_0, 0), (self.sync_to_pdu_0_0_0, 0))    
        self.connect((self.ccsds_viterbi_0_0_0, 0), (self.digital_diff_decoder_bb_0_0, 0))    
        self.connect((self.ccsds_viterbi_0_1, 0), (self.digital_diff_decoder_bb_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.digital_pfb_clock_sync_xxx_0_0, 0))    
        self.connect((self.digital_binary_slicer_fb_1, 0), (self.sync_to_pdu_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.blocks_delay_0_0_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.ccsds_viterbi_0, 0))    
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_lms_dd_equalizer_cc_0_0, 0))    
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.sync_to_pdu_0_1, 0))    
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.sync_to_pdu_0_0, 0))    
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.digital_lms_dd_equalizer_cc_0_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0_0, 0), (self.digital_binary_slicer_fb_1, 0))    
        self.connect((self.fcdproplus_fcdproplus_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.fcdproplus_fcdproplus_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.analog_feedforward_agc_cc_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.low_pass_filter_3_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.low_pass_filter_3_0_0, 0), (self.analog_nbfm_rx_0, 0))    

    def get_callsign(self):
        return self.callsign

    def set_callsign(self, callsign):
        self.callsign = callsign

    def get_gpredict_port(self):
        return self.gpredict_port

    def set_gpredict_port(self, gpredict_port):
        self.gpredict_port = gpredict_port

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def get_sub_sps(self):
        return self.sub_sps

    def set_sub_sps(self, sub_sps):
        self.sub_sps = sub_sps
        self.set_sub_rrc_taps(firdes.root_raised_cosine(self.sub_nfilts, self.sub_nfilts, 1.0/float(self.sub_sps), self.sub_alpha, 11*self.sub_sps*self.sub_nfilts))

    def get_sub_nfilts(self):
        return self.sub_nfilts

    def set_sub_nfilts(self, sub_nfilts):
        self.sub_nfilts = sub_nfilts
        self.set_sub_rrc_taps(firdes.root_raised_cosine(self.sub_nfilts, self.sub_nfilts, 1.0/float(self.sub_sps), self.sub_alpha, 11*self.sub_sps*self.sub_nfilts))

    def get_sub_alpha(self):
        return self.sub_alpha

    def set_sub_alpha(self, sub_alpha):
        self.sub_alpha = sub_alpha
        self.set_sub_rrc_taps(firdes.root_raised_cosine(self.sub_nfilts, self.sub_nfilts, 1.0/float(self.sub_sps), self.sub_alpha, 11*self.sub_sps*self.sub_nfilts))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_doppler_freq(self.freq)
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.doppler_freq - self.freq + self.offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq - self.freq + self.offset + 25e3)
        self.fcdproplus_fcdproplus_0.set_freq(self.freq-self.offset)

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.alpha, 11*self.sps*self.nfilts))

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.sync_to_pdu_0_1_0.set_threshold(self.threshold)
        self.sync_to_pdu_0_1.set_threshold(self.threshold)
        self.sync_to_pdu_0_0_0.set_threshold(self.threshold)
        self.sync_to_pdu_0_0.set_threshold(self.threshold)
        self.sync_to_pdu_0.set_threshold(self.threshold)

    def get_sub_rrc_taps(self):
        return self.sub_rrc_taps

    def set_sub_rrc_taps(self, sub_rrc_taps):
        self.sub_rrc_taps = sub_rrc_taps
        self.digital_pfb_clock_sync_xxx_0_0.update_taps((self.sub_rrc_taps))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.rrc_taps))

    def get_rf_samp_rate(self):
        return self.rf_samp_rate

    def set_rf_samp_rate(self, rf_samp_rate):
        self.rf_samp_rate = rf_samp_rate
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((filter.firdes.low_pass(1,self.rf_samp_rate,10000,2000)))
        self.freq_xlating_fir_filter_xxx_0.set_taps((filter.firdes.low_pass(1,self.rf_samp_rate,5000,2000)))

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.doppler_freq - self.freq + self.offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq - self.freq + self.offset + 25e3)
        self.fcdproplus_fcdproplus_0.set_freq(self.freq-self.offset)

    def get_if_samp_rate(self):
        return self.if_samp_rate

    def set_if_samp_rate(self, if_samp_rate):
        self.if_samp_rate = if_samp_rate
        self.low_pass_filter_3_0_0.set_taps(firdes.low_pass(1, self.if_samp_rate, 8e3, 2e3, firdes.WIN_HAMMING, 6.76))

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.doppler_freq - self.freq + self.offset)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.doppler_freq - self.freq + self.offset + 25e3)

    def get_af_samp_rate(self):
        return self.af_samp_rate

    def set_af_samp_rate(self, af_samp_rate):
        self.af_samp_rate = af_samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.af_samp_rate, 200, 50, firdes.WIN_HAMMING, 6.76))


def argument_parser():
    description = 'LilacSat-2 decoder for FUNcube Dongle Pro+'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default='',
        help="Set your callsign [default=%default]")
    parser.add_option(
        "", "--gpredict-port", dest="gpredict_port", type="intx", default=4532,
        help="Set GPredict port [default=%default]")
    parser.add_option(
        "", "--latitude", dest="latitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set latitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--longitude", dest="longitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set longitude (format 00.000 or -00.000) [default=%default]")
    return parser


def main(top_block_cls=lilacsat2_fcdpp, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(callsign=options.callsign, gpredict_port=options.gpredict_port, latitude=options.latitude, longitude=options.longitude)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()

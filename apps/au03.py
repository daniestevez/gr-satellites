#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: QB50 AU03 i-INSPIRE II decoder
# Author: Daniel Estevez
# Description: QB50 AU03 i-INSPIRE II decoder
# GNU Radio version: 3.7.13.5
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from sync_to_pdu_packed import sync_to_pdu_packed  # grc-generated hier_block
import satellites


class au03(gr.top_block):

    def __init__(self, callsign='', ip='::', latitude=0, longitude=0, port=7355, recstart=''):
        gr.top_block.__init__(self, "QB50 AU03 i-INSPIRE II decoder")

        ##################################################
        # Parameters
        ##################################################
        self.callsign = callsign
        self.ip = ip
        self.latitude = latitude
        self.longitude = longitude
        self.port = port
        self.recstart = recstart

        ##################################################
        # Variables
        ##################################################
        self.threshold = threshold = 4
        self.access_code = access_code = "11000011101010100110011001010101"

        ##################################################
        # Blocks
        ##################################################
        self.sync_to_pdu_packed_0 = sync_to_pdu_packed(
            packlen=255+3,
            sync=access_code,
            threshold=threshold,
        )
        self.satellites_u482c_decode_0 = satellites.u482c_decode(False, -1, -1, -1)
        self.satellites_submit_0 = satellites.submit('https://db.satnogs.org/api/telemetry/', 42731, callsign, longitude, latitude, recstart)
        self.satellites_print_timestamp_0 = satellites.print_timestamp('%Y-%m-%d %H:%M:%S', True)
        self.satellites_AU03_telemetry_parser_0 = satellites.au03_telemetry_parser()
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, 48000, 2600, 1000, firdes.WIN_HAMMING, 6.76))
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
        	samples_per_symbol=10,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.blocks_udp_source_0 = blocks.udp_source(gr.sizeof_short*1, ip, port, 1472, False)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 32767.0)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.analog_sig_source_x_0 = analog.sig_source_c(48000, analog.GR_COS_WAVE, -3600, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_print_timestamp_0, 'out'), (self.satellites_AU03_telemetry_parser_0, 'in'))
        self.msg_connect((self.satellites_u482c_decode_0, 'out'), (self.satellites_print_timestamp_0, 'in'))
        self.msg_connect((self.satellites_u482c_decode_0, 'out'), (self.satellites_submit_0, 'in'))
        self.msg_connect((self.sync_to_pdu_packed_0, 'out'), (self.satellites_u482c_decode_0, 'in'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_udp_source_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.sync_to_pdu_packed_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))

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

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.sync_to_pdu_packed_0.set_threshold(self.threshold)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.sync_to_pdu_packed_0.set_sync(self.access_code)


def argument_parser():
    description = 'QB50 AU03 i-INSPIRE II decoder'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default='',
        help="Set your callsign [default=%default]")
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


def main(top_block_cls=au03, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(callsign=options.callsign, ip=options.ip, latitude=options.latitude, longitude=options.longitude, port=options.port, recstart=options.recstart)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: KISS client telemetry submitter
# Author: Daniel Estevez
# Description: KISS client telemetry submitter
# Generated: Fri Jan 20 11:22:32 2017
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import kiss
import sids


class kiss_submitter(gr.top_block):

    def __init__(self, callsign='', host='localhost', latitude=0, longitude=0, norad=0, port='8001', recstart=''):
        gr.top_block.__init__(self, "KISS client telemetry submitter")

        ##################################################
        # Parameters
        ##################################################
        self.callsign = callsign
        self.host = host
        self.latitude = latitude
        self.longitude = longitude
        self.norad = norad
        self.port = port
        self.recstart = recstart

        ##################################################
        # Blocks
        ##################################################
        self.sids_submit_0 = sids.submit('http://tlm.pe0sat.nl/tlmdb/frame_db.php', norad, callsign, longitude, latitude, recstart)
        self.kiss_kiss_to_pdu_0 = kiss.kiss_to_pdu(True)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_CLIENT", host, port, 10000, False)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))    
        self.msg_connect((self.kiss_kiss_to_pdu_0, 'out'), (self.sids_submit_0, 'in'))    
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.kiss_kiss_to_pdu_0, 0))    

    def get_callsign(self):
        return self.callsign

    def set_callsign(self, callsign):
        self.callsign = callsign

    def get_host(self):
        return self.host

    def set_host(self, host):
        self.host = host

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude

    def get_norad(self):
        return self.norad

    def set_norad(self, norad):
        self.norad = norad

    def get_port(self):
        return self.port

    def set_port(self, port):
        self.port = port

    def get_recstart(self):
        return self.recstart

    def set_recstart(self, recstart):
        self.recstart = recstart


def argument_parser():
    description = 'KISS client telemetry submitter'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--callsign", dest="callsign", type="string", default='',
        help="Set your callsign [default=%default]")
    parser.add_option(
        "", "--host", dest="host", type="string", default='localhost',
        help="Set Host [default=%default]")
    parser.add_option(
        "", "--latitude", dest="latitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set latitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--longitude", dest="longitude", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set longitude (format 00.000 or -00.000) [default=%default]")
    parser.add_option(
        "", "--norad", dest="norad", type="intx", default=0,
        help="Set NORAD ID [default=%default]")
    parser.add_option(
        "-p", "--port", dest="port", type="string", default='8001',
        help="Set Port [default=%default]")
    parser.add_option(
        "", "--recstart", dest="recstart", type="string", default='',
        help="Set start of recording, if processing a recording (format YYYY-MM-DD HH:MM:SS) [default=%default]")
    return parser


def main(top_block_cls=kiss_submitter, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(callsign=options.callsign, host=options.host, latitude=options.latitude, longitude=options.longitude, norad=options.norad, port=options.port, recstart=options.recstart)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()

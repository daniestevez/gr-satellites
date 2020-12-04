# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: CCSDS/NASA-GSFC Viterbi decoder
# Author: Daniel Estevez
# Description: Viterbi27 decoder with convention (POLYB, ~POLYA) (output is unpacked)
# GNU Radio version: 3.8.0.0

from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal




class ccsds_viterbi(gr.hier_block2):
    def __init__(self, code = 'CCSDS'):
        gr.hier_block2.__init__(
            self, "CCSDS/NASA-GSFC Viterbi decoder",
                gr.io_signature(1, 1, gr.sizeof_float*1),
                gr.io_signature(1, 1, gr.sizeof_char*1),
        )

        ##################################################
        # Variables
        ##################################################
        polys = {'CCSDS' : [79, -109],
                 'NASA-DSN' : [-109, 79],
                 'CCSDS uninverted' : [79, 109],
                 'NASA-DSN uninverted' : [109, 79],
                }
        self.dec_cc = dec_cc = fec.cc_decoder.make(80, 7, 2, polys[code],
                                                       0, -1, fec.CC_STREAMING, False)

        ##################################################
        # Blocks
        ##################################################
        self.fec_extended_decoder_0_0 = fec.extended_decoder(decoder_obj_list=dec_cc, threading= None, ann=None, puncpat='11', integration_period=10000)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.fec_extended_decoder_0_0, 0), (self, 0))
        self.connect((self, 0), (self.fec_extended_decoder_0_0, 0))

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc

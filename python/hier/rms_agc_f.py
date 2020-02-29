# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RMS AGC
# Author: Daniel Estevez
# Description: AGC using RMS
# GNU Radio version: 3.8.0.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal




class rms_agc_f(gr.hier_block2):
    def __init__(self, alpha=1e-2, reference=0.5):
        gr.hier_block2.__init__(
            self, "RMS AGC",
                gr.io_signature(1, 1, gr.sizeof_float*1),
                gr.io_signature(1, 1, gr.sizeof_float*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.alpha = alpha
        self.reference = reference

        ##################################################
        # Blocks
        ##################################################
        self.blocks_rms_xx_0 = blocks.rms_ff(alpha)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1.0/reference)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(1e-20)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_divide_xx_0, 0), (self, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_rms_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self, 0), (self.blocks_rms_xx_0, 0))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.blocks_rms_xx_0.set_alpha(self.alpha)

    def get_reference(self):
        return self.reference

    def set_reference(self, reference):
        self.reference = reference
        self.blocks_multiply_const_vxx_0.set_k(1.0/self.reference)

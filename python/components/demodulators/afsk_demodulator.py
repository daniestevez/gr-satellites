#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from gnuradio import gr, filter
from gnuradio.filter import firdes
from .fsk_demodulator import fsk_demodulator
from ...utils.options_block import options_block

class afsk_demodulator(gr.hier_block2, options_block):
    """
    Hierarchical block to demodulate AFSK.

    The input can be either IQ or real. For IQ input, it is assumed
    that the data is FM modulated, so FM demodulation is performed.
    For real input, it is assumed that the data is already FM
    demodulated.

    Args:
        baudrate: Baudrate in symbols per second (float)
        sample_rate: Sample rate in samples per second (float)
        iq: Whether the input is IQ or real (bool)
        af_carrier: Audio frequency carrier in Hz (float)
        deviation: Deviation in Hz, negative inverts the sidebands (float)
        options: Options from argparse
    """
    def __init__(self, baudrate, samp_rate, iq, af_carrier, deviation, options = None):
        gr.hier_block2.__init__(self, "afsk_demodulator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex if iq else gr.sizeof_float),
            gr.io_signature(1, 1, gr.sizeof_float))
        options_block.__init__(self, options)
        
        if iq:
            self.demod = analog.quadrature_demod_cf(1)
            self.connect(self, self.demod)
        else:
            self.demod = self

        filter_cutoff = 2 * abs(deviation)
        filter_transition = 0.1 * abs(deviation)
        taps = firdes.low_pass(1, samp_rate, filter_cutoff, filter_transition)
        self.xlating = filter.freq_xlating_fir_filter_fcf(1, taps, af_carrier, samp_rate)

        self.fsk = fsk_demodulator(baudrate, samp_rate, deviation = deviation, iq = True, options = options)

        self.connect(self.demod, self.xlating, self.fsk, self)

    @classmethod
    def add_options(cls, parser):
        """
        Adds CCSDS concatenated deframer specific options to the argparse parser
        """
        fsk_demodulator.add_options(parser)

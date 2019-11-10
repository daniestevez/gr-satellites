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

from gnuradio import gr, analog, digital, filter
from gnuradio.filter import firdes
from math import ceil, pi
from ...utils.options_block import options_block

class fsk_demodulator(gr.hier_block2, options_block):
    """
    Hierarchical block to demodulate FSK.

    The input can be either IQ or real. For IQ input, it is assumed
    that the data is FM modulated, so FM demodulation is performed.
    For real input, it is assumed that the data is already FM
    demodulated.

    Args:
        baudrate: Baudrate in symbols per second (float)
        sample_rate: Sample rate in samples per second (float)
        iq: Whether the input is IQ or real (bool)
        options: Options from argparse
    """
    def __init__(self, baudrate, samp_rate, iq, options = None):
        gr.hier_block2.__init__(self, "fsk_demodulator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex if iq else gr.sizeof_float),
            gr.io_signature(1, 1, gr.sizeof_float))
        options_block.__init__(self, options)
        
        if iq:
            self.demod = analog.quadrature_demod_cf(0.5*samp_rate/(2*pi*self.options.deviation))
            self.connect(self, self.demod)
        else:
            self.demod = self
        
        sps = samp_rate / baudrate
        max_sps = 10
        if sps > max_sps:
            decimation = ceil(sps / max_sps)
        else:
            decimation = 1
        sps /= decimation

        # Some "okay" filter parameters depending on baudrate
        filter_cutoff = baudrate * 0.6
        filter_transition = baudrate * 0.2
        
        taps = firdes.low_pass(1, samp_rate, filter_cutoff, filter_transition)
        self.lowpass = filter.fir_filter_fff(decimation, taps)

        gain_mu = self.options.gain_mu
        gain_omega = 0.25 * gain_mu * gain_mu
        mu = 0.5

        self.clock_recovery = digital.clock_recovery_mm_ff(sps, gain_omega, mu, gain_mu, self.options.clock_offset_limit)

        self.connect(self.demod, self.lowpass, self.clock_recovery, self)

    _default_gain_mu = 0.5
    _default_omega_relative_limit = 0.01
    _default_deviation_hz = 3000
    
    @classmethod
    def add_options(cls, parser):
        """
        Adds FSK demodulator specific options to the argparse parser
        """
        parser.add_argument('--clock_offset_limit', type = float, default = cls._default_omega_relative_limit, help = 'Maximum clock offset (relative) [default=%(default)r]')
        parser.add_argument('--gain_mu', type = float, default = cls._default_gain_mu, help = 'Gain for MM clock recovery [default=%(default)r]')
        parser.add_argument('--deviation', type = float, default = cls._default_deviation_hz, help = 'Deviation (Hz) [default=%(default)r]')

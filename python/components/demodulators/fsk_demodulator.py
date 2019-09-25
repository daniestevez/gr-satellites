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

from gnuradio import gr, digital, filter
from gnuradio.filter import firdes
from math import ceil

class fsk_demodulator(gr.hier_block2):
    """
    Hierarchical block to demodulate FSK.

    TODO: describe input

    Args:
        baudrate: Baudrate in symbols per second (float)
        sample_rate: Sample rate in samples per second (float)
    """
    def __init__(self, baudrate, samp_rate):
        gr.hier_block2.__init__(self, "fsk_demodulator",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(1, 1, gr.sizeof_float))
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

        gain_mu = 0.5
        gain_omega = 0.25 * gain_mu * gain_mu
        mu = 0.5
        omega_relative_limit = 200e-6
        self.clock_recovery = digital.clock_recovery_mm_ff(sps, gain_omega, mu, gain_mu, omega_relative_limit)

        self.connect(self, self.lowpass, self.clock_recovery, self)

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

from gnuradio import gr, analog, blocks, digital, filter
from gnuradio.filter import firdes
from math import ceil, pi
from ...hier.rms_agc import rms_agc
from ...utils.options_block import options_block
from ... import manchester_sync

class bpsk_demodulator(gr.hier_block2, options_block):
    """
    Hierarchical block to demodulate BPSK.

    The input can be either IQ or real.

    Args:
        baudrate: Baudrate in symbols per second (float)
        sample_rate: Sample rate in samples per second (float)
        iq: Whether the input is IQ or real (bool)
        f_offset: Frequency offset in Hz (float)
        differential: Perform non-coherent DBPSK decoding (bool)
        manchester: Use Manchester coding (bool)
        options: Options from argparse
    """
    def __init__(self, baudrate, samp_rate, iq, f_offset = None, differential = False, manchester = False, options = None):
        gr.hier_block2.__init__(self, "bpsk_demodulator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex if iq else gr.sizeof_float),
            gr.io_signature(1, 1, gr.sizeof_float))
        options_block.__init__(self, options)

        if manchester:
            baudrate *= 2
        sps = samp_rate / baudrate
        max_sps = 10
        if sps > max_sps:
            decimation = ceil(sps / max_sps)
        else:
            decimation = 1
        sps /= decimation

        filter_cutoff = baudrate * 2.0
        filter_transition = baudrate * 0.2

        if f_offset is None:
            f_offset = self.options.f_offset
        if f_offset is None:
            if iq:
                f_offset = 0
            elif baudrate <= 2400:
                f_offset = 1500
            else:
                f_offset = 12000

        taps = firdes.low_pass(1, samp_rate, filter_cutoff, filter_transition)
        f = filter.freq_xlating_fir_filter_ccf if iq else filter.freq_xlating_fir_filter_fcf
        self.xlating = f(decimation, taps, f_offset, samp_rate)

        agc_ref = 0.5
        self.agc = rms_agc(1e-2, agc_ref)

        fll_bw = 2*pi*decimation/samp_rate*self.options.fll_bw
        self.fll = digital.fll_band_edge_cc(sps, self.options.rrc_alpha, 100, fll_bw)

        filter_cutoff2 = baudrate * 1.0
        filter_transition2 = baudrate * 0.1
        taps2 = firdes.low_pass(1, samp_rate/decimation, filter_cutoff2, filter_transition2)
        self.lowpass = filter.fir_filter_ccf(1, taps2)
        
        nfilts = 16
        rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), self.options.rrc_alpha, int(ceil(11*sps*nfilts)))
        clk_bw = 2*pi/sps*self.options.clk_bw
        self.clock_recovery = digital.pfb_clock_sync_ccf(sps, clk_bw, rrc_taps, nfilts, nfilts//2, self.options.clk_limit, 1)

        self.connect(self, self.xlating, self.agc, self.fll, self.lowpass, self.clock_recovery)

        self.complex_to_real = blocks.complex_to_real(1)

        if manchester:
            self.manchester = manchester_sync(self.options.manchester_history)
            self.connect(self.clock_recovery, self.manchester)
        else:
            self.manchester = self.clock_recovery
                
        if differential:
            self.delay = blocks.delay(gr.sizeof_gr_complex, 1)
            self.multiply_conj = blocks.multiply_conjugate_cc(1)
            sign = -1 if manchester else 1
            self.multiply_const = blocks.multiply_const_ff(sign/agc_ref**2, 1) # take care about inverion in Manchester
            self.connect(self.manchester, (self.multiply_conj, 0))
            self.connect(self.manchester, self.delay, (self.multiply_conj, 1))
            self.connect(self.multiply_conj, self.complex_to_real, self.multiply_const, self)
        else:
            costas_bw = 2*pi/baudrate*self.options.costas_bw
            self.costas = digital.costas_loop_cc(costas_bw, 2, False)
            self.multiply_const = blocks.multiply_const_ff(1/agc_ref, 1)
            self.connect(self.manchester, self.costas, self.complex_to_real, self.multiply_const, self)

    _default_rrc_alpha = 0.35
    _default_fll_bw = 100
    _default_clk_rel_bw = 0.1
    _default_clk_limit = 0.01
    _default_costas_bw = 150
    _default_manchester_history = 32
    
    @classmethod
    def add_options(cls, parser):
        """
        Adds BPSK demodulator specific options to the argparse parser
        """
        parser.add_argument('--f_offset', type = float, default = None, help = 'Frequency offset (Hz) [default=1500 or 12000]')
        parser.add_argument('--rrc_alpha', type = float, default = cls._default_rrc_alpha, help = 'RRC roll-off (Hz) [default=%(default)r]')
        parser.add_argument('--fll_bw', type = float, default = cls._default_fll_bw, help = 'FLL bandwidth (Hz) [default=%(default)r]')
        parser.add_argument('--clk_bw', type = float, default = cls._default_clk_rel_bw, help = 'Clock recovery bandwidth (relative to baudrate) [default=%(default)r]')
        parser.add_argument('--clk_limit', type = float, default = cls._default_clk_limit, help = 'Clock recovery limit (relative to baudrate) [default=%(default)r]')
        parser.add_argument('--costas_bw', type = float, default = cls._default_costas_bw, help = 'Costas loop bandwidth (Hz) [default=%(default)r]')
        parser.add_argument('--manchester_history', type = int, default = cls._default_manchester_history, help = 'Manchester recovery history (symbols) [default=%(default)r]')

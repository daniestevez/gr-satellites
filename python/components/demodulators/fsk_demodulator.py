#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, analog, digital, filter
from gnuradio.filter import firdes
import numpy as np

from math import ceil, pi
import pathlib
import sys

from ...hier.rms_agc_f import rms_agc_f
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
        deviation: Deviation in Hz, negative inverts sidebands (float)
        subaudio: Use subaudio demodulation (bool)
        dc_block: Use DC-block (bool)
        dump_path: Path to dump internal signals to files (str)
        options: Options from argparse
    """
    def __init__(self, baudrate, samp_rate, iq, deviation = None, subaudio = False,
                     dc_block = True,
                     dump_path = None, options = None):
        gr.hier_block2.__init__(self, "fsk_demodulator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex if iq else gr.sizeof_float),
            gr.io_signature(1, 1, gr.sizeof_float))
        options_block.__init__(self, options)

        use_agc = self.options.use_agc or not iq
        if self.options.disable_dc_block:
            dc_block = False

        if dump_path is not None:
            dump_path = pathlib.Path(dump_path)
        
        if deviation is not None:
            _deviation = deviation
        else:
            _deviation = self.options.deviation

        # prevent problems due to baudrate too high
        if baudrate >= samp_rate:
            print(f'Sample rate {samp_rate} sps insufficient for {baudrate} baud FSK demodulation. Demodulator will not work.',
                      file = sys.stderr)
            baudrate = samp_rate / 2
        
        if iq:
            # Cut to Carson's bandwidth rule before quadrature demod.
            # Note that _deviation can be negative to encode that the
            # low tone corresponds to the symbol 1 and the high tone
            # corresponds to the symbol 0.
            carson_cutoff = abs(_deviation) + baudrate / 2
            fir_taps = firdes.low_pass(1, samp_rate, carson_cutoff, 0.1 * carson_cutoff)
            self.demod_filter = filter.fir_filter_ccf(1, fir_taps)
            self.demod = analog.quadrature_demod_cf(samp_rate/(2*pi*_deviation))
            self.connect(self, self.demod_filter, self.demod)
        else:
            self.demod = self
        
        sps = samp_rate / baudrate
        max_sps = 10
        if sps > max_sps:
            decimation = ceil(sps / max_sps)
        else:
            decimation = 1
        sps /= decimation

        if subaudio:
            # some not-so-bad filter parameters for subaudio processing
            subaudio_cutoff = 2.0/3.0 * baudrate
            subaudio_transition = subaudio_cutoff / 4.0
            subaudio_taps = firdes.low_pass(1, samp_rate, subaudio_cutoff, subaudio_transition)
            self.subaudio_lowpass = filter.fir_filter_fff(1, subaudio_taps)
        
        # square pulse filter
        sqfilter_len = int(samp_rate / baudrate)
        taps = np.ones(sqfilter_len)/sqfilter_len
        self.lowpass = filter.fir_filter_fff(decimation, taps)

        if dc_block:
            self.dcblock = filter.dc_blocker_ff(ceil(sps * 32), True)
        else:
            self.dcblock = self.lowpass # to simplify connections below

        if use_agc:
            agc_constant = 2e-2 / sps # This gives a time constant of 50 symbols
            self.agc = rms_agc_f(agc_constant, 1)

        if dump_path is not None:
            self.waveform = blocks.file_sink(gr.sizeof_float, str(dump_path / 'waveform.f32'))

        ted_gain = 1.47 # "empiric" formula for TED gain of Gardner detector 1.47 symbol^{-1}
        damping = 1.0
        self.clock_recovery = digital.symbol_sync_ff(digital.TED_GARDNER,
                                                     sps,
                                                     self.options.clk_bw,
                                                     damping,
                                                     ted_gain,
                                                     self.options.clk_limit * sps,
                                                     1,
                                                     digital.constellation_bpsk().base(),
                                                     digital.IR_PFB_NO_MF)

        if dump_path is not None:
            self.clock_recovery_out = blocks.file_sink(gr.sizeof_float, str(dump_path / 'clock_recovery_out.f32'), False)
            self.clock_recovery_err = blocks.file_sink(gr.sizeof_float, str(dump_path / 'clock_recovery_err.f32'), False)
            self.clock_recovery_T_inst = blocks.file_sink(gr.sizeof_float, str(dump_path / 'clock_recovery_T_inst.f32'), False)
            self.clock_recovery_T_avg = blocks.file_sink(gr.sizeof_float, str(dump_path / 'clock_recovery_T_avg.f32'), False)
            self.connect(self.clock_recovery, self.clock_recovery_out)
            self.connect((self.clock_recovery, 1), self.clock_recovery_err)
            self.connect((self.clock_recovery, 2), self.clock_recovery_T_inst)
            self.connect((self.clock_recovery, 3), self.clock_recovery_T_avg)

        conns = [self.demod]
        if subaudio:
            conns.append(self.subaudio_lowpass)
        conns.append(self.lowpass)
        if dc_block:
            conns.append(self.dcblock)
        self.connect(*conns)
        if use_agc:
            self.connect(self.dcblock, self.agc, self.clock_recovery)
            if dump_path is not None:
                self.connect(self.agc, self.waveform)            
        else:
            self.connect(self.dcblock, self.clock_recovery)
            if dump_path is not None:
                self.connect(self.dcblock, self.waveform)
        self.connect(self.clock_recovery, self)

    _default_clk_rel_bw = 0.06
    _default_clk_limit = 0.004
    _default_deviation_hz = 5000
    
    @classmethod
    def add_options(cls, parser):
        """
        Adds FSK demodulator specific options to the argparse parser
        """
        parser.add_argument('--clk_bw', type = float, default = cls._default_clk_rel_bw, help = 'Clock recovery bandwidth (relative to baudrate) [default=%(default)r]')
        parser.add_argument('--clk_limit', type = float, default = cls._default_clk_limit, help = 'Clock recovery limit (relative to baudrate) [default=%(default)r]')
        parser.add_argument('--deviation', type = float, default = cls._default_deviation_hz, help = 'Deviation (Hz) [default=%(default)r]')
        parser.add_argument('--use_agc', action = 'store_true', help = 'Use AGC (for IQ input. AGC always on for real input)')
        parser.add_argument('--disable_dc_block', action = 'store_true', help = 'Disable DC block')

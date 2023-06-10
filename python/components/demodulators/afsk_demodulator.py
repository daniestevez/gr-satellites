#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, filter, analog
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
        dump_path: Path to dump internal signals to files (str)
        options: Options from argparse
    """
    def __init__(self, baudrate, samp_rate, iq, af_carrier,
                 deviation, dump_path=None, options=None):
        gr.hier_block2.__init__(
            self,
            'afsk_demodulator',
            gr.io_signature(1, 1,
                            gr.sizeof_gr_complex if iq else gr.sizeof_float),
            gr.io_signature(1, 1, gr.sizeof_float))
        options_block.__init__(self, options)

        if iq:
            # Cut to Carson's bandwidth rule before quadrature demod.
            # Assume that the FM modulator used a deviation of 3 kHz,
            # which is typical.
            fm_deviation = 3000
            # Note that deviation can be negative to encode that the
            # low tone corresponds to the symbol 1 and the high tone
            # corresponds to the symbol 0.
            carson_cutoff = fm_deviation + af_carrier + abs(deviation)
            self.demod = analog.quadrature_demod_cf(1)
            if carson_cutoff >= samp_rate / 2:
                # Sample rate is already narrower than Carson's
                # bandwidth. Do not filter
                self.connect(self, self.demod)
            else:
                # Sample rate is wider than Carson's bandwidth.
                # Lowpass filter before demod.
                fir_taps = firdes.low_pass(
                    1, samp_rate, carson_cutoff, 0.1 * carson_cutoff)
                self.demod_filter = filter.fir_filter_ccf(1, fir_taps)
                self.connect(self, self.demod_filter, self.demod)
        else:
            self.demod = self

        filter_cutoff = 2 * abs(deviation)
        filter_transition = 0.1 * abs(deviation)
        taps = firdes.low_pass(1, samp_rate, filter_cutoff, filter_transition)
        self.xlating = filter.freq_xlating_fir_filter_fcf(
            1, taps, af_carrier, samp_rate)

        self.fsk = fsk_demodulator(
            baudrate, samp_rate, deviation=deviation, iq=True,
            dc_block=False, dump_path=dump_path, options=options)

        self.connect(self.demod, self.xlating, self.fsk, self)

    @classmethod
    def add_options(cls, parser):
        """Adds CCSDS concatenated deframer options to the argparse parser"""
        fsk_demodulator.add_options(parser)

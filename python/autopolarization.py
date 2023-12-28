#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020-2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr


class autopolarization(gr.sync_block):
    def __init__(self, fft_size=2048, fft_avg=1, iir_weight=0.1):
        gr.sync_block.__init__(
            self,
            name='autopolarization',
            in_sig=[np.complex64]*2,
            out_sig=[np.complex64]*2
        )
        self.fft_size = fft_size
        self.fft_avg = fft_avg
        self.set_output_multiple(fft_size * fft_avg)
        self.iir_weight = iir_weight
        self.noise_ampl = np.ones(2)
        self.sig_ampl = np.ones(2)
        self.phase = 0

    def work(self, input_items, output_items):
        x = np.array([inp.reshape((-1, self.fft_avg, self.fft_size))
                      for inp in input_items])
        # axes for x are:
        # (channel: 2, block, fft_num: fft_avg, fft_bin: fft_size)

        fx = np.fft.fft(x)
        fx_sq_avg = np.average(np.abs(fx)**2, axis=2)
        noise_ampl = np.sqrt(np.median(fx_sq_avg, axis=2))

        fx_sq_avg_ch_max = np.max(fx_sq_avg/noise_ampl[..., np.newaxis]**2,
                                  axis=0)
        peak_idx = np.argmax(fx_sq_avg_ch_max, axis=1)

        f_cross = np.average(fx[0] * np.conjugate(fx[1]), axis=1)
        phase = np.angle(f_cross[np.arange(f_cross.shape[0]),
                                 peak_idx])
        # technically this should have - noise_ampl
        sig_ampl = fx_sq_avg[:, np.arange(fx_sq_avg.shape[1]), peak_idx]
        sig_ampl = np.sqrt(np.clip(sig_ampl, 0, np.inf))

        # update IIR filters
        for j in range(x.shape[1]):
            noise_ampl[:, j] = (1-self.iir_weight)*self.noise_ampl \
                + self.iir_weight*noise_ampl[:, j]
            self.noise_ampl = noise_ampl[:, j]
            sig_ampl[:, j] = (1-self.iir_weight)*self.sig_ampl \
                + self.iir_weight*sig_ampl[:, j]
            self.sig_ampl = sig_ampl[:, j]
            phase_diff = phase[j] - self.phase
            phase_diff = (phase_diff + np.pi) % (2*np.pi) - np.pi
            phase[j] = self.phase + self.iir_weight*phase_diff
            self.phase = (phase[j] + np.pi) % (2*np.pi) - np.pi

        tau = np.log10(sig_ampl[0]/noise_ampl[0]+1e-6) \
            - np.log10(sig_ampl[1]/noise_ampl[1]+1e-6)
        tau = 20*tau/6*0.5 + 0.5
        tau = np.clip(tau, 0, 1)
        # note tau = 1 if sig[0] is 6dB stronger than sig[1] and
        # tau = 0 if sig[0] is 6dB weaker than sig[1]
        a_phase = (tau - 1) * phase
        b_phase = tau * phase
        # note -a_phase + b_phase = phase

        alpha = (np.exp(1j*a_phase)
                 * sig_ampl[0] / noise_ampl[0])[:, np.newaxis]
        beta = (np.exp(1j*b_phase)
                * sig_ampl[1] / noise_ampl[1])[:, np.newaxis]

        y = x.reshape((x.shape[0], x.shape[1], self.fft_avg * self.fft_size))
        y = y / noise_ampl[..., np.newaxis] * np.sqrt(self.fft_size)
        output_items[0][:] = (alpha * y[0] + beta * y[1]).ravel()
        output_items[1][:] = (
            np.conjugate(beta) * y[0] - np.conjugate(alpha) * y[1]).ravel()
        return len(output_items[0])

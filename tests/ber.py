#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Daniel Estevez <daniel@destevez.net>.
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

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import scipy.special
from gnuradio import gr, digital, analog, blocks, fft, channels
from gnuradio.fft import window
from satellites.components.demodulators import bpsk_demodulator, fsk_demodulator

RAND_SEED = 42

class BERSim(gr.top_block):
    def __init__(self, ber_block, ncorrelations, lfsr_bits = 16):
        gr.top_block.__init__(self)

        prn_len = 2**lfsr_bits
        prn = np.concatenate((scipy.signal.max_len_seq(lfsr_bits)[0], [1]))
        prn_fft_conj = np.conjugate(np.fft.fft(2*prn-1))

        self.source = blocks.vector_source_b(prn, True, 1, [])
        
        self.ber_block = ber_block
        
        self.char2float = blocks.char_to_float(1, 0.5)
        self.add_const = blocks.add_const_ff(-1.0)
        self.source_vector = blocks.stream_to_vector(gr.sizeof_float, prn_len)

        self.fft = fft.fft_vfc(prn_len, True, window.rectangular(prn_len), 1)
        self.prn_fft_source = blocks.vector_source_c(prn_fft_conj, True, prn_len, [])
        self.multiply_ffts = blocks.multiply_vcc(prn_len)
        self.ifft = fft.fft_vcc(prn_len, False, np.ones(prn_len)/prn_len**2, False, 1)
        self.corr_mag = blocks.complex_to_mag(prn_len)
        self.max_corr = blocks.max_ff(prn_len, 1)
        self.multiply_const = blocks.multiply_const_ff(-0.5)
        self.add_const2 = blocks.add_const_ff(0.5)
        
        self.head = blocks.head(gr.sizeof_float, ncorrelations)
        self.sink = blocks.vector_sink_f()

        self.connect(self.source, self.ber_block, self.char2float, self.add_const,
                         self.source_vector, self.fft, (self.multiply_ffts,0),
                         self.ifft, self.corr_mag, self.max_corr, self.multiply_const,
                         self.add_const2, self.head, self.sink)
        self.connect(self.prn_fft_source, (self.multiply_ffts,1))

class BPSK(gr.hier_block2):
    def __init__(self, ebn0, nbits):
        gr.hier_block2.__init__(self, 'BPSK',
            gr.io_signature(1, 1, gr.sizeof_char),
            gr.io_signature(1, 1, gr.sizeof_char))

        samp_rate = 48e3
        sps = 5
        self.head = blocks.head(gr.sizeof_char, nbits)
        self.pack = blocks.pack_k_bits_bb(8)
        self.bpsk_constellation = digital.constellation_bpsk().base()
        self.modulator = digital.generic_mod(
            constellation = self.bpsk_constellation,
            differential = False,
            samples_per_symbol = sps,
            pre_diff_code = True,
            excess_bw = 0.35,
            verbose = False,
            log = False)
        
        spb = sps
        self.channel = channels.channel_model(np.sqrt(spb)/10**(ebn0/20), 0, 1.0, [1], RAND_SEED, False)

        self.demod = bpsk_demodulator(samp_rate/sps, samp_rate, iq = True)
        self.slice = digital.binary_slicer_fb()

        self.connect(self, self.head, self.pack, self.modulator, self.channel,
                         self.demod, self.slice, self)

class FSK(gr.hier_block2):
    def __init__(self, ebn0, nbits):
        gr.hier_block2.__init__(self, 'FSK',
            gr.io_signature(1, 1, gr.sizeof_char),
            gr.io_signature(1, 1, gr.sizeof_char))

        samp_rate = 48e3
        sps = 5
        deviation = 5000
        bt = 1.0
        self.head = blocks.head(gr.sizeof_char, nbits)
        self.pack = blocks.pack_k_bits_bb(8)
        self.modulator = digital.gfsk_mod(
            samples_per_symbol = sps,
            sensitivity = 2*np.pi*deviation/samp_rate,
            bt = bt,
            verbose = False,
            log = False)
        
        spb = sps
        self.channel = channels.channel_model(np.sqrt(spb)/10**(ebn0/20), 0, 1.0, [1], RAND_SEED, False)

        self.demod = fsk_demodulator(samp_rate/sps, samp_rate, deviation = deviation, iq = True)
        self.slice = digital.binary_slicer_fb()

        self.connect(self, self.head, self.pack, self.modulator, self.channel,
                         self.demod, self.slice, self)

def compute_ber(ber_block_class, ebn0, drop_correlations = 2):
    ncorrelations = 100
    nbits = int(ncorrelations * 2**16 * 1.1) # 1.1 to add a bit of margin
    fg = BERSim(ber_block_class(ebn0, nbits), ncorrelations)
    print(f'Computing BPSK BER for EbN0 = {ebn0:.01f} dB')
    fg.run()
    return np.average(fg.sink.data()[drop_correlations:])

def ber_bpsk_awgn(ebn0):
    """Calculates theoretical bit error rate in AWGN (for BPSK and given Eb/N0)"""
    return 0.5 * scipy.special.erfc(10**(ebn0/20))

def ber_fsk_awgn(ebn0):
    """Calculates theoretical bit error rate in AWGN (for FPSK and given Eb/N0)"""
    return 0.5 * np.exp(-0.5*10**(ebn0/10))

if __name__ == '__main__':
    print('Computing BPSK BER')
    ebn0s = np.arange(-2, 10.5, 0.5)
    bers = [compute_ber(BPSK, ebn0) for ebn0 in ebn0s]
    bers_theory = [ber_bpsk_awgn(ebn0) for ebn0 in ebn0s]

    fig, ax = plt.subplots()
    ax.semilogy(ebn0s, bers_theory, '.-', label = 'Theoretical BPSK BER')
    ax.semilogy(ebn0s, bers, '.-', label = 'gr-satellites demodulator')
    ax.set_title('BPSK BER')
    ax.set_xlabel('Eb/N0 (dB)')
    ax.set_ylabel('BER')
    ax.legend()
    ax.grid()
    fig.savefig('ber_bpsk.png')
    print('Saved output to ber_bpsk.png')
    
    print('Computing FSK BER')
    ebn0s = np.arange(-2, 17.5, 0.5)
    bers = [compute_ber(FSK, ebn0) for ebn0 in ebn0s]
    bers_theory = [ber_fsk_awgn(ebn0) for ebn0 in ebn0s]

    fig, ax = plt.subplots()
    ax.semilogy(ebn0s, bers_theory, '.-', label = 'Theoretical non-coherent FSK BER')
    ax.semilogy(ebn0s, bers, '.-', label = 'gr-satellites demodulator')
    ax.set_title('FSK BER deviation 5kHz, GFSK BT = 1')
    ax.set_xlabel('Eb/N0 (dB)')
    ax.set_ylabel('BER')
    ax.legend()
    ax.grid()
    fig.savefig('ber_fsk.png')
    print('Saved output to ber_fsk.png')

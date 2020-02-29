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
from gnuradio import gr, digital, blocks, channels, analog
from satellites.components.demodulators import bpsk_demodulator, fsk_demodulator

RAND_SEED = 42

samp_rate = 48e3
sps = 5

class LockInSim(gr.top_block):
    def __init__(self, lockin_block, time):
        gr.top_block.__init__(self)

        nbits = int(time * samp_rate / sps)
        self.source = blocks.vector_source_b(list(map(int, np.random.randint(0, 2, nbits))), False)
        
        self.lockin_block = lockin_block
        self.sink = blocks.null_sink(gr.sizeof_float)

        self.connect(self.source, self.lockin_block, self.sink)

class BPSK(gr.hier_block2):
    def __init__(self, ebn0):
        gr.hier_block2.__init__(self, 'BPSK',
            gr.io_signature(1, 1, gr.sizeof_char),
            gr.io_signature(1, 1, gr.sizeof_float))

        f_offset = 50
        packet_length = 0.2
        
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

        self.packet_tx = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE, 1/packet_length,
                                            1, 0, 0)
        self.packet_tx_c = blocks.float_to_complex(1)
        self.tx = blocks.multiply_vcc(1)
        
        spb = sps
        self.channel = channels.channel_model(np.sqrt(spb)/10**(ebn0/20), f_offset/samp_rate, 1.0, [0,0,1], RAND_SEED, False)

        self.demod = bpsk_demodulator(samp_rate/sps, samp_rate, iq = True, dump_path = '/tmp/lockin_bpsk')

        self.connect(self, self.pack, self.modulator, self.tx, self.channel, self.demod, self)
        self.connect(self.packet_tx, self.packet_tx_c, (self.tx, 1))

class FSK(gr.hier_block2):
    def __init__(self, ebn0):
        gr.hier_block2.__init__(self, 'FSK',
            gr.io_signature(1, 1, gr.sizeof_char),
            gr.io_signature(1, 1, gr.sizeof_float))

        f_offset = 500
        packet_length = 0.2

        deviation = 5000
        bt = 1
        self.pack = blocks.pack_k_bits_bb(8)
        self.modulator = digital.gfsk_mod(
            samples_per_symbol = sps,
            sensitivity = 2*np.pi*deviation/samp_rate,
            bt = bt,
            verbose = False,
            log = False)

        self.packet_tx = analog.sig_source_f(samp_rate, analog.GR_SQR_WAVE, 1/packet_length,
                                            1, 0, 0)
        self.packet_tx_c = blocks.float_to_complex(1)
        self.tx = blocks.multiply_vcc(1)
        
        spb = sps
        self.channel = channels.channel_model(np.sqrt(spb)/10**(ebn0/20), f_offset/samp_rate, 1.0, [0,0,1], RAND_SEED, False)

        self.demod = fsk_demodulator(samp_rate/sps, samp_rate, deviation = deviation, iq = True, dump_path = '/tmp/lockin_fsk')

        self.connect(self, self.pack, self.modulator, self.tx, self.channel, self.demod, self)
        self.connect(self.packet_tx, self.packet_tx_c, (self.tx, 1))

if __name__ == '__main__':
    fg = LockInSim(BPSK(10), 1)
    fg.run()
    fg = LockInSim(FSK(15), 1)
    fg.run()

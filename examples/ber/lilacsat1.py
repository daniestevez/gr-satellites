#!/usr/bin/env python2
#
# Copyright 2012,2013 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import math
import numpy
from gnuradio import gr, digital
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import channels
from gnuradio import fec
import sys

try:
    from scipy.special import erfc
except ImportError:
    print "Error: could not import scipy (http://www.scipy.org/)"
    sys.exit(1)

try:
    import pylab
except ImportError:
    print "Error: could not import pylab (http://matplotlib.sourceforge.net/)"
    sys.exit(1)

from lilacsat1_ber_bpsk import *
from lilacsat1_ber_viterbi import *
    
# Best to choose powers of 10
N_BITS = 1e8
SKIP = 1000
RAND_SEED = 42

def berawgn(EbN0):
    """ Calculates theoretical bit error rate in AWGN (for BPSK and given Eb/N0) """
    return 0.5 * erfc(math.sqrt(10**(float(EbN0)/10)))

class BitErrors(gr.hier_block2):
    """test"""
    def __init__(self):
        gr.hier_block2.__init__(self, "BitErrors",
                gr.io_signature(1, 1, gr.sizeof_char),
                gr.io_signature(1, 1, gr.sizeof_int))

        intdump_decim = min(int(N_BITS/10), 100000)
        self.connect(self,
                     blocks.skiphead(gr.sizeof_char, SKIP),
                     blocks.not_bb(),
                     blocks.and_const_bb(1),
                     blocks.uchar_to_float(),
                     blocks.integrate_ff(intdump_decim),
                     blocks.multiply_const_ff(1.0/intdump_decim),
                     self)

class BERAWGNSimu(gr.top_block):
    " This contains the simulation flow graph "
    def __init__(self, EbN0, viterbi=False):
        gr.top_block.__init__(self)

        self.sps = 5
        alpha = 0.35

        const = digital.constellation_bpsk().base()
        modulator = digital.generic_mod(
          constellation=const,
          differential=False,
          samples_per_symbol=self.sps,
          pre_diff_code=True,
          excess_bw=alpha,
          verbose=False,
          log=False,
          )
        channel = channels.channel_model(
        	noise_voltage=self.EbN0_to_noise_voltage(EbN0, viterbi),
        	frequency_offset=0,
        	epsilon=1.0,
        	taps=(0, 0, (1+1j)/numpy.sqrt(2), ),
        	noise_seed=RAND_SEED,
        	block_tags=False
        )
        self.sink  = blocks.vector_sink_f()
        biterrors = BitErrors()

        dut = lilacsat1_ber_viterbi() if viterbi else lilacsat1_ber_bpsk()

        pack = blocks.pack_k_bits_bb(8)
        descrambler = digital.descrambler_bb(0x21, 0x00, 16)
        self.connect(blocks.vector_source_b([1], repeat=True),
                     blocks.head(gr.sizeof_char, int(N_BITS)),
                     digital.scrambler_bb(0x21, 0x00, 16),
                     digital.diff_encoder_bb(2),
                     pack)
        self.connect(modulator, channel,
                     blocks.multiply_const_cc(0.1), # we set some amplitude to test the agc # signal amplitude 1 seems very important
                     dut,
                     digital.diff_decoder_bb(2),
                     descrambler)
        self.connect(biterrors, self.sink)
        
        if viterbi:
            deinterleave_viterbi = blocks.deinterleave(gr.sizeof_char)
            interleave_viterbi = blocks.interleave(gr.sizeof_char)
            self.connect(pack,
                         fec.encode_ccsds_27_bb(),
                         deinterleave_viterbi)
            self.connect((deinterleave_viterbi, 0),
                         (interleave_viterbi, 1))
            self.connect((deinterleave_viterbi, 1),
                         blocks.not_bb(),
                         blocks.and_const_bb(1),
                         (interleave_viterbi, 0))
            self.connect(interleave_viterbi,
                         blocks.pack_k_bits_bb(8),
                         modulator)
            descrambler2 = digital.descrambler_bb(0x21, 0x00, 16)
            self.connect((dut, 1),
                        digital.diff_decoder_bb(2),
                        descrambler2)
            or2 = blocks.or_bb()
            self.connect(descrambler, or2)
            self.connect(descrambler2, (or2, 1))
            self.connect(or2, biterrors)
            #self.sinkviterbi1 = blocks.vector_sink_b()
            #self.sinkviterbi2 = blocks.vector_sink_b()
            #self.connect(descrambler, self.sinkviterbi1)
            #self.connect(descrambler2, self.sinkviterbi2)

        else:
            self.connect(pack, modulator)
            self.connect(descrambler, biterrors)            

    def EbN0_to_noise_voltage(self, EbN0, viterbi):
        """ Converts Eb/N0 to a complex noise voltage (assuming unit symbol power) """
        spb = float(self.sps)*2.0 if viterbi else float(self.sps) # samples per bit
        return 1.0 / math.sqrt(1/spb * 10**(float(EbN0)/10))

def simulate_ber(EbN0, viterbi = False):
    """ All the work's done here: create flow graph, run, read out BER """
    print "Eb/N0 = %d dB" % EbN0
    fg = BERAWGNSimu(EbN0, viterbi)
    fg.run()
    data = fg.sink.data()
    factor = 3.0 if viterbi else 6.0 # each bit error produces 6 errors, taking into account differential coding and scrambler
    return numpy.sum(data)/(factor*len(data))

if __name__ == "__main__":
    EbN0_min = 0
    EbN0_max = 12
    EbN0_range = range(EbN0_min, EbN0_max+1)
    ber_theory = [berawgn(x)      for x in EbN0_range]
    print "Simulating uncoded BPSK..."
    ber_simu_bpsk   = [simulate_ber(x, False) for x in EbN0_range]
    print "Simulating Viterbi..."
    ber_simu_viterbi   = [simulate_ber(x, True) for x in EbN0_range]

    f = pylab.figure()
    s = f.add_subplot(1,1,1)
    s.semilogy(EbN0_range, ber_theory, 'g-.', label="Theoretical uncoded BPSK")
    s.semilogy(EbN0_range, ber_simu_bpsk, 'b-o', label="Simulated uncoded BPSK")
    s.semilogy(EbN0_range, ber_simu_viterbi, 'r-o', label="Simulated Viterbi")
    s.set_title('BER Simulation')
    s.set_xlabel('Eb/N0 (dB)')
    s.set_ylabel('BER')
    s.legend()
    s.grid()
    pylab.show()

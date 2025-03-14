#!/usr/bin/env python3
# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gnuradio import gr
import numpy
import pmt


# Based on the Mobitex Coding library
# https://git.tu-berlin.de/rft/com/mobitub-2/-/blob/master/gr-tnc_nx/lib/mobitex_coding.cc
class Scrambler:
    seed = 0b1_1111_1111

    def __init__(self):
        self.reset_scrambler()

    def reset_scrambler(self):
        self.register = self.seed
        self.bytes_idx = 0

    def scramble(self, bit):
        # XOR input with LFSR output
        bit ^= self.register & 1

        # Calculate feedback using parity of bits 0 and 4
        if ((self.register & 1) ^ ((self.register >> 4) & 1)):
            self.register |= 0b10_0000_0000

        # Shift register and insert feedback at MSB
        self.register = ((self.register >> 1) & 0b1_1111_1111)

        return bit


class mobitex_scrambler_bb(gr.sync_block):
    """
    Mobitex scrambler block

    Input is stream of bits,
    Output is stream of bits.
    """
    scrambler = Scrambler()

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='mobitex_scrambler_bb',
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8],
        )

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        # get all tags within the window of input_items[0]
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))

        offsets = []
        for tag in tagTuple:
            if pmt.to_python(tag.key) == 'frame_header':
                # Store relative offset
                offsets.append(tag.offset - self.nitems_read(0))

        for i in range(len(in0)):
            if i in offsets:
                self.scrambler.reset_scrambler()
            bit = in0[i]
            out[i] = self.scrambler.scramble(bit)

        return len(out)

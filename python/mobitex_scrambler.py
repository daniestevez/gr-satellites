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
    seed = 0x01FF

    def __init__(self):
        self.reset_scrambler()

    def reset_scrambler(self):
        self.scramble_shift_reg = self.seed
        self.bytes_idx = 0

    def scramble(self, bit):
        # register-bit 9th stage is "1"
        if self.scramble_shift_reg & 0x0001:
            bit ^= 1

        # Check 5th and 9th Stage of
        if (
            ((self.scramble_shift_reg & 0x0011) == 0x0010) or
            ((self.scramble_shift_reg & 0x0011) == 0x0001)
        ):
            self.scramble_shift_reg |= 0x0200

        self.scramble_shift_reg = (self.scramble_shift_reg >> 1) & 0x01FF

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

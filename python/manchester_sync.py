#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import collections

import numpy as np
from gnuradio import gr


def branch_weight(x):
    return -np.sum(np.real(x[::2] * np.conjugate(x[1::2])))


class manchester_sync(gr.decim_block):
    """
    Synchronize to a Manchester-coded signal and output symbols

    The input to this block is a BPSK Manchester-coded signal at
    2 samples per symbol. The block finds the Manchester clock phase,
    wipes the Manchester clock and outputs the symbols at 1 samples per
    symbol.

    Args:
        history: The number of bits to look back to find the clock phase
    """
    def __init__(self, history):
        gr.decim_block.__init__(
            self,
            name='manchester_sync',
            in_sig=[np.complex64],
            out_sig=[np.complex64],
            decim=2)
        size = 2 * (history + 1)
        self.samples = collections.deque(np.zeros(size, dtype=np.complex64),
                                         maxlen=size)

    def work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        for i, x in enumerate(zip(inp[::2], inp[1::2])):
            self.samples.extend(x)
            z = np.array(self.samples, dtype=np.complex64)
            b0 = branch_weight(z[2:])
            b1 = branch_weight(z[1:-1])
            if b0 >= b1:
                output = 0.5*(z[-2] - z[-1])
            else:
                output = 0.5*(z[-3] - z[-2])
            out[i] = output

        return len(out)

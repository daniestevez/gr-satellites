#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr

class nrzi_encode(gr.sync_block):
    """
    docstring for block nrzi_encode
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="nrzi_encode",
            in_sig=[numpy.uint8],
            out_sig=[numpy.uint8])
        self.last = 0

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        for i, x in enumerate(in0):
            out[i] = self.last = ~(x ^ self.last) & 1

        return len(out)


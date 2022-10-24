#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import random

from gnuradio import gr, blocks, gr_unittest
import numpy as np

# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites import phase_unwrap


class qa_phase_unwrap(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_unwrap(self):
        data = np.cumsum(np.concatenate([
            np.full(2000, 0.1),
            np.full(2000, -0.1),
            np.full(3000, 0.25),
            np.full(3000, -0.2),
            ]))
        data_wrap = data % (2 * np.pi)
        # Do some arbitrary additions of multiples of 2 * pi
        data_wrap[::7] -= 2 * np.pi
        data_wrap[2::5] += 4 * np.pi

        self.source = blocks.vector_source_f(data_wrap, False)
        self.sink = blocks.vector_sink_b(12)
        self.unwrap = phase_unwrap()

        self.tb.connect(self.source, self.unwrap, self.sink)
        self.tb.run()

        data_out = np.array(self.sink.data(), 'uint8').reshape(-1, 12)
        int_cycles = data_out[:, :8].ravel().view('int64')
        frac_rad = data_out[:, 8:].ravel().view('float32')
        unwrapped = 2 * np.pi * int_cycles.astype('float') + frac_rad
        np.testing.assert_almost_equal(unwrapped, data, decimal=6)


if __name__ == '__main__':
    gr_unittest.run(qa_phase_unwrap)

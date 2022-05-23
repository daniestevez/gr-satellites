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

from satellites import costas_loop_8apsk_cc


class qa_costas_loop_8apsk_cc(gr_unittest.TestCase):
    # This is inspired by the QA test of the costas loop
    # in gr-digital

    def setUp(self):
        random.seed(0)
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def setup_and_run_fg(self):
        self.source = blocks.vector_source_c(self.data, False)
        self.sink = blocks.vector_sink_c()

        self.tb.connect(self.source, self.costas, self.sink)
        self.tb.run()

    def test_zero_gain(self):
        loop_bw = 0.0
        self.costas = costas_loop_8apsk_cc(loop_bw)
        self.data = 100 * [complex(1, 0), ]
        self.setup_and_run_fg()
        self.assertComplexTuplesAlmostEqual(self.sink.data(), self.data, 5)

    def test_doesnt_diverge(self):
        # Test loop doesn't diverge given perfect data
        loop_bw = 0.1
        self.costas = costas_loop_8apsk_cc(loop_bw)
        self.data = [np.exp(1j * 2 * np.pi * random.randint(0, 7) / 7.0)
                     for _ in range(100)]
        self.setup_and_run_fg()
        self.assertComplexTuplesAlmostEqual(self.sink.data(), self.data, 5)

    def test_convergence(self):
        # Test convergence with a static rotation
        loop_bw = 0.1
        self.costas = costas_loop_8apsk_cc(loop_bw)

        rotation = np.exp(1j * 0.2)
        data = [np.exp(1j * 2 * np.pi * random.randint(0, 7) / 7.0)
                for _ in range(100)]
        self.data = [rotation * d for d in data]
        self.setup_and_run_fg()
        start = 50  # only check after loop has converged
        self.assertComplexTuplesAlmostEqual(
            self.sink.data()[start:], data[start:], 2)


if __name__ == '__main__':
    gr_unittest.run(qa_costas_loop_8apsk_cc)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, gr_unittest
import numpy as np
import pmt

# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites.hier import rms_agc_f


class qa_rms_agc_f(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_zero_input(self):
        """Tests that if the input is zero, the output is also zero.

        In some architectures we have found that the calculations produce nan
        if the number that we put in the denominator to avoid 0/0 is too small.
        """
        n = 256
        source = blocks.vector_source_f([0] * n, False, 1, [])
        sink = blocks.vector_sink_f(1, n)
        agc = rms_agc_f(alpha=1e-2, reference=1.0)
        self.tb.connect(source, agc, sink)

        self.tb.start()
        self.tb.wait()

        expected = np.zeros(n, 'float32')
        np.testing.assert_equal(
            sink.data(), expected, 'AGC output is not zero')


if __name__ == '__main__':
    gr_unittest.run(qa_rms_agc_f)

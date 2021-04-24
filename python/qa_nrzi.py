#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
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

from satellites import nrzi_encode, nrzi_decode


class qa_nrzi(gr_unittest.TestCase):
    def setUp(self):
        test_size = 256
        self.data = np.random.randint(0, 2, test_size, dtype='uint8')
        self.source = blocks.vector_source_b(self.data, False, 1, [])
        self.sink = blocks.vector_sink_b(1, 0)
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None
        del(self.data)
        del(self.source)
        del(self.sink)

    def test_encode(self):
        """Performs NRZI encode and checks the result"""
        encode = nrzi_encode()

        self.tb.connect(self.source, encode, self.sink)
        self.tb.start()
        self.tb.wait()

        expected = np.cumsum((1 ^ self.data) & 1) & 1

        np.testing.assert_equal(
            self.sink.data(), expected,
            'NRZI encode output does not match expected result')

    def test_decode(self):
        """Performs NRZI decode and checks the result"""
        decode = nrzi_decode()

        self.tb.connect(self.source, decode, self.sink)
        self.tb.start()
        self.tb.wait()

        expected = self.data[1:] ^ self.data[:-1] ^ 1

        np.testing.assert_equal(
            self.sink.data()[1:], expected,
            'NRZI decode output does not match expected result')

    def test_encode_decode(self):
        """Performs NRZI encode and decode and checks the result"""
        encode = nrzi_encode()
        decode = nrzi_decode()

        self.tb.connect(self.source, encode, decode, self.sink)
        self.tb.start()
        self.tb.wait()

        np.testing.assert_equal(
            self.sink.data(), self.data,
            'NRZI encoded and decoded output does not match input')


if __name__ == '__main__':
    gr_unittest.run(qa_nrzi)

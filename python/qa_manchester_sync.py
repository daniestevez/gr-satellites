#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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

from satellites import manchester_sync_cc, manchester_sync_ff


class qa_manchester_sync(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_manchester_sync_cc_no_offset(self):
        self.manchester_sync_test('c', False)

    def test_manchester_sync_cc_offset(self):
        self.manchester_sync_test('c', True)

    def test_manchester_sync_ff_no_offset(self):
        self.manchester_sync_test('f', False)

    def test_manchester_sync_ff_offset(self):
        self.manchester_sync_test('f', True)

    def manchester_sync_test(self, type_, offset):
        bits = 2 * np.random.randint(2, size=4096) - 1
        manchester_bits = np.repeat(bits, 2) * np.tile([1, -1], bits.size)
        if offset:
            manchester_bits[:-1] = manchester_bits[1:]

        source_block = {'f': blocks.vector_source_f,
                        'c': blocks.vector_source_c}[type_]
        self.source = source_block(manchester_bits)
        sink_block = {'f': blocks.vector_sink_f,
                      'c': blocks.vector_sink_c}[type_]
        self.sink = sink_block(1, bits.size)
        block_size = 32
        manchester_sync_block = {'f': manchester_sync_ff,
                                 'c': manchester_sync_cc}[type_]
        self.manchester_sync = manchester_sync_block(block_size)

        self.tb.connect(self.source, self.manchester_sync, self.sink)
        self.tb.run()

        sink_data = self.sink.data()
        print(type_, offset)
        if offset:
            np.testing.assert_equal(sink_data[1:], bits[1:])
        else:
            np.testing.assert_equal(sink_data, bits)


if __name__ == '__main__':
    gr_unittest.run(qa_manchester_sync)

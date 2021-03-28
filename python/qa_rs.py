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

from satellites import encode_rs, decode_rs


class qa_rs(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()
        self.dbg = blocks.message_debug()

    def tearDown(self):
        self.tb.msg_connect((self.encode, 'out'), (self.decode, 'in'))
        self.tb.msg_connect((self.decode, 'out'), (self.dbg, 'store'))

        pdu = pmt.cons(pmt.PMT_NIL,
                       pmt.init_u8vector(len(self.data), self.data))
        self.encode.to_basic_block()._post(pmt.intern('in'), pdu)
        self.encode.to_basic_block()._post(
            pmt.intern('system'),
            pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        self.tb.start()
        self.tb.wait()

        result = pmt.u8vector_elements(pmt.cdr(self.dbg.get_message(0)))
        np.testing.assert_equal(self.data, result,
                                'Decoded data does not match encoder input')

        self.tb = None

    def test_conventional(self):
        self.encode = encode_rs(False, 1)
        self.decode = decode_rs(False, 1)
        self.data = np.random.randint(0, 256, 223, dtype='uint8')

    def test_dual(self):
        self.encode = encode_rs(True, 1)
        self.decode = decode_rs(True, 1)
        self.data = np.random.randint(0, 256, 223, dtype='uint8')

    def test_shortened(self):
        self.encode = encode_rs(False, 1)
        self.decode = decode_rs(False, 1)
        self.data = np.random.randint(0, 256, 100, dtype='uint8')

    def test_interleave(self):
        interleave = 5
        self.encode = encode_rs(False, interleave)
        self.decode = decode_rs(False, interleave)
        self.data = np.random.randint(0, 256, 150 * interleave, dtype='uint8')

    def test_custom_rs(self):
        self.encode = encode_rs(8, 0x11d, 1, 1, 16, 1)
        self.decode = decode_rs(8, 0x11d, 1, 1, 16, 1)
        self.data = np.random.randint(0, 256, 255 - 16, dtype='uint8')


if __name__ == '__main__':
    gr_unittest.run(qa_rs)

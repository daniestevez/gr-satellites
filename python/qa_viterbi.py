#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, gr_unittest
import pmt
import numpy as np

# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites import convolutional_encoder, viterbi_decoder

class qa_viterbi(gr_unittest.TestCase):
    def test_viterbi(self):
        tb = gr.top_block()
        dbg = blocks.message_debug()
        k = 5
        p = [25, 23]
        enc = convolutional_encoder(k, p)
        dec = viterbi_decoder(k, p)
        data = np.random.randint(2, size = 1000, dtype = 'uint8')
        pdu = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(data), bytes(data)))
  
        tb.msg_connect((enc, 'out'), (dec, 'in'))
        tb.msg_connect((dec, 'out'), (dbg, 'store'))
        enc.to_basic_block()._post(pmt.intern('in'), pdu)
        enc.to_basic_block()._post(pmt.intern('system'),
                pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        tb.start()
        tb.wait()

        out = pmt.u8vector_elements(pmt.cdr(dbg.get_message(0)))
        self.assertEqual(bytes(out), bytes(data),
                                "Encoded and decoded message does not match original")

if __name__ == '__main__':
    gr_unittest.run(qa_viterbi)

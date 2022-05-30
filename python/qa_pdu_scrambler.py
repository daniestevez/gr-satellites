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

from satellites import pdu_scrambler


class qa_pdu_scrambler(gr_unittest.TestCase):
    def test_pdu_scrambler(self):
        self.tb = gr.top_block()
        self.dbg = blocks.message_debug()
        size = 1024
        sequence = np.random.randint(0, 256, size)
        npdus = 16
        msgs = [np.random.randint(0, 256, size=np.random.randint(0, size),
                                  dtype='uint8')
                for _ in range(npdus)]
        pdus = [pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(m), bytes(m)))
                for m in msgs]
        self.scrambler = pdu_scrambler(sequence)
        self.tb.msg_connect((self.scrambler, 'out'), (self.dbg, 'store'))
        for pdu in pdus:
            self.scrambler.to_basic_block()._post(pmt.intern('in'), pdu)
        self.scrambler.to_basic_block()._post(
            pmt.intern('system'),
            pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        self.tb.run()

        for j, msg in enumerate(msgs):
            out = pmt.u8vector_elements(pmt.cdr(self.dbg.get_message(j)))
            np.testing.assert_equal(out, msg ^ sequence[:msg.size])

        self.tb = None


if __name__ == '__main__':
    gr_unittest.run(qa_pdu_scrambler)

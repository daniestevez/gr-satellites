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

from satellites import pdu_head_tail


class qa_pdu_head_tail(gr_unittest.TestCase):
    def test_pdu_head_tail(self):
        for mode in range(4):
            with self.subTest(mode=mode):
                self.run_mode(mode)

    def run_mode(self, mode):
        tb = gr.top_block()
        dbg = blocks.message_debug()
        num = 10
        sizes = [15, 8]
        test_data = list(range(np.max(sizes)))
        msgs = [test_data[:x] for x in sizes]
        pdus = [pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(m), m))
                for m in msgs]
        head_tail = pdu_head_tail(mode, num)

        tb.msg_connect((head_tail, 'out'), (dbg, 'store'))
        for pdu in pdus:
            head_tail.to_basic_block()._post(pmt.intern('in'), pdu)
        head_tail.to_basic_block()._post(
            pmt.intern('system'),
            pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        tb.start()
        tb.wait()

        for j, msg in enumerate(msgs):
            out = pmt.u8vector_elements(pmt.cdr(dbg.get_message(j)))
            if mode == 0:
                expected = msg[:num]
            elif mode == 1:
                expected = msg[:-num]
            elif mode == 2:
                expected = msg[-num:]
            elif mode == 3:
                expected = msg[num:]
            else:
                raise ValueError('Invalid mode')
            self.assertEqual(
                out, expected,
                "PDU head/tail output does not match expected value")


if __name__ == '__main__':
    gr_unittest.run(qa_pdu_head_tail)

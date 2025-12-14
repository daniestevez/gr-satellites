#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, gr_unittest
import pmt

# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites import message_counter


class qa_message_counter(gr_unittest.TestCase):
    def test_message_counter(self):
        tb = gr.top_block()
        counter = message_counter()
        dbg = blocks.message_debug()
        sink = blocks.message_debug()
        tb.msg_connect((counter, 'out'), (sink, 'store'))
        tb.msg_connect((counter, 'count'), (dbg, 'store'))

        num_messages = 32
        for _ in range(num_messages):
            counter.to_basic_block()._post(pmt.intern('in'), pmt.PMT_NIL)
        counter.to_basic_block()._post(
            pmt.intern('system'),
            pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        tb.start()
        tb.wait()

        self.assertEqual(sink.num_messages(), num_messages)
        self.assertEqual(dbg.num_messages(), num_messages)
        for n in range(num_messages):
            msg = sink.get_message(n)
            self.assertTrue(pmt.equal(msg, pmt.PMT_NIL))
            count = dbg.get_message(n)
            expected = pmt.cons(pmt.intern('count'), pmt.from_long(n + 1))
            self.assertTrue(pmt.equal(count, expected))


if __name__ == '__main__':
    gr_unittest.run(qa_message_counter)

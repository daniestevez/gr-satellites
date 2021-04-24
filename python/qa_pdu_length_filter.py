#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
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

from satellites import pdu_length_filter


class qa_pdu_length_filter(gr_unittest.TestCase):
    def test_pdu_length_filter(self):
        tb = gr.top_block()
        dbg = blocks.message_debug()
        sizes = [25, 50, 100]
        test_data = list(range(np.max(sizes)))
        msgs = [test_data[:x] for x in sizes]
        pdus = [pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(m), m))
                for m in msgs]
        length_filter = pdu_length_filter(40, 60)

        tb.msg_connect((length_filter, 'out'), (dbg, 'store'))
        for pdu in pdus:
            length_filter.to_basic_block()._post(pmt.intern('in'), pdu)
        length_filter.to_basic_block()._post(
            pmt.intern('system'),
            pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        tb.start()
        tb.wait()

        self.assertEqual(
            dbg.num_messages(), 1,
            'Incorrect number of messages passed by PDU Length Filter')
        out = pmt.u8vector_elements(pmt.cdr(dbg.get_message(0)))
        self.assertEqual(
            len(out), 50,
            'PDU Length Filter output does not match expected')


if __name__ == '__main__':
    gr_unittest.run(qa_pdu_length_filter)

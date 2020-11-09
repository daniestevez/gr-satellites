#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
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

from satellites import pdu_add_meta

class qa_pdu_add_meta(gr_unittest.TestCase):
    def test_pdu_add_meta(self):
        tb = gr.top_block()
        dbg = blocks.message_debug()
        meta = pmt.make_dict()
        meta = pmt.dict_add(meta, pmt.intern('k1'), pmt.intern('v1'))
        meta = pmt.dict_add(meta, pmt.intern('k2'), pmt.intern('v2'))
        add_meta = pdu_add_meta(meta)

        pdu = pmt.cons(pmt.PMT_NIL, pmt.make_u8vector(10, 0))

        tb.msg_connect((add_meta, 'out'), (dbg, 'store'))

        add_meta.to_basic_block()._post(pmt.intern('in'), pdu)
        add_meta.to_basic_block()._post(pmt.intern('system'),
                                pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        tb.start()
        tb.wait()

        pdu_out = dbg.get_message(0)
        meta_out = pmt.car(pdu_out)
        self.assertTrue(pmt.dict_has_key(meta_out, pmt.intern('k1')),
                            'Test key k1 not in output PDU metadata')
        self.assertTrue(pmt.dict_has_key(meta_out, pmt.intern('k2')),
                            'Test key k1 not in output PDU metadata')
        self.assertEqual(pmt.u8vector_elements(pmt.cdr(pdu_out)),
                             pmt.u8vector_elements(pmt.cdr(pdu)),
                             'Output PDU data does not match input PDU data')

if __name__ == '__main__':
    gr_unittest.run(qa_pdu_add_meta)

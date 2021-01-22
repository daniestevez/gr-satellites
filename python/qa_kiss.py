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

from satellites import kiss_to_pdu, pdu_to_kiss

class qa_kiss(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_encoder_decoder(self):
        """Connects a PDU to KISS and KISS to PDU and tries to send some PDUs through"""
        pdu2kiss = pdu_to_kiss(include_timestamp = True)
        kiss2pdu = kiss_to_pdu()
        pdu2tag = blocks.pdu_to_tagged_stream(blocks.byte_t)
        dbg = blocks.message_debug()

        self.tb.connect(pdu2tag, kiss2pdu)
        self.tb.msg_connect((pdu2kiss, 'out'), (pdu2tag, 'pdus'))
        self.tb.msg_connect((kiss2pdu, 'out'), (dbg, 'store'))

        test_size = 150
        test_number_frames = 7
        test_data = [np.random.randint(0, 256, test_size, dtype = 'uint8')
                         for _ in range(test_number_frames)]
        for td in test_data:
            test_frame = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(test_size, td))
            pdu2kiss.to_basic_block()._post(pmt.intern('in'), test_frame)
        pdu2kiss.to_basic_block()._post(pmt.intern('system'),
                pmt.cons(pmt.intern('done'), pmt.from_long(1)))
        
        self.tb.start()
        self.tb.wait()

        for j,td in enumerate(test_data):
            result_data = pmt.u8vector_elements(pmt.cdr(dbg.get_message(j)))
            np.testing.assert_equal(td, result_data,
                                "KISS to PDU output does not match expected frame")

if __name__ == '__main__':
    gr_unittest.run(qa_kiss)

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

from satellites import fixedlen_tagger
from satellites.grtypes import byte_t
from satellites.grpdu import tagged_stream_to_pdu


class qa_fixedlen_tagger(gr_unittest.TestCase):
    def setUp(self):
        self.syncword_tag = 'syncword'
        self.packetlen_tag = 'packet_len'
        self.packet_len = 100
        self.data = np.arange(16384, dtype='uint8')
        self.tag_positions = [50, 213, 217, 230, 1530, 1531]
        tags = [gr.python_to_tag((j, pmt.intern(self.syncword_tag),
                                  pmt.intern('sync'), pmt.intern('test_src')))
                for j in self.tag_positions]
        self.source = blocks.vector_source_b(self.data, False, 1, tags)
        self.tag2pdu = tagged_stream_to_pdu(byte_t,
                                            self.packetlen_tag)
        self.debug = blocks.message_debug()
        self.tagger = fixedlen_tagger(self.syncword_tag, self.packetlen_tag,
                                      self.packet_len, np.byte)
        self.tb = gr.top_block()
        self.tb.connect(self.source, self.tagger, self.tag2pdu)
        self.tb.msg_connect((self.tag2pdu, 'pdus'), (self.debug, 'store'))

    def tearDown(self):
        self.tb = None

    def test_tagger(self):
        """Runs some test data through the tagger and checks resulting PDUs"""
        self.tb.start()
        self.tb.wait()

        self.assertEqual(self.debug.num_messages(), len(self.tag_positions),
                         'Unexpected number of PDUs')
        for j, pos in enumerate(self.tag_positions):
            pdu = np.array(pmt.u8vector_elements(
                pmt.cdr(self.debug.get_message(j))), dtype='uint8')
            expected = self.data[pos:pos+self.packet_len]
            np.testing.assert_equal(pdu, expected,
                                    'PDU values do not match expected')


if __name__ == '__main__':
    gr_unittest.run(qa_fixedlen_tagger)

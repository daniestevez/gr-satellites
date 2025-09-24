#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021-2022 Daniel Estevez <daniel@destevez.net>
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

from satellites import fixedlen_to_pdu
from satellites.grtypes import byte_t


class qa_fixedlen_tagger(gr_unittest.TestCase):
    def setUp(self):
        self.syncword_tag = 'syncword'
        self.packetlen_tag = None
        self.packet_lengths = None

        self.debug = blocks.message_debug()
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_fixed_packet_size(self):
        """Runs some data through Fixedlen to PDU with fixed packet size and
        checks resulting PDUs"""
        self.packet_len = 100
        self.sync_positions = [50, 213, 217, 230, 1530, 1531]
        self.datalen = 3000
        self.common_test()

    def test_variable_packet_size(self):
        """Runs some data through Fixedlen to PDU with variable packet size and
        checks resulting PDUs"""
        self.packetlen_tag = 'packet_len'
        self.packet_len = 256
        self.sync_positions = [0, 17, 123, 244, 317, 525, 2357, 10728,
                               10729, 11425, 11500, 12328, 13743, 14000,
                               14001, 15732]
        self.packet_lengths = [215, 3, None, 117, 15, 200, 1, 17, 25,
                               None, 0, 143, 209, 125, 40, 13]
        self.datalen = 20000
        self.common_test()

    def common_test(self):
        if self.packet_lengths is None:
            self.packet_lengths = [None] * len(self.sync_positions)
        sync_tags = [
            gr.python_to_tag((j, pmt.intern(self.syncword_tag),
                              pmt.intern('sync'), pmt.intern('test_src')))
            for j in self.sync_positions
        ]
        length_tags = [
            gr.python_to_tag((j, pmt.intern(self.packetlen_tag),
                              pmt.from_long(length), pmt.intern('test_src')))
            for j, length in zip(self.sync_positions, self.packet_lengths)
            if length is not None
        ]
        tags = sync_tags + length_tags

        self.data = np.arange(self.datalen, dtype='uint8')
        self.source = blocks.vector_source_b(self.data, False, 1, tags)
        kwargs = {}
        if self.packetlen_tag is not None:
            kwargs['packet_length_tag'] = self.packetlen_tag
        self.fixedlen_to_pdu = fixedlen_to_pdu(
            byte_t, self.syncword_tag, self.packet_len, **kwargs)

        self.tb.connect(self.source, self.fixedlen_to_pdu)
        self.tb.msg_connect((self.fixedlen_to_pdu, 'pdus'),
                            (self.debug, 'store'))

        self.tb.start()
        self.tb.wait()

        self.assertEqual(self.debug.num_messages(), len(self.sync_positions),
                         'Unexpected number of PDUs')
        for j, pos in enumerate(self.sync_positions):
            pdu = np.array(pmt.u8vector_elements(
                pmt.cdr(self.debug.get_message(j))), dtype='uint8')
            length = self.packet_lengths[j]
            if length is None:
                length = self.packet_len
            expected = self.data[pos:pos+length]
            np.testing.assert_equal(
                pdu, expected,
                f'PDU values do not match for PDU number {j}')


if __name__ == '__main__':
    gr_unittest.run(qa_fixedlen_tagger)

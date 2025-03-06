#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import copy

from gnuradio import gr, blocks, gr_unittest
from gnuradio.pdu import pdu_lambda, pdu_set
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

from satellites.mobitex_fec_block import mobitex_fec
from satellites.crcs import crc16_ccitt_x25


FIXTURE = {
    'in': '1ABCF3FCC1D10B922D18DE0818D0000005DCC130000007D72C8D115FA198',
    'out': {
        'msg': '1ACFFC1D0B2218E01800005DC000007D2CD15F19',
        'tags': {
            'corrected_errors': 1,
            'uncorrected_errors': 0,
        },
    },
}
FIXTURE2 = copy.deepcopy(FIXTURE)
FIXTURE2['out']['tags']['crc_valid'] = True
FIXTURE2['out']['msg'] = FIXTURE['out']['msg'][:-4]


def msg_from_str(input_str: str):
    msg = np.frombuffer(
        bytes.fromhex(input_str.replace(' ', '')),
        dtype='uint8',
    )
    return msg


def pdu_from_str(input_str: str):
    msg = msg_from_str(input_str)
    pdu = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(msg), msg))
    return pdu


class qa_mobitex_fec(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()
        self.dbg = blocks.message_debug()

    def test_mobitex_fec(self):
        """
        Test the mobitex_fec
        """
        self.pdus_in = [pdu_from_str(FIXTURE['in'])]
        self.msgs_out = [msg_from_str(FIXTURE['out']['msg'])]
        self.tags_out = [FIXTURE['out']['tags']]

        dut = mobitex_fec()
        self.input = (dut, 'in')
        self.output = (dut, 'out')

        self.run_test()

    def test_mobitex_crc(self):
        """
        Test the mobitex_fec as well as the (Mobitex-Block) CRC
        """
        self.pdus_in = [pdu_from_str(FIXTURE2['in'])]
        self.msgs_out = [msg_from_str(FIXTURE2['out']['msg'])]
        self.tags_out = [FIXTURE2['out']['tags']]

        fec = mobitex_fec()
        crc = crc16_ccitt_x25(swap_endianness=False)
        crc_ok = pdu_set(k=pmt.intern('crc_valid'), v=pmt.from_bool(True))
        crc_fail = pdu_set(k=pmt.intern('crc_valid'), v=pmt.from_bool(False))
        demux = pdu_lambda(lambda x: x, 'RAW')

        self.tb.msg_connect((fec, 'out'), (crc, 'in'))

        self.tb.msg_connect((crc, 'ok'), (crc_ok, 'pdus'))
        self.tb.msg_connect((crc, 'fail'), (crc_fail, 'pdus'))

        self.tb.msg_connect((crc_ok, 'pdus'), (demux, 'pdu'))
        self.tb.msg_connect((crc_fail, 'pdus'), (demux, 'pdu'))

        self.input = (fec, 'in')
        self.output = (demux, 'pdu')

        self.run_test()

    def run_test(self):
        """
        Test the DUT by passing the input PDUs (self.pdus_in) to 'in' and
        checking the output messages from 'out' against the desired output
        (self.msgs_out) and desired output tags (self.tags_out).

        The input block and port is specified by the self.input tuple.
        The output block and port is specified by the self.output tuple.
        """
        # Prepare flowgraph
        self.tb.msg_connect(self.output, (self.dbg, 'store'))

        # Send PDUs
        for pdu in self.pdus_in:
            self.input[0].to_basic_block()._post(
                pmt.intern(self.input[1]), pdu)

        # Send 'done=1'
        self.input[0].to_basic_block()._post(
            pmt.intern('system'),
            pmt.cons(pmt.intern('done'), pmt.from_long(1)))

        # Run flowgraph
        self.tb.run()

        # Check results
        actual_msg_count = self.dbg.num_messages()
        desired_msg_count = len(self.msgs_out)
        self.assertEqual(actual_msg_count, desired_msg_count)

        for idx, (desired_msg, desired_tags) in enumerate(
            zip(self.msgs_out, self.tags_out)
        ):
            msg_pmt = self.dbg.get_message(idx)

            # Check message
            actual_msg = np.array(
                pmt.u8vector_elements(pmt.cdr(msg_pmt)),
                dtype='uint8')
            np.testing.assert_array_equal(actual_msg, desired_msg)

            # Check tags
            actual_tags = pmt.to_python(pmt.car(msg_pmt))
            self.assertDictEqual(actual_tags, desired_tags)


if __name__ == '__main__':
    gr_unittest.run(qa_mobitex_fec)

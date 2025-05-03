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
from gnuradio.blocks import pdu_set
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

from satellites.mobitex_fec import (
    init_syndrome_table, encode, decode, Status,
    pack_2b, unpack_2b,
)


class qa_mobitex_fec(gr_unittest.TestCase):
    def test_init_syndrome_table(self):
        desired_syndrom_table = {
            1: 0, 2: 1, 4: 2, 8: 3, 5: 4, 6: 5,
            9: 6, 10: 7, 7: 8, 11: 9, 13: 10, 14: 11}
        actual_syndrom_table = init_syndrome_table()
        self.assertEqual(desired_syndrom_table, actual_syndrom_table)

    def test_encode(self):
        # Example with zero bit errors
        message = 0x2C
        desired_codeword = 0x2C8

        actual_codeword = encode(message)
        self.assertEqual(actual_codeword, desired_codeword)

    def test_decode(self):
        codeword = 0x2C8
        desired_message = 0x2C
        desired_status = Status.NO_ERROR

        actual_message, _, actual_status = decode(codeword)
        self.assertEqual(actual_status, desired_status)
        self.assertEqual(actual_message, desired_message)

    def test_decode2(self):
        # Example with single-bit error
        codeword = 0x2C8
        codeword = codeword | 0b0010_0000
        desired_message = 0x2C
        desired_status = Status.ERROR_CORRECTED

        actual_message, _, actual_status = decode(codeword)
        self.assertEqual(actual_status, desired_status)
        self.assertEqual(actual_message, desired_message)

    def test_decode3(self):
        # Example with two bit errors; collision and thus invalid correction
        codeword = 0x2C8
        codeword = codeword | 0b0010_0010

        desired_status = Status.ERROR_CORRECTED
        desired_message = 0x2E

        actual_message, _, actual_status = decode(codeword)
        self.assertEqual(actual_status, desired_status)
        self.assertEqual(actual_message, desired_message)

    def test_pack2b(self):
        codeword0, codeword1 = 0x580, 0x444
        desired_code = bytes.fromhex('580444')

        actual_code = pack_2b(codeword0, codeword1)

        self.assertEqual(desired_code, actual_code)

    def test_unpack2b(self):
        code = bytes.fromhex('AFFEFE')
        desired_codeword0 = 0xaff
        desired_codeword1 = 0xefe
        actual_codeword0, actual_codeword1 = unpack_2b(code)

        self.assertEqual(actual_codeword0, desired_codeword0)
        self.assertEqual(actual_codeword1, desired_codeword1)

    def test_edge_cases(self):
        # Test edge cases and error conditions

        # Test all possible 8-bit values
        for i in range(256):
            codeword = encode(i)
            fec = codeword & 0xf

            assert 0 <= fec <= 0xF
            decoded, _, status = decode(codeword)
            assert status == status.NO_ERROR
            assert decoded == i

        # For one example message,
        # test all possible single-bit errors.
        message = 0x2C
        codeword = encode(message)

        for bit in range(12):
            corrupted = codeword ^ (1 << bit)
            decoded, _, status = decode(corrupted)
            assert status == Status.ERROR_CORRECTED
            assert decoded == message


if __name__ == '__main__':
    gr_unittest.run(qa_mobitex_fec)

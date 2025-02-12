#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
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

from satellites.mobitex_to_datablocks import (
    check_callsign_crc, compare_expected_callsign, decode_unknown_callsign,
    decode_control, encode_control,
)


class qa_mobitex_to_datablocks(gr_unittest.TestCase):
    def test_check_callsign_crc(self):
        fixture = [
            (b'DP0BEM', b'\x4d\xf7', True),
            (b'DP0BEX', b'\x4d\xf7', False),
        ]

        for callsign, crc, desired_result in fixture:
            actual_result = check_callsign_crc(callsign, crc)
            self.assertEqual(actual_result, desired_result)

    def test_compare_expected_callsign(self):
        fixture = [
            ((b'DP0BEM', b'\x4d\xf7', b'DP0BEM'), (b'\x4d\xf7', 0)),
            ((b'DQ0BEM', b'\x4d\xf7', b'DP0BEM'), (b'\x4d\xf7', 1)),
            ((b'EQ0BEM', b'\x4d\xf7', b'DP0BEM'), (b'\x4d\xf7', 2)),
            ((b'\x1b@@@L!', b'\x4d\xf7', b'DP0BEM'), (b'\x4d\xf7', 17)),
        ]

        for input, desired_output in fixture:
            callsign, crc, callsign_ref = input
            desired_crc_ref, desired_bit_errors = desired_output

            actual_crc_ref, actual_bit_errors = compare_expected_callsign(
                    callsign,
                    crc,
                    callsign_ref
                )
            self.assertEqual(actual_crc_ref, desired_crc_ref)
            self.assertEqual(actual_bit_errors, desired_bit_errors)

    def test_decode_unknown_callsign(self):
        fixture = [
            # No bit error
            ((b'DP0BEM', b'\x4d\xf7', 2), (b'DP0BEM', b'\x4d\xf7', 0)),
            # 1 bit error in callsign
            ((b'EP0BEM', b'\x4d\xf7', 2), (b'DP0BEM', b'\x4d\xf7', 1)),
            # 1 bit error in crc
            ((b'DP0BEM', b'\x5d\xf7', 2), (b'DP0BEM', b'\x4d\xf7', 1)),
            # 4 bit errors in callsign
            ((b'EQ0BEN', b'\x4d\xf7', 4), (b'DP0BEM', b'\x4d\xf7', 4)),
            # Bit error count exceeded
            ((b'EQ0BEN', b'\x4d\xf7', 2), None),
            # False-positive solutions when too many bit flips are allowed
            ((b'EQ1BEN', b'\x5d\xf6', 4), (b'EU1BEO', b'}\xf6', 3)),
        ]
        for input, desired_output in fixture:
            callsign, crc, max_bit_flips = input

            actual_output = decode_unknown_callsign(
                    callsign,
                    crc,
                    max_bit_flips,
                )

            if desired_output is None:
                self.assertIsNone(actual_output)
                continue

            desired_callsign, desired_crc, desired_bit_errors = desired_output
            actual_callsign, actual_crc, actual_bit_errors = actual_output
            self.assertEqual(actual_bit_errors, desired_bit_errors)

    def test_decode_control(self):
        fixture = [
            # No bit error
            ((0x3f, 0x02, 0xc6), ((0x3f, 0x02, 0xc6), 0)),
            # One bit errors
            ((0b0011_1011, 0x02, 0xc6), ((0x3f, 0x02, 0xc6), 1)),
            # Two bit errors
            ((0b0011_1010, 0x02, 0xc6), None),
        ]

        for control_and_fec, desired_result in fixture:
            actual_result = decode_control(*control_and_fec)
            if desired_result is None:
                self.assertIsNone(actual_result)
                continue

            actual_bytes = bytes(actual_result[0])
            actual_bit_errors = actual_result[1]

            desired_bytes = bytes(desired_result[0])
            desired_bit_errors = desired_result[1]

            self.assertEqual(actual_bytes, desired_bytes)
            self.assertEqual(actual_bit_errors, desired_bit_errors)

    def test_encode_control(self):
        fixture = [
            ((0x00, 0x00), 0x00),
            ((0x3f, 0x01), 0xc5),
            ((0x3f, 0x02), 0xc6),
            ((0xff, 0xff), 0xff),
        ]

        for control, desired_fec in fixture:
            actual_fec = encode_control(*control)
            self.assertEqual(actual_fec, desired_fec)


if __name__ == '__main__':
    gr_unittest.run(qa_mobitex_to_datablocks)

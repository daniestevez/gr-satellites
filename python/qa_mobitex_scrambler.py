#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr_unittest
import numpy as np

# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites.mobitex_scrambler import Scrambler


FIXTURE = {
    'in': bytes.fromhex(
        '000000000000000000000000000000000000000000000000000000000000'),
    'out': bytes.fromhex(
        'ff83df1732094ed1e7cd8a91c6d5c4c44021184e5586f4dc8a15a7ec92df'),
}


def _unpack_bits(data):
    for byte in data:
        for i in range(8):
            bit = (byte >> (7 - i)) & 0x01
            yield bit


def unpack_bits(data: bytes) -> [int]:
    """Unpack bytes into a list of bits"""
    return list(_unpack_bits(data))


class qa_mobitex_scrambler(gr_unittest.TestCase):
    def setUp(self):
        self.bits_in = unpack_bits(FIXTURE['in'])
        self.desired_output = unpack_bits(FIXTURE['out'])

    def test_mobitex_scrambler(self):
        scrambler = Scrambler()
        actual_output = [scrambler.scramble(bit) for bit in self.bits_in]

        np.testing.assert_array_equal(actual_output, self.desired_output)

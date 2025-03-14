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

from satellites.mobitex_fec import init_syndrome_table


class qa_mobitex_fec(gr_unittest.TestCase):
    def test_init_syndrome_table(self):
        desired_syndrom_table = {
            1: 0, 2: 1, 4: 2, 8: 3, 5: 4, 6: 5,
            9: 6, 10: 7, 7: 8, 11: 9, 13: 10, 14: 11}
        actual_syndrom_table = init_syndrome_table()
        self.assertEqual(desired_syndrom_table, actual_syndrom_table)

if __name__ == '__main__':
    gr_unittest.run(qa_mobitex_fec)

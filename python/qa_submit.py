#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
# Copyright 2025 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr_unittest

# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites.submit import parse_timestamp


class qa_submit(gr_unittest.TestCase):
    def test_parse_timestamp(self):
        # parse timestamps in various formats
        t0 = parse_timestamp('2025-10-02T17:49:22.123456789Z')
        self.assertEqual(str(t0), '2025-10-02 17:49:22.123456+00:00')

        t1 = parse_timestamp('2025-10-02T20:47:24.587123442')
        self.assertEqual(str(t1), '2025-10-02 20:47:24.587123+00:00')

        t2 = parse_timestamp('2025-10-02T20:50:03.157291322Z')
        self.assertEqual(str(t2), '2025-10-02 20:50:03.157291+00:00')

        t3 = parse_timestamp('2025-10-02 20:50:03')
        self.assertEqual(str(t3), '2025-10-02 20:50:03+00:00')

        t4 = parse_timestamp('2025-10-02T17:49:22+02:00')
        self.assertEqual(str(t4), '2025-10-02 15:49:22+00:00')

        t5 = parse_timestamp('2025-10-02T17:49:22+02:30')
        self.assertEqual(str(t5), '2025-10-02 15:19:22+00:00')

        t6 = parse_timestamp('2025-10-02T17:49:22+02:00:00.01')
        self.assertEqual(str(t6), '2025-10-02 15:49:21.990000+00:00')

        # get elapsed time
        elapsed = (t1 - t0).total_seconds()
        self.assertEqual(elapsed, 3 * 3600 - 2 * 60 + 2 + 0.587123 - 0.123456)

        # propagate time (as in submit.py)
        t_prop = t2 - t1 + t0
        self.assertEqual(str(t_prop), '2025-10-02 17:52:00.693624+00:00')

        # format as needed in submit.py
        t0_fmt = t0.replace(tzinfo=None).isoformat()[:-3] + 'Z'
        self.assertEqual(t0_fmt, '2025-10-02T17:49:22.123Z')

        # compute KISS timestamp
        t0_kiss = round(t0.timestamp() * 1e3)
        self.assertEqual(t0_kiss, 1759427362123)


if __name__ == '__main__':
    gr_unittest.run(qa_submit)

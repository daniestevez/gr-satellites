#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020, 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys

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

from satellites.components.datasinks import kiss_server_sink


class qa_kiss_server_sink(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        """Tries to create a KISS server sink instance

        It uses several combinations of parameters
        """
        kiss_server_sink('', 1234)
        kiss_server_sink('127.0.0.1', 4567)


if __name__ == '__main__':
    gr_unittest.run(qa_kiss_server_sink)

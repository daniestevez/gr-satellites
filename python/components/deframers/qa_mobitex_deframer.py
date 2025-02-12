#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#           2025 Fabian P. Schmidt <kerel@mailbox.org>
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

from satellites.components.deframers import mobitex_deframer


class qa_mobitex_deframer(gr_unittest.TestCase):
    def setUp(self):
        file_base = __file__.rstrip('.py')
        self.symbols_path = file_base + '_symbols.f32'
        self.frame_path = file_base + '_frame.bin'

        self.tb = gr.top_block()

        self.frames_desired = [np.fromfile(self.frame_path, dtype='uint8')]

    def tearDown(self):
        self.tb = None

    def test_mobitex_deframer(self):
        """Test mobitex deframer

        Loads symbols from a BEESAT-9 packet and checks if mobitex_deframer
        produces the expected output and intermediate data (stored in
        reference files)"""
        input = blocks.file_source(gr.sizeof_float, self.symbols_path)

        deframer = mobitex_deframer(
            nx=True,
            callsign='DP0BEM',
            callsign_threshold=0,
            syncword_threshold=0,
        )
        dbg_frame = blocks.message_debug()

        self.tb.connect(input, deframer)
        self.tb.msg_connect((deframer, 'out'), (dbg_frame, 'store'))
        self.tb.start()
        self.tb.wait()

        num_msgs_desired = len(self.frames_desired)
        num_msgs_actual = dbg_frame.num_messages()
        self.assertEqual(num_msgs_actual, num_msgs_desired)

        for idx, frame_desired in enumerate(self.frames_desired):
            frame_actual = np.array(
                pmt.u8vector_elements(pmt.cdr(dbg_frame.get_message(idx))),
                dtype=np.uint8)
            np.testing.assert_array_equal(frame_actual, frame_desired)


if __name__ == '__main__':
    gr_unittest.run(qa_mobitex_deframer)

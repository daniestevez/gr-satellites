#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks, gr_unittest
import pmt
import numpy as np

# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites.components.deframers import ao40_fec_deframer

class qa_ao40_fec_deframer(gr_unittest.TestCase):
    def setUp(self):
        file_base = __file__.rstrip('.py')
        self.symbols_path = file_base + '_symbols.f32'
        self.frame_path = file_base + '_frame.f32'
        self.post_viterbi_reference = [118, 72, 14, 192, 154, 13, 112, 188, 142, 51, 95,
                                           173, 105, 181, 151, 206, 90, 144, 117, 197, 59,
                                           162, 191, 59, 11, 17, 241, 200, 135, 226, 34,
                                           67, 162, 31, 41, 162, 199, 160, 234, 36, 126,
                                           45, 118, 156, 165, 148, 228, 214, 47, 177, 251,
                                           145, 138, 229, 97, 136, 179, 203, 169, 215, 166,
                                           138, 149, 114, 227, 48, 204, 3, 86, 21, 166,
                                           242, 239, 57, 182, 97, 10, 21, 136, 145, 64,
                                           135, 165, 150, 196, 210, 242, 48, 39, 13, 199,
                                           63, 115, 109, 170, 28, 110, 232, 220, 142, 72,
                                           120, 41, 141, 123, 194, 53, 125, 219, 170, 164,
                                           125, 108, 186, 190, 65, 241, 21, 46, 102, 248,
                                           70, 7, 12, 131, 196, 252, 69, 58, 29, 252, 127,
                                           175, 30, 27, 157, 227, 243, 26, 128, 123, 163,
                                           251, 204, 161, 251, 148, 140, 131, 65, 169, 18,
                                           5, 31, 33, 134, 55, 209, 45, 30, 160, 33, 188,
                                           19, 150, 58, 31, 65, 79, 74, 95, 25, 156, 178,
                                           167, 127, 92, 188, 183, 29, 90, 224, 230, 200,
                                           98, 68, 49, 201, 0, 21, 164, 176, 58, 59, 31,
                                           140, 9, 158, 177, 45, 85, 43, 163, 103, 220, 208,
                                           130, 182, 255, 223, 189, 151, 96, 80, 71, 234,
                                           159, 142, 8, 127, 249, 221, 163, 188, 170, 115,
                                           110, 21, 7, 140, 126, 29, 22, 158, 77, 234, 192,
                                           52, 223, 232, 251, 149, 220, 207, 228, 94, 244,
                                           5, 98, 122, 90, 74, 101, 213, 75, 255, 52, 42,
                                           128, 128, 193, 143, 179, 55, 197, 105, 56, 98,
                                           35, 68, 178, 131, 1, 113, 101, 128, 64, 13, 5,
                                           165, 169, 159, 118, 179, 112, 92, 119, 194, 35,
                                           141, 77, 129, 180, 19, 23, 247, 52, 38, 233, 32,
                                           158, 11, 230, 188, 228, 96, 46, 155, 115, 28, 15,
                                           212, 110, 122, 27, 135, 117, 22, 44, 27]
        self.frame_reference = [137, 0, 0, 0, 0, 0, 0, 0, 0, 31, 204, 0, 206, 2, 209, 0, 0,
                          7, 8, 9, 9, 0, 0, 5, 1, 1, 0, 64, 19, 47, 200, 242, 92,
                          143, 52, 35, 243, 186, 11, 93, 98, 116, 81, 199, 234, 250,
                          105, 74, 154, 159, 0, 9, 239, 160, 31, 244, 167, 234, 74,
                          198, 143, 17, 64, 17, 30, 16, 247, 1, 62, 32, 100, 0, 215,
                          139, 248, 215, 148, 200, 147, 168, 42, 218, 82, 166, 14, 88,
                          14, 200, 15, 78, 1, 29, 32, 90, 0, 219, 148, 168, 170, 138,
                          152, 19, 172, 105, 10, 166, 168, 16, 230, 16, 146, 15, 184,
                          1, 80, 32, 100, 0, 215, 150, 168, 193, 139, 72, 37, 171, 169,
                          202, 206, 157, 16, 118, 15, 201, 16, 85, 1, 58, 32, 90, 0, 215,
                          151, 41, 8, 140, 72, 79, 169, 106, 90, 242, 164, 16, 57, 15,
                          123, 15, 134, 1, 73, 32, 100, 0, 215, 148, 8, 208, 138, 216,
                          42, 173, 106, 90, 126, 180, 14, 83, 14, 155, 14, 183, 1, 9, 32,
                          90, 0, 219, 153, 168, 242, 143, 232, 56, 175, 170, 138, 194,
                          158, 14, 222, 15, 72, 14, 49, 1, 49, 32, 90, 0, 206, 155, 200,
                          255, 136, 104, 27, 178, 106, 90, 202, 167, 15, 195, 14, 116, 14,
                          88, 1, 52, 32, 90, 0, 215, 155, 57, 27, 151, 184, 197, 176, 43,
                          58, 214, 181, 1, 107, 0, 106, 2, 158, 0, 3, 32, 19, 0]
        
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_ao40_fec_deframer(self):
        """Loads symbols from an AO-73 packet and checks if ao40_fec_deframer produces the expected output and intermediate data (stored in a reference files)"""
        test_data = blocks.file_source(gr.sizeof_float, self.symbols_path)
        deframer = ao40_fec_deframer()
        dbg_sync = blocks.message_debug()
        dbg_deinterleave = blocks.message_debug()
        dbg_frame = blocks.message_debug()
        dbg_viterbi = blocks.message_debug()

        self.tb.connect(test_data, deframer)
        self.tb.msg_connect((deframer.deframer, 'out'), (dbg_sync, 'store'))
        self.tb.msg_connect((deframer.deinterleaver, 'out'), (dbg_deinterleave, 'store'))
        self.tb.msg_connect((deframer.viterbi_decoder, 'out'), (dbg_viterbi, 'store'))
        self.tb.msg_connect((deframer, 'out'), (dbg_frame, 'store'))
        self.tb.start()
        self.tb.wait()

        synced = pmt.f32vector_elements(pmt.cdr(dbg_sync.get_message(0)))
        synced_reference = np.fromfile(self.frame_path, dtype = 'float32')
        self.assertFloatTuplesAlmostEqual(synced, synced_reference,
                                              "synchronizer output doesn't match expected result")

        deinterleaved = pmt.f32vector_elements(pmt.cdr(dbg_deinterleave.get_message(0)))
        rows = 80
        cols = 65
        skip = 65
        output_size = 5132
        deinterleaved_reference = synced_reference.reshape((cols,rows)).transpose().ravel()[skip:][:output_size]
        self.assertFloatTuplesAlmostEqual(deinterleaved, deinterleaved_reference,
                                              "deinterleaver output doesn't match expected result")

        post_viterbi = pmt.u8vector_elements(pmt.cdr(dbg_viterbi.get_message(0)))
        post_viterbi_reference = np.unpackbits(np.array(self.post_viterbi_reference, dtype='uint8'))
        np.testing.assert_equal(post_viterbi, post_viterbi_reference,
                             "Viterbi decoder output doesn't match expected result")

        frame = pmt.u8vector_elements(pmt.cdr(dbg_frame.get_message(0)))
        self.assertEqual(frame, self.frame_reference,
                             "ao40_fec_deframer() final output doesn't match expected frame")
        
if __name__ == '__main__':
    gr_unittest.run(qa_ao40_fec_deframer)

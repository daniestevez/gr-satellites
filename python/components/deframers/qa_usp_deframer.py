#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
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

from satellites.components.deframers import usp_deframer

class qa_usp_deframer(gr_unittest.TestCase):
    def setUp(self):
        frame_long = """
24 c8 d6 9c 06 17 78 af 8c f5 8d 82 57 a5 36 8e 
58 c2 fa 4f ec bd 1a 64 95 5b 91 77 97 ce a8 09 
f5 26 3e 74 a1 21 96 4c 8a 08 11 ec cf 08 8f bc 
30 9f 88 7f 77 d3 8f b2 cf 77 07 59 c7 09 47 16 
a5 ce 36 59 e8 ee 9a c7 80 69 23 35 26 3e ad 3a 
e4 53 21 08 12 bc 1f 43 46 4d c6 c2 8b e2 27 7c 
4f fb f6 09 50 5e de 51 1c 3c 90 0e 66 e1 58 aa 
0c 5b d5 da 18 75 f9 cb 3d d2 ec a7 f3 02 db 5a 
97 38 d9 67 a3 ba 6b 1e 01 a4 8c d4 98 fa b4 eb 
91 4c 84 20 4a f0 7d 0d 19 37 1b 0a 2c d6 bf 1f 
c7 10 cb 95 08 ae 91 05 be 3b fb 93 50 49 ad 3a 
06 d8 62 5e 78 7a 9d b5 9c 48 0e ef c2 c1 6a 6a 
85 75 d6 f6 f2 54 ce c0 c9 8a 95 cb e4 4a a3 74 
5a f1 3c 68 6f 25 79 38 49 c8 8f b1 9f 92 77 c4 
ff bf 60 95 05 ed e5 11 c3 c9 00 e6 6e 15 8a a0 
c5 bd 5d a1 87 5f 9c b3 dd 2e ca 7f 30 2d b5 a9 
73 8d 96 7a 3b a6 b1 e0 1a 48 cd 49 8f ab 4e b9 
14 c8 42 04 af 07 d0 d1 93 71 b0 a2 f8 89 df 13 
fe fd 82 54 17 b7 94 47 0f 24 03 99 b8 56 2a 83 
16 f5 76 86 1d 7e 72 cf 74 bb 29 fc c0 b6 d6 a5 
ce 36 59 e8 ee 9a c7 80 69 23 35 26 3e ad 3a e4 
53 21 08 12 bc 1f 43 46 4d c6 c2 8b e2 27 7c 4f 
fb f6 09 50 5e de 51 1c 3c 90 0e 66 e1 58 aa 0c 
5b d5 da 18 75 f9 cb 3d d2 ec a7 f3 02 db 5a 97 
38 d9 67 a3 ba 6b 1e 01 a4 8c d4 98 fa b4 eb 91 
4c 84 20 4a f0 7d 0d 19 37 1b 0a 2f 88 9d f1 3f 
ef d8 25 41 7b 79 44 70 f2 40 39 9b 85 62 a8 31 
6f 57 68 61 d7 e7 2c f7 4b b2 9f cc 0b 6d 6a 5c 
e3 65 9e 8e e9 ac 75 48 a5 8a 95 f3 a4 12 87 01 
0f 08 58 d8 fc 00 a1 9e 32 26 33 e3 00 c4 10 a0 
df b5 3a b4 07 09 49 0b 27 d9 37 cf e9 59 8d 8c 
93 65 49 05 01 70 b8 c5 d8 07 d0 ea b5 a4 06 46 
eb 3a c8 05 f9 f3 
"""
        frame_long = frame_long.replace(' ', '').replace('\n', '')
        self.frame_long = np.frombuffer(bytes.fromhex(frame_long),
                                        dtype = 'uint8')

        frame_short = """
71 9d 83 c9 53 42 2d fa 8c f5 8d 82 6c 61 8a fe 
58 c2 fa 4f ec bd 1a 64 95 5b 91 77 97 ce a8 09 
f5 26 3e 74 a1 21 96 4c 8a 08 11 ec cf 08 8f bc 
e9 3f 50 49 a0 a3 8f b2 cf 77 07 59 fc cd fb 66 
a5 ce 38 9d 1e 1b a1 9d 6f 57 8a 30 b3 04 b8 42 
0a 8a c5 48 7f 98 18 3f a8 1d d8 8d 4f da 01 cc 
4f fb f6 09 50 5e de 51 cb ba 35 b5 15 53 35 10 
56 42 4d 4c bc b4 1e 52 4f 8a 5b f4 f7 2e 07 c9 
5d 1e 20 5e d0 4c 7f 1f 13 1c 76 15 d9 46 b6 2d 
75 51 c5 7e f8 50 72 67 42 5a 04 1e 6a e0 1a 7e 
9d d0 29 f1 57 2c 20 fb 9e 20 1e fe ff ff f9 12 
a0 d6 2d 46 76 1f 8d ee de f8 63 67 20 8c 8c bb 
05 a7 95 0a d9 8b 4c 14 19 7b 07 29 46 99 5e 3c 
e5 e2 da ab 03 7c b5 25 53 14 ad e7 2b 61 ff 37 
9e c8 d1 b3 8e db f8 6d 2c db f7 8e ed 31 b6 ab 
5f 34 27 6e a5 1f 7b 31 b5 eb 6e 74 23 dc 5a bf 
45 41 53 64 ad d5 9d 59 f2 2e e5 39 d6 e8 de b5 
6b da 8b 84 3d b1 56 9f 51 4a c9 9d c6 34 7a aa 
07 e4 bc 43 43 3d c5 9b 5b f1 8b 58 54 53 bb 59 
c6 72 57 31 e3 83 af 4d d4 c5 68 4e 6e 7a 15 36 
9e 3a 46 d0 4b c8 ae 7d 1b c4 f4 eb 65 87 49 ba 
6f 9a 51 90 22 9e 12 95 ec b4 42 4a 85 76 5e 4f 
49 50 83 4f 26 ea 29 5d a9 56 d3 24 b2 5c cd 1b 
ba 9e db d2 3b 72 1d 16 5b d1 57 72 ec 21 e6 7d 
91 57 56 8a 0a dd 9a c2 a2 b7 b5 3d bb 11 bc 82 
e9 9a 83 8d 8f 90 14 1b da c4 56 ca 2b b3 aa 9a 
7b d2 49 2e cd 46 78 aa 6b f0 66 0f 64 cb 16 60 
07 e6 55 12 67 2d 18 6a 17 12 92 db 25 97 69 45 
b5 43 16 93 56 94 75 a1 fa a2 67 4e e8 d8 42 87 
3b 2b e0 6b 5b 17 06 17 54 e4 c4 d6 d6 4b 7d 22 
4f 33 2f b2 d2 59 45 49 ca b4 a5 53 c2 96 21 29 
ec 88 a9 37 c3 0b 5e 58 c5 26 9c c2 ae a4 c4 4a 
7a cc c0 74 1d 09
"""
        frame_short = frame_short.replace(' ', '').replace('\n', '')
        self.frame_short = np.frombuffer(bytes.fromhex(frame_short),
                                        dtype = 'uint8')

        self.frames = (self.frame_long, self.frame_short)

        frame_long_out = """
a464829c8c4060a4a66060a6406f00f01642020001004200000000
000000000000000000000000000000000000000000000000000000
000000000000000000000000000000001b1bff671f20250eaab140
60f43c01002400f01c
"""
        frame_long_out = frame_long_out.replace('\n', '')
        self.frame_long_out = np.frombuffer(bytes.fromhex(frame_long_out),
                                        dtype = 'uint8')
        frame_short_out = """
a464829c8c4060a4a66060a6406f00f0e1ff020001000300002606
"""
        frame_short_out = frame_short_out.replace('\n', '')
        self.frame_short_out = np.frombuffer(bytes.fromhex(frame_short_out),
                                        dtype = 'uint8')
        self.frames_out = (self.frame_long_out, self.frame_short_out)
        
        self.sync = np.array([80, 114, 246,  75,  45, 144, 177, 245], dtype = 'uint8')
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_usp_fec_deframer(self):
        """Inserts a long and a short frame into the USP deframer and checks the output"""
        frames = [np.concatenate([self.sync, f, np.zeros(1500, dtype = 'uint8')])
                      for f in self.frames]
        frames = [2 * np.unpackbits(f).astype('float32') - 1 for f in frames]
        frames = np.concatenate(frames)
        vector = blocks.vector_source_f(frames, False, 1, [])
        deframer = usp_deframer()
        dbg = blocks.message_debug()

        self.tb.connect(vector, deframer)
        self.tb.msg_connect((deframer, 'out'), (dbg, 'store'))
        self.tb.start()
        self.tb.wait()

        for j, frame in enumerate(self.frames_out):
            out = np.array(pmt.u8vector_elements(pmt.cdr(dbg.get_message(j))),
                               dtype = 'uint8')
            np.testing.assert_equal(out, frame, 'Output frame does not match')
        
if __name__ == '__main__':
    gr_unittest.run(qa_usp_deframer)

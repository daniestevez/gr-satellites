#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
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

from satellites.telemetry.by02 import frameB

    
class qa_by02(gr_unittest.TestCase):
    def test_frameB(self):
        """Tries to parse a frameB"""
        frame = """08 10 2c 2d 00 55 55 55 55 55 55 00 26 e7 90 ff 
ff ff ff 00 00 00 00 51 ee 65 00 01 00 49 4e 30 
4f 52 59 0a 49 11 29 00 c8 d7 43 00 00 55 ff 00 
00 1b 56 aa aa aa aa aa aa aa aa aa aa aa aa aa 
aa aa aa aa aa aa aa aa aa aa aa aa aa aa aa aa 
aa"""
        frame = bytes().fromhex(frame.replace(' ','').replace('\n', ''))
        data = frameB.parse(frame)
        self.assertEqual(data.header.spacecraft_id, 129,
                             'TM header spacecraft ID is not correct')
        self.assertEqual(data.header.master_channel_frame_count, 44,
                             'TM header master channel frame count is not correct')
        self.assertEqual(data.header.virtual_channel_frame_count, 45,
                             'TM header virtual channel frame count is not correct')
        self.assertEqual(data.header.virtual_channel_id, 0,
                             'TM header virtual channel ID is not correct')
        self.assertEqual(data.hk_AVR.callsign, b'IN0ORY',
                              'Decoded callsign is not correct')
        self.assertEqual(frame, frameB.build(data),
                             'Rebuilt frame does not equal original frame')
        
if __name__ == '__main__':
    gr_unittest.run(qa_by02)

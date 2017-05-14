#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import pmt
import array

codec2_frame_len = 7
chunk_len = 24
bits_per_byte = 8
packet_len = 116

class lilacsat1_demux(gr.sync_block):
    """
    docstring for block lilacsat1_demux
    """
    def __init__(self, tag):
        gr.sync_block.__init__(self,
            name="lilacsat1_demux",
            in_sig=[numpy.int8],
            out_sig=[])

        self.position = -1
        self.tag = pmt.string_to_symbol(tag)

        self.message_port_register_out(pmt.intern('kiss'))
        self.message_port_register_out(pmt.intern('codec2'))
        

    def work(self, input_items, output_items):
        inp = input_items[0]

#        print "WORK!! chunk = ", inp
#        print "position = ", self.position

        ran = range(len(inp) - codec2_frame_len*bits_per_byte + 1)
        for i in ran:
            tags = self.get_tags_in_window(0, i, i+1, self.tag)
            if tags:
                # syncword received
#                print "RESET!"
                self.position = 0
#                print inp[i:]
            if self.position >= packet_len*bits_per_byte:
                self.position = -1
            if self.position == -1:
                continue
            if self.position % bits_per_byte == 0:
                if (self.position/bits_per_byte + 4) % chunk_len == chunk_len-codec2_frame_len:
                    codec2 = array.array('B', inp[i:i+codec2_frame_len*bits_per_byte])
                    self.message_port_pub(pmt.intern('codec2'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(codec2), codec2)))
                elif (self.position/bits_per_byte + 4) % chunk_len < chunk_len-codec2_frame_len:
                    kiss = array.array('B', inp[i:i+bits_per_byte])
                    self.message_port_pub(pmt.intern('kiss'), pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(kiss), kiss)))
            self.position += 1

        return len(ran)

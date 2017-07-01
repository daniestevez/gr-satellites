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

import numpy
from gnuradio import gr
import pmt

import collections

class fixedlen_tagger(gr.basic_block):
    """
    docstring for block fixedlen_tagger
    """
    def __init__(self, syncword_tag, packetlen_tag, packet_len, stream_type):
        gr.basic_block.__init__(self,
            name="fixedlen_tagger",
            in_sig=[stream_type],
            out_sig=[stream_type])
        self.syncword_tag = pmt.string_to_symbol(syncword_tag)
        self.packetlen_tag = pmt.string_to_symbol(packetlen_tag)
        self.packet_len = packet_len
        self.stream = collections.deque(maxlen=packet_len - 1)
        self.maxtag = -1
        self.data = []
        self.tags = []
        self.tags_to_write = []
        self.written = 0
        self.really_written = 0

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        window = list(self.stream) + inp.tolist()
        
        alltags = self.get_tags_in_range(0, self.maxtag + 1, self.nitems_read(0) + len(inp), self.syncword_tag)
        for tag in alltags:
            if tag.offset not in self.tags:
                self.maxtag = max(self.maxtag, tag.offset)
                self.tags.append(tag.offset)
        tags = self.tags[:] # modifying self.tags during the loop could disturb the loop control, so we copy it
        for tag in tags:
            if (tag >= self.nitems_read(0) - len(self.stream)) and (tag < self.nitems_read(0) + len(inp) - self.packet_len + 1):
                self.tags.remove(tag)
                start = tag - self.nitems_read(0) + len(self.stream)
                packet = window[start : start + self.packet_len]
                self.data += packet
                self.tags_to_write.append(self.written)
                self.written += self.packet_len

        self.stream.extend(inp.tolist())

        len_write = min(len(self.data), len(out))
        out[:len_write] = self.data[:len_write]
        self.data = self.data[len_write:]
        self.really_written += len_write

        tags = self.tags_to_write[:] # again, this is to avoid disturbing the loop
        for tag in tags:
            if tag < self.really_written:
                self.tags_to_write.remove(tag)
                self.add_item_tag(0, tag, self.packetlen_tag, pmt.from_long(self.packet_len))
                
        self.consume(0, len(inp))
        return len_write

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import collections

import numpy
from gnuradio import gr
import pmt


class fixedlen_tagger(gr.basic_block):
    """
    docstring for block fixedlen_tagger
    """
    def __init__(self, syncword_tag, packetlen_tag, packet_len, stream_type):
        gr.basic_block.__init__(
            self,
            name='fixedlen_tagger',
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

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.stream.maxlen = self.packet_len

    def try_to_flush(self, out):
        # Try to send as much items as we have in buffer
        len_write = min(len(self.data), len(out))
        out[:len_write] = self.data[:len_write]
        self.data = self.data[len_write:]
        self.really_written += len_write

        for tag in self.tags_to_write[:]:
            # Modifying self.tags_to_write during the loop would
            # disturb the loop control, so we copy it
            if tag < self.really_written:
                self.tags_to_write.remove(tag)
                self.add_item_tag(0, tag, self.packetlen_tag,
                                  pmt.from_long(self.packet_len))

        return len_write

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        if self.data:
            # Write as much as possible without consuming input
            return self.try_to_flush(out)

        window = list(self.stream) + inp.tolist()

        alltags = self.get_tags_in_range(0, self.maxtag + 1,
                                         self.nitems_read(0) + len(inp),
                                         self.syncword_tag)
        for tag in alltags:
            if tag.offset not in self.tags:
                self.maxtag = max(self.maxtag, tag.offset)
                self.tags.append(tag.offset)
        for tag in self.tags[:]:
            # Modifying self.tags during the loop would disturb the
            # loop control, so we copy it
            if (tag >= self.nitems_read(0) - len(self.stream)
                    and
                    tag < self.nitems_read(0) + len(inp)
                    - self.packet_len + 1):
                self.tags.remove(tag)
                start = tag - self.nitems_read(0) + len(self.stream)
                packet = window[start:start+self.packet_len]
                self.data += packet
                self.tags_to_write.append(self.written)
                self.written += self.packet_len

        self.stream.extend(inp.tolist())

        self.consume(0, len(inp))
        return self.try_to_flush(out)

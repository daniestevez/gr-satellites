#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from .imagereceiver import ImageReceiver


block_size = 46

swiatowid_image_block = Struct(
    'sequence' / Int16ul,
    'data' / Bytes(block_size)
    )


class ImageReceiverSwiatowid(ImageReceiver):
    def filename(self, fid):
        return f'{fid}.jpg'

    def chunk_size(self):
        return block_size

    def parse_chunk(self, chunk):
        if len(chunk) != swiatowid_image_block.sizeof():
            return None
        try:
            frame = swiatowid_image_block.parse(chunk)
        except ConstructError:
            return None
        return frame


swiatowid = ImageReceiverSwiatowid

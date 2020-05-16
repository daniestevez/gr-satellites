#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct.core import ConstructError

from .imagereceiver import ImageReceiver
from ..telemetry import by70_1 as tlm

class ImageReceiverBY701(ImageReceiver):
    def filename(self, fid):
        return f'{fid}.jpg'

    def parse_chunk(self, chunk):
        try:
            frame = tlm.parse(chunk)
        except ConstructError:
            return None
        return frame.camera

by70_1 = ImageReceiverBY701

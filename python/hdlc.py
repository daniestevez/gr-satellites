#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy

from . import crc as _crc_module

_crc_fn = _crc_module(16, 0x1021, 0xffff, 0xffff, True, True)

flag = bytes([0] + 6*[1] + [0])


def crc_ccitt(data):
    return _crc_fn.compute(list(data))

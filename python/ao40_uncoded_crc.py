#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from . import crc as _crc_module

_crc_fn = _crc_module(16, 0x1021, 0xffff, 0x0, False, False)


def crc(data):
    return _crc_fn.compute(list(data))

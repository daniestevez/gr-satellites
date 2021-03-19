#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from .ax25 import Frame

usp = Struct(
    'ethertype' / Hex(Int16ub),
    'length' / Int16ul,
    'ax25' / Frame
    )

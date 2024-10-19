#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2024 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from .ccsds import SpacePacketPrimaryHeader

asrtu = Struct(
    'primary_header' / SpacePacketPrimaryHeader,
    'payload' / Hex(GreedyBytes),
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from ..ccsds.telemetry import PrimaryHeader, OCFTrailer


trisat = Struct(
    'tm_primary_header' / PrimaryHeader,
    'payload' / Bytes(211),
    'ocf' / OCFTrailer,
    'crc' / Int16ub
    )

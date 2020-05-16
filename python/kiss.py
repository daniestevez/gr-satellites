#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy

FEND = numpy.uint8(0xc0)
FESC = numpy.uint8(0xdb)
TFEND = numpy.uint8(0xdc)
TFESC = numpy.uint8(0xdd)

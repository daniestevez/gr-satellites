#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

'''
gr-satellites datasource components

The datasources read frames or packets from some source, such
as a KISS file

The output of these blocks are PDUs with the frames.
'''

from .kiss_file_source import kiss_file_source

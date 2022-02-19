#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# This gives a wrapper around gnuradio.pdu (GNU Radio 3.10)
# and gnuradio.blocks (GNU Radio 3.9), so that the same gr-satellites
# code base can work with both versions of GNU Radio

from gnuradio import gr

api_version = int(gr.api_version())
if api_version == 9:
    from gnuradio.blocks import tagged_stream_to_pdu, pdu_to_tagged_stream
elif api_version >= 10:
    from gnuradio.pdu import tagged_stream_to_pdu, pdu_to_tagged_stream
else:
    raise ValueError('unsupported GNU Radio API version', api_version)

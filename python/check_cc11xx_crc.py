#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr

from .crcs import crc16_cc11xx


class check_cc11xx_crc(gr.hier_block2):
    """Deprecated. Use satellites.crc16_cc11xx() from crcs.py instead."""
    def __init__(self, verbose=False):
        gr.hier_block2.__init__(
            self,
            name='check_cc11xx_crc',
            input_signature=gr.io_signature(0, 0, 0),
            output_signature=gr.io_signature(0, 0, 0))

        self._crc = crc16_cc11xx(discard_crc=True)

        self.message_port_register_hier_in('in')
        self.message_port_register_hier_out('ok')
        self.message_port_register_hier_out('fail')

        self.msg_connect(self, 'in', self._crc, 'in')
        self.msg_connect(self._crc, 'ok', self, 'ok')
        self.msg_connect(self._crc, 'fail', self, 'fail')

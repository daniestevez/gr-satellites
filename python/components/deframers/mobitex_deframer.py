#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import importlib

from gnuradio import gr, blocks, digital


class mobitex_deframer(gr.hier_block2):
    """
    Hierarchical block to deframe Mobitex and Mobitex-NX

    The input is a float stream of soft symbols. The output are PDUs
    with Mobitex-NX frames.

    This uses the gr-tnc_nx OOT module, but only attempts to import
    it when __init__() is called.

    Args:
        nx: use NX mode (boolean)
        options: Options from argparse
    """
    def __init__(self, nx=False, options=None):
        gr.hier_block2.__init__(
            self,
            'mobitex_deframer',
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_out('out')

        self.invert = blocks.multiply_const_ff(-1, 1)
        self.slicer = digital.binary_slicer_fb()
        try:
            tnc_nx = importlib.import_module('tnc_nx')
        except ImportError as e:
            print('Unable to import tnc_nx')
            print('gr-tnc_nx needs to be installed to use Mobitex')
            raise e
        syncword = 0x0ef0 if nx else 0x5765
        self.mobitex = tnc_nx.nx_decoder(syncword, nx)

        self.connect(self, self.invert, self.slicer, self.mobitex)
        self.msg_connect((self.mobitex, 'out'), (self, 'out'))

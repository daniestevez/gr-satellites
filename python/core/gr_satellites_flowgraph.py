#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Daniel Estevez <daniel@destevez.net>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from gnuradio import gr
from ..components import demodulators
from ..components import deframers
from ..components import datasinks

import functools

def set_options(cl, *args, **kwargs):
    """
    Given a class, returns a derived class with some fixed
    options set in the constructor.

    This is intended to generate GNU Radio blocks with some options set
    by deriving from blocks that allow for options.

    Args:
        cl: the base class to derive from (class)
        *args: arguments to pass to the __init__ method
        **kwargs: keyword arguments to pass to the __init__ method
    """
    class C(cl):
        __init__ = functools.partialmethod(cl.__init__, *args, **kwargs)

    return C

class gr_satellites_flowgraph(gr.hier_block2):
    """
    gr-satellites decoder flowgraph

    Uses a YAML file with a satellite description to create a
    hierarchical flowgraph for that satellite

    TODO: describe input and output
    """
    def __init__(self, satyaml, samp_rate):
        gr.hier_block2.__init__(self, "gr_satellites_flowgraph",
            gr.io_signature(1, 1, gr.sizeof_float),
            gr.io_signature(0, 0, 0))

        self.set_default_config()

        # TODO: contol all sorts of lookup errors
        self._datasinks = dict()
        for key, info in satyaml['data'].items():
            datasink = getattr(datasinks, info['decoder'])()
            self._datasinks[key] = datasink

        self._demodulators = dict()
        self._deframers = dict()
        for key, transmitter in satyaml['transmitters'].items():
            baudrate = transmitter['baudrate']
            demodulator = self.get_demodulator(transmitter['modulation'])(baudrate = baudrate, samp_rate = samp_rate)
            deframer = self.get_deframer(transmitter['framing'])()
            self.connect(self, demodulator, deframer)
            self._demodulators[key] = demodulator
            self._deframers[key] = deframer

            for data in transmitter['data']:
                self.msg_connect((deframer, 'out'), (self._datasinks[data], 'in'))

    def get_demodulator(self, modulation):
        return self._demodulator_hooks[modulation]

    def get_deframer(self, framing):
        return self._deframer_hooks[framing]
                    
    def set_default_config(self):
        """
        Sets default configuration parameters for the decoder
        """
        default_sync_threshold = 4
        self._demodulator_hooks = {
            'FSK' : demodulators.fsk_demodulator,
                             }
        self._deframer_hooks = {
            'AX.25' : set_options(deframers.ax25_deframer, g3ruh_scrambler = 'False'),
            'AX.25 G3RUH' : set_options(deframers.ax25_deframer, g3ruh_scrambler = 'True'),
            'AX100 ASM+Golay' : set_options(deframers.ax100_deframer, mode = 'ASM', syncword_threshold = default_sync_threshold),
            'AX100 Reed Solomon' : set_options(deframers.ax100_deframer, mode = 'RS', syncword_threshold = default_sync_threshold),
                          }

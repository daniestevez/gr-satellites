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
from ..components import datasources
from ..components import transports
from ..satyaml import yamlfiles

import functools
import yaml
import argparse
import itertools

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

def try_add_options(x, parser):
    """
    Given an object x, calls x.add_options(parser) if add_options
    is an attribute of x.

    Args:
       x: an object
       parser: an argparser ArgumentParser
    """
    if hasattr(x, 'add_options'):
        x.add_options(parser)
        
class gr_satellites_flowgraph(gr.hier_block2):
    """
    gr-satellites decoder flowgraph

    Uses a YAML file with a satellite description to create a
    hierarchical flowgraph for that satellite. There are two modes of
    operation. If this is called from GRC, then only demodulation and
    deframing is done, getting all messages to the 'out' output port. If
    this is not called from GRC, then messages are routed to data sinks
    as appropriate.

    Args:
        file: filename of the YAML file to load (string)
        name: satellite name to search in all YAML files (string)
        norad: NORAD ID to search in all YAML files (int)
        samp_rate: sample rate (float)
        iq: use IQ or real input (bool)
        grc_block: whether this is called from GRC (bool)
        options: options from argparser
        config: configuration file from configparser
        pdu_in: use PDU input instead of samples (bool)

    Note that exactly one of file, name and norad should be specified
    """
    def __init__(self, file = None, name = None, norad = None, samp_rate = None, iq = False,\
                 grc_block = False, options = None, config = None, pdu_in = False):
        gr.hier_block2.__init__(self, "gr_satellites_flowgraph",
            gr.io_signature(0, 0, 0) if pdu_in else \
              gr.io_signature(1, 1, gr.sizeof_gr_complex if iq else gr.sizeof_float),
            gr.io_signature(0, 0, 0))

        if pdu_in:
            self.message_port_register_hier_in('in')
        elif samp_rate is None:
            raise ValueError('samp_rate not specified')

        satyaml = self.open_satyaml(file, name, norad)

        # TODO: contol all sorts of lookup errors
        if grc_block:
            self.message_port_register_hier_out('out')
        else:
            self._datasinks = dict()
            self._additional_datasinks = list()
            if options.hexdump:
                self._additional_datasinks.append(datasinks.hexdump_sink())
            else:
                for key, info in satyaml['data'].items():
                    if 'decoder' in info:
                        ds = getattr(datasinks, info['decoder'])
                        try:
                            datasink = ds(options = options)
                        except TypeError: # raised if ds doesn't have an options parameter
                            datasink = ds()
                    elif 'telemetry' in info:
                        datasink = datasinks.telemetry_parser(info['telemetry'], options = options)
                    else:
                        datasink = datasinks.hexdump_sink()
                    self._datasinks[key] = datasink
            if options is not None and options.kiss_out:
                self._additional_datasinks.append(datasinks.kiss_file_sink(options.kiss_out, bool(options.kiss_append)))
            if config.getboolean('Groundstation', 'submit_tlm'):
                self._additional_datasinks.extend(self.get_telemetry_submitters(satyaml, config))
            self._transports = dict()
            if 'transports' in satyaml:
                for key, info in satyaml['transports'].items():
                    transport = self.get_transport(info['protocol'])()
                    self._transports[key] = transport
                    if not options.hexdump:
                        for data in info['data']:
                            self.msg_connect((transport, 'out'), (self._datasinks[data], 'in'))

        if pdu_in:
            for sink in itertools.chain(self._datasinks.values(), self._additional_datasinks):
                self.msg_connect((self, 'in'), (sink, 'in'))
        else:
            self._demodulators = dict()
            self._deframers = dict()
            for key, transmitter in satyaml['transmitters'].items():
                baudrate = transmitter['baudrate']
                demodulator_additional_options = dict()
                try:
                    demodulator_additional_options['deviation'] = transmitter['deviation']
                    demodulator_additional_options['af_carrier'] = transmitter['af_carrier']
                except KeyError:
                    pass
                demodulator = self.get_demodulator(transmitter['modulation'])(baudrate = baudrate, samp_rate = samp_rate, iq = iq, options = options, **demodulator_additional_options)
                deframer_additional_options = dict()
                try:
                    deframer_additional_options['frame_size'] = transmitter['frame size']
                except KeyError:
                    pass
                deframer = self.get_deframer(transmitter['framing'])(options = options, **deframer_additional_options)
                self.connect(self, demodulator, deframer)
                self._demodulators[key] = demodulator
                self._deframers[key] = deframer

                if grc_block:
                    self.msg_connect((deframer, 'out'), (self, 'out'))
                else:
                    if not options.hexdump:
                        if 'data' in transmitter:
                            for data in transmitter['data']:
                                self.msg_connect((deframer, 'out'), (self._datasinks[data], 'in'))
                        if 'transports' in transmitter:
                            for transport in transmitter['transports']:
                                self.msg_connect((deframer, 'out'), (self._transports[transport], 'in'))
                    for s in self._additional_datasinks:
                        self.msg_connect((deframer, 'out'), (s, 'in'))
                    if 'additional_data' in transmitter:
                        for k, v in transmitter['additional_data'].items():
                            self.msg_connect((deframer, k), (self._datasinks[v], 'in'))

    def get_telemetry_submitters(self, satyaml, config):
        """
        Returns a list of block instances of telemetry submitters appropriate for this satellite

        Args:
            satyaml: satellite YAML file, as returned by self.open_satyaml
            config: configuration file from configparser
        """
        norad = satyaml['norad']
        submitters = [datasinks.telemetry_submit('SatNOGS', norad, config)]
        for server in satyaml.get('telemetry_servers', []):
            submitters.append(datasinks.telemetry_submit(server, norad, config))
        return submitters

    def get_demodulator(self, modulation):
        return self._demodulator_hooks[modulation]

    def get_deframer(self, framing):
        return self._deframer_hooks[framing]

    def get_transport(self, protocol):
        return self._transport_hooks[protocol]

    @staticmethod
    def open_satyaml(file, name, norad):
        if sum([x is not None for x in [file, name, norad]]) != 1:
            raise ValueError('exactly one of file, name and norad needs to be specified')
        
        if file is not None:
            satyaml = yamlfiles.get_yamldata(file)
        elif name is not None:
            satyaml = yamlfiles.search_name(name)
        else:
            satyaml = yamlfiles.search_norad(norad)

        return satyaml

    @classmethod
    def add_options(cls, parser, file = None, name = None, norad = None):
        satyaml = cls.open_satyaml(file, name, norad)

        demod_options = parser.add_argument_group('demodulation')
        deframe_options = parser.add_argument_group('deframing')
        data_options = parser.add_argument_group('data sink')

        for info in satyaml['data'].values():
            if 'decoder' in info:
                try_add_options(getattr(datasinks, info['decoder']), data_options)
            if 'telemetry' in info:
                try_add_options(datasinks.telemetry_parser, data_options)
    
        for transmitter in satyaml['transmitters'].values():
            try_add_options(cls._demodulator_hooks[transmitter['modulation']], demod_options)
            try_add_options(cls._deframer_hooks[transmitter['framing']], deframe_options)

    # Default parameters
    _demodulator_hooks = {
        'AFSK' : demodulators.afsk_demodulator,
        'FSK' : demodulators.fsk_demodulator,
        'BPSK' : demodulators.bpsk_demodulator,
        'BPSK Manchester' : set_options(demodulators.bpsk_demodulator, manchester = True),
        'DBPSK' : set_options(demodulators.bpsk_demodulator, differential = True),
        'DBPSK Manchester' : set_options(demodulators.bpsk_demodulator, differential = True, manchester = True),
    }
    _deframer_hooks = {
        'AX.25' : set_options(deframers.ax25_deframer, g3ruh_scrambler = False),
        'AX.25 G3RUH' : set_options(deframers.ax25_deframer, g3ruh_scrambler = True),
        'AX100 ASM+Golay' : set_options(deframers.ax100_deframer, mode = 'ASM'),
        'AX100 Reed Solomon' : set_options(deframers.ax100_deframer, mode = 'RS'),
        '3CAT-1' : deframers.sat_3cat_1_deframer,
        'Astrocast FX.25 NRZ-I' : set_options(deframers.astrocast_fx25_deframer, nrzi = True),
        'Astrocast FX.25 NRZ' : set_options(deframers.astrocast_fx25_deframer, nrzi = False),
        'Astrocast 9k6' : deframers.astrocast_9k6_deframer,
        'AO-40 FEC' : deframers.ao40_fec_deframer,
        'AO-40 uncoded' : deframers.ao40_uncoded_deframer,
        'TT-64' : deframers.tt64_deframer,
        'ESEO' : deframers.eseo_deframer,
        'Lucky-7' : deframers.lucky7_deframer,
        'Reaktor Hello World' : deframers.reaktor_hello_world_deframer,
        'S-NET' : deframers.snet_deframer,
        'Swiatowid' : deframers.swiatowid_deframer,
        'NuSat' : deframers.nusat_deframer,
        'K2SAT' : deframers.k2sat_deframer,
        'CCSDS Reed-Solomon' : deframers.ccsds_rs_deframer,
        'CCSDS Reed-Solomon dual' : set_options(deframers.ccsds_rs_deframer, dual_basis = True),
        'CCSDS Reed-Solomon differential' : set_options(deframers.ccsds_rs_deframer, differential = True),
        'CCSDS Reed-Solomon dual differential' : set_options(deframers.ccsds_rs_deframer, differential = True, dual_basis = True),
        'CCSDS Concatenated' : deframers.ccsds_concatenated_deframer,
        'CCSDS Concatenated dual' : set_options(deframers.ccsds_concatenated_deframer, dual_basis = True),
        'CCSDS Concatenated differential' : set_options(deframers.ccsds_concatenated_deframer, differential = True),
        'CCSDS Concatenated dual differential' : set_options(deframers.ccsds_concatenated_deframer, differential = True, dual_basis = True),
        'LilacSat-1' : deframers.lilacsat_1_deframer,
        'AAUSAT-4' : deframers.aausat4_deframer,
        'NGHam' : set_options(deframers.ngham_deframer, decode_rs = True),
        'NGHam no Reed Solomon' : set_options(deframers.ngham_deframer, decode_rs = False),
    }
    _transport_hooks = {
        'KISS' : transports.kiss_transport,
        'KISS no control byte' : set_options(transports.kiss_transport, control_byte = False),
        'KISS KS-1Q' : set_options(transports.kiss_transport, control_byte = False, header_remove_bytes = 3),
    }

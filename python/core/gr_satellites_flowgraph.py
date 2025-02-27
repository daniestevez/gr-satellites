#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019-2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import argparse
import functools
import itertools
import os
import shlex
import yaml

from gnuradio import gr, zeromq
import pmt

from ..components import datasinks
from ..components import datasources
from ..components import deframers
from ..components import demodulators
from ..components import transports
from ..satyaml import yamlfiles
from .. import pdu_add_meta


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


def filter_translate_dict(d, key_translation):
    """
    Filter and translate the keys of a dictionary

    Args:
        d: a dictionary to filter and translate
        keys_translation: a dictionary of key translations
    """
    return {key_translation[k]: v
            for k, v in d.items() if k in key_translation}


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
        dump_path: Path to dump internal signals to files (str)

    Note that exactly one of file, name and norad should be specified
    """
    def __init__(self, file=None, name=None, norad=None,
                 samp_rate=None, iq=False, grc_block=False,
                 options=None, config=None, pdu_in=False,
                 dump_path=None):
        gr.hier_block2.__init__(
            self,
            'gr_satellites_flowgraph',
            gr.io_signature(0, 0, 0)
            if pdu_in else
            gr.io_signature(1, 1,
                            gr.sizeof_gr_complex
                            if iq else gr.sizeof_float),
            gr.io_signature(0, 0, 0))

        self.samp_rate = samp_rate
        self.iq = iq
        self.grc_block = grc_block
        self.dump_path = dump_path
        self.config = config

        # Load up options, similarly to option block
        if type(options) is str:
            p = argparse.ArgumentParser(prog=self.__class__.__name__,
                                        conflict_handler='resolve')
            gr_satellites_flowgraph.add_options(p, file, name, norad)
            options = p.parse_args(shlex.split(options))

        self.options = options

        if pdu_in:
            self.message_port_register_hier_in('in')
        elif samp_rate is None:
            raise ValueError('samp_rate not specified')

        self.satyaml = satyaml = yamlfiles.open_satyaml(file, name, norad)

        if grc_block:
            self.message_port_register_hier_out('out')
        else:
            self._datasinks = dict()
            self._additional_datasinks = list()
            do_telemetry = not (self.options is not None
                                and self.options.hexdump)
            for key, info in satyaml['data'].items():
                is_telemetry = ('telemetry' in info
                                or info == 'unknown')
                if not is_telemetry or do_telemetry:
                    self._init_datasink(key, info)
            self._init_additional_datasinks()
            self._transports = dict()
            if 'transports' in satyaml:
                for key, info in satyaml['transports'].items():
                    self._init_transport(key, info)

        if pdu_in:
            for sink in itertools.chain(
                    self._datasinks.values(), self._additional_datasinks):
                self.msg_connect((self, 'in'), (sink, 'in'))
        else:
            self._demodulators = dict()
            self._deframers = dict()
            self._taggers = dict()
            for key, transmitter in satyaml['transmitters'].items():
                self._init_demodulator_deframer(key, transmitter)

    def _init_datasink(self, key, info):
        """Initialize a datasink

        Initializes a datasink according to a SatYAML entry

        Args:
            key: the name of the datasink entry in SatYAML
            info: the body of the datasink entry in SatYAML
        """
        if 'decoder' in info:
            ds = getattr(datasinks, info['decoder'])
            try:
                datasink = ds(options=self.options)
            except TypeError:  # raised if ds doesn't have an options parameter
                datasink = ds()
        elif 'telemetry' in info:
            datasink = datasinks.telemetry_parser(info['telemetry'],
                                                  options=self.options)
        elif 'files' in info:
            datasink = datasinks.file_receiver(info['files'],
                                               options=self.options)
        elif 'image' in info:
            datasink = datasinks.file_receiver(
                info['image'], options=self.options, display=True)
        else:
            datasink = datasinks.hexdump_sink()
        self._datasinks[key] = datasink

    def _init_additional_datasinks(self):
        """Initialize additional datasinks

        Creates all the datasinks that are not explicitly indicated
        in the SatYAML (telemetry submit, KISS output, etc.)
        """
        if self.options is not None and self.options.kiss_out:
            self._additional_datasinks.append(
                datasinks.kiss_file_sink(self.options.kiss_out,
                                         bool(self.options.kiss_append),
                                         options=self.options))
        if self.options is not None and self.options.kiss_server:
            self._additional_datasinks.append(
                datasinks.kiss_server_sink(self.options.kiss_server_address,
                                           self.options.kiss_server,
                                           options=self.options))
        if self.options is not None and self.options.zmq_pub:
            self._additional_datasinks.append(
                zeromq.pub_msg_sink(self.options.zmq_pub))

        # The GR_SATELLITES_SUBMIT_TLM environment variable takes precendence
        # over the configuration to choose whether to enable telemetry
        # submission
        tlm_env = os.environ.get('GR_SATELLITES_SUBMIT_TLM')
        if tlm_env is not None:
            tlm_submit = bool(int(tlm_env))
        else:
            tlm_submit = self.config.getboolean('Groundstation', 'submit_tlm')
        if tlm_submit:
            self._additional_datasinks.extend(
                self.get_telemetry_submitters(self.satyaml, self.config,
                                              self.options))

        if self.options is not None and self.options.hexdump:
            self._additional_datasinks.append(datasinks.hexdump_sink())

    def _init_transport(self, key, info):
        """Initialize a transport

        Initializes a transport according to a SatYAML entry and connects
        it to the appropriate datasink

        Args:
            key: the name of the transport entry in SatYAML
            info: the body of the transport entry in SatYAML
        """
        if 'virtual_channels' in info:
            args = {'virtual_channels': info['virtual_channels']}
        else:
            args = {}
        transport = self.get_transport(info['protocol'])(**args)
        self._transports[key] = transport
        if not self.options.hexdump:
            for data in info['data']:
                self.msg_connect(
                    (transport, 'out'), (self._datasinks[data], 'in'))

    def _init_demodulator_deframer(self, key, transmitter):
        """Initialize a demodulator and deframer

        Creates a demodulator and deframer according to a SatYAML
        entry and connects the deframer to the data and transports

        Args:
            key: name of the transmitter entry in the SatYAML
            transmitter: transmitter entry in the SatYAML
        """
        baudrate = transmitter['baudrate']
        demod_options = ['deviation', 'fm_deviation', 'af_carrier']
        demod_options = {k: k for k in demod_options}
        demodulator_additional_options = filter_translate_dict(transmitter,
                                                               demod_options)
        demodulator = self.get_demodulator(transmitter['modulation'])(
            baudrate=baudrate, samp_rate=self.samp_rate, iq=self.iq,
            dump_path=self.dump_path, options=self.options,
            **demodulator_additional_options)
        deframe_options = {
            'frame size': 'frame_size',
            'precoding': 'precoding',
            'RS basis': 'rs_basis',
            'RS interleaving': 'rs_interleaving',
            'convolutional': 'convolutional',
            'scrambler': 'scrambler',
            }
        deframer_additional_options = filter_translate_dict(transmitter,
                                                            deframe_options)
        deframer = self.get_deframer(transmitter['framing'])(
            options=self.options, **deframer_additional_options)
        self.connect(self, demodulator, deframer)
        self._demodulators[key] = demodulator
        self._deframers[key] = deframer

        self._connect_transmitter_to_data(key, transmitter, deframer)

    def _connect_transmitter_to_data(self, key, transmitter, deframer):
        """Connect a deframer to the datasinks and transports

        Connects a deframer to the datasinks and transports indicated in
        the SatYAML file

        Args:
            transmitter: the transmitter entry in SatYAML
            deframer: the deframer to connect
        """
        # Add a tagger
        meta = pmt.make_dict()
        meta = pmt.dict_add(meta, pmt.intern('transmitter'),
                            pmt.intern(key))
        tagger = pdu_add_meta(meta)
        self._taggers[key] = tagger
        self.msg_connect((deframer, 'out'), (tagger, 'in'))

        if self.grc_block:
            # If we are a GRC block we have no datasinks
            # so we connect directly to our output
            self.msg_connect((tagger, 'out'), (self, 'out'))
            return

        for s in self._additional_datasinks:
            self.msg_connect((tagger, 'out'), (s, 'in'))
        for data in transmitter.get('data', []):
            if data in self._datasinks:
                # The datasink may not exist if it's a telemetry parser
                # and we're running in hexdump mode
                self.msg_connect(
                    (tagger, 'out'), (self._datasinks[data], 'in'))
        for transport in transmitter.get('transports', []):
            self.msg_connect(
                (tagger, 'out'), (self._transports[transport], 'in'))

        if 'additional_data' in transmitter:
            for k, v in transmitter['additional_data'].items():
                # Add a tagger
                tagger = pdu_add_meta(meta)
                self._taggers[(key, k)] = tagger
                self.msg_connect((deframer, k), (tagger, 'in'))
                self.msg_connect((tagger, 'out'), (self._datasinks[v], 'in'))

    def get_telemetry_submitters(self, satyaml, config, options):
        """
        Returns a list of block instances of telemetry submitters

        The telemetry submitters are those appropriate for this satellite

        Args:
            satyaml: satellite YAML file, as returned by yamlfiles.open_satyaml
            config: configuration file from configparser
        """
        norad = satyaml['norad']
        submitters = [
            datasinks.telemetry_submit(
                'SatNOGS', norad=norad, config=config, options=options)]
        for server in satyaml.get('telemetry_servers', []):
            port = None
            url = None
            if server.startswith('HIT '):
                port = server.split()[1]
                server = 'HIT'
            elif server.startswith('SIDS '):
                url = server.split()[1]
                server = 'SIDS'
            submitters.append(datasinks.telemetry_submit(
                server, norad=norad, port=port, url=url, config=config,
                options=options))
        return submitters

    def get_demodulator(self, modulation):
        return self._demodulator_hooks[modulation]

    def get_deframer(self, framing):
        return self._deframer_hooks[framing]

    def get_transport(self, protocol):
        return self._transport_hooks[protocol]

    @classmethod
    def add_options(cls, parser, file=None, name=None, norad=None):
        satyaml = yamlfiles.open_satyaml(file, name, norad)

        demod_options = parser.add_argument_group('demodulation')
        deframe_options = parser.add_argument_group('deframing')
        data_options = parser.add_argument_group('data sink')

        for info in satyaml['data'].values():
            if 'decoder' in info:
                try_add_options(getattr(datasinks, info['decoder']),
                                data_options)
            if 'telemetry' in info:
                try_add_options(datasinks.telemetry_parser, data_options)
            if 'files' in info or 'image' in info:
                try_add_options(datasinks.file_receiver, data_options)

        for transmitter in satyaml['transmitters'].values():
            try_add_options(cls._demodulator_hooks[transmitter['modulation']],
                            demod_options)
            try_add_options(cls._deframer_hooks[transmitter['framing']],
                            deframe_options)

    # Default parameters
    _demodulator_hooks = {
        'AFSK': demodulators.afsk_demodulator,
        'FSK': demodulators.fsk_demodulator,
        'BPSK': demodulators.bpsk_demodulator,
        'BPSK Manchester': set_options(demodulators.bpsk_demodulator,
                                       manchester=True),
        'DBPSK': set_options(demodulators.bpsk_demodulator,
                             differential=True),
        'DBPSK Manchester': set_options(demodulators.bpsk_demodulator,
                                        differential=True, manchester=True),
        'FSK subaudio': set_options(demodulators.fsk_demodulator,
                                    subaudio=True),
        }
    _deframer_hooks = {
        'AX.25': set_options(deframers.ax25_deframer, g3ruh_scrambler=False),
        'AX.25 G3RUH': set_options(deframers.ax25_deframer,
                                   g3ruh_scrambler=True),
        'AX100 ASM+Golay': set_options(deframers.ax100_deframer, mode='ASM'),
        'AX100 Reed Solomon': set_options(deframers.ax100_deframer,
                                          mode='RS'),
        '3CAT-1': deframers.sat_3cat_1_deframer,
        'Astrocast FX.25 NRZ-I': set_options(deframers.astrocast_fx25_deframer,
                                             nrzi=True),
        'Astrocast FX.25 NRZ': set_options(deframers.astrocast_fx25_deframer,
                                           nrzi=False),
        'AO-40 FEC': deframers.ao40_fec_deframer,
        'AO-40 FEC short': set_options(deframers.ao40_fec_deframer,
                                       short_frames=True),
        'AO-40 FEC CRC-16-ARC': set_options(deframers.ao40_fec_deframer,
                                            crc=True),
        'AO-40 FEC CRC-16-ARC short': set_options(deframers.ao40_fec_deframer,
                                                  short_frames=True,
                                                  crc=True),
        'AO-40 uncoded': deframers.ao40_uncoded_deframer,
        'TT-64': deframers.tt64_deframer,
        'ESEO': deframers.eseo_deframer,
        'Lucky-7': deframers.lucky7_deframer,
        'Reaktor Hello World': deframers.reaktor_hello_world_deframer,
        'S-NET': deframers.snet_deframer,
        'SALSAT': set_options(deframers.snet_deframer, buggy_crc=False),
        'Swiatowid': deframers.swiatowid_deframer,
        'NuSat': deframers.nusat_deframer,
        'K2SAT': deframers.k2sat_deframer,
        'CCSDS Reed-Solomon': deframers.ccsds_rs_deframer,
        'CCSDS Concatenated': deframers.ccsds_concatenated_deframer,
        'CCSDS Uncoded': set_options(deframers.ccsds_rs_deframer, rs_en=False),
        'LilacSat-1': deframers.lilacsat_1_deframer,
        'AAUSAT-4': deframers.aausat4_deframer,
        'NGHam': set_options(deframers.ngham_deframer, decode_rs=True),
        'NGHam no Reed Solomon': set_options(deframers.ngham_deframer,
                                             decode_rs=False),
        'SMOG-P RA': deframers.smogp_ra_deframer,
        'SMOG-1 RA': set_options(deframers.smogp_ra_deframer,
                                 variant='SMOG-1'),
        'MRC-100 RA': set_options(deframers.smogp_ra_deframer,
                                  variant='MRC-100'),
        'SMOG-P Signalling': deframers.smogp_signalling_deframer,
        'SMOG-1 Signalling': set_options(deframers.smogp_signalling_deframer,
                                         new_protocol=True),
        'OPS-SAT': deframers.ops_sat_deframer,
        'U482C': deframers.u482c_deframer,
        'UA01': deframers.ua01_deframer,
        'Mobitex': deframers.mobitex_deframer,
        'Mobitex-NX': set_options(deframers.mobitex_deframer, nx=True),
        'TUBIN': set_options(
            deframers.mobitex_deframer, nx=True, callsign='DP0TBN',
            callsign_threshold=12),
        'BEESAT-1': set_options(
            deframers.mobitex_deframer, nx=True, variant='BEESAT-1',
            callsign='DP0BEE', callsign_threshold=12),
        'BEESAT-9': set_options(
            deframers.mobitex_deframer, nx=True, variant='BEESAT-9',
            callsign='DP0BEM', callsign_threshold=12),
        'FOSSASAT': deframers.fossasat_deframer,
        'AISTECHSAT-2': deframers.aistechsat_2_deframer,
        'AALTO-1': deframers.aalto1_deframer,
        'Grizu-263A': deframers.grizu263a_deframer,
        'IDEASSat': deframers.ideassat_deframer,
        'YUSAT': deframers.yusat_deframer,
        'AX5043': deframers.ax5043_deframer,
        'USP': deframers.usp_deframer,
        'DIY-1': deframers.diy1_deframer,
        'BINAR-1': deframers.binar1_deframer,
        'BINAR-2': deframers.binar2_deframer,
        'Endurosat': deframers.endurosat_deframer,
        'SanoSat': deframers.sanosat_deframer,
        'FORESAIL-1': set_options(
            deframers.ax100_deframer,
            mode='ASM',
            syncword='00011010110011111111110000011101'),
        'HSU-SAT1': deframers.hsu_sat1_deframer,
        'GEOSCAN': deframers.geoscan_deframer,
        'Light-1': set_options(
            deframers.reaktor_hello_world_deframer,
            syncword='light-1'),
        'SPINO': deframers.spino_deframer,
        'QUBIK': deframers.qubik_deframer,
        'OpenLST': deframers.openlst_deframer,
        'HADES-D': set_options(deframers.hades_deframer, satellite='HADES-D'),
        'HADES-R': set_options(deframers.hades_deframer, satellite='HADES-R'),
        }
    _transport_hooks = {
        'KISS': transports.kiss_transport,
        'KISS no control byte': set_options(transports.kiss_transport,
                                            control_byte=False),
        'KISS KS-1Q': set_options(transports.kiss_transport,
                                  control_byte=False, header_remove_bytes=3),
        'TM KISS': transports.tm_kiss_transport,
        'TM short KISS': set_options(transports.tm_kiss_transport,
                                     short_tm=True),
        }

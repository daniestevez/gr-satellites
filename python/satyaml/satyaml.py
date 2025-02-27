#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019-2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import pathlib
import string
import yaml


class YAMLError(Exception):
    def __init__(self, message):
        self.message = message


_default_path = pathlib.Path(__file__).parent


class SatYAML:
    def __init__(self, path=_default_path):
        self._path = pathlib.Path(path)
    modulations = [
        'AFSK', 'FSK', 'BPSK', 'BPSK Manchester', 'DBPSK',
        'DBPSK Manchester', 'FSK subaudio',
        ]
    framings = [
        'AX.25', 'AX.25 G3RUH', 'AX100 ASM+Golay', 'AX100 Reed Solomon',
        '3CAT-1', 'Astrocast FX.25 NRZ-I', 'Astrocast FX.25 NRZ',
        'AO-40 FEC', 'AO-40 FEC short', 'AO-40 uncoded', 'TT-64', 'ESEO',
        'Lucky-7', 'Reaktor Hello World', 'S-NET', 'Swiatowid', 'NuSat',
        'K2SAT', 'CCSDS Reed-Solomon', 'CCSDS Concatenated', 'CCSDS Uncoded',
        'LilacSat-1', 'AAUSAT-4', 'NGHam', 'NGHam no Reed Solomon',
        'SMOG-P RA', 'SMOG-1 RA', 'SMOG-P Signalling', 'SMOG-1 Signalling',
        'MRC-100 RA',
        'OPS-SAT', 'U482C', 'UA01', 'SALSAT', 'Mobitex', 'Mobitex-NX',
        'FOSSASAT', 'AISTECHSAT-2', 'AALTO-1', 'Grizu-263A', 'IDEASSat',
        'YUSAT', 'AX5043', 'USP', 'AO-40 FEC CRC-16-ARC',
        'AO-40 FEC CRC-16-ARC short', 'DIY-1', 'BINAR-1', 'Endurosat',
        'SanoSat', 'FORESAIL-1', 'HSU-SAT1', 'GEOSCAN', 'Light-1',
        'SPINO', 'QUBIK', 'BINAR-2', 'OpenLST', 'HADES-D', 'HADES-R',
        'TUBIN', 'BEESAT-1', 'BEESAT-9',
        ]
    transports = [
        'KISS', 'KISS no control byte', 'KISS KS-1Q', 'TM KISS',
        'TM short KISS',
        ]
    top_level_words = [
        'name', 'alternative_names', 'norad', 'telemetry_servers',
        'data', 'transports', 'transmitters',
        ]

    def check_yaml(self, yml):
        d = self.get_yamldata(yml)
        for word in d:
            if word not in self.top_level_words:
                raise YAMLError(f'Unknown word {word} in {yml}')
        if 'name' not in d:
            raise YAMLError(f'Missing name field in {yml}')
        if 'norad' not in d:
            raise YAMLError(f'Missing norad field in {yml}')
        if type(d['norad']) is not int:
            raise YAMLError(f'NORAD field does not contain a number in {yml}')
        if 'telemetry_servers' in d:
            for server in d['telemetry_servers']:
                if (server not in ['SatNOGS', 'FUNcube', 'PWSat', 'BME',
                                   'BMEWS']
                        and not server.startswith('HIT ')
                        and not server.startswith('SIDS ')):
                    raise YAMLError(f'Unknown telemetry server {server}')
        if 'data' not in d:
            raise YAMLError(f'Missing data field in {yml}')
        if 'transports' in d:
            for key, transport in d['transports'].items():
                if 'protocol' not in transport:
                    raise YAMLError(
                        f'Missing protocol field in transport {key}')
                if transport['protocol'] not in self.transports:
                    raise YAMLError(
                        f'Unknown protocol field in transport {key}')
                if transport['protocol'] in ['TM KISS', 'TM short KISS']:
                    if 'virtual_channels' not in transport:
                        raise YAMLError(
                            f'virtual_channels field missing in '
                            f'transport {key}')
                    if not isinstance(transport['virtual_channels'], list):
                        raise YAMLError('virtual_channels is not a list')
                    for vc in transport['virtual_channels']:
                        if not isinstance(vc, int):
                            raise YAMLError(
                                'virtual_channel value is not an int')
        if 'transmitters' not in d:
            raise YAMLError(f'Missing transmitters field in {yml}')
        for key, transmitter in d['transmitters'].items():
            if 'frequency' not in transmitter:
                raise YAMLError(f'Missing frequency field in {key} in {yml}')
            if type(transmitter['frequency']) not in [float, int]:
                raise YAMLError(
                    'Frequency field does not contain a float '
                    f'in {key} in {yml}')
            if 'modulation' not in transmitter:
                raise YAMLError(f'Missing modulation field in {key} in {yml}')
            if transmitter['modulation'] not in self.modulations:
                raise YAMLError(f'Unknown modulation in {key} in {yml}')
            if 'baudrate' not in transmitter:
                raise YAMLError(f'Missing baudrate field in {key} in {yml}')
            if type(transmitter['baudrate']) not in [float, int]:
                raise YAMLError(
                    'Baudrate field does not contain a float in '
                    f'{key} in {yml}')
            if transmitter['modulation'] == 'AFSK':
                if 'af_carrier' not in transmitter:
                    raise YAMLError(
                        f'Missing af_carrier field for AFSK in {key} in {yml}')
                if 'deviation' not in transmitter:
                    raise YAMLError(
                        f'Missing deviation field for AFSK in {key} in {yml}')
            if ('af_carrier' in transmitter
                    and type(transmitter['af_carrier']) not in [float, int]):
                raise YAMLError(
                    'af_carrier field does not contain a float '
                    f'in {key} in {yml}')
            if ('deviation' in transmitter
                    and type(transmitter['deviation']) not in [float, int]):
                raise YAMLError(
                    'Deviation field does not contain a float '
                    f'in {key} in {yml}')
            if ('fm_deviation' in transmitter
                    and type(transmitter['fm_deviation']) not in [float, int]):
                raise YAMLError(
                    'FM deviation field does not contain a float '
                    f'in {key} in {yml}')
            if 'framing' not in transmitter:
                raise YAMLError(f'Missing framing field in {key} in {yml}')
            if transmitter['framing'] not in self.framings:
                raise YAMLError(f'Unknown framing in {key} in {yml}')
            if transmitter['framing'] in ['CCSDS Reed-Solomon',
                                          'CCSDS Concatenated']:
                if 'RS basis' not in transmitter:
                    raise YAMLError(f'No RS basis field in {key} in {yml}')
                if ('precoding' in transmitter
                        and transmitter['precoding'] != 'differential'):
                    raise YAMLError(
                        f'Invalid precoding value {transmitter["precoding"]} '
                        f'for {key} in {yml}')
                if transmitter['RS basis'] not in ['conventional', 'dual']:
                    raise YAMLError(
                        f'Invalid RS basis value {transmitter["RS basis"]} '
                        f'for {key} in {yml}')
                if ('RS interleaving' in transmitter
                        and type(transmitter['RS interleaving']) is not int):
                    raise YAMLError(
                        f'RS interleaving does not contain an int '
                        f'in {key} in {yml}')
                if ('scrambler' in transmitter
                        and transmitter['scrambler'] not in ['CCSDS', 'none']):
                    raise YAMLError(
                        f'Invalid scrambler value {transmitter["scrambler"]} '
                        f'for {key} in {yml}')
                if ('convolutional' in transmitter
                        and transmitter['convolutional'] not in [
                            'CCSDS', 'NASA-DSN', 'CCSDS uninverted',
                            'NASA-DSN uninverted']):
                    raise YAMLError(
                        'Invalid convolutional value '
                        f'{transmitter["convolutional"]} for {key} in {yml}')
            if 'data' not in transmitter and 'transports' not in transmitter:
                raise YAMLError(
                    f'No data or transport field in {key} in {yml}')
            if 'data' in transmitter:
                for dd in transmitter['data']:
                    if dd not in d['data']:
                        raise YAMLError(
                            f'Data entry {dd} used in {key} is not defined '
                            f'in data field in {yml}')
            if 'transport' in transmitter:
                for t in transmitter['transports']:
                    if t not in d['transports']:
                        raise YAMLError(
                            f'Transport entry {t} used in {key} is not '
                            f'defined in transports field in {yml}')
            if 'additional_data' in transmitter:
                for k, dd in transmitter['additional_data'].items():
                    if dd not in d['data']:
                        raise YAMLError(
                            f'Additional data entry {dd} used in {key} is not '
                            f'defined in data field in {yml}')

    def load_all_yaml(self):
        return [self.get_yamldata(f) for f in self.yaml_files()]

    def yaml_files(self):
        return self._path.glob('*.yml')

    def get_yamldata(self, yml):
        with open(yml, encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _get_satnames(self, yml):
        d = self.get_yamldata(yml)
        alternative = d.get('alternative_names', [])
        if alternative is None:
            alternative = []
        return [d['name']] + alternative

    def _get_satnorad(self, yml):
        d = self.get_yamldata(yml)
        return d['norad']

    def _canonical_name(self, name):
        """Perform some substitutions to match names which are loosely equal"""
        return ''.join([a for a in name.casefold()
                        if a not in string.punctuation + string.whitespace])

    def search_name(self, name):
        name = self._canonical_name(name)
        for yml in self.yaml_files():
            satnames = [self._canonical_name(n)
                        for n in self._get_satnames(yml)]
            if name in satnames:
                return self.get_yamldata(yml)
        raise ValueError('satellite not found')

    def search_norad(self, norad):
        for yml in self.yaml_files():
            if norad == self._get_satnorad(yml):
                return self.get_yamldata(yml)
        raise ValueError('satellite not found')

    def open_satyaml(self, file=None, name=None, norad=None):
        if sum([x is not None for x in [file, name, norad]]) != 1:
            raise ValueError(
                'exactly one of file, name and norad needs to be specified')

        if file is not None:
            return self.get_yamldata(file)
        elif name is not None:
            return self.search_name(name)
        else:
            return self.search_norad(norad)


yamlfiles = SatYAML()

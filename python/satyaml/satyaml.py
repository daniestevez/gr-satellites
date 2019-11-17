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

import yaml
import pathlib

class YAMLError(Exception):
    def __init__(self, message):
        self.message = message

_default_path = pathlib.Path(__file__).parent

class SatYAML:
    def __init__(self, path = _default_path):
        self._path = pathlib.Path(path)

    modulations = ['FSK', 'BPSK', 'DBPSK']
    framings = ['AX.25', 'AX.25 G3RUH', 'AX100 ASM+Golay', 'AX100 Reed Solomon',\
                '3CAT-1', 'Astrocast FX.25 NRZ-I', 'Astrocast FX.25 NRZ', 'Astrocast 9k6',\
                'AO-40 FEC', 'TT-64']
    
    def check_yaml(self, yml):
        d = self.get_yamldata(yml)
        if 'name' not in d:
            raise YAMLError(f'Missing name field in {yml}')
        if 'norad' not in d:
            raise YAMLError(f'Missing norad field in {yml}')
        if type(d['norad']) is not int:
            raise YAMLError(f'NORAD field does not contain a number in {yml}')
        if 'telemetry_servers' in d:
            for server in d['telemetry_servers']:
                if server not in ['SatNOGS', 'FUNcube', 'PWSat']:
                    raise YAMLError(f'Unknown telemetry server {server}')
        if 'data' not in d:
            raise YAMLError(f'Missing data field in {yml}')
        if 'transmitters' not in d:
            raise YAMLError(f'Missing transmitters field in {yml}')
        for key, transmitter in d['transmitters'].items():
            if 'frequency' not in transmitter:
                raise YAMLError(f'Missing frequency field in {key} in {yml}')
            if type(transmitter['frequency']) not in [float, int]:
                raise YAMLError(f'Frequency field does not contain a float in {key} in {yml}')
            if 'modulation' not in transmitter:
                raise YAMLError(f'Missing modulation field in {key} in {yml}')
            if transmitter['modulation'] not in self.modulations:
                raise YAMLError(f'Unknown modulation in {key} in {yml}')
            if 'baudrate' not in transmitter:
                raise YAMLError(f'Missing baudrate field in {key} in {yml}')
            if type(transmitter['baudrate']) not in [float, int]:
                raise YAMLError(f'Baudrate field does not contain a float in {key} in {yml}')
            if 'framing' not in transmitter:
                raise YAMLError(f'Missing framing field in {key} in {yml}')
            if transmitter['framing'] not in self.framings:
                raise YAMLError(f'Unknown framing in {key} in {yml}')
            if 'data' not in transmitter:
                raise YAMLError(f'Missing data field in {key} in {yml}')
            for dd in transmitter['data']:
                if dd not in d['data']:
                    raise YAMLError(f'Data entry {dd} used in {key} is not defined in data field in {yml}')
            
    def check_all_yaml(self):
        for yml in self.yaml_files():
            self.check_yaml(yml)

    def yaml_files(self):
        return self._path.glob('*.yml')

    def get_yamldata(self, yml):
        with open(yml) as f:
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
    
    def search_name(self, name):
        for yml in self.yaml_files():
            if name in self._get_satnames(yml):
                return self.get_yamldata(yml)
        raise ValueError('satellite not found')

    def search_norad(self, norad):
        for yml in self.yaml_files():
            if norad == self._get_satnorad(yml):
                return self.get_yamldata(yml)
        raise ValueError('satellite not found')

yamlfiles = SatYAML()

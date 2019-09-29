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

from .. import satyaml

class SatYAML:
    def __init__(self, path = pathlib.Path(satyaml.__path__[0])):
        self._path = pathlib.Path(path)

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

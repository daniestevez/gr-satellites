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

from pathlib import Path
import configparser

def open_config():
    """
    Opens and returns the gr-satellites config .ini file

    If the ini file does not exist, it creates a default one
    """
    config_dir = Path.home() / '.gr_satellites'
    config_filename = config_dir / 'config.ini'

    if not config_dir.exists():
        Path.mkdir(config_dir)

    if not config_filename.exists():
        return write_default_config(config_filename)

    config = configparser.ConfigParser()
    config.read(config_filename)
    return config

def write_default_config(file):
    """
    Writes a default configuration and returns the
    default configuration values.

    Args:
        file: the filename to write to
    """
    config = configparser.ConfigParser()
    config['Groundstation'] = {
        'callsign' : '',
        'latitude' : 0,
        'longitude' : 0,
        'submit_tlm' : 'yes',
    }

    config['FUNcube'] = {
        'site_id' : '',
        'auth_code' : '',
    }
    
    config['PW-Sat2'] = {
        'credentials_file' : '',
    }

    config['BME'] = {
        'user' : '',
        'password' : '',
    }

    with open(file, 'w') as f:
        config.write(f)

    return config

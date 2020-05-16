#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

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

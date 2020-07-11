#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks
from ... import submit, funcube_submit, pwsat2_submitter, bme_submitter

class telemetry_submit(gr.hier_block2):
    """
    Hierarchical block for telemetry submission

    The input are PDUs with frames

    These are submitted to a telemetry server

    Args:
        server: 'SatNOGS', 'FUNcube', 'PWSat' or 'BME' (string)
        norad: NORAD ID (int)
        config: configuration file from configparser
        options: options from argparse
    """
    def __init__(self, server, norad = None, config = None, options = None):
        gr.hier_block2.__init__(self, "telemetry_submit",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        self.message_port_register_hier_in('in')

        if server == 'SatNOGS':
            url = 'https://db.satnogs.org/api/telemetry/'
            self.submit = submit(url, norad, config['Groundstation']['callsign'],\
                                 float(config['Groundstation']['longitude']),\
                                 float(config['Groundstation']['latitude']),\
                                 '')
        elif server == 'FUNcube':
            url = 'http://data.amsat-uk.org'
            self.submit = funcube_submit(url, config['FUNcube']['site_id'], config['FUNcube']['auth_code'])
        elif server == 'PWSat':
            self.submit = pwsat2_submitter(config['PW-Sat2']['credentials_file'], '')
        elif server == 'BME':
            satellites = {44830 : 'atl1', 44832 : 'smogp'}
            satellite = satellites[norad]
            self.submit = bme_submitter(config['BME']['user'], config['BME']['password'], satellite)
        else:
            raise ValueError('Unsupported telemetry server')

        self.msg_connect((self, 'in'), (self.submit, 'in'))

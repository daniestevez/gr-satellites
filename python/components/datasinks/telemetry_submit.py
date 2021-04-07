#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr, blocks

from ... import submit, funcube_submit
from ... import pwsat2_submitter, bme_submitter, pdu_to_kiss
from ...utils.options_block import options_block


class telemetry_submit(gr.hier_block2, options_block):
    """
    Hierarchical block for telemetry submission

    The input are PDUs with frames

    These are submitted to a telemetry server

    Args:
        server: 'SatNOGS', 'FUNcube', 'PWSat', 'BME' or 'SIDS' (string)
        norad: NORAD ID (int)
        port: TCP port to connect to (used by HIT) (str)
        url: SIDS URL (used by SIDS) (str)
        config: configuration file from configparser
        options: options from argparse
    """
    def __init__(self, server, norad=None, port=None, url=None,
                 config=None, options=None):
        gr.hier_block2.__init__(
            self,
            'telemetry_submit',
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0))
        options_block.__init__(self, options)

        self.message_port_register_hier_in('in')

        if server in ['SatNOGS', 'SIDS']:
            if server == 'SatNOGS':
                url = 'https://db.satnogs.org/api/telemetry/'
            initial_timestamp = getattr(self.options, 'start_time', '')
            self.submit = submit(url, norad,
                                 config['Groundstation']['callsign'],
                                 float(config['Groundstation']['longitude']),
                                 float(config['Groundstation']['latitude']),
                                 initial_timestamp)
        elif server == 'FUNcube':
            url = 'http://data.amsat-uk.org'
            self.submit = funcube_submit(
                url, config['FUNcube']['site_id'],
                config['FUNcube']['auth_code'])
        elif server == 'PWSat':
            self.submit = pwsat2_submitter(
                config['PW-Sat2']['credentials_file'], '')
        elif server == 'BME':
            satellites = {44830: 'atl1', 44832: 'smogp', 47964: 'smog1'}
            satellite = satellites[norad]
            self.submit = bme_submitter(
                config['BME']['user'], config['BME']['password'], satellite)
        elif server == 'HIT':
            try:
                self.tcp = blocks.socket_pdu(
                    'TCP_CLIENT', '127.0.0.1', port, 10000, False)
            except RuntimeError as e:
                print('Could not connect to telemetry proxy:', e)
                print('Disabling telemetry submission...')
                return
            self.submit = pdu_to_kiss(control_byte=False)
            self.msg_connect((self.submit, 'out'), (self.tcp, 'pdus'))
        else:
            raise ValueError('Unsupported telemetry server')

        self.msg_connect((self, 'in'), (self.submit, 'in'))

    @classmethod
    def add_options(cls, parser):
        """
        Adds telemetry submit specific options to the argparse parser
        """
        parser.add_argument(
            '--start_time', type=str, default='',
            help='Recording start timestamp')

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

from gnuradio import gr, blocks
from ... import submit, funcube_submit, pwsat2_submitter

class telemetry_submit(gr.hier_block2):
    """
    Hierarchical block for telemetry submission

    The input are PDUs with frames

    These are submitted to a telemetry server

    Args:
        server: 'SatNOGS', 'FUNcube' or 'PWSat' (string)
        norad: NORAD ID (int)
        config: configuration file from configparser
    """
    def __init__(self, server, norad = None, config = None):
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
            self.submit = pwsat2_submitter(config['PW-Sat2']['credentials_file'])
        else:
            raise ValueError('Unsupported telemetry server')

        self.msg_connect((self, 'in'), (self.submit, 'in'))

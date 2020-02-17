#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017, 2020 Daniel Estevez <daniel@destevez.net>
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

import numpy
from gnuradio import gr
import pmt

from .telemetry.funcube import Frame, Callsign, WholeOrbit
import struct

import construct

WHOLEORBIT_SIZE = 23
PAYLOAD_SIZE = 200
WHOLEORBIT_MAX = 12

class funcube_telemetry_parser(gr.basic_block):
    """
    docstring for block telemetry_parser
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="funcube_telemetry_parser",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.last_chunk = None
        self.last_seq = None

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytes(pmt.u8vector_elements(msg))

        if len(packet) != 256:
            return

#        try:
        data = Frame.parse(packet)
#        except:
#            print('Could not parse FUNcube telemetry frame')
#            return
        if data:
            print('Frame type {}'.format(data.header.frametype))
            if not hasattr(data.header.frametype, '__getitem__'):
                print('Unknown frame type. Not processing frame.')
                return
            print('-'*40)
            print('Realtime telemetry:')
            print('-'*40)
            print((data.realtime))
            print('-'*40)
            if data.header.frametype[:2] == 'FM':
                print('Fitter Message {}'.format(data.header.frametype[2]))
                print('-'*40)
                print((data.payload))
            if data.header.frametype[:2] == 'HR':
                print('High resolution {}'.format(data.header.frametype[2]))
                print('-'*40)
                print((data.payload))
            if data.header.frametype[:2] == 'WO':
                chunk = int(data.header.frametype[2:])
                try:
                    seq = data.realtime.search('seqnumber')
                except AttributeError:
                    print('Unknown realtime format. Unable to get seqnumber.')
                    print()
                    return
                remaining = (PAYLOAD_SIZE*chunk) % WHOLEORBIT_SIZE
                recover = True
                if chunk != 0:
                    if self.last_chunk == chunk - 1 and self.last_seq == seq:
                        # can recover for last WO packet
                        wo = self.last_wo + data.payload[:-remaining]
                    else:
                        recover = False
                        last_chunk_remaining = (PAYLOAD_SIZE*(chunk-1)) % WHOLEORBIT_SIZE
                        wo = data.payload[WHOLEORBIT_SIZE-last_chunk_remaining:-remaining]
                else:
                    wo = data.payload[:-remaining]
                assert len(wo) % WHOLEORBIT_SIZE == 0
                wos = WholeOrbit(data.header.satid)[len(wo) // WHOLEORBIT_SIZE].parse(wo)
                self.last_chunk = chunk
                self.last_wo = data.payload[-remaining:]
                self.last_seq = seq
                print('Whole orbit {}'.format(chunk))
                if not recover:
                    print('(could not recover data from previous beacon)')
                print('-'*40)
                print(wos)
                if chunk == WHOLEORBIT_MAX:
                    print('-'*40)
                    # callsign included
                    print('Callsign: {}'.format(Callsign.parse(self.last_wo)))
            print()
        else:
            print('Could not parse beacon')
            print()

        

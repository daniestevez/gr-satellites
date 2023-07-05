#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json

from gnuradio import gr
import pmt
import websocket


class bme_ws_submitter(gr.basic_block):
    """
    Submits telemetry to wss://gnd.bme.hu:8070/send
    """
    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='bme_ws_submitter',
            in_sig=[],
            out_sig=[])

        self.ws = websocket.WebSocket()
        url = 'wss://gnd.bme.hu:8070/send'
        try:
            self.ws.connect(url)
        except Exception:
            print(f'could not connect to {url}; '
                  'disabling telemetry submission')
            self.ws = None

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def __del__(self):
        if self.ws is not None:
            self.ws.close()

    def submit(self, frame):
        if self.ws is None:
            return
        data = f'"data": "{frame.hex().upper()}"'
        self.ws.send(data)
        response = self.ws.recv()
        response = json.loads('{' + response + '}')
        error = any([v != 0 for k, v in response.items()
                     if 'error' in k])
        if error:
            print(f'server did not accept frame; returned: {response}')

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return

        frame = bytes(pmt.u8vector_elements(msg))
        try:
            self.submit(frame)
        except Exception as e:
            print(f'failed to submit frame: {e}')

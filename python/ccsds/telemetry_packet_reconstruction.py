#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This was made under ESA Summer of Code in Space 2019
# by Athanasios Theocharis, mentored by Daniel Estevez
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import pmt

from .telemetry import PrimaryHeader as TMPrimaryHeader
from .space_packet import PrimaryHeader as SPPrimaryHeader


class telemetry_packet_reconstruction(gr.basic_block):
    """
    Extract variable-length CCSDS Space Packets from a stream of Transfer Frames.

    Assumption: Channel multiplexing has already been performed by an earlier stage.

    Input: PDUs with Transfer Frames
    Output: PDUs with Packets
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="telemetry_packet_reconstruction",
            in_sig=[],
            out_sig=[])
        self.next_frame_count_expected = None
        self.partial_header = []
        self.partial_data_field = []
        self.packet_data_length = None

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        transfer_frame = bytes(pmt.u8vector_elements(msg))
        tf_header = TMPrimaryHeader.parse(transfer_frame)
        tf_data_field = transfer_frame[TMPrimaryHeader.sizeof():-4 if tf_header.ocf_flag else 0]

        # Detect frame loss for this virtual channel
        if (self.next_frame_count_expected is not None
            and tf_header.virtual_channel_frame_count != self.next_frame_count_expected):
                # Frame loss detected!
                # missing = tf_header.virtual_channel_frame_count - self.next_frame_count_expected
                # print(f'Frame loss detected, {missing} frame(s), expected {self.next_frame_count_expected} got {tf_header.virtual_channel_frame_count}')
                self._reset()
        self.next_frame_count_expected = (tf_header.virtual_channel_frame_count + 1) % 256

        # Extract packets
        if tf_header.first_header_pointer == 0b111_1111_1111:
            # No packet starts in the TF Data Field
            # Consume all octets that belong to a packet that began in an earlier transfer frame
            self._work(tf_data_field)
        elif tf_header.first_header_pointer == 0b111_1111_1110:
            # TF only contains idle data / OID
            return
        else:
            # Consume octets that belong to a packet that began in an earlier transfer frame
            if tf_header.first_header_pointer > 0:
                self._work(tf_data_field[:tf_header.first_header_pointer])
            # Reset packet extraction to indicate the start of a new packet
            self._reset()
            # Consume remaining octets that belong to the one (or more) packets that begin in this transfer frame
            self._work(tf_data_field[tf_header.first_header_pointer:])

    def _reset(self):
        self.partial_header = []
        self.partial_data_field = []
        self.packet_data_length = None

    def _work(self, octets):
        for octet in octets:
            if len(self.partial_header) < SPPrimaryHeader.sizeof():
                # in packet primary header
                self.partial_header.append(octet)
                if len(self.partial_header) == SPPrimaryHeader.sizeof():
                    self._parse_header()
            else:
                # in packet data field
                self.partial_data_field.append(octet)
                if len(self.partial_data_field) == self.packet_data_length:
                    self._send_packet()
                    self._reset()

    def _parse_header(self):
        header = SPPrimaryHeader.parse(bytes(self.partial_header))
        self.packet_data_length = header.data_length + 1

    def _send_packet(self):
        packet = self.partial_header + self.partial_data_field
        pdu_out = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet))
        self.message_port_pub(pmt.intern('out'), pdu_out)

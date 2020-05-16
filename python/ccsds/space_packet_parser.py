#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
# This was made under ESA Summer of Code in Space 2019
# by Athanasios Theocharis, mentored by Daniel Estevez
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

import numpy
from gnuradio import gr
import pmt
from . import space_packet

class space_packet_parser(gr.basic_block):
    """

    """

    def __init__(self, time_header, time_format, pfield, id_time):
        gr.basic_block.__init__(self,
                                name="Space Packet Parser",
                                in_sig=[],
                                out_sig=[])
        self.time_header = time_header
        self.time_format = time_format if time_header == 0 else 0
        self.pfield = pfield if time_header == 0 else 0
        self.basic_time_num_octets_cuc = id_time.basic_time_num_octets_cuc if time_header == 0 else 0
        self.fractional_time_num_octets_cuc = id_time.fractional_time_num_octets_cuc if time_header == 0 else 0
        self.additional_octets_basic_time_cuc = id_time.additional_basic_time_num_octets_cuc if time_header == 0 else 0
        self.additional_octets_fractional_time_cuc = id_time.additional_fractional_time_num_octets_cuc if time_header == 0 else 0
        self.length_of_day_cds = id_time.len_of_day if time_header == 0 else 0
        self.length_of_submillisecond_cds = id_time.len_of_submilsecs if time_header == 0 else 0
        self.calendar_variation_ccs = id_time.calendar_variation if time_header == 0 else 0
        self.number_of_subsecond_ccs = id_time.num_of_subsecs if time_header == 0 else 0
        self.add_z_terminator = id_time.add_z if time_header == 0 else 0
        self.ascii_dec_num = id_time.ascii_dec if time_header == 0 else 0


        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = bytearray(pmt.u8vector_elements(msg))
        if self.pfield == 1:
            packet_formats = [space_packet.FullPacketCUCWithPField, space_packet.FullPacketCDSWithPField,
                              space_packet.FullPacketCCSWithPField]
        else:
            packet_formats = [space_packet.FullPacketCUCNoPField, space_packet.FullPacketCDSNoPField,
                              space_packet.FullPacketCCSNoPField]

        packet_formats.extend([space_packet.FullPacketASCIIA, space_packet.FullPacketASCIIB,
                              space_packet.FullPacketNoTimeStamp])
        try:
            if self.time_header == 0:
                try:
                    packet_format = packet_formats[self.time_format]
                except IndexError:
                    print("Time Format Unknown")
                    return
            else:
                packet_format = packet_formats[5]

            if self.pfield == 0 and self.time_format <= 2 and self.time_header == 0:
                if self.time_format == 0:
                    data = packet_format.parse(packet[:], num_of_basic_time_units = 1+ self.basic_time_num_octets_cuc + self.additional_octets_basic_time_cuc, num_of_fractional_time_units = self.fractional_time_num_octets_cuc + self.additional_octets_fractional_time_cuc)
                elif self.time_format == 1:
                    data = packet_format.parse(packet[:], length_of_day_segment = self.length_of_day_cds, length_of_submillisecond_segment = self.length_of_submillisecond_cds)
                else:
                    data = packet_format.parse(packet[:], calendar_variation_flag = self.calendar_variation_ccs, resolution = self.number_of_subsecond_ccs)
            else:
                if self.time_header == 0 and self.time_format > 2:
                    if self.ascii_dec_num < 0 or self.ascii_dec_num > 6:
                        print()
                        "Decimals of ASCII in Space Packet Parser block should be between 0 and 6. The number was automatically set to 1."
                        self.ascii_dec_num = 1
                    data = packet_format.parse(packet[:], number_of_decimals=self.ascii_dec_num, add_Z=self.add_z_terminator)
                else:
                    data = packet_format.parse(packet[:])
        except:
            print("Could not decode space packet")
            return
        print(data)

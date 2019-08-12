#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
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
#

import numpy
from gnuradio import gr
from datetime import datetime
import pmt
import array
import space_packet

class space_packet_time_stamp_adder(gr.basic_block):
    """
    Time Stamp Adder (CCSDS 301.0-B-4)
    The user should study the time code formats book and fill only the necessary fields.

    On another note, the space packet parser, in case of a time stamp addition, will only display information
    if a PField is used, since metadata are crucial to the parsing of the time stamp.

    The user, in general, should check the code of the preferred time format and confirm that the behavior is
    the wanted one. Great care should be taken on the variability of the size. (E.g. in ASCII A time format,
    the user should define the size of the decimal fraction of the second subfield.)
    """
    def __init__(self, input_manual_automatic, time_format, pfield, pfield_extension, time_code_identification_cuc,
                 epoch_year_cuc, epoch_month_cuc, epoch_day_cuc, basic_time_num_octets_cuc, fractional_time_num_octets_cuc, pfield_extension_extended,
                 additional_octets_basic_time_cuc, additional_octets_fractional_time_cuc, rsvd_cuc,
                 time_code_identification_cds, epoch_identification_cds, epoch_year_cds, epoch_month_cds, epoch_day_cds,
                 length_of_day_cds,
                 length_of_submillisecond_cds, time_code_identification_ccs, calendar_variation_ccs,
                 number_of_subsecond_ccs, year, month, day, hour, minute, second, microsecond):
        gr.basic_block.__init__(self,
            name="space_packet_time_stamp_adder",
            in_sig=[],
            out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.input_manual_automatic = input_manual_automatic
        self.time_format = time_format
        self.pfield = pfield #Checks if the P-Field will be used
        self.pfield_extension = pfield_extension #Checks if the PField will be extended
        self.time_code_identification_cuc = time_code_identification_cuc
        self.epoch_year_cuc = epoch_year_cuc
        self.epoch_month_cuc = epoch_month_cuc
        self.epoch_day_cuc = epoch_day_cuc
        self.basic_time_num_octets_cuc = basic_time_num_octets_cuc
        self.fractional_time_num_octets_cuc = fractional_time_num_octets_cuc
        self.pfield_extension_extended = pfield_extension_extended #Checks if the PField Extension will be extended
        self.additional_octets_basic_time_cuc = additional_octets_basic_time_cuc
        self.additional_octets_fractional_time_cuc = additional_octets_fractional_time_cuc
        self.rsvd_cuc = rsvd_cuc
        self.time_code_identification_cds = time_code_identification_cds
        self.epoch_identification_cds = epoch_identification_cds
        self.epoch_year_cds = epoch_year_cds
        self.epoch_month_cds = epoch_year_cds
        self.epoch_day_cds = epoch_day_cds
        self.length_of_day_cds = length_of_day_cds
        self.length_of_submillisecond_cds = length_of_submillisecond_cds
        self.time_code_identification_ccs = time_code_identification_ccs
        self.calendar_variation_ccs = calendar_variation_ccs
        self.number_of_subsecond_ccs = number_of_subsecond_ccs
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        ##################################################
        # Blocks
        ##################################################
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))


    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print
            "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = pmt.u8vector_elements(msg)

        mask = 0b11111111 #Use this to take the last 8 bits of a number

        if self.input_manual_automatic == 1:
            now = datetime.now()
            self.year = now.year
            self.month = now.month
            self.day = now.day
            self.hour = now.hour
            self.minute = now.minute
            self.second = now.second
            self.microsecond = now.microsecond

        if self.time_format == 0: #CUC
            if self.pfield == 1:
                size = 2 + self.basic_time_num_octets_cuc + self.fractional_time_num_octets_cuc + 2 + \
                       self.additional_octets_basic_time_cuc + self.additional_octets_fractional_time_cuc
                finalHeader = numpy.array(numpy.zeros(size), dtype=int)
                #User should define the allocation of the unsegmented time code format here
            else:
                print "Agency should define unsegmented code"
        elif self.time_format == 1: #CDS
            if self.pfield == 1:
                temp_size = 0
                if self.length_of_submillisecond_cds == 1 or self.length_of_submillisecond_cds == 2:
                    temp_size = self.length_of_submillisecond_cds
                finalHeader = numpy.array(numpy.zeros(7 + 1*self.length_of_day_cds + 2*temp_size), dtype=int)
                finalHeader[0] = self.pfield_extension << 7 + self.time_code_identification_cds << 4 + self.epoch_identification_cds << 3 + self.length_of_day_cds << 2 + self.length_of_submillisecond_cds
                if self.length_of_day_cds == 0:
                    finalHeader[1] = daysSinceEpoch() >> 8
                    finalHeader[2] = daysSinceEpoch() & mask
                    finalHeader[3] = msOfTheDay() >> 24
                    finalHeader[4] = (msOfTheDay() >> 16) & mask
                    finalHeader[5] = (msOfTheDay() >> 8) & mask
                    finalHeader[6] = msOfTheDay() & mask
                    if temp_size == 1:
                        finalHeader[7] = self.microsecond >> 8
                        finalHeader[8] = self.microsecond & mask
                    elif temp_size == 2:
                        finalHeader[7] = self.microsecond >> 24
                        finalHeader[8] = (self.microsecond >> 16) & mask
                        finalHeader[9] = (self.microsecond >> 8) & mask
                        finalHeader[10] = self.microsecond & mask
                else:
                    finalHeader[1] = daysSinceEpoch() >> 16
                    finalHeader[2] = (daysSinceEpoch() >> 8) & mask
                    finalHeader[3] = daysSinceEpoch() & mask
                    finalHeader[4] = msOfTheDay() >> 24
                    finalHeader[5] = (msOfTheDay() >> 16) & mask
                    finalHeader[6] = (msOfTheDay() >> 8) & mask
                    finalHeader[7] = msOfTheDay() & mask
                    if temp_size == 1:
                        finalHeader[8] = self.microsecond >> 8
                        finalHeader[9] = self.microsecond & mask
                    elif temp_size == 2:
                        finalHeader[8] = self.microsecond >> 24
                        finalHeader[9] = (self.microsecond >> 16) & mask
                        finalHeader[10] = (self.microsecond >> 8) & mask
                        finalHeader[11] = self.microsecond & mask


        elif self.time_format == 2: #CCS
            print "elif"
        elif self.time_format == 3: #ASCII A
            print "eliif"
        elif self.time_format == 4: #ASCII B
            print "elif"
        else:
            print "Time Format Unknown"



        finalPacket = numpy.append(finalHeader, packet)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)

    def daysSinceEpoch(self):
        if self.epoch_identification_cds == 0:
            self.epoch_year_cds = 1958
            self.epoch_month_cds = 1
            self.epoch_day_cds = 1

        return (self.year - self.epoch_year_cds)*365 + (self.month - self.epoch_month_cds)*30 + self.day - self.epoch_day_cds

    def msOfTheDay(self):
        return self.hour*60*60*1000 + self.minute*60*1000 + self.second * 1000
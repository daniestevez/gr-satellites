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
import datetime

from gnuradio import gr
import construct
import pmt
import array
from . import space_packet

class space_packet_time_stamp_adder(gr.basic_block):
    """
    Time Stamp Adder (CCSDS 301.0-B-4)
    --- The user should study the time code formats book and fill only the necessary fields.

    --- The user, in general, should check the code of the preferred time format and confirm that the behavior is
    the wanted one. Great care should be taken on the variability of the size. (E.g. in ASCII A time format,
    the user should define the size of the decimal fraction of the second subfield and should change the finalHeader array.)

    --- Automated time only prints a timestamp down to microseconds

    --- When defining an epoch, the user should check that it fits into the bytes that were assigned to hold the difference.
        E.g. If the epoch "0001 January 1" is defined in CDS, then it will not be able to fit today's date into a 16-bit
        DAYS part.
    """
    def __init__(self, input_manual_automatic, time_format, pfield, pfield_extension, time_code_identification_cuc,
                 epoch_year_cuc, epoch_month_cuc, epoch_day_cuc, pfield_extension_extended,rsvd_cuc,
                 time_code_identification_cds, epoch_identification_cds, epoch_year_cds, epoch_month_cds, epoch_day_cds,
                 time_code_identification_ccs, year, month, day, hour, minute, second, microsecond, picosecond, id_time):
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
        self.basic_time_num_octets_cuc = id_time.basic_time_num_octets_cuc
        self.fractional_time_num_octets_cuc = id_time.fractional_time_num_octets_cuc
        self.pfield_extension_extended = pfield_extension_extended #Checks if the PField Extension will be extended
        self.additional_octets_basic_time_cuc = id_time.additional_basic_time_num_octets_cuc
        self.additional_octets_fractional_time_cuc = id_time.additional_fractional_time_num_octets_cuc
        self.rsvd_cuc = rsvd_cuc
        self.time_code_identification_cds = time_code_identification_cds
        self.epoch_identification_cds = epoch_identification_cds
        self.epoch_year_cds = epoch_year_cds
        self.epoch_month_cds = epoch_month_cds
        self.epoch_day_cds = epoch_day_cds
        self.length_of_day_cds = id_time.len_of_day
        self.length_of_submillisecond_cds = id_time.len_of_submilsecs
        self.time_code_identification_ccs = time_code_identification_ccs
        self.calendar_variation_ccs = id_time.calendar_variation
        self.number_of_subsecond_ccs = id_time.num_of_subsecs
        self.add_z_terminator = id_time.add_z
        self.ascii_dec_num = id_time.ascii_dec
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        self.picosecond = picosecond
        self.id_time = id_time
        if self.time_code_identification_cuc == 1:
            self.epoch_cuc = datetime.datetime(1958, 1, 1, tzinfo=datetime.timezone.utc)
        else:
            self.epoch_cuc = datetime.datetime(
                self.epoch_year_cuc, self.epoch_month_cuc, self.epoch_day_cuc,
                tzinfo=datetime.timezone.utc)

        if self.epoch_identification_cds == 0:
            self.epoch_cds = datetime.datetime(1958, 1, 1, tzinfo=datetime.timezone.utc)
        else:
            self.epoch_cds = datetime.datetime(self.epoch_year_cds, self.epoch_month_cds,
                self.epoch_day_cds, tzinfo=datetime.timezone.utc)

        ##################################################
        # Blocks
        ##################################################
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print()
            "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = pmt.u8vector_elements(msg)
        if self.input_manual_automatic == 1:
            self.now = datetime.datetime.now(tz=datetime.timezone.utc)
            if self.length_of_submillisecond_cds >= 2:
                self.length_of_submillisecond_cds = 1
            if self.number_of_subsecond_ccs >= 4:
                self.length_of_susecond_ccs = 3
        else:
            self.now = datetime.datetime(self.year, self.month, self.day, self.hour,
                self.minute, self.second, self.microsecond, tzinfo=datetime.timezone.utc)

        finalHeader = []

        if self.time_format == 0: #CUC
            basic_time = 1 + self.basic_time_num_octets_cuc
            fractional_time = self.fractional_time_num_octets_cuc

            if self.pfield == 1: #If it exists

                finalHeader.extend(array.array('B', space_packet.PFieldCUC.build(
                    dict(pfield_extension=self.pfield_extension,
                         time_code_identification=self.time_code_identification_cuc,
                         number_of_basic_time_unit_octets=self.basic_time_num_octets_cuc,
                         number_of_fractional_time_unit_octets=self.fractional_time_num_octets_cuc))).tolist())

                if self.pfield_extension == 1: #If it is extended
                    basic_time += self.additional_octets_basic_time_cuc
                    fractional_time +=self.additional_octets_fractional_time_cuc
                    finalHeader.extend(array.array('B', space_packet.PFieldCUCExtension.build(
                        dict(pfieldextension=self.pfield_extension_extended,
                             number_of_additional_basic_time_unit_octets=self.additional_octets_basic_time_cuc,
                             number_of_additional_fractional_time_unit_octets=self.additional_octets_fractional_time_cuc,
                             reserved_for_mission_definition=self.rsvd_cuc))).tolist())
            temp_diff = self.now - self.epoch_cuc
            total_basic = int(temp_diff.total_seconds())
            total_frac = int((temp_diff.total_seconds() - total_basic)*(256**fractional_time))
            finalHeader.extend(array.array('B', construct.BytesInteger(basic_time).build(total_basic)).tolist())
            finalHeader.extend(array.array('B', construct.BytesInteger(fractional_time).build(total_frac)).tolist())

        elif self.time_format == 1: #CDS
            if self.pfield == 1:
                finalHeader.extend(array.array('B', space_packet.PFieldCDS.build(dict(pfield_extension = self.pfield_extension,
                                                                                 time_code_identification = self.time_code_identification_cds,
                                                                                 epoch_identification = self.epoch_identification_cds,
                                                                                 length_of_day_segment = self.length_of_day_cds,
                                                                                 length_of_submillisecond_segment = self.length_of_submillisecond_cds))).tolist())
            days_len = 2 if self.length_of_day_cds == 0 else 3
            finalHeader.extend(
                array.array('B', construct.BytesInteger(days_len).build((self.now - self.epoch_cds).days)).tolist())
            finalHeader.extend(array.array('B', construct.Int32ub.build(self.now.microsecond/1000)).tolist())
            if self.length_of_submillisecond_cds == 1:
                finalHeader.extend(array.array('B', construct.Int16ub.build(self.now.microsecond % 1000)).tolist())
            elif self.length_of_submillisecond_cds == 2:
                finalHeader.extend(array.array('B', construct.Int32ub.build(self.picosecond)).tolist())

        elif self.time_format == 2: #CCS
            if self.pfield == 1:
                finalHeader.extend(array.array('B', space_packet.PFieldCCS.build(dict(pfield_extension = self.pfield_extension,
                                                                                 time_code_identification = self.time_code_identification_ccs,
                                                                                 calendar_variation_flag = self.calendar_variation_ccs,
                                                                                 resolution=self.number_of_subsecond_ccs))).tolist())
            finalHeader.extend(array.array('B', construct.Int16ub.build(self.now.year)).tolist())
            if self.calendar_variation_ccs == 0:
                finalHeader.extend(array.array('B', construct.Int8ub.build(self.now.month)).tolist())
                finalHeader.extend(array.array('B', construct.Int8ub.build(self.now.day)).tolist())
            else:
                finalHeader.extend(array.array('B', construct.Int16ub.build(self.now.timetuple().tm_yday)).tolist())

            finalHeader.extend(array.array('B', construct.Int8ub.build(self.now.hour)).tolist())
            finalHeader.extend(array.array('B', construct.Int8ub.build(self.now.minute)).tolist())
            finalHeader.extend(array.array('B', construct.Int8ub.build(self.now.second)).tolist())

            if self.number_of_subsecond_ccs >= 1:
                finalHeader.extend(array.array('B', construct.Int8ub.build(self.now.microsecond / 10 ** 4)).tolist())
            if self.number_of_subsecond_ccs >= 2:
                finalHeader.extend(
                    array.array('B', construct.Int8ub.build((self.now.microsecond / 10 ** 2) % 10 ** 2)).tolist())
            if self.number_of_subsecond_ccs >= 3:
                finalHeader.extend(array.array('B', construct.Int8ub.build(self.now.microsecond % 10 ** 2)).tolist())
            if self.number_of_subsecond_ccs >= 4:
                finalHeader.extend(
                    array.array('B', construct.Int8ub.build((self.picosecond % 10 ** 6) / 10 ** 4)).tolist())
            if self.number_of_subsecond_ccs >= 5:
                finalHeader.extend(
                    array.array('B', construct.Int8ub.build((self.picosecond % 10 ** 4) / 10 ** 2)).tolist())
            if self.number_of_subsecond_ccs >= 6:
                finalHeader.extend(array.array('B', construct.Int8ub.build(self.picosecond % 10 ** 2)).tolist())

        elif self.time_format == 3 or self.time_format == 4:
            if(self.ascii_dec_num < 0 or self.ascii_dec_num > 6):
                print("Decimals of ASCII in Time Stamp Adder block should be between 0 and 6. The number was automatically set to 1.")
                self.ascii_dec_num = 1

            if self.time_format == 3: # ASCII A
                arr = self.now.replace(tzinfo=None).isoformat()
            else: #ASCII B
                arr = self.now.strftime("%Y-%jT%H:%M:%S.%f")

            arr = arr[: -(6 - self.ascii_dec_num)]

            if (self.add_z_terminator == 1):
                arr += 'Z'

            finalHeader= array.array('B', arr).tolist()

        else:
            print("Time Format Unknown")

        finalPacket = numpy.append(finalHeader, packet)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)

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

'''
Construct for the CCSDS Space Packet ( CCSDS 133.0-B-1 )
The User, in case of utilizing the secondary header, should be careful and define the sizes of the payload.
After choosing which time format will be used, the User should check the sizes of the secondary header construct,
as well as the payload variable size of the FullPacket[TimeCodeFormat].
'''


from construct import *


PrimaryHeader = BitStruct('ccsds_version' / BitsInteger(3),
                          'packet_type' / BitsInteger(1),
                          'secondary_header_flag' / Flag,
                          'AP_ID' / BitsInteger(11),
                          'sequence_flags' / BitsInteger(2),
                          'packet_sequence_count_or_name' / BitsInteger(14),
                          'data_length' / BitsInteger(16))

PFieldCUC = BitStruct('pfield_extension' / Flag,
                      'time_code_identification' / BitsInteger(3),
                      'number_of_basic_time_unit_octets' / BitsInteger(2),
                      'number_of_fractional_time_unit_octets' / BitsInteger(2))

PFieldCUCExtension = BitStruct('pfieldextension' / Flag,
                               'number_of_additional_basic_time_unit_octets' / BitsInteger(2),
                               'number_of_additional_fractional_time_unit_octets' / BitsInteger(2),
                               'reserved_for_mission_definition' / BitsInteger(2))

TimeCodeCUC = Struct('pfield' / PFieldCUC,
                     'pfield_extended' / PFieldCUCExtension,
                     'tfield' / BitsInteger((this.pfield.number_of_basic_time_unit_octets +
                                     this.pfield.number_of_fractional_time_unit_octets + 2 +
                                     this.pfield_extended.number_of_additional_basic_time_unit_octets +
                                     this.pfield.number_of_additional_fractional_time_unit_octets)*8))

PFieldCDS = BitStruct('pfield_extension' / Flag,
                      'time_code_identification' / BitsInteger(3),
                      'epoch_identification' / BitsInteger(1),
                      'length_of_day_segment' / BitsInteger(1),
                      'length_of_submillisecond_segment' / BitsInteger(2))

TimeCodeCDS = Struct('pfield' / PFieldCDS,
                     'days' / BitsInteger((2+this.pfield.length_of_day_segment)*8),
                     'ms_of_day' / BitsInteger(32),
                     'submilliseconds_of_ms' / Byte[this.pfield.length_of_submillisecond_segment])

PFieldCCS = BitStruct('pfield_extension' / Flag,
                      'time_code_identification' / BitsInteger(3),
                      'calendar_variation_flag' / Flag,
                      'resolution' / BitsInteger(3))

TimeCodeCCS = Struct('pfield' / PFieldCCS,
                     'year' / Byte[2],
                     'month/dayOfMonth_or_dayOfYear' / Byte[2],
                     'hour' / Byte[1],
                     'month' / Byte[1],
                     'second' / Byte[1],
                     'subseconds' / Byte[this.pfield.resolution])

TimeCodeASCIIA = BitStruct('yearChar1' / Byte,
                           'yearChar2' / Byte,
                           'yearChar3' / Byte,
                           'yearChar4' / Byte,
                           'monthChar1' / Byte,
                           'monthChar2' / Byte,
                           'dayChar1' / Byte,
                           'dayChar2' / Byte,
                           'calendar_time_separator' / Byte,
                           'hourChar1' / Byte,
                           'hourChar2' / Byte,
                           'minuteChar1' / Byte,
                           'minuteChar2' / Byte,
                           'secondChar1' / Byte,
                           'secondChar2' / Byte,
                           'decimal_fraction_of_second' / Byte[1], #User should define this amount of bytes
                           'time_code_terminator' / Byte)

TimeCodeASCIIB = BitStruct('yearChar1' / Byte,
                           'yearChar2' / Byte,
                           'yearChar3' / Byte,
                           'yearChar4' / Byte,
                           'dayChar1' / Byte,
                           'dayChar2' / Byte,
                           'dayChar3' / Byte,
                           'calendar_time_separator' / Byte,
                           'hourChar1' / Byte,
                           'hourChar2' / Byte,
                           'minuteChar1' / Byte,
                           'minuteChar2' / Byte,
                           'secondChar1' / Byte,
                           'secondChar2' / Byte,
                           'decimal_fraction_of_second' / Byte[1], #User should define this amount of bytes
                           'time_code_terminator' / Byte)

FullPacketNoTimeStamp = Struct('primary' / PrimaryHeader,
                               'payload' / Byte[this.primary.data_length])

FullPacketCUC = Struct('primary' / PrimaryHeader,
                       'timestamp' / TimeCodeCUC,
                       'payload' / Byte[this.primary.data_length - 2 - this.timestamp.pfield.first_pfield.number_of_basic_time_unit_octets - this.timestamp.pfield.first_pfield.number_of_fractional_time_unit_octets])

#Since timestamp is permanent through Mission Phase, User should define payload timestamp size
FullPacketCDS = Struct('primary' / PrimaryHeader,
                       'timestamp' / TimeCodeCDS,
                       'payload' / Byte[this.primary.data_length - 7 - this.timestamp.pfield.length_of_day_segment - this.timestamp.pfield.length_of_submillisecond_segment])

FullPacketCCS = Struct('primary' / PrimaryHeader,
                       'timestamp' / TimeCodeCCS,
                       'payload' / Byte[this.primary.data_length - 8 - this.timestamp.pfield.resolution])

FullPacketASCIIA = Struct('primary' / PrimaryHeader,
                          'timestamp' / TimeCodeASCIIA,
                          'payload' / Byte[this.primary.data_length - 17]) #Change this depending on the number of decimal fractions of a second

FullPacketASCIIB = Struct('primary' / PrimaryHeader,
                          'timestamp' / TimeCodeASCIIA,
                          'payload' / Byte[this.primary.data_length - 16]) #Change this depending on the number of decimal fractions of a second
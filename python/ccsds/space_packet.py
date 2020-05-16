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

#########################################
## CUC related structs
#########################################

PFieldCUC = BitStruct('pfield_extension' / Flag,
                      'time_code_identification' / BitsInteger(3),
                      'number_of_basic_time_unit_octets' / BitsInteger(2),
                      'number_of_fractional_time_unit_octets' / BitsInteger(2))

PFieldCUCExtension = BitStruct('pfieldextension' / Flag,
                               'number_of_additional_basic_time_unit_octets' / BitsInteger(2),
                               'number_of_additional_fractional_time_unit_octets' / BitsInteger(3),
                               'reserved_for_mission_definition' / BitsInteger(2))

TimeCodeCUCWithPField = Struct('pfield' / PFieldCUC,
                               'pfield_extended' / If(this.pfield.pfield_extension == 1, PFieldCUCExtension),
                               'basic_time_unit' / IfThenElse(this.pfield.pfield_extension == 0,
                                                              BytesInteger(
                                                                  this.pfield.number_of_basic_time_unit_octets + 1),
                                                              BytesInteger(
                                                                  this.pfield.number_of_basic_time_unit_octets + 1 +
                                                                  this.pfield_extended.number_of_additional_basic_time_unit_octets)),

                               'fractional_time_unit' / IfThenElse(this.pfield.pfield_extension == 0,
                                                                   BytesInteger(
                                                                       this.pfield.number_of_fractional_time_unit_octets),
                                                                   BytesInteger(
                                                                       this.pfield.number_of_fractional_time_unit_octets +
                                                                       this.pfield_extended.number_of_additional_fractional_time_unit_octets)))

FullPacketCUCWithPField = Struct('primary' / PrimaryHeader,
                                 'timestamp' / TimeCodeCUCWithPField,
                                 'payload' / IfThenElse(this.timestamp.pfield.pfield_extension == 0,
                                                        Byte[
                                                            this.primary.data_length - 2 - this.timestamp.pfield.number_of_basic_time_unit_octets -
                                                            this.timestamp.pfield.number_of_fractional_time_unit_octets],
                                                        Byte[
                                                            this.primary.data_length - 3 - this.timestamp.pfield.number_of_basic_time_unit_octets - this.timestamp.pfield.number_of_fractional_time_unit_octets -
                                                            this.timestamp.pfield_extended.number_of_additional_basic_time_unit_octets - this.timestamp.pfield_extended.number_of_additional_fractional_time_unit_octets]))

TimeCodeCUCNoPField = Struct('basic_time_unit' / BytesInteger(this._._.num_of_basic_time_units),
                             'fractional_time_unit' / BytesInteger(this._._.num_of_fractional_time_units))

FullPacketCUCNoPField = Struct('primary' / PrimaryHeader,
                               'timestamp' / TimeCodeCUCNoPField,
                               'payload' / Byte[this.primary.data_length - this._.num_of_basic_time_units -
                                                          this._.num_of_fractional_time_units])

#########################################
## CDS related structs
#########################################

PFieldCDS = BitStruct('pfield_extension' / Flag,
                      'time_code_identification' / BitsInteger(3),
                      'epoch_identification' / BitsInteger(1),
                      'length_of_day_segment' / BitsInteger(1),
                      'length_of_submillisecond_segment' / BitsInteger(2))

TimeCodeCDSWithPField = Struct('pfield' / PFieldCDS,
                               'days' / BytesInteger(2 + this.pfield.length_of_day_segment),
                               'ms_of_day' / BytesInteger(4),
                               'submilliseconds_of_ms' / BytesInteger(2 * this.pfield.length_of_submillisecond_segment))

FullPacketCDSWithPField = Struct('primary' / PrimaryHeader,
                                 'timestamp' / TimeCodeCDSWithPField,
                                 'payload' / Byte[
                                     this.primary.data_length - 7 - this.timestamp.pfield.length_of_day_segment -
                                     2 * this.timestamp.pfield.length_of_submillisecond_segment])

TimeCodeCDSNoPField = Struct('days' / BytesInteger(2 + this._._.length_of_day_segment),
                             'ms_of_day' / BytesInteger(4),
                             'submilliseconds_of_ms' / BytesInteger(2 * this._._.length_of_submillisecond_segment))

FullPacketCDSNoPField = Struct('primary' / PrimaryHeader,
                               'timestamp' / TimeCodeCDSNoPField,
                               'payload' / Byte[
                                   this.primary.data_length - 6 - this._._.length_of_day_segment - 2 * this._._.length_of_submillisecond_segment])

#########################################
## CCS related structs
#########################################

PFieldCCS = BitStruct('pfield_extension' / Flag,
                      'time_code_identification' / BitsInteger(3),
                      'calendar_variation_flag' / Flag,
                      'resolution' / BitsInteger(3))

TimeCodeCCSWithPField = Struct('pfield' / PFieldCCS,
                               'year' / BytesInteger(2),
                               'month' / If(this.pfield.calendar_variation_flag == 0, BytesInteger(1)),
                               'dayOfMonth' / If(this.pfield.calendar_variation_flag == 0, BytesInteger(1)),
                               'dayOfYear' / If(this.pfield.calendar_variation_flag == 1, BytesInteger(1)),
                               'hour' / BytesInteger(1),
                               'minute' / BytesInteger(1),
                               'second' / BytesInteger(1),
                               'subseconds' / Byte[this.pfield.resolution])

FullPacketCCSWithPField = Struct('primary' / PrimaryHeader,
                                 'timestamp' / TimeCodeCCSWithPField,
                                 'payload' / Byte[this.primary.data_length - 8 - this.timestamp.pfield.resolution])

TimeCodeCCSNoPField = Struct('year' / BytesInteger(2),
                             'month' / If(this._._.calendar_variation_flag == 0, BytesInteger(1)),
                             'dayOfMonth' / If(this._._.calendar_variation_flag == 0, BytesInteger(1)),
                             'dayOfYear' / If(this._._.calendar_variation_flag == 1, BytesInteger(2)),
                             'hour' / BytesInteger(1),
                             'minute' / BytesInteger(1),
                             'second' / BytesInteger(1),
                             'subseconds' / Byte[this._._.resolution])

FullPacketCCSNoPField = Struct('primary' / PrimaryHeader,
                               'timestamp' / TimeCodeCCSNoPField,
                               'payload' / Byte[this.primary.data_length - 7 - this._.resolution])

#########################################
## ASCII A (Month - Day Format) related structs
#########################################

TimeCodeASCIIA = Struct('yearChar1' / BytesInteger(1),
                        'yearChar2' / BytesInteger(1),
                        'yearChar3' / BytesInteger(1),
                        'yearChar4' / BytesInteger(1),
                        'hyphen1' / BytesInteger(1),
                        'monthChar1' / BytesInteger(1),
                        'monthChar2' / BytesInteger(1),
                        'hyphen2' / BytesInteger(1),
                        'dayChar1' / BytesInteger(1),
                        'dayChar2' / BytesInteger(1),
                        'calendar_time_separator' / BytesInteger(1),
                        'hourChar1' / BytesInteger(1),
                        'hourChar2' / BytesInteger(1),
                        'colon1' / BytesInteger(1),
                        'minuteChar1' / BytesInteger(1),
                        'minuteChar2' / BytesInteger(1),
                        'colon2' / BytesInteger(1),
                        'secondChar1' / BytesInteger(1),
                        'secondChar2' / BytesInteger(1),
                        'dot' / BytesInteger(1),
                        'decimal_fraction_of_second' / Byte[this._._.number_of_decimals],
                        'time_code_terminator' / If(this._._.add_Z == 1, BytesInteger(1)))

FullPacketASCIIA = Struct('primary' / PrimaryHeader,
                          'timestamp' / TimeCodeASCIIA,
                          'payload' / Byte[this.primary.data_length - 20 - this._.number_of_decimals - this._.add_Z])

#########################################
## ASCII B (Day of the year Format) related structs
#########################################

TimeCodeASCIIB = Struct('yearChar1' / BytesInteger(1),
                        'yearChar2' / BytesInteger(1),
                        'yearChar3' / BytesInteger(1),
                        'yearChar4' / BytesInteger(1),
                        'hyphen1' / BytesInteger(1),
                        'dayChar1' / BytesInteger(1),
                        'dayChar2' / BytesInteger(1),
                        'dayChar3' / BytesInteger(1),
                        'calendar_time_separator' / BytesInteger(1),
                        'hourChar1' / BytesInteger(1),
                        'hourChar2' / BytesInteger(1),
                        'colon1' / BytesInteger(1),
                        'minuteChar1' / BytesInteger(1),
                        'minuteChar2' / BytesInteger(1),
                        'colon2' / BytesInteger(1),
                        'secondChar1' / BytesInteger(1),
                        'secondChar2' / BytesInteger(1),
                        'dot' / BytesInteger(1),
                        'decimal_fraction_of_second' / Byte[this._._.number_of_decimals],
                        'time_code_terminator' / If(1 == this._._.add_Z, BytesInteger(1)))

FullPacketASCIIB = Struct('primary' / PrimaryHeader,
                          'timestamp' / TimeCodeASCIIB,
                          'payload' / Byte[
                              this.primary.data_length - 18 - this._.number_of_decimals - this._.add_Z])

#########################################
## No Time Stamps
#########################################
FullPacketNoTimeStamp = Struct('primary' / PrimaryHeader,
                               'payload' / Byte[this.primary.data_length])

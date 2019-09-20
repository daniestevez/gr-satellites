#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Daniel Estevez <daniel@destevez.net>
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

from construct import *
from . import ccsds_space_packet
from . import ecss_pus

from .adapters import LinearAdapter

TMHeader = BitStruct(
    'version' / BitsInteger(2),
    'sc_id' / BitsInteger(10),
    'virtual_channel_id' / BitsInteger(4),
    'virtual_channel_frame_counter' / BitsInteger(8),
    'first_header_pointer' / BitsInteger(11),
    'empty_frame' / BitsInteger(1),
    'ocf_presence' / BitsInteger(1),
    'sequence_flags' / BitsInteger(2),
    'fixed_length_frame' / BitsInteger(1))

TMTail = Struct(
    'packet_errors' / Int16ub,
    'frame_errors' / Int16ub,
    'frame_error_control' / Int16ub)

SPTail = Struct(
    'PEC' / Int16ub)

TimeField = Struct(
    'day' / Int16ub,
    'milliseconds_of_day' / Int32ub)

OBC = Struct(
    'boot_cause' / Int32ub,
    'boot_count' / Int16ub,
    'clock' / Int32ub,
    'curr_flash' / Int16ub,
    'fs_mounted' / Int8ub,
    'ram_image' / Int8sb,
    'temp' / LinearAdapter(10, Int16sb)[2],
    'ticks' / Int32ub,
    'mag' / Float32b[3],
    'memfree' / Int32ub,
    'bufferfree' / Int32ub,
    'uptime' / Int32ub,
    'gyro' / Float32b[3],
    'gyro_temp' / Float32b,
    'flash_total' / Int64ub,
    'flash_used' / Int64ub,
    'flash_free' / Int64ub,
    'gpio_test' / Int8ub,
    'gpio_sw' / Int8ub,
    'gpio_pwr' / Int8ub,
    'om_state' / Int8ub,
    'om_sw_version' / Bytes(32),
    'op_tr_conn' / Int8ub,
    'op_tr_conn_active' / Int8ub)

EPS = Struct(
    'output_off_delta' / Int16ub[8],
    'output_on_delta' / Int16ub[8],
    'wdt_csp_pings_left' / Int8ub[2],
    'bootcause' / Int8ub,
    'cursun' / Int16ub,
    'curin' / Int16ub[3],
    'curout' / Int16ub[6],
    'cursys' / Int16ub,
    'temp' / Int16ub[6],
    'battmode' / Int8ub,
    'pptmode' / Int8ub,
    'counter_boot' / Int32ub,
    'latchup' / Int16ub[6],
    'counter_wdt_csp' / Int32ub[2],
    'counter_wdt_gnd' / Int32ub,
    'counter_wdt_i2c' / Int32ub,
    'output' / Int8ub[8],
    'wdt_gnd_time_left' / Int32ub,
    'wdt_i2c_time_left' / Int32ub,
    'vbatt' / Int16ub,
    'vboost' / Int16ub[3],
    'wdtcspc' / Int8ub[2])

TTC = Struct(
    'temp_brd' / LinearAdapter(10, Int16sb),
    'last_rferr' / Int16sb,
    'last_rssi' / Int16sb,
    'tot_rx_bytes' / Int32ub,
    'rx_bytes' / Int32ub,
    'tot_rx_count' / Int32ub,
    'rx_count' / Int32ub,
    'tot_tx_bytes' / Int32ub,
    'tx_bytes' / Int32ub,
    'tot_tx_count' / Int32ub,
    'tx_count' / Int32ub,
    'temp_pa' / LinearAdapter(10, Int16sb),
    'boot_cause' / Int32ub,
    'bgnd_rssi' / Int16sb,
    'active_conf' / Int8ub,
    'boot_count' / Int16ub,
    'last_contact' / Int32ub,
    'tx_duty' / Int8ub)

GSSBEntry = Struct(
    'reboots' / Int8ub,
    'current_state' / Int8ub,
    'antenna_state' / Int8ub,
    'attempts_total' / Int16ub)

GSSB =  GSSBEntry[4]

TTCGSSB = Struct(
    'gssb' / GSSB,
    'ttc' / TTC)

AOCS = Struct(
    'extmag_valid' / Int8ub,
    'extmag' / Float32b[3],
    'gps_pos_dev' / Float32b[3],
    'gps_pos' / Float32b[3],
    'gps_valid' / Int8ub,
    'gyro_valid' / Int8ub,
    'gyro' / Float32b[3],
    'mag' / Float32b[3],
    'mag_valid' / Int8ub,
    'status_run' / Int8sb,
    'acs_mode' / Int8sb,
    'ads_mode' / Int8sb,
    'ephem_mode' / Int8sb,
    'bdot_detumb' / Int8ub,
    'boot_cause' / Int32ub,
    'boot_count' / Int16ub,
    'cur_gssb' / Int16ub[2],
    'cur_pwm' / Int16ub,
    'cur_gps' / Int16ub,
    'cur_wde' / Int16ub)

Temps = Struct(
    'aocs_suns' / Float32b[5],
    'not_used' / Float32b,
    'aocs_extmag' / Float32b,
    'aocs_fss' / Float32b[5],
    'not_used2' / Float32b[3],
    'aocs_gyro' / Float32b,
    'aocs' / LinearAdapter(10, Int16sb)[2],
    'eps' / Int16sb[6],
    'obc' / LinearAdapter(10, Int16sb)[2],
    'obc_gyro' / Float32b,
    'ttc_brd' / LinearAdapter(10, Int16sb),
    'ttc_pa' / LinearAdapter(10, Int16sb))

payloads = {1 : OBC, 2 : EPS, 3 : TTCGSSB, 4 : AOCS, 5: Temps}

UserData = Struct(
    'id' / Int16ub,
    'data' / Switch(this.id, payloads, default = Bytes(this._.space_packet_header.data_length-16))
    )

Beacon = Struct(
    'tm_header' / TMHeader,
    'space_packet_header' / ccsds_space_packet.PrimaryHeader,
    'pus_header' / ecss_pus.TMSecondaryHeader,
    'pus_time_field' / TimeField,
    'payload' / UserData,
    'space_packet_tail' / SPTail,
    'tm_tail' / TMTail)

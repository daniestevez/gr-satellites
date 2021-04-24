#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import datetime

from construct import *
from .ax25 import Header


# An adapted version of Space Packet primary header
# where the APID is broken down as used by the PicSat mission
PrimaryHeader = BitStruct(
    'ccsds_version' / BitsInteger(3),
    'packet_type' / Flag,
    'secondary_header_flag' / Flag,
    'process_id' / BitsInteger(4),
    'level_flag' / Flag,
    'payload_flag' / Flag,
    'packet_category' / BitsInteger(5),
    'sequence_flag' / BitsInteger(2),
    'packet_id' / BitsInteger(14),
    'data_length' / BitsInteger(16)
    )


class TimeAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        d = obj - datetime.datetime(1970, 1, 1)
        return Container(
            days=d.days,
            milliseconds=d.seconds * 1000 + d.microseconds / 1000)

    def _decode(self, obj, context, path=None):
        return (datetime.datetime(1970, 1, 1)
                + datetime.timedelta(
                    days=obj.days,
                    seconds=obj.milliseconds/1000,
                    microseconds=(obj.milliseconds % 1000) * 1000))


SecondaryHeaderTM = TimeAdapter(
    Struct('days' / Int16ub, 'milliseconds' / Int32ub))

SecondaryHeaderTC = BitStruct(
    'req_ack_reception' / Flag,
    'req_fmt_reception' / Flag,
    'req_exe_reception' / Flag,
    'telecommand_id' / BitsInteger(10),
    'emitter_id' / BitsInteger(3),
    'signature' / Bytes(16)
    )

AntStatus = Struct(
    'undeployed' / Flag,
    'timeout' / Flag,
    'deploying' / Flag
    )

BeaconA = BitStruct(
    Padding(1),
    'solar_panel_error_flags' / Flag[5],
    'i_adcs_get_attitude_error' / Flag,
    'i_adcs_get_status_register_error' / Flag,
    Padding(1),
    'fram_enable_error_flag' / Flag,
    'ants_error_flag' / Flag[2],
    'trxvu_tx_error_flag' / Flag,
    'trxvu_rx_error_flag' / Flag,
    'obc_supervisor_error_flag' / Flag,
    'gom_eps_error_flag' / Flag,
    'ant1_status_b' / AntStatus,
    Padding(1),
    'ant2_status_b' / AntStatus,
    'ignore_flag_ants_b_status' / Flag,
    'ant3_status_b' / AntStatus,
    Padding(1),
    'ant4_status_b' / AntStatus,
    'armed_ants_b_status' / Flag,
    'ant1_status_a' / AntStatus,
    Padding(1),
    'ant2_status_a' / AntStatus,
    'ignore_flag_ants_a_status' / Flag,
    'ant3_status_a' / AntStatus,
    Padding(1),
    'ant4_status_a' / AntStatus,
    'armed_ants_a_status' / Flag
    )

BeaconB = Struct(
    'solar_panel_temps' / Int16ub[5],
    'ants_temperature' / Int16ub[2],
    'tx_trxvu_hk_current' / Int16ub,
    'tx_trxvu_hk_forwardpower' / Int16ub,
    'tx_trxvu_tx_reflectedpower' / Int16ub,
    'tx_trxvu_hk_pa_temp' / Int16ub,
    'rx_trxvu_hk_pa_temp' / Int16ub,
    'rx_trxvu_hk_board_temp' / Int16ub,
    'eps_hk_temp_batts' / Int16sb,
    'eps_hk_batt_mode' / Int8ub,
    'eps_h_kv_batt' / Int8ub,
    'eps_hk_boot_cause' / Int32ub,
    'n_reboots_eps' / Int32ub,
    'n_reboots_obc' / Int32ub,
    'quaternions' / Float32b[4],
    'angular_rates' / Float32b[3]
    )

BeaconC = BitStruct(
    Padding(12),
    'adcs_stat_flag_hl_op_tgt_cap' / Flag,
    'adcs_stat_flag_hl_op_tgt_track_fix_wgs84' / Flag,
    'adcs_stat_flag_hl_op_tgt_track_nadir' / Flag,
    'adcs_stat_flag_hl_op_tgt_track' / Flag,
    'adcs_stat_flag_hl_op_tgt_track_const_v' / Flag,
    'adcs_stat_flag_hl_op_spin' / Flag,
    Padding(1),
    'adcs_stat_flag_hl_op_sunp' / Flag,
    'adcs_stat_flag_hl_op_detumbling' / Flag,
    'adcs_stat_flag_hl_op_measure' / Flag,
    Padding(5),
    'adcs_stat_flag_datetime_valid' / Flag,
    Padding(1),
    'adcs_stat_flag_hl_op_safe' / Flag,
    'adcs_stat_flag_hl_op_idle' / Flag,
    Padding(1)
    )

BeaconD = Struct(
    'up_time' / Int32ub,
    'last_fram_log_fun_err_code' / Int16sb,
    'last_fram_log_line_code' / Int16ub,
    'last_fram_log_file_crc_code' / Int32ub,
    'last_fram_log_counter' / Int16ub,
    'average_photon_count' / Int16ub,
    'sat_mode' / Int8ub,
    'tc_sequence_count' / Int16ub
    )

Beacon = Struct(Padding(3), BeaconA, BeaconB, BeaconC, BeaconD)

PayloadBeaconFlags = BitStruct(
    'hk_flag' / Flag,
    'cheatmode_flag' / Flag,
    'tec_flag' / Flag,
    'sensors_flag' / Flag,
    'hv_flag' / Flag,
    'dac_flag' / Flag,
    'interrupt_flag' / Flag,
    'diode_flag' / Flag
    )

PayloadBeacon = Struct(
    'message' / Bytes(29),
    'phot' / Int16ub,
    'mode' / Int8ub,
    'acqmode' / Int8ub,
    PayloadBeaconFlags,
    'proc_freq' / Int8ub,
    'volt5' / Int16ub,
    'amp5' / Int16ub,
    'amp3' / Int16ub,
    'volthv' / Int16ub,
    'amphv' / Int16ub,
    'temps' / Int16sb[4],
    'vitec' / Int16ub,
    'temp0' / Int16ub,
    'errortherm' / Int16ub,
    'vref' / Int16ub,
    'pitch' / Int16sb,
    'roll' / Int16sb,
    'yaw' / Int16sb
    )

picsat = Struct(
    'ax25_header' / Header,
    'primary_header' / PrimaryHeader,
    'secondary_header' / IfThenElse(
        lambda c: c.primary_header.packet_type,
        SecondaryHeaderTC, SecondaryHeaderTM),
    'packet' / Switch(
        lambda c: (c.primary_header.payload_flag,
                   c.primary_header.packet_category),
        {
            (False, 1): Beacon,
            (True, 7): PayloadBeacon,
            }, default=Pass
        )
    )

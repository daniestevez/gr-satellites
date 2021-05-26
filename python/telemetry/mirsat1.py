#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from .ax25 import Header as AX25Header


BeaconA = BitStruct(
    Bytewise(Const(b'\x00')),  # start byte
    'obc_boot_image' / BitsInteger(8),
    'onboard_time' / BitsInteger(32),
    'uptime' / BitsInteger(32),
    'spacecraft_mode' / BitsInteger(3),
    'separation_seq_state' / BitsInteger(4),
    'solar_array_deploy' / BitsInteger(4)[4],
    'antenna_deploy' / BitsInteger(16)[8],
    'adm_soft_fire_count' / BitsInteger(8),
    'adm_hard_fire_count' / BitsInteger(8),
    'adm_tlm' / BitsInteger(80)[10],
    'sadm_check_count' / BitsInteger(5),
    'sadm_telemetry' / BitsInteger(64)[10],
    'i2c_nack_addr_count' / BitsInteger(32),
    'i2c_hw_state_err_count' / BitsInteger(32),
    'i2c_isr_err_count' / BitsInteger(32),
    'battery_current_dir' / Enum(BitsInteger(1), discharging=0, charging=1),
    'battery_current' / BitsInteger(10),
    'battery_current_msb' / BitsInteger(1)
    )

BeaconPartB = BitStruct(
    'battery_current_lsbs' / BitsInteger(9),
    'battery_current' / BitsInteger(10),
    'battery_voltage' / BitsInteger(10)[3],
    'battery_temp' / BitsInteger(10),
    'solar_current' / BitsInteger(10),
    'solar_voltage' / BitsInteger(10)[9],  # last 5 unused
    'eps_bus_voltage' / BitsInteger(10)[4],
    'eps_bus_current' / BitsInteger(10)[4],
    'adcs_raw_gyro' / Bytewise(Int16ub[3]),
    'adcs_mtq_dir_duty' / BitsInteger(8)[6],
    'adcs_status' / BitsInteger(16),
    'adcs_bus_voltage' / BitsInteger(16)[3],
    'adcs_bus_current' / BitsInteger(16)[3],
    'adcs_board_temp' / BitsInteger(16),
    'adcs_adc_ref' / BitsInteger(16),
    'adcs_sensor_current' / BitsInteger(16),
    'adcs_mtq_current' / BitsInteger(16),
    'adcs_array_temp' / BitsInteger(16)[6],
    'adcs_css_raw' / BitsInteger(16)[6],
    'fss_active' / BitsInteger(2)[6],
    'css_active_selected' / BitsInteger(2)[6],
    'adcs_sun_processed' / BitsInteger(16)[3],
    'reserved' / BitsInteger(16)[4],
    'adcs_detumble_counter' / BitsInteger(16),
    'adcs_mode' / BitsInteger(16),
    'adcs_state' / BitsInteger(16),
    'reservedA' / BitsInteger(10),
    'reservedB' / BitsInteger(4),
    'reservedC' / BitsInteger(16),
    'reservedD' / BitsInteger(3),
    'reservedE' / BitsInteger(4),
    'cmc_rx_lock' / Flag,
    'cmc_rx_frame_count' / BitsInteger(16),
    'cmc_rx_packet_count' / BitsInteger(16),
    'cmc_rx_dropped_error_count' / BitsInteger(16),
    'cmc_rx_crc_error_count' / BitsInteger(16),
    'cmc_rx_overrun_error_count' / BitsInteger(8),
    'cmc_rx_protocol_error_count' / BitsInteger(16),
    'cmc_smps_temperature' / Bytewise(Int8ub),
    'cmc_pa_temperature' / Bytewise(Int8ub),
    'ax25_mux_channel_enable' / Flag[3],
    'digipeater_enable' / Flag,
    'pacsat_broadcast_enable' / Flag,
    'pacsat_broadcast_in_progress' / Flag,
    'param_valid_flags' / Flag[40],
    Padding(5),
    'checksum' / BitsInteger(16),
)

BeaconHeader = Struct(
    'packet_type' / Int8ub,
    'apid' / Int8ub,
    'sequence_count' / Int16ub,
    'length' / Int16ub,
    'reserved' / Int8ub,
    'service_type' / Const(b'\x03'),
    'service_subtype' / Const(b'\x19')
    )

BeaconPartA = Struct(
    'beacon_header' / BeaconHeader,
    'beacon' / BeaconA,
    )

mirsat1 = Struct(
    'ax25_header' / AX25Header,
    'telemetry' / If(
        this.ax25_header.pid == 0xF0,
        Struct(
            'header' / Bytes(6),
            'beacon' / Select(BeaconPartA, BeaconPartB)
            ))
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *
from ..adapters import AffineAdapter, LinearAdapter

TMPrimaryHeader = BitStruct(
    'transfer_frame_version_number' / BitsInteger(2),
    'spacecraft_id' / BitsInteger(10),
    'virtual_channel_id' / BitsInteger(3),
    'ocf_flag' / Flag,
    'master_channel_frame_count' / BitsInteger(8),
    'virtual_channel_frame_count' / BitsInteger(8),
    'first_header_pointer' / BitsInteger(8)
    )

syncA = bytes([0x55, 0x55, 0x55, 0x55, 0x55, 0x55,
                   0x00, 0x00, 0x08, 0x77, 0x80, 0x00, 0x00, 0x63])

syncB = bytes([0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x00, 0x26])

IVbat = LinearAdapter(2.5, Int16sb)
UVbat = LinearAdapter(2000.0, Int16sb)

Id = BitStruct(
    'other' / BitsInteger(13),
    'transponder' / Flag,
    'beacon' / Flag,
    'telemetry' / Flag
    )

hk_STM32_first_half = Struct(
    'id' / Id,
    'config' / Int8ub,
    'last_command' / Int8ub,
    'payload_mode' / Int8ub,
    'tx_mode' / Int8ub,
    'gain_tx' / Int16sb,
    'i_3v3' / LinearAdapter(10.0, Int16sb),
    'u_3v3' / LinearAdapter(2000.0, Int16sb),
    'i_vbat_tx' / IVbat,
    'u_vbat_tx' / UVbat,
    'i_vbat_rx' / IVbat,
    'u_vbat_rx' / UVbat,
    't_stm32' / AffineAdapter(1.0/0.29296875, (304.0 - 25.0)/0.29296875, Int16sb),
    't_pa' / LinearAdapter(8.0*16.0, Int16sb),
    'n_tx_rf' / Int16ub,
    'n_rx_rf' / Int16ub,
    'n_tx_err_rf' / Int16ub,
    'n_rx_err_rf' / Int16ub,
    'n_tx_can' / Int16ub,
    'n_rx_can' / Int16ub,
    'n_tx_err_can' / Int16ub,
    'n_rx_err_can' / Int16ub,
    'n_tc' / Int32ub,
    'dc_fm_tc' / Int16sb,
    'dc_fm_ham' / Int16sb,
    'rssi_fm_tc' / Int32ub,
    'rssi_fm_ham' / Int32ub,
    'reset_flag' / Int8ub,
    'sys_flag' / Int8ub,
    'dma_overflow' / Int16ub,
    'runtime_msb' / Int16ub
)

hk_STM32_second_half = Struct(
    'runtime_lsb' / Int16ub,
    'reset_count' / Int32ub,
    'ctcss_count' / Int32ub,
    'ctcss_det' / Float32b
    )

hk_AVR = Struct(
    'adf7021_ld' / Int8ub,
    'err_flag' / Int8ub,
    'callsign' / Bytes(6),
    'n_tx_232' / Int16ub,
    'n_rx_232' / Int16ub,
    'runtime' / Int32ub,
    'rssi_analog' / Int8ub,
    'n_rssi_const' / Int8ub,
    'unlock_count' / Int8ub,
    'reset_flag' / Int8ub,
    'reset_count' / Int32ub
    )

frameA = Struct(
    'header' / TMPrimaryHeader,
    Const(syncA),
    'hk_STM32_first' / hk_STM32_first_half
    )

frameB = Struct(
    'header' / TMPrimaryHeader,
    Const(syncB),
    'hk_STM32_second' / hk_STM32_second_half,
    'hk_AVR' / hk_AVR,
    'padding' / Bytes(30)
    )

framePadding = Struct(
    'header' / TMPrimaryHeader,
    'padding' / Bytes(76)
    )

by02 = Select(frameA, frameB, framePadding)

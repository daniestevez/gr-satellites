#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 jgromes <gromes.jan@gmail.com>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from ..adapters import LinearAdapter


FuncId = Enum(
    Int8ul,
    RESP_PONG=0x20,
    RESP_REPEATED_MESSAGE=0x21,
    RESP_REPEATED_MESSAGE_CUSTOM=0x22,
    RESP_SYSTEM_INFO=0x23,
    RESP_PACKET_INFO=0x24,
    RESP_STATISTICS=0x25,
    RESP_FULL_SYSTEM_INFO=0x26,
    RESP_STORE_AND_FORWARD_ASSIGNED_SLOT=0x27,
    RESP_FORWARDED_MESSAGE=0x28,
    RESP_PUBLIC_PICTURE=0x29,
    RESP_DEPLOYMENT_STATE=0x2A,
    RESP_RECORDED_SOLAR_CELLS=0x2B,
    RESP_CAMERA_STATE=0x2C,
    RESP_RECORDED_IMU=0x2D,
    RESP_MANUAL_ACS_RESULT=0x2E,
    RESP_GPS_LOG=0x2F,
    RESP_GPS_LOG_STATE=0x30,
    RESP_FLASH_CONTENTS=0x31,
    RESP_CAMERA_PICTURE=0x32,
    RESP_CAMERA_PICTURE_LENGTH=0x33,
    RESP_GPS_COMMAND_RESPONSE=0x34,
    RESP_ACKNOWLEDGE=0x3F,
    )

Pong = Struct()

RepeatedMessage = Struct(
    'sender_id' / Int32ul,
    'msg' / HexDump(GreedyBytes),
    )

VoltageValue = LinearAdapter(1e3/20, Int8ul)
CurrentValue = LinearAdapter(1e6/10, Int16sl)
TempValue = LinearAdapter(1e3/10, Int16sl)

SystemInfo = Struct(
    'mppt_v_out' / VoltageValue,
    'mmpt_i_out' / CurrentValue,
    'onboard_time' / Int32ul,
    'power_cfg' / BitStruct(
        Padding(1),
        'mppt_keep_alive' / Flag,
        'mppt_temp_switch' / Flag,
        Padding(2),
        'lp_active' / Flag,
        'lp_enabled' / Flag,
        'tx_enabled' / Flag,
        ),
    'reset_ctr' / Int16ul,
    'xa_v_in' / VoltageValue,
    'xb_v_in' / VoltageValue,
    'za_v_in' / VoltageValue,
    'zb_v_in' / VoltageValue,
    'y_v_in' / VoltageValue,
    'batt_temp' / TempValue,
    'obc_temp' / TempValue,
    'flash_err_ctr' / Int32ul,
    )

SNRValue = LinearAdapter(1/4, Int8sl)
RSSIValue = LinearAdapter(1/-2, Int8ul)

PacketInfo = Struct(
    'last_snr' / SNRValue,
    'last_rssi' / RSSIValue,
    'lora_valid_ctr' / Int16ul,
    'lora_invalid_ctr' / Int16ul,
    'fsk_valid_ctr' / Int16ul,
    'fsk_invalid_ctr' / Int16ul,
    )

StatsEntryTemp = Struct(
    'min' / TempValue,
    'avg' / TempValue,
    'max' / TempValue,
    )

StatsEntryCurrent = Struct(
    'min' / CurrentValue,
    'avg' / CurrentValue,
    'max' / CurrentValue,
    )

StatsEntryVoltage = Struct(
    'min' / VoltageValue,
    'avg' / VoltageValue,
    'max' / VoltageValue,
    )

StatsEntryFloat = Struct(
    'min' / Float32l,
    'avg' / Float32l,
    'max' / Float32l,
    )

StatsTemperatures = Struct(
    'panel_y' / StatsEntryTemp,
    'top' / StatsEntryTemp,
    'bottom' / StatsEntryTemp,
    'battery' / StatsEntryTemp,
    'sec_battery' / StatsEntryTemp,
    )

StatsCurrents = Struct(
    'xa' / StatsEntryCurrent,
    'xb' / StatsEntryCurrent,
    'za' / StatsEntryCurrent,
    'zb' / StatsEntryCurrent,
    'y' / StatsEntryCurrent,
    'mppt' / StatsEntryCurrent,
    )

StatsVoltages = Struct(
    'xa' / StatsEntryVoltage,
    'xb' / StatsEntryVoltage,
    'za' / StatsEntryVoltage,
    'zb' / StatsEntryVoltage,
    'y' / StatsEntryVoltage,
    'mppt' / StatsEntryVoltage,
    )

StatsLight = Struct(
    'panel_y' / StatsEntryFloat,
    'top' / StatsEntryFloat,
    )

StatsAxes = Struct(
    'x' / StatsEntryFloat,
    'y' / StatsEntryFloat,
    'z' / StatsEntryFloat,
    )

StatsIMU = Struct(
    'gyro' / StatsAxes,
    'accel' / StatsAxes,
    'mag' / StatsAxes,
    )

Statistics = Struct(
    'flags' / BitStruct(
        Padding(3),
        'has_imu' / Flag,
        'has_light' / Flag,
        'has_volt' / Flag,
        'has_curr' / Flag,
        'has_temp' / Flag,
        ),
    'stats' / Struct(
        'temperature' / Optional(If(this._.flags.has_temp, StatsTemperatures)),
        'current' / Optional(If(this._.flags.has_curr, StatsCurrents)),
        'voltage' / Optional(If(this._.flags.has_volt, StatsVoltages)),
        'light' / Optional(If(this._.flags.has_light, StatsLight)),
        'imu' / Optional(If(this._.flags.has_imu, StatsIMU)),
        ),
    )

FullSystemInfo = Struct(
    'mppt_v_out' / VoltageValue,
    'mmpt_i_out' / CurrentValue,
    'onboard_time' / Int32ul,
    'power_cfg' / BitStruct(
        Padding(1),
        'mppt_keep_alive' / Flag,
        'mppt_temp_switch' / Flag,
        Padding(2),
        'lp_active' / Flag,
        'lp_enabled' / Flag,
        'tx_enabled' / Flag,
        ),
    'reset_ctr' / Int16ul,
    'xa_v_in' / VoltageValue,
    'xa_i_in' / CurrentValue,
    'xb_v_in' / VoltageValue,
    'xb_i_in' / CurrentValue,
    'za_v_in' / VoltageValue,
    'za_i_in' / CurrentValue,
    'zb_v_in' / VoltageValue,
    'zb_i_in' / CurrentValue,
    'y_v_in' / VoltageValue,
    'y_i_in' / CurrentValue,
    'y_temp' / TempValue,
    'obc_board_temp' / TempValue,
    'bottom_temp' / TempValue,
    'batt_temp' / TempValue,
    'sec_batt_temp' / TempValue,
    'mcu_temp' / TempValue,
    'y_lux' / Float32l,
    'top_lux' / Float32l,
    'x_bridge_fault' / Int8ul,
    'y_bridge_fault' / Int8ul,
    'z_bridge_fault' / Int8ul,
    'flash_err_ctr' / Int32ul,
    'fsk_rx_len' / Int8ul,
    'lora_rx_len' / Int8ul,
    'sensors' / BitStruct(
        'light_top' / Flag,
        'light_y' / Flag,
        'curr_mppt' / Flag,
        'curr_y' / Flag,
        'curr_zb' / Flag,
        'curr_za' / Flag,
        'curr_xb' / Flag,
        'curr_xa' / Flag,
        ),
    'last_adcs_res' / Int8ul,
    )

StoreAndForwardAssigned = Struct(
    'assigned_slot' / Int16ul,
    )

ForwardedMessage = Struct(
    'msg' / HexDump(GreedyBytes),
    )

DeploymentState = Struct(
    'deploy_ctr' / Int8ul,
    )

CameraState = Struct(
    'cam_state' / Int32ul,
    )

SampleAxes = Struct(
    'x' / Float32l,
    'y' / Float32l,
    'z' / Float32l,
    )

RecordedIMU = Struct(
    'flags' / BitStruct(
        Padding(5),
        'has_mag' / Flag,
        'has_accel' / Flag,
        'has_gyro' / Flag,
        ),
    'samples' / Struct(
        'gyro' / Optional(If(this._.flags.has_gyro, SampleAxes)),
        'accel' / Optional(If(this._.flags.has_accel, SampleAxes)),
        'mag' / Optional(If(this._.flags.has_mag, SampleAxes)),
        )
    )

ManualACSResult = Struct(
    'x_bridge_fault' / Int8ul,
    'y_bridge_fault' / Int8ul,
    'z_bridge_fault' / Int8ul,
    'adcs_elapsed' / Int32ul,
    )

GPSLog = Struct(
    'time' / Int32ul,
    'data' / HexDump(GreedyBytes),
    )

GPSLogState = Struct(
    'length' / Int32ul,
    'last_entry_addr' / Int32ul,
    'last_fix_addr' / Int32ul,
    )

FlashContents = Struct(
    'data' / HexDump(GreedyBytes),
    )

CameraPicture = Struct(
    'packet_id' / Int16ul,
    'data' / HexDump(GreedyBytes),
    )

CameraPictureLength = Struct(
    'len' / Int32ul,
    )

GPSCommandResponse = Struct(
    'resp' / HexDump(GreedyBytes),
    )

Acknowledge = Struct(
    'acked_func_id' / FuncId,
    'status' / Enum(
        Int8ul,
        ACK_OK=0x00,
        ACK_CALLSIGN_MISMATCH=0x01,
        ACK_RX_FAILED=0x02,
        ACK_FUNC_ID_FAILED=0x03,
        ACK_DECRYPT_FAILED=0x04,
        ACK_OPT_DATA_LEN_FAILED=0x05,
        ACK_FUNC_ID_UKNOWN=0x06,
        ),
    )

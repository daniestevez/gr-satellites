#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

from construct import *
from ..adapters import AffineAdapter, LinearAdapter

Id = Enum(Int8ub,\
              beacon_ngham_obdh_data = 0x00,\
              beacon_ngham_eps_data = 0x01,\
              beacon_ngham_ttc_data = 0x02,\
              beacon_ax25_obdh_data = 0x03,\
              beacon_ax25_eps_data = 0x04,\
              beacon_ax25_ttc_data = 0x05,\
              downlink_telemetry = 0x10,\
              downlink_ping_answer = 0x11,\
              downlink_data_request_answer = 0x12,\
              downlink_hibernation_feedback = 0x13,\
              downlink_charge_reset_feedback = 0x14,\
              downlink_message_broadcast = 0x15,\
              downlink_payload_x_status = 0x16,\
              downlink_rush_status = 0x17,\
              uplink_ping_request = 0x20,\
              uplink_data_request = 0x21,\
              uplink_enter_hibernation = 0x22,\
              uplink_leave_hibernation = 0x23,\
              uplink_charge_reset = 0x24,\
              uplink_broadcast_message = 0x25,\
              uplink_payload_x_status_request = 0x26,\
              uplink_payload_x_status_swap = 0x27,\
              uplink_payload_x_data_upload = 0x28,\
              uplink_rush_enable = 0x29\
              )

BatteryVoltage = LinearAdapter(32/4.883e-3, Int16ub)
BatteryTemperature = LinearAdapter(32/0.125, Int24ub)
BatteryCharge = LinearAdapter(1/6.25e-4, Int16ub)
SolarPanelCurrent = LinearAdapter(1/((2.5/4095)*(1/(0.05*0.025*3300))), Int16ub)
SolarPanelVoltage = AffineAdapter(4095/2.5, -93.1/100, Int16ub)
ImuAccel = LinearAdapter(32768.0/16.0, Int16sb)
ImuGyro = LinearAdapter(32768.0/250, Int16sb)

OBDHStatus = BitStruct(
    Padding(3),
    'antenna' / Flag,
    'imu' / Flag,
    'sd_card' / Flag,
    'rush' / Flag,
    'eps' / Flag
    )

SystemTime = Struct(
    'seconds' / Int8ub,
    'minutes' / Int24ub,
    )

EPS = Struct(
    'battery_voltage' / BatteryVoltage[2],
    'battery_temperature' / BatteryTemperature[2],
    'battery_charge' / BatteryCharge,
    'solar_panel_current' / SolarPanelCurrent[6],
    'solar_panel_voltage' / SolarPanelVoltage[3],
    'energy_level' / Int8ub,
    )

OBDH = Struct(
    'eps' / EPS,
    'status' / OBDHStatus,
    'imu_accelerometer' / ImuAccel[3],
    'imu_gyroscope' / ImuGyro[3],
    'system_time' / SystemTime,
    'odbh_resets' / Int8ub
    )

floripasat = Struct(
    'ngham_padding' / Int8ub,
    'id' / Id,
    'callsign' / Bytes(7),
    'payload' / Switch(this.id, {
        'beacon_ngham_obdh_data' : OBDH,
        'beacon_ngham_eps_data' : EPS,
        'beacon_ax25_obdh_data' : OBDH,
        'beacon_ax25_eps_data' : EPS,
        }, default = GreedyBytes)
    )

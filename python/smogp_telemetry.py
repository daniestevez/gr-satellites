#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 Daniel Estevez <daniel@destevez.net>
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
from .adapters import AffineAdapter, LinearAdapter, UNIXTimestampAdapter

Timestamp = UNIXTimestampAdapter(Int32sl)

Temperature = LinearAdapter(10.0, Int16sl)
Voltage = LinearAdapter(1000.0, Int16ul)

AntennaStatus = Enum(BitsInteger(2), closed = 0, open = 1, not_monitored = 2, invalid = 3)

PanelStatus = BitStruct(
    'panel_number' / BitsInteger(3),
    'antenna_status' / AntennaStatus,
    Padding(3)
    )

MPPT = Struct(
    'timestamp' / Timestamp,
    'temperature' / Temperature,
    'light_sensor' / Voltage,
    'input_current' / Int16ul,
    'input_voltage' / Voltage,
    'output_current' / Int16ul,
    'output_voltage' / Voltage,
    'panel_status' / PanelStatus
    )

AckInfo = Struct(
    'serial' / Int16sl,
    'rssi' / AffineAdapter(2.0, 2.0 * 131.0, Int8ul)
    )

Telemetry1 = Struct(
    'timestamp' / Timestamp,
    'mppts' / MPPT[6],
    'ack_info' / AckInfo[3],
    )

DeploymentStatus = BitStruct(
    'deployment_switch' / Flag[2],
    'remove_before_flight' / Flag,
    Padding(1),
    'pcu_deployment' / Flag,
    'antenna_deployment' / Flag,
    Padding(2)
    )

PCU_DEP = Struct(
    'timestamp' / Timestamp,
    'deployment_status' / DeploymentStatus,
    'pcu_boot_counter' / Int16ul,
    'pcu_uptime_minutes' / Int16ul
    )

SDC = Struct(
    'input_current' / Int16ul,
    'output_current' / Int16ul,
    'output_voltage' / Voltage)

SDCLimiters = BitStruct(
    'sdc1_overcurrent_status' / Flag,
    'sdc1_overvoltage_status' / Flag,
    'sdc2_overcurrent_status' / Flag,
    'sdc2_overvoltage_status' / Flag,
    Padding(4)
    )

PCU_SDC = Struct(
    'timestamp' / Timestamp,
    'sdcs' / SDC[2],
    'limiters' / SDCLimiters
    )

BatteryStatus = BitStruct(
    'battery_charge_overcurrent' / Flag,
    'battery_charge_overvoltage' / Flag,
    'battery_discharge_overcurrent' / Flag,
    'battery_discharge_overvoltage' / Flag,
    'battery_charge_enabled' / Flag,
    'battery_discharge_enabled' / Flag,
    Padding(2)
    )

PCU_Bat = Struct(
    'timestamp' / Timestamp,
    'battery_voltage' / Voltage,
    'battery_charge_current' / Int16ul,
    'battery_discharge_current' / Int16ul,
    'battery_status' / BatteryStatus
    )

OBCLimiter = BitStruct(
    'obc_overcurrent' / Flag[2],
    Padding(6)
    )

PCU_Bus = Struct(
    'timestamp' / Timestamp,
    'unregulated_bus_voltage' / Voltage,
    'regulated_bus_voltage' / Voltage,
    'obc_current_consumption' / Int16ul[2],
    'obc_limiter' / OBCLimiter
    )

Telemetry2 = Struct(
    'timestamp' / Timestamp,
    'pcu_dep' / PCU_DEP[2],
    'pcu_sdc' / PCU_SDC[2],
    'pcu_bat' / PCU_Bat[2], # Note ATL-1 doesn't use pcu_bat, but leaves these bytes unused
    'pcu_bus' / PCU_Bus[2],
    'ack_info' / AckInfo[3]
    )

ComStatus = BitStruct(
    'com_data_rate' / BitsInteger(3),
    'tx_power_level' / BitsInteger(2),
    Padding(3)
    )

ComProtection = BitStruct(
    'com1_overcurrent' / Flag,
    'com2_overcurrent' / Flag,
    'com1_limiter_switch' / Flag,
    'com2_limiter_switch' / Flag,
    'com1_limiter_switch_override' / Flag,
    'com2_limiter_switch_override' / Flag,
    Padding(2)
    )
    
Functional = BitStruct(
    'msen' / Flag[2],
    'flash' / Flag[2],
    'rtcc' / Flag[2],
    Padding(1),
    'current_com' / BitsInteger(1)
    )

COM = Struct(
    'timestamp' / Timestamp,
    'swr_bridge' / Int8ul,
    'last_rx_rssi' / Int8sl,
    'spectrum_analyzer_status' / Int8ul,
    'active_com_voltage' / Voltage,
    'active_com_temperature' / Temperature,
    'active_com_spectrum_analyzer_temperature' / Temperature
    )

TID = Struct(
    'timestamp' / Timestamp,
    'temperature' / Temperature,
    'voltage' / Voltage,
    'radfet_voltage' / Int24ub[2],
    'measurement_serial' / Int16ul
    )

MSEN = Struct(
    'msen_gyroscope' / Int16sl[3],
    'msen_magneto' / Int16sl[3],
    Padding(6),
    'msen_temperature' / Temperature
    )

Telemetry3 = Struct(
    'timestamp' / Timestamp,
    'obc_supply_voltage' / Voltage,
    'rtcc_temperature' / Int16sl[2],
    Padding(2),
    'eps2_panel_a_temperature' / Temperature[2],
    'com_status' / ComStatus,
    'com_tx_current' / Int16ul,
    'com_rx_current' / Int16ul,
    'com_protection' / ComProtection,
    'msen' / MSEN[2],
    'functional' / Functional,
    'com' / COM,
    'tid' / TID[2],
    'ack_info' / AckInfo[3]
    )    

UplinkStats = Struct(
    'valid_packets' / Int32sl,
    'rx_error_wrong_size' / Int16ul,
    'rx_error_golay_failed' / Int16ul,
    'rx_error_wrong_signature' / Int16ul,
    'rx_error_invalid_serial' / Int16ul,
    'obc_com_trx_error_statistic' / Int32ul
    )

Beacon = Struct(
    'timestamp' / Timestamp,
    'beacon_message' / PaddedString(80, 'utf8'),
    'uplink_stats' / UplinkStats,
    'ack_info' / AckInfo[3]
    )    

Frame = Struct(
    'type' / Int8ul,
    'payload' / Switch(this.type, {
        1 : Telemetry1,
        2 : Telemetry2,
        3 : Telemetry3,
        4 : Beacon,
        }, default = GreedyBytes)
    )

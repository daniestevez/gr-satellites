#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019-2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

from construct import *
from ..adapters import AffineAdapter, LinearAdapter, UNIXTimestampAdapter, TableAdapter

import numpy as np

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

# This is like SMOG-P but with some extra fields at the end
Telemetry2_SMOG1 = Struct(
    'timestamp' / Timestamp,
    'pcu_dep' / PCU_DEP[2],
    'pcu_sdc' / PCU_SDC[2],
    'pcu_bat' / PCU_Bat[2], # Note ATL-1 doesn't use pcu_bat, but leaves these bytes unused
    'pcu_bus' / PCU_Bus[2],
    'ack_info' / AckInfo[3],
    'pcu_voltage' / Voltage[2]
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

Functional_SMOG1 = BitStruct(
    'msen' / Flag[2],
    'flash' / Flag[2],
    'rtcc' / Flag[2],
    'obc' / BitsInteger(1), # active OBC
    'current_com' / BitsInteger(1) # active COM
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

MSEN_SMOG1 = Struct(
    'msen_gyroscope' / Int16sl[3],
    'msen_magneto' / Int16sl[3],
    'msen_accel' / Int16sl[3],
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

# This is like SMOG-P but with an some fields instead of padding
Telemetry3_SMOG1 = Struct(
    'timestamp' / Timestamp,
    'obc_supply_voltage' / Voltage,
    'rtcc_temperature' / Temperature[2],
    'obc_temperature' / Temperature,
    'eps2_panel_a_temperature' / Temperature[2],
    'com_status' / ComStatus,
    'com_tx_current' / Int16ul,
    'com_rx_current' / Int16ul,
    'com_protection' / ComProtection,
    'msen' / MSEN_SMOG1[2],
    'functional' / Functional_SMOG1,
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

DiagnosticStatus = BitStruct(
    'energy_mode' / BitsInteger(3),
    'tcxo_works' / Flag,
    'filesystem_works' / Flag,
    'filesystem_uses_flash2' / Flag,
    Padding(2)
    )

DiagnosticInfo = Struct(
    Padding(1),
    'num_recv_pkt_garbage' / Int8ul,
    'num_recv_pkt_bad_serial' / Int8ul,
    'num_recv_pkt_invalid' / Int8ul,
    'last_uplink_timestamp' / Timestamp,
    'obc_uptime_min' / Int24ub,
    'com_uptime_min' / Int24ub,
    'tx_voltage_drop_10mv' / Int8ul,
    'timed_task_count' / Int8ul,
    'status' / DiagnosticStatus
    )

# This includes notable changes with repect to SMOG-P
# uplink_stats is replaced by diagnostic_stats and version
Beacon_SMOG1 = Struct(
    'timestamp' / Timestamp,
    'beacon_message' / PaddedString(80, 'utf8'),
    'diagnostic_stats' / DiagnosticInfo,
    'version' / PaddedString(7, 'utf8'),
    'ack_info' / AckInfo[3]
    )

SpectrumResult = Struct(
    'timestamp' / Timestamp,
    'startfreq' / Int32ul,
    'stepfreq' / Int32ul,
    'rbw' / Int8ul,
    'pckt_index' / Int8ul,
    'pckt_count' / Int8ul,
    'spectrum_len' / Int16ul,
    Padding(2),
    'measid' / Int16ul,
    'spectrum_data' / Bytes(this.spectrum_len)
    )

# This adds the field request_uplink_serial
# in comparison to SMOG-P
SpectrumResult_SMOG1 = Struct(
    'timestamp' / Timestamp,
    'startfreq' / Int32ul,
    'stepfreq' / Int32ul,
    'rbw' / Int8ul,
    'pckt_index' / Int8ul,
    'pckt_count' / Int8ul,
    'spectrum_len' / Int16ul,
    'request_uplink_serial' / Int16ul,
    'measid' / Int16ul,
    'spectrum_data' / Bytes(this.spectrum_len)
    )

File = Struct(
    'file_id' / Int8ul,
    'file_type' / Int8ul,
    'page_addr' / Int16ul,
    'file_size' / Int24ub,
    'timestamp' / Timestamp,
    'filename' / PaddedString(10, 'utf8')
    )

FileInfo = Struct(
    'timestamp' / Timestamp,
    'files' / File[5]
    )

FileFragment = Struct(
    'timestamp' / Timestamp,
    'pckt_index' / Int16ul,
    'pckt_count' / Int16ul,
    'file_type' / Int8ul,
    'page_addr' / Int16ul,
    'file_size' / Int24ub,
    'timestamp' / Timestamp,
    'filename' / PaddedString(10, 'utf8'),
    'data' / Bytes(217)
    )

ADCResultsEntry = Struct(
    'vcc' / Voltage,
    'vbg' / Voltage,
    'vcore' / Voltage,
    'vextref' / Voltage,
    'an' / Voltage[4]
    )

ADCResults = Struct(
    'timestamp' / Timestamp,
    'internal_reference' / ADCResultsEntry,
    'external_reference' / ADCResultsEntry
    )

ATLSPIStatus = BitStruct(
    'spi_mux_functional' / Flag,
    'msen_cs_pin_select_failed' / Flag,
    'rtcc_cs_pin_select_failed' / Flag,
    'flash_cs_pin_select_failed' / Flag,
    'all_cs_pin_deselect_failed' / Flag,
    'miso_pin_test_failed' / Flag,
    'mosi_pin_test_failed' / Flag,
    'sclk_pin_test_failed' / Flag
    )

ATLBusStatus = Enum(Int8sl, unknown = 0, ok = 1, bit_error = -1, no_response = -2, bus_error = -3)

ValidFlag = Enum(Int8ul, valid = ord('V'))

ATLTelemetry1 = Struct(
    'uptime' / Int32sl,
    'system_time' / Timestamp,
    'obc_id' / Int8ul,
    'oscillator' / Enum(Int8ul, internal = ord('I'), external = ord('E')),
    'adc_results_valid' / ValidFlag,
    'adc_results' / ADCResults,
    'spi_status' / ATLSPIStatus,
    'spi_flash_startcount' / Int8ul,
    'spi_msen_startcount' / Int8ul,
    'spi_rtcc_startcount' / Int8ul,
    'random_number' / Int8ul,
    'mppt_bus_status' / Enum(Int8sl, no_data = 0, valid_data = 1, channel_number_mismatch = -1, checksum_error = -2,\
                                 no_response = -3, bus_error = -4)[6],
    'accu_bus_status' / ATLBusStatus[2],
    'pcu_bus_status' / ATLBusStatus[2],
    'current_com' / Int8ul,
    'com_uptime_seconds' / Int32sl,
    'com_tx_power_level' / TableAdapter([10, 25, 50, 100], Int8ul),
    'com_tx_current' / Int16sl,
    'com_rx_current' / Int16sl,    
    'com_tx_voltage_drop' / Voltage,
    'scheduled_spectrum_analysis_queue' / Int16ul,
    'scheduled_file_download_queue' / Int16ul,
    'energy_management_mod' / Enum(Int8ul, normal = 0, normal_reduced = 1, energy_saving = 2, emergency = 3),
    'morse_period' / Int8ul,
    'radio_cycle' / LinearAdapter(1e6, Int32sl),
    'sleep' / LinearAdapter(1e6, Int32sl),
    'last_telecomand_seconds_ago' / Int32sl,
    'automatic_antenna_openings' / Int16ul,
    'cpu_usage_cycles' / Int16ul,
    'cpu_idle_us' / Int32sl,
    'cpu_work_over_us' / Int32sl,
    'obc_flash_checksum' / Hex(Int32ul),
    'obc_flash_checksum_prev_diff' / Hex(Int32ul),
    'scheduled_datalog_queue' / Int16ul,
    'current_scheduled_datalog' / Int16ul
    )

ATLTelemetry2 = Struct(
    'msen_data_valid' / ValidFlag,
    'timestamp' / Timestamp,
    'temperature' / Float32l,
    'msen_gyroscope' / Float32l[3],
    'msen_magneto_raw' / Int16sl[3],
    'msen_magnto_min_max_valid' / Enum(Int8ul, yes = ord('Y')),
    'msen_magneto_min_max' / Int16sl[6],
    'msen_magneto_scale' / Float32l[3],
    'msen_magneto' / Float32l[3],
    'ack_info' / AckInfo[17]
    )

ATLACCUMeasurement = Struct(
    'valid' / Int8ul,
    '1wbus' / Int8ul,
    'timestamp' / Timestamp,
# TODO implement corrections from https://github.com/szlldm/smogp_atl1_gndsw/blob/master/main.h
    'battery_current_raw' / Int16ul,
    'temperatures_raw' / Int16ul[6]
    )

ATLTelemetry3 = Struct(
    'timestamp' / Timestamp,
    'accu_measurements' / ATLACCUMeasurement[4]
    )

SMOGPTelemetry1 = Struct(
    'uptime' / Int32sl,
    'system_time' / Timestamp,
    'obc_id' / Int8ul,
    'oscillator' / Enum(Int8ul, internal = ord('I'), external = ord('E')),
    'adc_results_valid' / ValidFlag,
    'adc_results' / ADCResults,
    'spi_status' / ATLSPIStatus,
    'spi_flash_startcount' / Int8ul,
    'spi_msen_startcount' / Int8ul,
    'spi_rtcc_startcount' / Int8ul,
    'random_number' / Int8ul,
    'mppt_bus_status' / Enum(Int8sl, no_data = 0, valid_data = 1, channel_number_mismatch = -1, checksum_error = -2,\
                                 no_response = -3, bus_error = -4)[6],
    'accu_bus_status' / ATLBusStatus[2],
    'pcu_bus_status' / ATLBusStatus[2],
    'current_com' / Int8ul,
    'com_uptime_seconds' / Int32sl,
    'com_tx_power_level' / TableAdapter([10, 11, 12, 13, 14, 15, 16, 25, 29, 33, 38, 42, 46, 50, 75, 100], Int8ul),
    'com_tx_current' / Int16sl,
    'com_rx_current' / Int16sl,    
    'com_tx_voltage_drop' / Voltage,
    'scheduled_spectrum_analysis_queue' / Int16ul,
    'scheduled_file_download_queue' / Int16ul,
    'energy_management_mod' / Enum(Int8ul, normal = 0, normal_reduced = 1, energy_saving = 2, emergency = 3),
    'morse_period' / Int8ul,
    'radio_cycle' / LinearAdapter(1e6, Int32sl),
    'sleep' / LinearAdapter(1e6, Int32sl),
    'last_telecomand_seconds_ago' / Int32sl,
    'automatic_antenna_openings' / Int16ul,
    'cpu_usage_cycles' / Int16ul,
    'cpu_idle_us' / Int32sl,
    'cpu_work_over_us' / Int32sl,
    'obc_flash_checksum' / Hex(Int32ul),
    'obc_flash_checksum_prev_diff' / Hex(Int32ul),
    'scheduled_datalog_queue' / Int16ul,
    'current_scheduled_datalog' / Int16ul
    )

smogp = Struct(
    'type' / Int8ul,
    'payload' / Switch(this.type, {
        1 : Telemetry1,
        2 : Telemetry2,
        3 : Telemetry3,
        4 : Beacon,
        5 : SpectrumResult,
        6 : FileInfo,
        7 : FileFragment,
        33 : SMOGPTelemetry1,
        34 : ATLTelemetry2, # SMOGPTelemetry2 is exactly the same as ATLTelemetry2
        129 : ATLTelemetry1,
        130 : ATLTelemetry2,
        131 : ATLTelemetry3,
        }, default = GreedyBytes)
    )

smog1 = Struct(
    'type' / Int8ul,
    'payload' / Switch(this.type, {
        1 : Telemetry1,
        2 : Telemetry2_SMOG1,
        3 : Telemetry3_SMOG1,
        4 : Beacon_SMOG1,
        5 : SpectrumResult_SMOG1,
        7 : FileFragment,
        }, default = GreedyBytes)
    )

signalling_prbs = np.array([0x97, 0xfd, 0xd3, 0x7b, 0x0f, 0x1f, 0x6d,\
                            0x08, 0xf7, 0x83, 0x5d, 0x9e, 0x59, 0x82,\
                            0xc0, 0xfd, 0x1d, 0xca, 0xad, 0x3b, 0x5b,\
                            0xeb, 0xd4, 0x93, 0xe1, 0x4a, 0x04, 0xd2,\
                            0x28, 0xdd, 0xf9, 0x01, 0x53, 0xd2, 0xe6,\
                            0x6c, 0x5b, 0x25, 0x65, 0x31, 0xc5, 0x7c,\
                            0xe7, 0xf1, 0x38, 0x61, 0x2d, 0x5c, 0x03,\
                            0x3a, 0xc6, 0x88, 0x90, 0xdb, 0x8c, 0x8c,\
                            0x42, 0xf3, 0x51, 0x75, 0x43, 0xa0, 0x83, 0x93], dtype = 'uint8')

signalling_prbs_tx = np.array([0xA3, 0x9E, 0x1A, 0x55, 0x6B, 0xCB, 0x5C, 0x2F,
                               0x2A, 0x5C, 0xAD, 0xD5, 0x32, 0xFE, 0x85, 0x1D,
                               0xDC, 0xE8, 0xBC, 0xE5, 0x13, 0x7E, 0xBA, 0xBD,
                               0x9D, 0x44, 0x31, 0x51, 0x3C, 0x92, 0x26, 0x6C,
                               0xF3, 0x68, 0x98, 0xDA, 0xA3, 0xBA, 0x7F, 0x84,
                               0x86, 0x32, 0x95, 0xAC, 0x8D, 0x4E, 0x66, 0x8B,
                               0x7F, 0x7B, 0xE0, 0x14, 0xE2, 0x3C, 0x49, 0x45,
                               0x32, 0xE4, 0x5C, 0x44, 0xF5, 0x6D, 0x2D, 0x0A],
                              dtype = 'uint8')

downlink_speeds = [500, 1250, 2500, 5000, 12500]
codings = ['RX', 'AO-40 short', 'AO-40', 'RA (260, 128)', 'RA (514, 256)']
                            
class smogp_signalling:
    @staticmethod
    def parse(packet):
        if len(packet) != 64:
            print('Error: signalling packet length != 64')
            return

        prbs = np.frombuffer(packet[:-6], dtype = 'uint8')
        ber_prbs = np.sum((np.unpackbits(prbs) ^ np.unpackbits(signalling_prbs[6:])).astype('int')) / (prbs.size * 8)
        ber_prbs_tx = np.sum((np.unpackbits(prbs) ^ np.unpackbits(signalling_prbs_tx[6:])).astype('int')) / (prbs.size * 8)
        sig_type = 'RX' if ber_prbs < ber_prbs_tx else 'TX'
        ber_prbs = min(ber_prbs, ber_prbs_tx)

        flags = np.unpackbits(np.frombuffer(packet[-6:], dtype = 'uint8')).reshape((-1, 8))
        decoded_flags = 1*(np.sum(flags, axis = 1) > 4)

        try:
            downlink_speed = downlink_speeds[np.packbits(decoded_flags[:3])[0] >> 5]
        except IndexError:
            print(f'Error: invalid downlink speed {decoded_flags[:3]}')
            return

        try:
            coding = codings[np.packbits(decoded_flags[3:])[0] >> 5]
        except IndexError:
            print(f'Error: invalid coding {decoded_flags[3:]}')
            return

        return f'Signalling packet: mode {sig_type}, BER {ber_prbs:.4f}, rate {downlink_speed} baud, coding {coding}'

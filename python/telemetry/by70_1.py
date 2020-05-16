#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

from construct import *
from .csp import CSPHeader
from ..adapters import LinearAdapter

from math import log10

PayloadMode = BitStruct('open_telecommand' / Flag,\
                     'camera_task' / Flag,\
                     'valid_image_data' / Flag,\
                     'camera_power' / Flag,\
                     'rest' / Nibble)

Iv3 = LinearAdapter(10.0, Int16sl)
Ivbatt = LinearAdapter(2.5, Int16sl)
Voltage = LinearAdapter(2000.0, Int16sl)

class TSTM32Adapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(4096.0*(2.5*(obj - 25.0) + 760.0)/3000.0)
    def _decode(self, obj, context, path = None):
        return (obj * 3000.0 / 4096.0 - 760.0) / 2.5 + 25.0
TSTM32 = TSTM32Adapter(Int16sl)

class TPAAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(obj*16.0) << 3
    def _decode(self, obj, context, path = None):
        return (obj >> 3) / 16.0
TPA = TPAAdapter(Int16sl)

DCFMTC = LinearAdapter(352.7, Int16sl)
DCFMHam = LinearAdapter(6864.0, Int16sl)

class RSSIAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return int(10**((obj + 147.0)/10.0))
    def _decode(self, obj, context, path = None):
        return 10*log10(obj) - 147.0
RSSI = RSSIAdapter(Int32ul)

Runtime = LinearAdapter(1000.0, Int32ul)
CTCSSCount = LinearAdapter(0.04, Int32ul)

# COM STM32 Housekeeping Packet             
Hk_STM32 = Struct(Const(b'\x1c\xa1'),\
                  'config' / Int8ul,\
                  'flag_direct_ins' / Int8ul,\
                  'payload_mode' / PayloadMode,\
                  'tx_mode' / Int8ul,\
                  'gain_tx' / Int16sl,\
                  'i_3v3' / Iv3,\
                  'u_3v3' / Voltage,\
                  'i_vbat_tx' / Ivbatt,\
                  'u_vbat_tx' / Voltage,\
                  'i_vbat_rx' / Ivbatt,\
                  'u_vbat_rx' / Voltage,\
                  't_stm32' / TSTM32,\
                  't_pa' / TPA,\
                  'n_tx_rf' / Int16ul,\
                  'n_rx_rf' / Int16ul,\
                  'n_tx_err_rf' / Int16ul,\
                  'n_tx_err_rf' / Int16ul,\
                  'n_tx_i2c' / Int16ul,\
                  'n_rx_i2c' / Int16ul,\
                  'n_tx_err_i2c' / Int16ul,\
                  'n_rx_err_i2c' / Int16ul,\
                  'n_tc' / Int32ul,\
                  'dc_fm_tc' / DCFMTC,\
                  'dc_fm_ham' / DCFMHam,\
                  'rssi_fm_tc' / RSSI,\
                  'rssi_fm_ham' / RSSI,\
                  'reset_flag' / Int8ul,\
                  'sys_flag' / Int8ul,\
                  'dma_overflow' / Int16ul,\
                  'runtime' / Runtime,\
                  'reset_count' / Int32ul,\
                  'ctcss_count' / CTCSSCount,\
                  'ctcss_det' / Float32l)

# COM STM32 Config Packet
Cfg = Struct(Const(b'\x1c\xa2'),\
             'gain_tx_HI' / Int16sl,\
             'gain_tx_LO' / Int16sl,\
             'bias_I' / Int16sl,\
             'bias_Q' / Int16sl,\
             'threshold_u_vbat_rx_powerdown' / Int16sl,\
             'threshold_u_vbat_rx_repeateroff' / Int16sl,\
             'threshold_t_pa' / Int8sl,\
             'cam_ham_interval' / Int8ul,\
             'cam_ham_en' / Int8ul,\
             'ctcss_en' / Int8ul,\
             'ctcss_n_integration' / Int8ul,\
             'ctcss_n_tail' / Int8ul,\
             'ctcss_coeff' / Float32l,\
             'ctcss_threshold' / Float32l,\
             'gain_fmdm_ham' / Float32l,\
             'gain_fmdm_tc' / Float32l,\
             'interval_hk_OBC' / Int32ul,\
             'interval_hk_TLM' / Int32ul,\
             'interval_hk_BEACON' / Int32ul,\
             'message' / Bytes(28),\
             'cam_delay' / Int32ul,\
             'crc' / Int32ul)

# COM AVR Housekeeping Packet
Hk_AVR = Struct(Const(b'\x1c\xa3'),\
                'adf7021_ld' / Int8ul,\
                'err_flag' / Int8ul,\
                'n_tx_i2c' / Int16ul,\
                'n_rx_i2c' / Int16ul,\
                'n_tx_232' / Int16ul,\
                'n_rx_232' / Int16ul,\
                'runtime' / Runtime,\
                'rssi_analog' / Int8ul,\
                'n_rssi_const' / Int8ul,\
                'unlock_count' / Int8ul,\
                'reset_flag' / Int8ul,\
                'reset_count' / Int32ul )

# LilacSat-1 Generic Telemetry Data
LilacSat1Tlm = Struct(Const(b'\xaa\xa1'),\
                   'ttc_payload_mode'/ Int8ul,\
                   'ttc_tx_mode' / Int8ul,\
                   'ttc_i_vbat_tx' / Int8ul,\
                   'ttc_t_pa' / Int8sl,\
                   'ttc_adf7021_lock' / Int8ul,\
                   'ttc_n_tc' / Int32ul,\
                   'ttc_rssi_fm_tc' / Int8ul,\
                   'eps_bat_vol_average' / Int8ul,\
                   'eps_bat_cur' / Int8sl,\
                   'eps_5v_cur' / Int8ul,\
                   'esp_3v3_cur' / Int8ul,\
                   'eps_5v_dcdc_temp' / Int16sl,\
                   'eps_bat_temp' / Int16sl,\
                   'eps_reserved' / Byte[2],\
                   'adcs_q1' / Int16sl,\
                   'adcs_q2' / Int16sl,\
                   'adcs_q3' / Int16sl,\
                   'adcs_w1' / Int16sl,\
                   'adcs_w2' / Int16sl,\
                   'adcs_w3' / Int16sl,\
                   'adcs_mode' / Int16sl,\
                   'adcs_long' / Int16sl,\
                   'adcs_lat' / Int16sl,\
                   'adcs_height' / Int16sl,\
                   'adcs_reserved' / Byte[5],\
                   'obc_gps_power_state' / Int8ul,\
                   'obc_eps_low_state' / Int8ul,\
                   'obc_year' / Int16ul,\
                   'obc_month' / Int8ul,\
                   'obc_day' / Int8ul,\
                   'obc_hour' / Int8ul,\
                   'obc_minute' / Int8ul,\
                   'obc_second' / Int8ul,\
                   'obc_reserved' / Byte,\
                   'inms_script_en' / Int8ul,\
                   'inms_power_on' / Int8ul,\
                   'inms_script_no' / Int8ul,\
                   'inms_script_seq' / Int8ul,\
                   'inms_script_execed' / Int8ul,\
                   'inms_script_checksum_ok' / Int8ul,\
                   'inms_slot_not_empty' / Int8ul,\
                   'inms_reserved' / Byte[2])

# OBC Housekeeping Parameters
Hk_OBC = Struct(Const(b'\x1a\xa1'),\
                'com_iic1_bus_status' / Int8ul,\
                'eps_iic1_bus_status' / Int8ul,\
                'gps_power_status' / Int8ul,\
                'battery_low_indicator' / Int8ul,\
                'gps_lock_status' / Int8ul,\
                'onboard_time_source' / Int8ul,\
                'time_onboard_year' / Int16ul,\
                'time_onboard_month' / Int8ul,\
                'time_onboard_day' / Int8ul,\
                'time_onboard_hour' / Int8ul,\
                'time_onboard_min' / Int8ul,\
                'time_onboard_sec' / Int8ul,\
                'delayed_command_count' / Int8ul,\
                'interface_board_3v3_current_a' / Int16ul,\
                'interface_board_5v_current_b' / Int16ul,\
                'obc_board_3v3_current_tsc103' / Int16ul,\
                'obc_board_5v_current_ina219' / Int16ul,\
                'obc_board_5v_voltage_ina219' / Int16ul,\
                Padding(2),\
                'csp_sent_packet' / Int32ul,\
                'csp_received_packet' / Int32ul,\
                'received_command_count' / Int32ul,\
                'obc_power_on_time' / Int32ul,\
                'obc_reset_count' / Int16ul,\
                'obc_log_file_index' / Int16ul,\
                'com_log_file_index' / Int16ul,\
                'eps_log_file_index' / Int16ul,\
                'com_log_2_file_index' / Int16ul,\
                'inms_enable_status_script_power'  / Int8ul,\
                'inms_running_status_script_no_seq_no' / Int8ul,\
                'adcs_log_file_index' / Int16ul,\
                'inms_temperature_sensing_point' / Float32l,\
                'stm32_temperature' / Int16ul,\
                'current_storage_card_telemetry_ftp' / Int8ul,\
                'gps_leap_second_correction' / Int8sl,\
                'inms_file_index' / Int32ul)

Magnetometer = LinearAdapter(1/4.0, Int16sl)
Gyroscope = LinearAdapter(32768.0/57.2958, Int16sl)
TempADIS = LinearAdapter(1/0.0739, Int16sl)
FineSun = LinearAdapter(16384.0, Int16sl)
CoarseSun = LinearAdapter(32.0, Int16sl)
Latitude = LinearAdapter(360.0, Int16sl)
Longitude = LinearAdapter(180.0, Int16sl)
Altitude = LinearAdapter(1/20.0, Int16sl)

# ADCS Parameters (OBC)
ADCS_Par = Struct(Const(b'\x1a\xa2'),\
                  'magnetometer_hmc5883l' / Magnetometer[3],\
                  'magnetometer_hmc1043l' / Magnetometer[3],\
                  'gyroscope_mpu3300' / Gyroscope[3],\
                  'gyroscope_mpu3300_temperature' / Int16sl,\
                  'gyroscope_adis16448' / Gyroscope[3],\
                  'temperature_adis16448' / TempADIS,\
                  'magnetometer_adis16448' / Magnetometer[3],\
                  'fine_sun_sensor' / FineSun[3],\
                  'coarse_sun_sensor' / CoarseSun[5],\
                  'magnetometer_mix' / Float32l,\
                  'modeflag_2' / Int32ul,\
                  'modeflag_1' / Int16ul,\
                  'flywheel_speed' / Int16sl,\
                  'adcs_interruption_counting' / Int16ul,\
                  'kf_quaternions' / FineSun[3],\
                  'gyroscope_quaternions' / FineSun[3],\
                  'coarse_sun_sensor_temperature' / Int16sl[5],\
                  'latitude' / Latitude ,\
                  'longitude' / Longitude,\
                  'altitude' / Altitude,\
                  'fine_sun_sensor_temperature' / Int16sl)

# Orbit Paramaters (OBC)
Orbit_Par = Struct(Const(b'\x1a\xa8'),\
                   'year' / Int8ul,\
                   'month' / Int8ul,\
                   'day' / Int8ul,\
                   'hour' / Int8ul,\
                   'minute' / Int8ul,\
                   'second' / Int8ul,\
                   'position' / Float64l[3],\
                   'velocity' / Float64l[3],\
                   'oev_a' / Float64l,\
                   'oev_e' / Float64l,\
                   'oev_i' / Float64l,\
                   'oev_omega' / Float64l,\
                   'oev_w' / Float64l,\
                   'oev_theta' / Float64l)

# OBC Variable Threshold Parameter
OBC_Threshold = Struct(Const(b'\x1a\xa9'),\
                       'eps_batter_low_voltage_threshold' / Int16ul,\
                       'eps_overcurrent_threshold' / Int16ul,\
                       'eps_critical_battery_low_voltage_threshold' / Int16ul,\
                       'eps_critical_overcurrent_threshold' / Int16ul,\
                       'eps_overcurrent_hysteresis' / Int16ul,\
                       'gps_time_error_threshold' / Int16ul,\
                       'gps_position_malfunction_threshold' / Int16ul[3],\
                       'gps_velocity_malfunction_threshold' / Int16ul[3])

# Orbit Parameter (OBC)
Orbital_Par = Struct(Const(b'\x1a\xaa'),\
                     'packet_header' / Int16ul,\
                     'frame_header' / Int8ul,\
                     'frame_length' / Int8ul,\
                     'gps_bd_lock_status' / Int8ul,\
                     'week_of_year' / Int16ul,\
                     'second_of_week' / Float64l,\
                     'gps_satellite_in_use_obs' / Int8ul,\
                     'gps_satellite_in_use_pdop' / Int16ul,\
                     'xyz' / Float64l[3],\
                     'v' / Float64l[3],\
                     'gps_clock_error' / Float32l,\
                     'gps_clock_drift' / Float32l,\
                     'bd_clock_error' / Float32l,\
                     'bd_clock_drift' / Float32l,\
                     'checksum' / Int8ul)

CurrentVoltage = LinearAdapter(1000.0, Int16sl)
Temp = LinearAdapter(16.0, Int16sl)

EPS_Status = BitStruct('reboot_enable_2_status' / Flag,\
                       Padding(1),\
                       'reboot_enable_1_status' / Flag,\
                       Padding(1),\
                       'antenna_2_deploy_status' / Flag,\
                       Padding(1),\
                       'antenna_1_deploy_status' / Flag,\
                       Padding(1),\
                       'antenna_deploy_disable_control' / Flag,\
                       Padding(7))

# EPS Housekeeping Parameter
Hk_EPS = Struct(Const(b'\x1e\xa1'),\
                'mppt_output_current' / CurrentVoltage[5],\
                'battery_output_current' / CurrentVoltage[3],\
                '5v_output_current' / CurrentVoltage,\
                '3v3_output_current' / CurrentVoltage,\
                'main_bus_output_current' / CurrentVoltage,\
                'antenna_deployment_current' / CurrentVoltage,\
                'mppt_output_voltage' / CurrentVoltage[5],\
                'battery_output_voltage' / CurrentVoltage[3],\
                '5v_output_voltage' / CurrentVoltage,\
                '3v3_output_voltage' / CurrentVoltage,\
                'main_bus_output_voltage' / CurrentVoltage,\
                'antenna_deployment_voltage' / CurrentVoltage,\
                'mptt_temperature' / Temp,\
                'battery_charger_temperature' / Temp,\
                'battery_temperature' / Temp,\
                'main_bus_diode_temperature' / Temp,\
                '5v_regulator_temperature' / Temp,\
                '3v3_regulator_temperature' / Temp,\
                '5v_ocp_temperature' / Temp,\
                '3v3_ocp_temperature' / Temp,\
                'status' / EPS_Status,\
                'power_on_time' / LinearAdapter(1000.0, Int32ul),\
                'iic_sent_packet_count' / Int16ul,\
                'iic_received_packet_count' / Int16ul,\
                'output_reboot_wdt_in_minute' / Int16ul,\
                'eps_reboot_wdt_in_minute' / Int16ul,\
                'eps_reboot_count' / Int16ul)

# EPS Onboard Parameters
EPS_Onboard = Struct(Const(b'\x1e\xa2'),\
                     'onboard_software_version' / Int8ul[3],\
                     'onboard_software_compile_date' / Int8ul[4],\
                     Padding(1),\
                     'first_poweron_flag' / Int8ul,\
                     Padding(3),\
                     'output_reboot_wdt_enabled' / Int8ul,\
                     'output_reboot_timer_hr' / Int8ul,\
                     Padding(2),\
                     'eps_reboot_wdt_enabled' / Int8ul,\
                     'eps_reboot_timer_hr' / Int8ul,\
                     Padding(2),\
                     'auto_send_hk_data_enabled' / Int8ul,\
                     'auto_send_hk_data_period_sec' / Int8ul,\
                     Padding(2),\
                     'antenna_deployed' / Int8ul)

# EPS Reboot Log
EPS_Reboot = Struct(Const(b'\x1e\xa3'),\
                    'onboard_software_version' / Int8ul[3],\
                    'onboard_software_compile_date' / Int8ul[4],\
                    Padding(1),\
                    'last_output_reboot_source' / Int8ul,\
                    'last_output_reboot_timer' / Int8ul[4],\
                    Padding(3),\
                    'last_eps_reboot_source' / Int8ul,\
                    'last_eps_reboot_timer' / Int8ul[4],\
                    Padding(3),\
                    'current_onboard_reboot_timer' / Int8ul[4],\
                    Padding(4),\
                    'eps_reboot_count' / Int8ul[4])

# EPS Command Log
Command = Struct('cmd' / Int8ul[5],\
                 'source' / Int8ul,\
                 'received_time' / Int8ul[4])
    

EPS_Command = Struct(Const(b'\x1e\xa4'),\
                     'cmds' / Command[4])

Error = Struct('code' / Int8ul,\
               'time' / Int8ul[4])

# EPS Error Log
EPS_Error = Struct(Const(b'\x1e\xa5'),\
                   'critical_error' / Error[4],\
                   'error' / Error[4])

ImageData = Struct(
    'file_id' / Int32ul,
    'flag' / Int8sb,
    'filesize' / Int24ul,
    'offset' / Int24ul,
    'data' / Bytes(64)
    )
    
Frame = Select(Hk_STM32, Cfg, Hk_AVR, LilacSat1Tlm, Hk_OBC, ADCS_Par, Orbit_Par,\
               OBC_Threshold, Orbital_Par, Hk_EPS, EPS_Onboard, EPS_Reboot, EPS_Command,\
               EPS_Error)

by70_1 = Struct(
    'csp_header' / ByteSwapped(CSPHeader),
    'beacon' / If(this.csp_header.destination == 5, Frame),
    'camera' / If(this.csp_header.destination == 6, ImageData),
    'packet_count' / Int32ul,
    'crc' / Hex(Int32ul)
    )

taurus1 = Struct(
    'header' / Bytes(5+7), # This is a CCSDS header of some sort
    'beacon' / Frame
    )


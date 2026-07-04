#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# Copyright 2026 Hex20 Labs India Pvt Ltd
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
from .ax25 import Header
from ..adapters import PolynomialAdapter
from ..adapters import LinearAdapter
from ..ccsds import space_packet as ccsds_space_packet
from construct import Adapter, BitStruct, BitsInteger, Enum, Flag, Float32l, \
    GreedyBytes, If, Int16sl, Int16ul, Int32sl, Int32ul, Int8sl, \
    Int8ub, Int8ul, Padding, Struct, Switch
 
solar_panel_temp_poly = [91.394, -0.08949, 3.55e-05, -6.26e-09, 1.89e-13]
batt_thermistor_temp_poly = [
    87.1751343, -0.0786252941, 0.0000272861362, -0.00000000402689014]
subsystem_temp_poly = [91.394, -0.08949, 3.55e-05, -6.26e-09, 1.89e-13]


SecondaryHeader = Struct(
    'sh_coarse' / Int32ul,
    'sh_fine' / Int16ul,
)
 
koyo_beacon = Struct(
    'obctime' / Int32ul,
    'panel_0_curr' / LinearAdapter(1/0.001221001, Int16ul),
    'panel_1_curr' / LinearAdapter(1/0.001221001, Int16ul),
    'panel_2_curr' / LinearAdapter(1/0.001221001, Int16ul),
    'panel_3_curr' / LinearAdapter(1/0.001221001, Int16ul),
    'panel_0_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'panel_1_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'panel_2_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'panel_3_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'cdh_3v3_current' / LinearAdapter(1/0.001221001, Int16ul),
    'cdh_3v3_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'regulator_current' / LinearAdapter(1/0.001221001, Int16ul),
    'regulator_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'comm_current' / LinearAdapter(1/0.001221001, Int16ul),
    'comm_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'battery_discharge_current' / LinearAdapter(1/0.001221001, Int16ul),
    'battery_discharge_volt' / LinearAdapter(1/0.0004880429, Int16ul),
    'battery_charge_current' / LinearAdapter(1/0.001221001, Int16ul),
    'battery_charge_volt' / LinearAdapter(1/0.0004880429, Int16ul),
    'battery_heater_current' / LinearAdapter(1/0.001221001, Int16ul),
    'battery_heater_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'solar_panel_temp_0' / PolynomialAdapter(solar_panel_temp_poly, Int16ul),
    'solar_panel_temp_1' / PolynomialAdapter(solar_panel_temp_poly, Int16ul),
    'solar_panel_temp_2' / PolynomialAdapter(solar_panel_temp_poly, Int16ul),
    'solar_panel_temp_3' / PolynomialAdapter(solar_panel_temp_poly, Int16ul),
    'battery_thermistor_temp_1' / PolynomialAdapter(batt_thermistor_temp_poly, Int16ul),
    'battery_thermistor_temp_2' / PolynomialAdapter(batt_thermistor_temp_poly, Int16ul),
    'cdh_temp' / PolynomialAdapter(subsystem_temp_poly, Int16ul),
    'eps_temp' / PolynomialAdapter(subsystem_temp_poly, Int16ul),
 
    'aprs_pl_current' / LinearAdapter(1/0.001221001, Int16ul),
    'aprs_pl_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'mcb_current' / LinearAdapter(1/0.001221001, Int16ul),
    'mcb_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'adcs_current' / LinearAdapter(1/0.001221001, Int16ul),
    'adcs_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'amplified_space_current' / LinearAdapter(1/0.001221001, Int16ul),
    'amplified_space_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'cmg_current' / LinearAdapter(1/0.001221001, Int16ul),
    'cmg_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'fog_pl_current' / LinearAdapter(1/0.001221001, Int16ul),
    'fog_pl_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'if_card_mcu_current' / LinearAdapter(1/0.001221001, Int16ul),
    'if_card_mcu_volt' / LinearAdapter(1/0.004880429, Int16ul),
    'becon_pib_adc_reading' / Int16ul,
    'satellite_current_mode' / Int8ul,
    'pib_current_mode' / Int8ul,
    'safe_exit_thresh' / Int16ul,
    'safe_enter_thresh' / Int16ul,
    'nominal_exit_thresh' / Int16ul,
    'nominal_enter_thresh' / Int16ul,
    'antenna_deploy_retry_flag' / Int8ul,
    'solar_panel_deploy_retry_flag' / Int8ul,
    'boot_counter' / Int32ul,
    'last_command_opcode' / Int8ul,
    'command_accept_count' / Int32ul,
    'command_reject_count' / Int32ul,
    'beacon_flash_write_pointer' / Int32ul,
    'adcs_flash_write_pointer' / Int32ul,
    'uhf_flash_write_pointer' / Int32ul,
    'amplified_space_flash_write_pointer' / Int32ul,
    'fog_flash_write_pointer' / Int32ul,
    'aprs_flash_write_pointer' / Int32ul,
    'beacon_flash_read_pointer' / Int32ul,
    'adcs_flash_read_pointer' / Int32ul,
    'uhf_flash_read_pointer' / Int32ul,
    'amplified_space_flash_read_pointer' / Int32ul,
    'fog_flash_read_pointer' / Int32ul,
    'aprs_flash_read_pointer' / Int32ul,
    'beacon_sd_write_pointer' / Int32ul,
    'adcs_sd_write_pointer' / Int32ul,
    'uhf_sd_write_pointer' / Int32ul,
    'amplified_space_sd_write_pointer' / Int32ul,
    'fog_sd_write_pointer' / Int32ul,
    'aprs_sd_write_pointer' / Int32ul,
    'beacon_sd_read_pointer' / Int32ul,
    'adcs_sd_read_pointer' / Int32ul,
    'uhf_sd_read_pointer' / Int32ul,
    'amplified_space_sd_read_pointer' / Int32ul,
    'fog_sd_read_pointer' / Int32ul,
    'aprs_sd_read_pointer' / Int32ul,
    'rtc_time_in_seconds' / Int32ul,
    'as_event_rem_count' / Int16ul,
    'fog_event_rem_count' / Int16ul,
    'as_event_status' / Int8ul,
    'fog_event_status' / Int8ul,
    'rtc_hundredths_of_seconds' / Int8ul,
    'rtc_seconds' / Int8ul,
    'rtc_minutes' / Int8ul,
    'rtc_hours' / Int8ul,
    'rtc_day' / Int8ul,
    'rtc_date' / Int8ul,
    'rtc_month' / Int8ul,
    'rtc_year' / Int16ul,
    'uhf_channel' / Int8ul,
    'pib_health_status' / Int8ul,
    'sd_card_failure_count' / Int8ul,
    'static_table_crc_status' / Int8ul,
    'dynamic_table_crc_status' / Int8ul,
    
)
 
koyo = Struct(
    'ax25_header' / Header,
    'primary_header' / ccsds_space_packet.PrimaryHeader,
    'secondary_header' / If(
        lambda c: c.primary_header.secondary_header_flag,
        SecondaryHeader
    ),
    'packet' / Switch(
        lambda c: c.primary_header.AP_ID,
        {
            0x01: koyo_beacon,
        },
        default=GreedyBytes
    )
)
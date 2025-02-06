#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Hex20 Labs India Pvt Ltd
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .ax25 import Header
from ..adapters import PolynomialAdapter
from ..adapters import LinearAdapter
from construct import Adapter, BitStruct, BitsInteger, Enum, Flag, Float32l, \
    GreedyBytes, If, Int16sl, Int16ul, Int32sl, Int32ul, Int8sl, \
    Int8ub, Int8ul, Padding, Struct, Switch

solar_panel_temp_poly = [91.394, -0.08949, 3.55e-05, -6.26e-09, 1.89e-13]
batt_thermistor_temp_poly = [
    87.1751343, -0.0786252941, 0.0000272861362, -0.00000000402689014]
subsystem_temp_poly = [91.394, -0.08949, 3.55e-05, -6.26e-09, 1.89e-13]

nila_header = Struct(
    'sync_word_1' / Int8ul,
    'sync_word_2' / Int8ul,
    'sync_word_3' / Int8ul,
    'version' / Int8ul,
    'ap_id' / Int8ul,
    'seq_no' / Int16ul,
    'pkt_len' / Int16ul,
    'obc_time' / Int32ul,
)

nila_beacon = Struct(
    'obctime' / Int32ul,
    'sat_curr_mode' / Enum(Int8ul, SAFE=0, NOMINAL=1),
    'safe_exit_thresh' / Int16ul,
    'safe_enter_thresh' / Int16ul,
    'battchg_volt' / LinearAdapter(1/0.00125, Int16ul),
    'battchg_curr' / LinearAdapter(1/0.00125, Int16ul),
    'dep_retry_flag' / Int8ul,
    'pl_on_flag' / Int8ul,
    'oot_counter' / Int32ul,
    'last_cmd_opcode' / Int8ul,
    'cmd_accpt_count' / Int32ul,
    'cmd_rjct_count' / Int32ul,
    'bcn_flash_write_ptr' / Int32ul,
    'bcn_flash_read_ptr' / Int32ul,
    'pl_flash_write_ptr' / Int32ul,
    'pl_flash_read_ptr' / Int32ul,
    'ads_flash_write_ptr' / Int32ul,
    'ads_flash_read_ptr' / Int32ul,
    'uhf_flash_write_ptr' / Int32ul,
    'uhf_flash_read_ptr' / Int32ul,

    'panel_0_curr' / LinearAdapter(1/0.0005, Int16ul),
    'panel_1_curr' / LinearAdapter(1/0.0005, Int16ul),
    'panel_2_curr' / LinearAdapter(1/0.0005, Int16ul),
    'panel_0_volt' / LinearAdapter(1/0.001, Int16ul),
    'panel_1_volt' / LinearAdapter(1/0.001, Int16ul),
    'panel_2_volt' / LinearAdapter(1/0.001, Int16ul),

    'cdh_3v3_current' / LinearAdapter(1/0.0005, Int16ul),
    'uhf_6v_current' / LinearAdapter(1/0.0005, Int16ul),
    'ads_12v_current' / LinearAdapter(1/0.0005, Int16ul),
    'cdh_3v3_volt' / LinearAdapter(1/0.001, Int16ul),
    'uhf_6v_volt' / LinearAdapter(1/0.001, Int16ul),
    'ads_12v_volt' / LinearAdapter(1/0.001, Int16ul),

    'pl_12v_current' / LinearAdapter(1/0.0005, Int16ul),
    'battery_heater_current' / LinearAdapter(1/0.0005, Int16ul),
    'main_battery_current' / LinearAdapter(1/0.0005, Int16ul),
    'pl_12v_volt' / LinearAdapter(1/0.001, Int16ul),
    'battery_heater_volt' / LinearAdapter(1/0.001, Int16ul),
    'main_battery_volt' / LinearAdapter(1/0.001, Int16ul),
    'temp_solarpanel0' / PolynomialAdapter(solar_panel_temp_poly, Int16ul),
    'temp_solarpanel1' / PolynomialAdapter(solar_panel_temp_poly, Int16ul),
    'temp_solarpanel2' / PolynomialAdapter(solar_panel_temp_poly, Int16ul),
    'temp_battery_thermistor1' /
    PolynomialAdapter(batt_thermistor_temp_poly, Int16ul),
    'temp_battery_thermistor2' /
    PolynomialAdapter(batt_thermistor_temp_poly, Int16ul),
    'temp_cdh' / PolynomialAdapter(subsystem_temp_poly, Int16ul),
    'temp_if_card' / PolynomialAdapter(subsystem_temp_poly, Int16ul),
    'temp_eps' / PolynomialAdapter(subsystem_temp_poly, Int16ul),
    'actcmdrejectnum' / Int8ul,
    'lastrejectedactuator' / Int8ul,
    'dcubedplcurrentactuator' / Int8ul,
    'dcubedplactuatorstatus_nD3PP' / Int8ul,
    'dcubedplactuatorstatus_nD3RN' / Int8ul,
    'dcubedplactuatorstatus_uD3PP' / Int8ul,
    'dcubedplactuatorstatus_uD3RN' / Int8ul,
    'dcubedplactuatorstatus_nD3SP' / Int8ul,
    'dcubedplactuatorstate_nD3PP' / Int8ul,
    'dcubedplactuatorstate_nD3RN' / Int8ul,
    'dcubedplactuatorstate_uD3PP' / Int8ul,
    'dcubedplactuatorstate_uD3RN' / Int8ul,
    'dcubedplactuatorstate_nD3SP' / Int8ul,
    'dcubedplactuatorretrycount_nD3PP'/Int8ul,
    'dcubedplactuatorretrycount_nD3RN'/Int8ul,
    'dcubedplactuatorretrycount_uD3PP'/Int8ul,
    'dcubedplactuatorretrycount_uD3RN'/Int8ul,
    'dcubedplactuatorretrycount_nD3SP'/Int8ul,
    'actuateoverrideflag' / Int8ul,
    'rtcseconds' / Int8ul,
    'rtcminutes' / Int8ul,
    'rtchours' / Int8ul,
    'rtcday' / Enum(Int8ul, SUN=1, MON=2, TUE=3,
                    WED=4, THU=5, FRI=6, SAT=6),
    'rtcdate' / Int8ul,
    'rtcmonth' / Enum(Int8ul, JAN=1, FEB=2, MAR=3, APR=4, MAY=5,
                      JUN=6, JUL=7, AUG=8, SEP=9, OCT=10, NOV=11, DEC=12),
    'rtcyear' / Int16ul,
    'I2Ctimeouteventcnt' / Int16ul,
    'squhfchannel' / Int8ul,
    'static_table_crc_status' /
    Enum(Int8ul, TABLE_NOT_CORRUPTED=1, TABLE_CORRUPTED=2),
    'dynamic_table_crc_status' /
    Enum(Int8ul, TABLE_NOT_CORRUPTED=1, TABLE_CORRUPTED=2),
)


nila_pl_pck = Struct(

    # Actuator 1
    'nila_pl_actuator_nD3PP' / Int8ul,
    'nila_pl_nD3PP_activation_status' / Int8ul,
    'nila_pl_nD3PP_activation_state' / Int8ul,
    'nila_pl_nD3PP_last_activation_time_day' / Int16ul,
    'nila_pl_nD3PP_last_activation_time_ms' / Int32ul,
    'nila_pl_nD3PP_last_feedback_time_day' / Int16ul,
    'nila_pl_nD3PP_last_feedback_time_ms' / Int32ul,
    'nila_pl_nD3PP_last_actuator_finish_time_day' / Int16ul,
    'nila_pl_nD3PP_last_actuator_finish_time_ms' / Int32ul,
    'nila_pl_nD3PP_actuator_feedback' / Int8ul,
    'nila_pl_nD3PP_v_before_activation' / Int16ul,
    'nila_pl_nD3PP_i_before_activation' / Int16ul,
    'nila_pl_nD3PP_t_before_activation' / Int16ul,
    'nila_pl_nD3PP_v_after_activation' / Int16ul,
    'nila_pl_nD3PP_i_after_activation' / Int16ul,
    'nila_pl_nD3PP_t_after_activation' / Int16ul,
    'nila_pl_nD3PP_retry_count' / Int8ul,

    # Actuator 2
    'nila_pl_actuator_nD3RN' / Int8ul,
    'nila_pl_nD3RN_activation_status' / Int8ul,
    'nila_pl_nD3RN_activation_state' / Int8ul,
    'nila_pl_nD3RN_last_activation_time_day' / Int16ul,
    'nila_pl_nD3RN_last_activation_time_ms' / Int32ul,
    'nila_pl_nD3RN_last_feedback_time_day' / Int16ul,
    'nila_pl_nD3RN_last_feedback_time_ms' / Int32ul,
    'nila_pl_nD3RN_last_actuator_finish_time_day' / Int16ul,
    'nila_pl_nD3RN_last_actuator_finish_time_ms' / Int32ul,
    'nila_pl_nD3RN_actuator_feedback' / Int8ul,
    'nila_pl_nD3RN_v_before_activation' / Int16ul,
    'nila_pl_nD3RN_i_before_activation' / Int16ul,
    'nila_pl_nD3RN_t_before_activation' / Int16ul,
    'nila_pl_nD3RN_v_after_activation' / Int16ul,
    'nila_pl_nD3RN_i_after_activation' / Int16ul,
    'nila_pl_nD3RN_t_after_activation' / Int16ul,
    'nila_pl_nD3RN_retry_count' / Int8ul,

    # Actuator 3
    'nila_pl_actuator_uD3PP' / Int8ul,
    'nila_pl_uD3PP_activation_status' / Int8ul,
    'nila_pl_uD3PP_activation_state' / Int8ul,
    'nila_pl_uD3PP_last_activation_time_day' / Int16ul,
    'nila_pl_uD3PP_last_activation_time_ms' / Int32ul,
    'nila_pl_uD3PP_last_feedback_time_day' / Int16ul,
    'nila_pl_uD3PP_last_feedback_time_ms' / Int32ul,
    'nila_pl_uD3PP_last_actuator_finish_time_day' / Int16ul,
    'nila_pl_uD3PP_last_actuator_finish_time_ms' / Int32ul,
    'nila_pl_uD3PP_actuator_feedback' / Int8ul,
    'nila_pl_uD3PP_v_before_activation' / Int16ul,
    'nila_pl_uD3PP_i_before_activation' / Int16ul,
    'nila_pl_uD3PP_t_before_activation' / Int16ul,
    'nila_pl_uD3PP_v_after_activation' / Int16ul,
    'nila_pl_uD3PP_i_after_activation' / Int16ul,
    'nila_pl_uD3PP_t_after_activation' / Int16ul,
    'nila_pl_uD3PP_retry_count' / Int8ul,

    # Actuator 4
    'nila_pl_actuator_uD3RN' / Int8ul,
    'nila_pl_uD3RN_activation_status' / Int8ul,
    'nila_pl_uD3RN_activation_state' / Int8ul,
    'nila_pl_uD3RN_last_activation_time_day' / Int16ul,
    'nila_pl_uD3RN_last_activation_time_ms' / Int32ul,
    'nila_pl_uD3RN_last_feedback_time_day' / Int16ul,
    'nila_pl_uD3RN_last_feedback_time_ms' / Int32ul,
    'nila_pl_uD3RN_last_actuator_finish_time_day' / Int16ul,
    'nila_pl_uD3RN_last_actuator_finish_time_ms' / Int32ul,
    'nila_pl_uD3RN_actuator_feedback' / Int8ul,
    'nila_pl_uD3RN_v_before_activation' / Int16ul,
    'nila_pl_uD3RN_i_before_activation' / Int16ul,
    'nila_pl_uD3RN_t_before_activation' / Int16ul,
    'nila_pl_uD3RN_v_after_activation' / Int16ul,
    'nila_pl_uD3RN_i_after_activation' / Int16ul,
    'nila_pl_uD3RN_t_after_activation' / Int16ul,
    'nila_pl_uD3RN_retry_count' / Int8ul,

    # Actuator 5
    'nila_pl_actuator_nD3SP' / Int8ul,
    'nila_pl_nD3SP_activation_status' / Int8ul,
    'nila_pl_nD3SP_activation_state' / Int8ul,
    'nila_pl_nD3SP_last_activation_time_day' / Int16ul,
    'nila_pl_nD3SP_last_activation_time_ms' / Int32ul,
    'nila_pl_nD3SP_last_feedback_time_day' / Int16ul,
    'nila_pl_nD3SP_last_feedback_time_ms' / Int32ul,
    'nila_pl_nD3SP_last_actuator_finish_time_day' / Int16ul,
    'nila_pl_nD3SP_last_actuator_finish_time_ms' / Int32ul,
    'nila_pl_nD3SP_actuator_feedback' / Int8ul,
    'nila_pl_nD3SP_v_before_activation' / Int16ul,
    'nila_pl_nD3SP_i_before_activation' / Int16ul,
    'nila_pl_nD3SP_t_before_activation' / Int16ul,
    'nila_pl_nD3SP_v_after_activation' / Int16ul,
    'nila_pl_nD3SP_i_after_activation' / Int16ul,
    'nila_pl_nD3SP_t_after_activation' / Int16ul,
    'nila_pl_nD3SP_retry_count' / Int8ul,
)

nila = Struct(
    'ax25_header' / Header,
    'hex20_header' / nila_header,
    'packet' / Switch(
        lambda c: c.hex20_header.ap_id,
        {
            0x10: nila_beacon,
            0x60: nila_pl_pck,
        },
        default=GreedyBytes
    ),
    'crc' / Int16ul,
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017, 2018, 2019, 2020 Daniel Estevez <daniel@destevez.net>
# Copyright 2022 The Regents of the University of Colorado
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from .ax25 import Header
from ..ccsds import space_packet as ccsds_space_packet
from ..adapters import PolynomialAdapter
from construct import Adapter, BitStruct, BitsInteger, Enum, Flag, Float32l, \
                      If, Int16sl, Int16ul, Int32sl, Int32ul, Int8sl, \
                      Int8ub, Int8ul, Padding, Struct, Switch


SecondaryHeader = Struct(
    'sh_coarse' / Int32ul,
    'sh_fine' / Int16ul,
)

cmd_opcodes = Enum(
    Int8ub,
    CMD_OPCODE_NOOP=0, CMD_OPCODE_ARM=1, CMD_OPCODE_RESET_STATS=2,
    CMD_OPCODE_FP_RESET=16, CMD_OPCODE_FP_RESET_RESULTS=17,
    CMD_OPCODE_FP_VALIDATE=18, CMD_OPCODE_FP_SET_TASK_STATE=19,
    CMD_OPCODE_FP_SET_WATCH_STATE=20, CMD_OPCODE_FP_DUMP_WATCH=21,
    CMD_OPCODE_FP_DUMP_RESULTS=22, CMD_OPCODE_FP_SET_WATCH_VALUES=23,
    CMD_OPCODE_FP_SET_WATCH_THRESH=24, CMD_OPCODE_FP_SET_WATCH_RESP=25,
    CMD_OPCODE_SET_PERF_MON_STATE=32, CMD_OPCODE_DES_RESET_STATS=33,
    CMD_OPCODE_DES_ADD_TASK=34, CMD_OPCODE_DES_SUB_TASK=35,
    CMD_OPCODE_DES_ADD_BACK=36, CMD_OPCODE_DES_SUB_BACK=37,
    CMD_OPCODE_DES_SET_TIME=38, CMD_OPCODE_SET_EVT_GROUP=48,
    CMD_OPCODE_SET_EVT_LOG=49, CMD_OPCODE_LOG_RESET_STATS=50,
    CMD_OPCODE_LOG_SET_MASK_STATE=51, CMD_OPCODE_LOG_RESET_LOG=52,
    CMD_OPCODE_LOG_ISSUE_LOG=53, CMD_OPCODE_LOAD_SEQUENCE=64,
    CMD_OPCODE_INIT_SEQUENCE=65, CMD_OPCODE_SET_SEQUENCE_STATE=66,
    CMD_OPCODE_VERIFY_SEQUENCE=67, CMD_OPCODE_STOP_SEQUENCE=68,
    CMD_OPCODE_FIND_SEQUENCE=69, CMD_OPCODE_INFO_SEQUENCE=70,
    CMD_OPCODE_DUMP_SEQUENCE=71, MEM_DUMP=80, MEM_LOAD=81, MEM_ERASE=82,
    MEM_XSUM=83, MEM_ABORT=84, MEM_RESET=85, MEM_LOAD_DWORD=86,
    MEM_LOAD_WORD=87, MEM_LOAD_BYTE=88, CMD_OPCODE_ISSUE_TLM_PKT=96,
    CMD_OPCODE_SET_TLM_RATE=97, CMD_OPCODE_SET_STREAM_STATE=98,
    CMD_OPCODE_PKT_SET_PRIORITY=99, CMD_OPCODE_UHF_PASS=128,
    CMD_OPCODE_UHF_INIT=129, CMD_OPCODE_UHF_RESP_STATE=130,
    CMD_OPCODE_UHF_SET_TX_GAP=131, CMD_OPCODE_ADCS_PASS=144,
    CMD_OPCODE_ADCS_RESET=145, CMD_OPCODE_ADCS_READ=146,
    CMD_OPCODE_ADCS_COARSE_POINT=147, CMD_OPCODE_ADCS_FINE_POINT=148,
    CMD_OPCODE_ADCS_RAM_POINT=149, CMD_OPCODE_ADCS_FINE_UPDATE=150,
    CMD_OPCODE_ADCS_RAM_UPDATE=151, CMD_OPCODE_ADCS_ECLIPSE_CHECK=152,
    CMD_OPCODE_EPS_PWR_ON=160, CMD_OPCODE_EPS_PWR_OFF=161,
    CMD_OPCODE_EPS_PWR_CYCLE=162, CMD_OPCODE_EPS_DEPLOY=163,
    CMD_OPCODE_EPS_HEATER_SETPOINT=164, CMD_OPCODE_EPS_HEATER_THRESH=165,
    CMD_OPCODE_EPS_ECLIPSE_THRESH=166, CMD_OPCODE_SD_WRITE_STATE=176,
    CMD_OPCODE_SD_READ=177, CMD_OPCODE_SD_READ_HALT=178,
    CMD_OPCODE_SD_PLAYBACK=179, CMD_OPCODE_SD_SELECT=181,
    CMD_OPCODE_SD_INIT=182, CMD_OPCODE_SD_SET_PARTITION=183,
    CMD_OPCODE_SD_UPDATE_PARTITION=184, CMD_OPCODE_SD_PWR_OFF=185,
    CMD_OPCODE_SD_RESET_FDRI=186, CMD_OPCODE_SD_SET_FDRI_LIMT=187,
    CMD_OPCODE_SD_TABLE_DEFAULT=188, CMD_OPCODE_CIP_SCI_MODE=208,
    CMD_OPCODE_SBAND_SET_PA=226, CMD_OPCODE_SBAND_SET_MODE=227,
    CMD_OPCODE_SBAND_SET_PA_LEVEL=228, CMD_OPCODE_SBAND_SET_SYNTH=229,
    CMD_OPCODE_SBAND_RESET=230, CMD_OPCODE_SBAND_DEBUG=231,
    CMD_OPCODE_SBAND_SET_ENCODER=232, CMD_OPCODE_SBAND_SYNC_ON=233,
    CMD_OPCODE_SBAND_SYNC_OFF=234, CMD_OPCODE_MODE_SET=240,
    CMD_OPCODE_MODE_AVOID=241, CMD_OPCODE_MODE_SET_THRESHOLD=242,
    CMD_OPCODE_MODE_CLEAR_CLT=243, CMD_OPCODE_MODE_SET_CLT_THRESHOLD=244,
    CMD_OPCODE_MODE_SET_LAUNCH_DELAY=245,
    CMD_OPCODE_MODE_SET_LAUNCH_DELAY_STATE=246,
    CMD_OPCODE_MODE_SET_DEPLOY_INT=247, CMD_OPCODE_MODE_SET_DEPLOY_FLAG=248,
    CMD_OPCODE_MODE_RESET_SC=249, CMD_OPCODE_MODE_AVOID_CLEAR=250,
    CMD_OPCODE_MODE_ECLIPSE_METHOD=251, CMD_OPCODE_MODE_AUTO_DIS=252,
    CMD_OPCODE_MODE_AUTO_ENA=253
)

pwr_status = BitStruct(
    'eclipse_state' / Enum(BitsInteger(1), SUN=0, ECLIPSE=1),
    'pwr_status_sd1' / Enum(BitsInteger(1), OFF=0, ON=1),
    'pwr_status_sd0' / Enum(BitsInteger(1), OFF=0, ON=1),
    'pwr_status_htr' / Enum(BitsInteger(1), OFF=0, ON=1),
    'pwr_status_sband' / Enum(BitsInteger(1), OFF=0, ON=1),
    'pwr_status_adcs' / Enum(BitsInteger(1), OFF=0, ON=1),
    'pwr_status_cip' / Enum(BitsInteger(1), OFF=0, ON=1),
    'pwr_status_daxss' / Enum(BitsInteger(1), OFF=0, ON=1)
)

alive_flags = BitStruct(
    'clt_state' / Enum(BitsInteger(1), OFF=0, ON=1),
    'alive_daxss' / Enum(BitsInteger(1), DEAD=0, ALIVE=1),
    'alive_cip' / Enum(BitsInteger(1), DEAD=0, ALIVE=1),
    'alive_adcs' / Enum(BitsInteger(1), DEAD=0, ALIVE=1),
    'alive_sband' / Enum(BitsInteger(1), DEAD=0, ALIVE=1),
    'alive_uhf' / Enum(BitsInteger(1), DEAD=0, ALIVE=1),
    'alive_sd1' / Enum(BitsInteger(1), DEAD=0, ALIVE=1),
    'alive_sd0' / Enum(BitsInteger(1), DEAD=0, ALIVE=1)
)

uhf_temp = BitStruct(
    'uhf_temp_buff' / BitsInteger(2),
    'uhf_temp' / BitsInteger(6)
)

uhf_config = BitStruct(
    'uhf_locked' / Enum(BitsInteger(1), OFF=0, ON=1),
    'uhf_readback' / Enum(BitsInteger(2), N=0, B=1, T=2),
    'uhf_swd' / Enum(BitsInteger(1), OFF=0, ON=1),
    'uhf_afc' / Enum(BitsInteger(1), OFF=0, ON=1),
    'uhf_echo' / Enum(BitsInteger(1), OFF=0, ON=1),
    'uhf_channel' / Enum(BitsInteger(2), A=0, B=1, D=2)
)

adcs_info = BitStruct(
    'adcs_att_valid' / BitsInteger(1),
    'adcs_refs_valid' / BitsInteger(1),
    'adcs_time_valid' / BitsInteger(1),
    'adcs_mode' / Enum(BitsInteger(1), SUN=0, FINE=1),
    'adcs_recom_sun_pt' / Enum(BitsInteger(1), NO=0, YES=1),
    'adcs_sun_pt_state' / Enum(BitsInteger(3), UNDEF_0=0, UNDEF_1=1,
                               SEARCH_INIT=2, SEARCHING=3, WAITING=4,
                               CONVERGING=5, ON_SUN=6, NOT_ACTIVE=7),
)

is1_beacon = Struct(
    'cmd_recv_count' / Int8ul,
    'cmd_fail_count' / Int8ul,
    'cmd_succ_count' / Int8ul,
    'cmd_succ_op' / cmd_opcodes,
    'cmd_fail_op' / cmd_opcodes,
    'cmd_fail_code' / Enum(Int8ul, SUCCESS=0, MODE=1, ARM=2,
                           SOURCE=3, OPCODE=4, METHOD=5, LENGTH=6,
                           RANGE=7),
    'pwr_status' / pwr_status,
    'sd_read_misc' / Int32ul,
    'sd_read_scic' / Int32ul,
    'sd_read_scid' / Int32ul,
    'sd_read_adcs' / Int32ul,
    'sd_read_beacon' / Int32ul,
    'sd_read_log' / Int32ul,
    'sd_write_misc' / Int32ul,
    'sd_write_scic' / Int32ul,
    'sd_write_scid' / Int32ul,
    'sd_write_adcs' / Int32ul,
    'sd_write_beacon' / Int32ul,
    'sd_write_log' / Int32ul,
    'cmd_loss_timer' / Int32ul,
    'alive_flags' / alive_flags,
    'cip_comstat' / Int32ul,
    'cip_temp1' / PolynomialAdapter([0.0, 0.007813], Int16sl),
    'cip_temp2' / PolynomialAdapter([0.0, 0.007813], Int16sl),
    'cip_temp3' / PolynomialAdapter([0.0, 0.007813], Int16sl),
    'uhf_temp' / uhf_temp,
    'uhf_config' / uhf_config,
    'sband_pa_curr' / PolynomialAdapter([0.0, 4e-05], Int16ul),
    'sband_pa_volt' / PolynomialAdapter([0.0, 0.004], Int16ul),
    'sband_rf_pwr' / PolynomialAdapter([0.0, 0.001139], Int16ul),
    'sband_pa_temp' / PolynomialAdapter([-50.0, 0.073242], Int16ul),
    'sband_top_temp' / PolynomialAdapter([0.0, 0.0625], Int16ul),
    'sband_bottom_temp' / PolynomialAdapter([0.0, 0.0625], Int16ul),
    'adcs_cmd_acpt' / Int8ul,
    'adcs_cmd_fail' / Int8ul,
    'adcs_time' / Int32ul,
    'adcs_info' / adcs_info,
    'adcs_star_temp' / PolynomialAdapter([0.0, 0.8], Int8sl),
    'adcs_wheel_temp1' / PolynomialAdapter([0.0, 0.005], Int16sl),
    'adcs_wheel_temp2' / PolynomialAdapter([0.0, 0.005], Int16sl),
    'adcs_wheel_temp3' / PolynomialAdapter([0.0, 0.005], Int16sl),
    'adcs_digi_bus_volt' / PolynomialAdapter([0.0, 0.00125], Int16sl),
    'adcs_sun_vec1' / PolynomialAdapter([0.0, 0.0001], Int16sl),
    'adcs_sun_vec2' / PolynomialAdapter([0.0, 0.0001], Int16sl),
    'adcs_sun_vec3' / PolynomialAdapter([0.0, 0.0001], Int16sl),
    'adcs_wheel_sp1' / PolynomialAdapter([0.0, 0.4], Int16sl),
    'adcs_wheel_sp2' / PolynomialAdapter([0.0, 0.4], Int16sl),
    'adcs_wheel_sp3' / PolynomialAdapter([0.0, 0.4], Int16sl),
    'adcs_body_rt1' / Int32sl,
    'adcs_body_rt2' / Int32sl,
    'adcs_body_rt3' / Int32sl,
    Padding(12),
    'daxss_time_sec' / Int32ul,
    'daxss_cmd_op' / Int8ul,
    'daxss_cmd_succ' / Int8ul,
    'daxss_cmd_fail' / Int8ul,
    'daxss_cdh_enables' / Int16ul,
    'daxss_cdh_temp' / PolynomialAdapter([0.0, 0.003906], Int16sl),
    'daxss_sps_rate' / Int32ul,
    'daxss_sps_x' / Int16ul,
    'daxss_sps_y' / Int16ul,
    'daxss_slow_count' / Int16ul,
    'bat_fg1' / PolynomialAdapter([0.0, 0.003906], Int16ul),
    'daxss_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'daxss_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'cdh_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'cdh_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'sband_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'sband_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'uhf_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'uhf_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'heater_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'heater_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'sp2_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'sp2_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'sp1_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'sp1_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'sp0_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'sp0_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'bat_vcell' / Int16ul,
    'gps_12v_2_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'gps_12v_2_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'gps_12v_1_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'gps_12v_1_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'bat_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'bat_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'adcs_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'adcs_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    '3p3_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    '3p3_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'cip_curr' / PolynomialAdapter([0.0, 0.0005], Int16ul),
    'cip_volt' / PolynomialAdapter([0.0, 0.001], Int16ul),
    'obc_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'eps_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'int_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'sp0_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'bat0_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'sp1_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'bat1_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'sp2_temp' / PolynomialAdapter([91.394, -0.089493, 3.6e-05], Int16ul),
    'bat_fg3' / PolynomialAdapter([0.0, 0.003906], Int16ul),
    'bat0_temp_conv' / Float32l,
    'bat1_temp_conv' / Float32l,
    'mode' / Enum(Int8ul, PHOENIX=0, SAFE=1, SCID=2, SCIC=3)
)

inspiresat_1 = Struct(
    'ax25_header' / Header,
    'primary_header' / ccsds_space_packet.PrimaryHeader,
    'secondary_header' / If(
        lambda c: c.primary_header.secondary_header_flag,
        SecondaryHeader
    ),
    'packet' / Switch(
        lambda c: (c.primary_header.AP_ID),
        {
            (0x01): is1_beacon
        }
    )
)

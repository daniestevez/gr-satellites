# Copyright 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024  Daniel Estevez
# <daniel@destevez.net>
# Copyright 2024 The Regents of the University of Colorado
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import BitsInteger, BitStruct, Enum, Padding, Struct
from ..adapters import PolynomialAdapter, LinearAdapter

ArmedFlag = Enum(BitsInteger(1), OFF=0, ARMED=1)

sw_cmd = BitStruct(
    'sw_cmd_recv_count' / BitsInteger(16),
    'sw_cmd_fmt_count' / BitsInteger(16),
    'sw_cmd_rjct_count' / BitsInteger(16),
    'sw_cmd_succ_count' / BitsInteger(16),
    Padding(32),
    'sw_cmd_fail_code' / Enum(BitsInteger(8), SUCCESS=0, MODE=1, ARM=2,
                              SOURCE=3, OPCODE=4, METHOD=5, LENGTH=6, RANGE=7,
                              CHECKSUM=8, PKT_TYPE=9),
    'sw_cmd_xsum_state' / Enum(BitsInteger(8), DIS=0, ENA=1),
    Padding(5),
    'sw_cmd_arm_state_uhf' / ArmedFlag,
    'sw_cmd_arm_state_seq' / ArmedFlag,
    'sw_cmd_arm_state_dbg' / ArmedFlag,
)
StateFlag = Enum(BitsInteger(1), OFF=0, ON=1)

sw_eps_aliveness = BitStruct(
    Padding(1),
    'sw_eps_pwr_state_inst4' / StateFlag,
    'sw_eps_pwr_state_inst3' / StateFlag,
    'sw_eps_pwr_state_inst2' / StateFlag,
    'sw_eps_pwr_state_inst1' / StateFlag,
    'sw_eps_pwr_state_sband' / StateFlag,
    'sw_eps_pwr_state_uhf' / StateFlag,
    'sw_eps_pwr_state_adcs' / StateFlag,
)

sw_time_since_rx = BitStruct(
    'sw_time_since_rx' / BitsInteger(32),
)

sw_bat_aliveness = BitStruct(
    Padding(7),
    'sw_bat_alive_state_battery0' / Enum(BitsInteger(1), DEAD=0, ALIVE=1),
)

sw_mode = BitStruct(
    'sw_mode_clt_count' / BitsInteger(8),
    'sw_mode_system_mode' / Enum(BitsInteger(8), PHOENIX=0, SAFE=1, NOMINAL=2),
    Padding(8),
)

sw_comm_aliveness = BitStruct(
    'sw_sband_pa_temp' / PolynomialAdapter([-5.000000e+01, 7.324219e-02],
                                           BitsInteger(16)),
    'sw_sband_pa_curr' / LinearAdapter(25000, BitsInteger(16)),
    Padding(8),
    'sw_uhf_alive' / BitsInteger(8),
    'sw_uhf_temp' / LinearAdapter(0.5, BitsInteger(8, signed=True)),
    Padding(8),
)

SeqState = Enum(BitsInteger(8), IDLE=0, ACTIVE=1, SUSPEND=2, PAUSE=3, STALE=4)
SeqStateStopCode = Enum(BitsInteger(8), NOMINAL=0, CMD=1, INIT=2, REJECT=3,
                        STALE=4, BAD_INT=5, INT_FAIL=6)
SeqExecBuff = Enum(BitsInteger(16), NVM_SMALL0=0, NVM_SMALL1=1, NVM_SMALL2=2,
                   NVM_SMALL3=3, NVM_SMALL4=4, NVM_SMALL5=5, NVM_SMALL6=6,
                   NVM_SMALL7=7, NVM_SMALL8=8, NVM_SMALL9=9, NVM_SMALL10=10,
                   NVM_SMALL11=11, NVM_SMALL12=12, NVM_SMALL13=13,
                   NVM_SMALL14=14, NVM_SMALL15=15, NVM_SMALL16=16,
                   NVM_SMALL17=17, NVM_SMALL18=18, NVM_SMALL19=19,
                   NVM_SMALL20=20, NVM_SMALL21=21, NVM_SMALL22=22,
                   NVM_SMALL23=23, NVM_SMALL24=24, NVM_SMALL25=25,
                   NVM_SMALL26=26, NVM_SMALL27=27, NVM_SMALL28=28,
                   NVM_SMALL29=29, NVM_SMALL30=30, NVM_SMALL31=31,
                   NVM_SMALL32=32, NVM_SMALL33=33, NVM_SMALL34=34,
                   NVM_SMALL35=35, NVM_SMALL36=36, NVM_SMALL37=37,
                   NVM_SMALL38=38, NVM_SMALL39=39, NVM_SMALL40=40,
                   NVM_SMALL41=41, NVM_SMALL42=42, NVM_SMALL43=43,
                   NVM_SMALL44=44, NVM_SMALL45=45, NVM_SMALL46=46,
                   NVM_SMALL47=47, NVM_SMALL48=48, NVM_SMALL49=49,
                   NVM_SMALL50=50, NVM_SMALL51=51, NVM_SMALL52=52,
                   NVM_SMALL53=53, NVM_SMALL54=54, NVM_SMALL55=55,
                   NVM_SMALL56=56, NVM_SMALL57=57, NVM_SMALL58=58,
                   NVM_SMALL59=59, NVM_SMALL60=60, NVM_SMALL61=61,
                   NVM_SMALL62=62, NVM_SMALL63=63, NVM_SMALL64=64,
                   NVM_SMALL65=65, NVM_SMALL66=66, NVM_SMALL67=67,
                   NVM_SMALL68=68, NVM_SMALL69=69, NVM_SMALL70=70,
                   NVM_SMALL71=71, NVM_SMALL72=72, NVM_SMALL73=73,
                   NVM_SMALL74=74, NVM_SMALL75=75, NVM_SMALL76=76,
                   NVM_SMALL77=77, NVM_SMALL78=78, NVM_SMALL79=79,
                   NVM_LARGE0=80, NVM_LARGE1=81, HOLDING0=82)

sw_sequence = BitStruct(
    'sw_seq_state_auto' / SeqState,
    'sw_seq_state_op1' / SeqState,
    'sw_seq_state_op2' / SeqState,
    'sw_seq_state_op3' / SeqState,
    'sw_seq_stop_code_auto' / SeqStateStopCode,
    'sw_seq_stop_code_op1' / SeqStateStopCode,
    'sw_seq_stop_code_op2' / SeqStateStopCode,
    'sw_seq_stop_code_op3' / SeqStateStopCode,
    'sw_seq_exec_buf_auto' / SeqExecBuff,
    'sw_seq_exec_buf_op1' / SeqExecBuff,
    'sw_seq_exec_buf_op2' / SeqExecBuff,
    'sw_seq_exec_buf_op3' / SeqExecBuff,
)

sw_partition = BitStruct(
    'sw_store_partition_write_misc' / BitsInteger(32),
    'sw_store_partition_read_misc' / BitsInteger(32),
    'sw_store_partition_write_adcs' / BitsInteger(32),
    'sw_store_partition_read_adcs' / BitsInteger(32),
    'sw_store_partition_write_beacon' / BitsInteger(32),
    'sw_store_partition_read_beacon' / BitsInteger(32),
    'sw_store_partition_write_log' / BitsInteger(32),
    'sw_store_partition_read_log' / BitsInteger(32),
    'sw_store_partition_write_sci' / BitsInteger(32),
    'sw_store_partition_read_sci' / BitsInteger(32),
)

sw_fp = BitStruct(
    'sw_fp_resp_count' / BitsInteger(16),
)
VoltageAdapter103 = LinearAdapter(103.5282425045552, BitsInteger(16))
VoltageAdapter112 = LinearAdapter(112.8375252473963, BitsInteger(16))
VoltageAdapter252 = LinearAdapter(252.2767981028785, BitsInteger(16))
VoltageAdapter620 = LinearAdapter(620.6168931918327, BitsInteger(16))
VoltageAdapter1241 = LinearAdapter(1241.21837996177, BitsInteger(16))
CurrentAdapter496 = LinearAdapter(496.4750273061265, BitsInteger(16))
CurrentAdapter819 = LinearAdapter(819.2020971573687, BitsInteger(16))
CurrentAdapter12412 = LinearAdapter(12412.1837996177, BitsInteger(16))

sw_ana = BitStruct(
    'sw_ana_bus_v' / VoltageAdapter112,
    'sw_ana_3p3_v' / VoltageAdapter620,
    'sw_ana_2p5_v' / VoltageAdapter1241,
    'sw_ana_1p8_v' / VoltageAdapter1241,
    'sw_ana_1p0_v' / VoltageAdapter1241,
    'sw_ana_3p3_i' / CurrentAdapter12412,
    'sw_ana_1p8_i' / CurrentAdapter12412,
    'sw_ana_1p0_i' / CurrentAdapter12412,
    'sw_ana_cdh_temp' / PolynomialAdapter([1.255500e+02, -1.362200e-01,
                                           9.861100e-05, -4.417600e-08,
                                           1.012500e-11, 9.390500e-16],
                                          BitsInteger(16)
                                          ),
    'sw_ana_cdh_3p3_ref' / PolynomialAdapter([1.255500e+02,
                                              -1.362200e-01],
                                             BitsInteger(16)),
    'sw_ana_sa1_v' / VoltageAdapter103,
    'sw_ana_sa1_i' / CurrentAdapter496,
    'sw_ana_sa2_v' / VoltageAdapter103,
    'sw_ana_sa2_i' / CurrentAdapter496,
    'sw_ana_bat1_v' / VoltageAdapter112,
    'sw_ana_eps_temp' / PolynomialAdapter([1.255500e+02, -1.362200e-01,
                                           9.861100e-05, -4.417600e-08,
                                           1.012500e-11, -9.390500e-16],
                                          BitsInteger(16)
                                          ),
    'sw_ana_eps_3p3_ref' / VoltageAdapter620,
    'sw_ana_eps_bus_v' / VoltageAdapter112,
    'sw_ana_eps_bus_i' / CurrentAdapter819,
    'sw_ana_xact_v' / VoltageAdapter112,
    'sw_ana_xact_i' / CurrentAdapter496,
    'sw_ana_uhf_v' / VoltageAdapter112,
    'sw_ana_uhf_i' / CurrentAdapter496,
    'sw_ana_sband_v' / VoltageAdapter112,
    'sw_ana_sband_i' / CurrentAdapter496,
    'sw_ana_axis1_volt' / VoltageAdapter252,
    'sw_ana_axis1_curr' / CurrentAdapter819,
    'sw_ana_axis2_volt' / VoltageAdapter252,
    'sw_ana_axis2_curr' / CurrentAdapter819,
    'sw_ana_axis3_volt' / VoltageAdapter252,
    'sw_ana_axis3_curr' / CurrentAdapter819,
    'sw_ana_afire_volt' / VoltageAdapter252,
    'sw_ana_afire_curr' / CurrentAdapter819,
    'sw_ana_ifb_therm1' / PolynomialAdapter([1.255500e+02, -1.362200e-01,
                                             9.861100e-05, -4.417600e-08,
                                             1.012500e-11, -9.390500e-16],
                                            BitsInteger(16)
                                            ),
)

VoltageAdapter66 = LinearAdapter(66.666666666666666, BitsInteger(8))
TempAdapter200 = LinearAdapter(200.0, BitsInteger(16, signed=True))
VecAdapter10000 = LinearAdapter(10000.0, BitsInteger(16, signed=True))
SpAdapter2 = LinearAdapter(2.5, BitsInteger(16, signed=True))
RtAdapter200000000 = LinearAdapter(200000000.0, BitsInteger(32, signed=True))
QuatAdapter2000000000 = LinearAdapter(2000000000.0, BitsInteger(32,
                                                                signed=True))

ADCSValid = Enum(BitsInteger(1), NO=0, YES=1)
sw_adcs = BitStruct(
    'sw_adcs_alive' / Enum(BitsInteger(8), OFF=0, DEAD=1, ALIVE=2),
    'sw_adcs_eclipse' / BitsInteger(8),
    'sw_adcs_att_valid' / ADCSValid,
    'sw_adcs_ref_valid' / ADCSValid,
    'sw_adcs_time_valid' / ADCSValid,
    'sw_adcs_mode' / Enum(BitsInteger(1), SUN_POINT=0, FINE_REF_POINT=1),
    'sw_adcs_recommend_sun_point' / ADCSValid,
    'sw_adcs_sun_point_state' / Enum(BitsInteger(3), NOT_ACTIVE=7,
                                     SEARCH_INIT=2, WAITING=4, CONVERGING=5,
                                     ON_SUN=6, SEARCHING=3, SUN_POINT=0,
                                     FINE_REF_POINT=1),
    Padding(8),
    'sw_adcs_analogs_voltage_2p5' / VoltageAdapter66,
    'sw_adcs_analogs_voltage_1p8' / VoltageAdapter66,
    'sw_adcs_analogs_voltage_1p0' / VoltageAdapter66,
    'sw_adcs_analogs_det_temp' / LinearAdapter(1.25, BitsInteger(8,
                                                                 signed=True)),
    'sw_adcs_analogs_motor1_temp' / TempAdapter200,
    'sw_adcs_analogs_motor2_temp' / TempAdapter200,
    'sw_adcs_analogs_motor3_temp' / TempAdapter200,
    'sw_adcs_analogs_digital_bus_v' / LinearAdapter(800.0, BitsInteger(16)),
    'sw_adcs_cmd_acpt' / BitsInteger(8),
    'sw_adcs_cmd_fail' / BitsInteger(8),
    'sw_adcs_sun_vec1' / VecAdapter10000,
    'sw_adcs_sun_vec2' / VecAdapter10000,
    'sw_adcs_sun_vec3' / VecAdapter10000,
    'sw_adcs_wheel_sp1' / SpAdapter2,
    'sw_adcs_wheel_sp2' / SpAdapter2,
    'sw_adcs_wheel_sp3' / SpAdapter2,
    'sw_adcs_body_rt1' / RtAdapter200000000,
    'sw_adcs_body_rt2' / RtAdapter200000000,
    'sw_adcs_body_rt3' / RtAdapter200000000,
    'sw_adcs_body_quat1' / QuatAdapter2000000000,
    'sw_adcs_body_quat2' / QuatAdapter2000000000,
    'sw_adcs_body_quat3' / QuatAdapter2000000000,
    'sw_adcs_body_quat4' / QuatAdapter2000000000,
)

payload_aliveness = BitStruct(
    'des_met_time_seconds' / BitsInteger(32),
    'sw_im_id' / BitsInteger(8),
    'payload_alive_axis1' / BitsInteger(8),
    'payload_alive_axis2' / BitsInteger(8),
    'payload_alive_axis3' / BitsInteger(8),
    'payload_alive_afire' / BitsInteger(8),
    Padding(8),
)

aepex_sw_stat = Struct(
    'sw_cmd' / sw_cmd,
    'sw_eps_aliveness' / sw_eps_aliveness,
    'sw_time_since_rx' / sw_time_since_rx,
    'sw_bat_aliveness' / sw_bat_aliveness,
    'sw_mode' / sw_mode,
    'sw_comm_aliveness' / sw_comm_aliveness,
    'sw_sequence' / sw_sequence,
    'sw_partition' / sw_partition,
    'sw_fp' / sw_fp,
    'sw_ana' / sw_ana,
    'sw_adcs' / sw_adcs,
    'payload_aliveness' / payload_aliveness
)

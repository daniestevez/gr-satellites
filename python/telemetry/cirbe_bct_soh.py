from ..adapters import LinearAdapter, PolynomialAdapter
from construct import Adapter, BitsInteger, BitStruct, Container, Enum, Flag, \
                      Float64b, Int8ub, Int16ub, Int32ub, Padding, Struct, \
                      Switch


soh_l0 = BitStruct(
    'wdt_2sec_cnt' / LinearAdapter(1.0, BitsInteger(3)),
    'reset_armed' / Enum(BitsInteger(1), ARMED=1, NOT_ARMED=0),
    'wdt_stat' / Enum(BitsInteger(1), NO_WDT=0, WDT=1),
    'wdt_en' / Enum(BitsInteger(1), DISABLED=0, ENABLED=1),
    'table_select' / Enum(BitsInteger(1), FLASH=0, COMPILED=1),
    'boot_relay' / Enum(BitsInteger(1), PRIMARY=1, REDUNDANT=0),
    'l0_acpt_cnt' / LinearAdapter(1.0, BitsInteger(8)),
    'l0_rjct_cnt' / LinearAdapter(1.0, BitsInteger(8)),
    'hw_sec_cnt' / LinearAdapter(1.0, BitsInteger(8)),
    Padding(64),
    'time_tag' / LinearAdapter(1.0, BitsInteger(32)),
    Padding(80),
    'spare_end' / LinearAdapter(1.0, BitsInteger(48)),
)


soh_command_tlm = BitStruct(
    'cmd_status' / Enum(BitsInteger(8), OK=0, BAD_APID=1, BAD_OPCODE=2,
                        BAD_DATA=3, NOW_READING=4, DONE_READING=5, IDLE=6,
                        NO_CMD_DATA=7, CMD_SRVC_OVERRUN=8, CMD_APID_OVERRUN=9,
                        INCORRECT_WHEEL_MODE=10, BAD_ELEMENT=11,
                        TABLES_BUSY=12, FLASH_NOT_ARMED=13,
                        THRUSTERS_DISABLED=14, ATT_ERR_TOO_HIGH=15,
                        ASYNC_REFUSED=16, DRIVER_ERROR=17),
    'realtime_cmd_accept_count' / LinearAdapter(1.0, BitsInteger(8)),
    'realtime_cmd_reject_count' / LinearAdapter(1.0, BitsInteger(8)),
    'stored_cmd_accept_count' / LinearAdapter(1.0, BitsInteger(8)),
    'stored_cmd_reject_count' / LinearAdapter(1.0, BitsInteger(8)),
)


soh_general = BitStruct(
    'scrub_status_overall' / Enum(BitsInteger(8), OK=0, FAIL=-1, IN_PROG=1,
                                  ABORTED=-2),
    'image_booted' / Enum(BitsInteger(8), PRIMARY=0, REDUNDANT=1),
    'image_auto_failover' / Enum(BitsInteger(8), OK=0, FAIL=1),
    'inertia_index' / LinearAdapter(1.0, BitsInteger(8)),
)


soh_time = Struct(
    'tai_seconds' / Float64b,
    'time_valid' / Enum(Int8ub, YES=1, NO=0),
    'rtc_health1_pack' / BitStruct(
        'health1_pack_spare2' / LinearAdapter(1.0, BitsInteger(1)),
        'rtc_osc_rst_count' / LinearAdapter(1.0, BitsInteger(3)),
        'rtc_init_time_at_boot' / Enum(BitsInteger(1), NO=0, YES=1),
        'rtc_sync_stat' / Enum(BitsInteger(1), OFF=0, ON=1),
        'rtc_alive' / Enum(BitsInteger(1), NO=0, YES=1),
        'rtc_power' / Enum(BitsInteger(1), OFF=0, ON=1),)
)


soh_refs = BitStruct(
    'position_wrt_eci1' / LinearAdapter(50000.002500000126, BitsInteger(32)),
    'position_wrt_eci2' / LinearAdapter(50000.002500000126, BitsInteger(32)),
    'position_wrt_eci3' / LinearAdapter(50000.002500000126, BitsInteger(32)),
    'velocity_wrt_eci1' / LinearAdapter(200000000.0, BitsInteger(32)),
    'velocity_wrt_eci2' / LinearAdapter(200000000.0, BitsInteger(32)),
    'velocity_wrt_eci3' / LinearAdapter(200000000.0, BitsInteger(32)),
    'modeled_sun_vector_body1' / LinearAdapter(25000.000625000015,
                                               BitsInteger(16)),
    'modeled_sun_vector_body2' / LinearAdapter(25000.000625000015,
                                               BitsInteger(16)),
    'modeled_sun_vector_body3' / LinearAdapter(25000.000625000015,
                                               BitsInteger(16)),
    'mag_model_vector_body1' / LinearAdapter(200000000.0, BitsInteger(16)),
    'mag_model_vector_body2' / LinearAdapter(200000000.0, BitsInteger(16)),
    'mag_model_vector_body3' / LinearAdapter(200000000.0, BitsInteger(16)),
    'refs_valid' / Enum(BitsInteger(8), YES=1, NO=0),
    'run_low_rate_task' / Enum(BitsInteger(8), YES=1, NO=0),
)


soh_att_det = BitStruct(
    'q_body_wrt_eci1' / LinearAdapter(2000000040.000001, BitsInteger(32)),
    'q_body_wrt_eci2' / LinearAdapter(2000000040.000001, BitsInteger(32)),
    'q_body_wrt_eci3' / LinearAdapter(2000000040.000001, BitsInteger(32)),
    'q_body_wrt_eci4' / LinearAdapter(2000000040.000001, BitsInteger(32)),
    'tracker_sol_mixed' / Enum(BitsInteger(1), NO=0, YES=1),
    Padding(1),
    'tracker2_data_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'tracker1_data_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'imu_data_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'meas_rate_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'meas_att_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'attitude_valid' / Enum(BitsInteger(1), NO=0, YES=1),
)


soh_att_cmd = BitStruct(
    'hr_cycle_safe_mode' / LinearAdapter(1.0, BitsInteger(32)),
    'health1_pack_spare1' / LinearAdapter(1.0, BitsInteger(1)),
    'sun_point_reason' / Enum(BitsInteger(3), BOOT=0, COMMAND=1,
                              ATTITUDE_INVALID=2, TIME_INVALID=3,
                              REFS_INVALID=4),
    'recommend_sun_point' / Enum(BitsInteger(1), NO=0, YES=1),
    Padding(2),
    'adcs_mode' / Enum(BitsInteger(1), SUN_POINT=0, FINE_REF_POINT=1),
)


soh_rw_drive = BitStruct(
    'filtered_speed_rpm1' / LinearAdapter(2.4999999375000015, BitsInteger(16)),
    'filtered_speed_rpm2' / LinearAdapter(2.4999999375000015, BitsInteger(16)),
    'filtered_speed_rpm3' / LinearAdapter(2.4999999375000015, BitsInteger(16)),
)


soh_tracker = BitStruct(
    'operating_mode' / Enum(BitsInteger(8), IDLE=0, INITIALIZE=1, STARID=2,
                            TRACK=3, PHOTO=4, CAL=5, BLOCK=6),
    'star_id_step' / Enum(BitsInteger(8), IDLE=0, INITIALIZE=1,
                          WAITING_FOR_IMAGE1=2, WAITING_FOR_IMAGE2=3,
                          CALCULATE_RATE=4, MAKE_UNIT_VECTORS=5,
                          AWAITING_TRISTAR=6, OK_FOUND_4=7, OK_FOUND_3=8,
                          TIME_OUT=9, SPARE=10, NO_MATCH=11),
    'att_status' / Enum(BitsInteger(8), OK=0, PENDING=1, BAD=2,
                        TOO_FEW_STARS=3, QUEST_FAILED=4, RESIDUALS_TOO_HIGH=5,
                        TOO_CLOSE_TO_EDGE=6, PIX_AMP_TOO_LOW=7,
                        PIX_AMP_TOO_HIGH=8, BACKGND_TOO_HIGH=9,
                        TRACK_FAILURE=10, PIX_SUM_TOO_LOW=11, UNUSED=12,
                        TOO_DIM_FOR_STARID=13, TOO_MANY_GROUPS=14,
                        TOO_FEW_GROUPS=15, CHANNEL_DISABLED=16,
                        TRACK_BLK_OVERLAP=17, OK_FOR_STARID=18,
                        TOO_CLOSE_TO_OTHER=19, TOO_MANY_PIXELS=20,
                        TOO_MANY_COLUMNS=21, TOO_MANY_ROWS=22, OPEN=23,
                        CLOSED=24, RATE_TOO_HIGH=25),
    'num_attitude_stars' / LinearAdapter(1.0, BitsInteger(8)),
)


soh_att_ctrl = BitStruct(
    'eigen_error' / LinearAdapter(659999963.0400021, BitsInteger(32)),
    'sun_point_angle_error' / LinearAdapter(333.33335555555703,
                                            BitsInteger(16)),
    'health1_pack_spare1' / LinearAdapter(1.0, BitsInteger(2)),
    'sun_source_failover' / Enum(BitsInteger(1), OK=0, FAIL=1),
    'sun_avoid_flag' / Enum(BitsInteger(1), NO=0, YES=1),
    Padding(1),
    'on_sun_flag' / Enum(BitsInteger(1), NO=0, YES=1),
    'momentum_too_high' / Enum(BitsInteger(1), NO=0, YES=1),
    'att_ctrl_active' / Enum(BitsInteger(1), NO=0, YES=1),
)


soh_momentum = BitStruct(
    'total_momentum_mag' / LinearAdapter(1999.9999200000032, BitsInteger(16)),
    'duty_cycle1' / LinearAdapter(1.0, BitsInteger(8)),
    'duty_cycle2' / LinearAdapter(1.0, BitsInteger(8)),
    'duty_cycle3' / LinearAdapter(1.0, BitsInteger(8)),
    'torque_rod_mode1' / Enum(BitsInteger(8), OFF=0, ON_POS=1,
                              ON_NEG=2, AUTO=3, MEASURED=4, MODELED=5,
                              DELAYED_AUTO=6, NO_FIELD_VALID=7, UNUSED1=8,
                              UNUSED2=9, BIDIRECTIONAL=10, POS_ONLY=11,
                              NEG_ONLY=12),
    'torque_rod_mode2' / Enum(BitsInteger(8), OFF=0, ON_POS=1,
                              ON_NEG=2, AUTO=3, MEASURED=4, MODELED=5,
                              DELAYED_AUTO=6, NO_FIELD_VALID=7, UNUSED1=8,
                              UNUSED2=9, BIDIRECTIONAL=10, POS_ONLY=11,
                              NEG_ONLY=12),
    'torque_rod_mode3' / Enum(BitsInteger(8), OFF=0, ON_POS=1,
                              ON_NEG=2, AUTO=3, MEASURED=4, MODELED=5,
                              DELAYED_AUTO=6, NO_FIELD_VALID=7, UNUSED1=8,
                              UNUSED2=9, BIDIRECTIONAL=10, POS_ONLY=11,
                              NEG_ONLY=12),
    'torque_rod_firing_pack_spare' / LinearAdapter(1.0, BitsInteger(1)),
    'torque_rod_direction3' / Enum(BitsInteger(1), POS=0, NEG=1),
    'torque_rod_direction2' / Enum(BitsInteger(1), POS=0, NEG=1),
    'torque_rod_direction1' / Enum(BitsInteger(1), POS=0, NEG=1),
    Padding(1),
    'torque_rod_enable3' / Enum(BitsInteger(1), DS=0, EN=1),
    'torque_rod_enable2' / Enum(BitsInteger(1), DS=0, EN=1),
    'torque_rod_enable1' / Enum(BitsInteger(1), DS=0, EN=1),
    'health1_pack_spare2' / LinearAdapter(1.0, BitsInteger(2)),
    'mag_source_failover' / Enum(BitsInteger(1), OK=0, FAULT=1),
    'tr_fault' / Enum(BitsInteger(1), FAULT=0, OK=1),
    'health1_pack_spare1' / LinearAdapter(1.0, BitsInteger(1)),
    'momentum_vector_enabled' / Enum(BitsInteger(1), NO=0, YES=1),
    'momentum_vector_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'tr_drive_power_state' / Enum(BitsInteger(1), OFF=0, ON=1),
)

soh_css = BitStruct(
    'sun_vector_body1' / LinearAdapter(10000.000300000009, BitsInteger(16)),
    'sun_vector_body2' / LinearAdapter(10000.000300000009, BitsInteger(16)),
    'sun_vector_body3' / LinearAdapter(10000.000300000009, BitsInteger(16)),
    'sun_vector_status' / Enum(BitsInteger(8), GOOD=0, COARSE=1, BAD=2),
    'css_invalid_count' / LinearAdapter(1.0, BitsInteger(16)),
    'health1_pack_spare1' / LinearAdapter(1.0, BitsInteger(1)),
    'sun_sensor_used' / LinearAdapter(1.0, BitsInteger(3)),
    'css_test_mode' / Enum(BitsInteger(1), NO=0, YES=1),
    'sun_vector_enabled' / Enum(BitsInteger(1), NO=0, YES=1),
    'meas_sun_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'css_power_state' / Enum(BitsInteger(1), OFF=0, ON=1),
)

soh_mag = BitStruct(
    'mag_vector_body1' / LinearAdapter(200000000.0, BitsInteger(16)),
    'mag_vector_body2' / LinearAdapter(200000000.0, BitsInteger(16)),
    'mag_vector_body3' / LinearAdapter(200000000.0, BitsInteger(16)),
    'mag_invalid_count' / LinearAdapter(1.0, BitsInteger(16)),
    'health1_pack_spare1' / LinearAdapter(1.0, BitsInteger(1)),
    'mag_sensor_used' / LinearAdapter(1.0, BitsInteger(3)),
    'mag_test_mode' / Enum(BitsInteger(1), NO=0, YES=1),
    'mag_vector_enabled' / Enum(BitsInteger(1), NO=0, YES=1),
    'mag_vector_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'mag_power_state' / Enum(BitsInteger(1), OFF=0, ON=1),
)

soh_imu = BitStruct(
    'imu_avg_vector_body1' / LinearAdapter(100000.0030000001, BitsInteger(16)),
    'imu_avg_vector_body2' / LinearAdapter(100000.0030000001, BitsInteger(16)),
    'imu_avg_vector_body3' / LinearAdapter(100000.0030000001, BitsInteger(16)),
    'imu_invalid_count' / LinearAdapter(1.0, BitsInteger(16)),
    'health1_pack_spare1' / LinearAdapter(1.0, BitsInteger(3)),
    'imu_valid_packets' / Enum(BitsInteger(1), NO=0, YES=1),
    'imu_test_mode' / Enum(BitsInteger(1), NO=0, YES=1),
    'imu_vector_enabled' / Enum(BitsInteger(1), NO=0, YES=1),
    'imu_vector_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'imu_power_state' / Enum(BitsInteger(1), OFF=0, ON=1),
)

soh_clock_sync = BitStruct(
    'hr_run_count' / LinearAdapter(1.0, BitsInteger(32)),
    'hr_exec_time_ms1' / LinearAdapter(1.0, BitsInteger(8)),
    'hr_exec_time_ms2' / LinearAdapter(1.0, BitsInteger(8)),
    'hr_exec_time_ms3' / LinearAdapter(1.0, BitsInteger(8)),
    'hr_exec_time_ms4' / LinearAdapter(1.0, BitsInteger(8)),
    'hr_exec_time_ms5' / LinearAdapter(1.0, BitsInteger(8)),
)

soh_analogs = BitStruct(
    'battery_voltage' / LinearAdapter(499.99997500000126, BitsInteger(16)),
)

soh_gps = BitStruct(
    'gps_cycles_since_crc_data' / LinearAdapter(1.0, BitsInteger(32)),
    'gps_lock_count' / LinearAdapter(1.0, BitsInteger(16)),
    'msg_used_satellites' / LinearAdapter(1.0, BitsInteger(8)),
    'gps_pos_lock' / Enum(BitsInteger(1), NO=0, YES=1),
    'gps_time_lock' / Enum(BitsInteger(1), NO=0, YES=1),
    'msg_data_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'gps_new_data_received' / Enum(BitsInteger(1), NO=0, YES=1),
    Padding(1),
    'gps_enable' / Enum(BitsInteger(1), NO=0, YES=1),
    'gps_valid' / Enum(BitsInteger(1), NO=0, YES=1),
    'health1_pack_spare1' / LinearAdapter(1.0, BitsInteger(1)),
)

soh_event_check = BitStruct(
    'latched_resp_fire_pack_bit8' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit7' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit6' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit5' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit4' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit3' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit2' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit1' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit16' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit15' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit14' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit13' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit12' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit11' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit10' / LinearAdapter(1.0, BitsInteger(1)),
    'latched_resp_fire_pack_bit9' / LinearAdapter(1.0, BitsInteger(1)),
)

soh_radio = BitStruct(
    'sd_minute_cur' / LinearAdapter(1.0, BitsInteger(32)),
    'sd_percent_used_total' / LinearAdapter(1.0, BitsInteger(8)),
    'sd_ok' / Enum(BitsInteger(8), YES=1, NO=0),
    'sd_fault_count' / LinearAdapter(1.0, BitsInteger(8)),
    'sq_channel' / LinearAdapter(1.0, BitsInteger(8)),
    'sq_trap_count' / LinearAdapter(1.0, BitsInteger(8)),
    'sq_temp' / LinearAdapter(1.0, BitsInteger(8)),
    'sdr_tx_tx_frames' / LinearAdapter(1.0, BitsInteger(32)),
    'sdr_tx_tx_power' / LinearAdapter(1.0, BitsInteger(8)),
    'sdr_tx_temp' / LinearAdapter(1.0, BitsInteger(8)),
    'sdr_tx_comm_error' / Enum(BitsInteger(8), NO=0, YES=1),
)

soh_tracker_ctrl = BitStruct(
    'tracker_att_valid' / Enum(BitsInteger(8), YES=1, NO=0)
)

cirbe_bct_soh = Struct(
    'soh_l0' / soh_l0,
    'soh_command_tlm' / soh_command_tlm,
    'soh_general' / soh_general,
    'soh_time' / soh_time,
    'soh_refs' / soh_refs,
    'soh_att_det' / soh_att_det,
    'soh_att_cmd' / soh_att_cmd,
    'soh_rw_drive' / soh_rw_drive,
    'soh_tracker' / soh_tracker,
    'soh_att_ctrl' / soh_att_ctrl,
    'soh_momentum' / soh_momentum,
    'soh_css' / soh_css,
    'soh_mag' / soh_mag,
    'soh_imu' / soh_imu,
    'soh_clock_sync' / soh_clock_sync,
    'soh_analogs' / soh_analogs,
    'soh_gps' / soh_gps,
    'soh_event_check' / soh_event_check,
    'soh_radio' / soh_radio,
    'soh_tracker_ctrl' / soh_tracker_ctrl,
)

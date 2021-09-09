from ..adapters import LinearAdapter
from construct import Adapter, BitsInteger, BitStruct, Container, Enum, Flag, \
                      Int8ub, Int16ub, Int32ub, Padding, Struct, Switch

SOH_L0 = BitStruct(
    'SOH_L0__WDT_2SEC_CNT' / BitsInteger(3),
    'SOH_L0__RESET_ARMED' / Enum(Flag, ARMED=1, NOT_ARMED=0),
    'SOH_L0__WDT_STAT' / Enum(Flag, NO_WDT=0, WDT=1),
    'SOH_L0__WDT_EN' / Enum(Flag, DISABLED=0, ENABLED=1),
    'SOH_L0__TABLE_SELECT' / Enum(Flag, FLASH=0, COMPILED=1),
    'SOH_L0__BOOT_RELAY' / Enum(Flag, PRIMARY=1, REDUNDANT=0),
    'SOH_L0__L0_ACPT_CNT' / BitsInteger(8),
    'SOH_L0__L0_RJCT_CNT' / BitsInteger(8),
    'SOH_L0__HW_SEC_CNT' / BitsInteger(8),
    Padding(64),
    'SOH_L0__TIME_TAG' / BitsInteger(32),
    Padding(32),
    'SOH_L0__PLD_TLM_ACK_CNT' / BitsInteger(8),
    'SOH_L0__PLD_CMD_CNT' / BitsInteger(8),
    'SOH_L0__PLD_TLM_TO_CNT' / BitsInteger(8),
    'SOH_L0__PLD_TLM_NAK_CNT' / BitsInteger(8),
    'SOH_L0__SPARE_END' / BitsInteger(64),
)

SOH_COMMAND_TLM = BitStruct(
    'SOH_COMMAND_TLM__CMD_STATUS' / Enum(BitsInteger(8), OK=0, BAD_APID=1,
                                         BAD_OPCODE=2, BAD_DATA=3,
                                         NOW_READING=4, DONE_READING=5, IDLE=6,
                                         NO_CMD_DATA=7, CMD_SRVC_OVERRUN=8,
                                         CMD_APID_OVERRUN=9,
                                         INCORRECT_WHEEL_MODE=10,
                                         BAD_ELEMENT=11, TABLES_BUSY=12,
                                         FLASH_NOT_ARMED=13,
                                         THRUSTERS_DISABLED=14,
                                         ATT_ERR_TOO_HIGH=15, ASYNC_REFUSED=16,
                                         DRIVER_ERROR=17),
    'SOH_COMMAND_TLM__REALTIME_CMD_ACCEPT_COUNT' / BitsInteger(8),
    'SOH_COMMAND_TLM__REALTIME_CMD_REJECT_COUNT' / BitsInteger(8),
    'SOH_COMMAND_TLM__STORED_CMD_ACCEPT_COUNT' / BitsInteger(8),
    'SOH_COMMAND_TLM__STORED_CMD_REJECT_COUNT' / BitsInteger(8),
    'SOH_COMMAND_TLM__MACROS_EXECUTING_PACK1' / BitsInteger(8),
    'SOH_COMMAND_TLM__MACROS_EXECUTING_PACK2' / BitsInteger(8),
)

SOH_GENERAL = BitStruct(
    'SOH_GENERAL__SCRUB_STATUS_OVERALL' / Enum(BitsInteger(8), OK=0, FAIL=-1),
    'SOH_GENERAL__IMAGE_BOOTED' / Enum(BitsInteger(8), PRIMARY=0, REDUNDANT=1),
    'SOH_GENERAL__IMAGE_AUTO_FAILOVER' / Enum(BitsInteger(8), OK=0, FAIL=1),
)

SOH_TIME = BitStruct(
    'SOH_TIME__TAI_SECONDS' / LinearAdapter(5.0, BitsInteger(32)),
    'SOH_TIME__TIME_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
)

SOH_REFS = BitStruct(
    'SOH_REFS__POSITION_WRT_ECI1' / LinearAdapter(50000, BitsInteger(32)),
    'SOH_REFS__POSITION_WRT_ECI2' / LinearAdapter(50000, BitsInteger(32)),
    'SOH_REFS__POSITION_WRT_ECI3' / LinearAdapter(50000, BitsInteger(32)),
    'SOH_REFS__VELOCITY_WRT_ECI1' / LinearAdapter(200000000, BitsInteger(32)),
    'SOH_REFS__VELOCITY_WRT_ECI2' / LinearAdapter(200000000, BitsInteger(32)),
    'SOH_REFS__VELOCITY_WRT_ECI3' / LinearAdapter(200000000, BitsInteger(32)),
    'SOH_REFS__REFS_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
)

SOH_ATT_DET = BitStruct(
    'SOH_ATT_DET__Q_BODY_WRT_ECI1' / LinearAdapter(2e9, BitsInteger(32)),
    'SOH_ATT_DET__Q_BODY_WRT_ECI2' / LinearAdapter(2e9, BitsInteger(32)),
    'SOH_ATT_DET__Q_BODY_WRT_ECI3' / LinearAdapter(2e9, BitsInteger(32)),
    'SOH_ATT_DET__Q_BODY_WRT_ECI4' / LinearAdapter(2e9, BitsInteger(32)),
    'SOH_ATT_DET__BODY_RATE1' / LinearAdapter(200000000, BitsInteger(32)),
    'SOH_ATT_DET__BODY_RATE2' / LinearAdapter(200000000, BitsInteger(32)),
    'SOH_ATT_DET__BODY_RATE3' / LinearAdapter(200000000, BitsInteger(32)),
    'SOH_ATT_DET__BAD_ATT_TIMER' / BitsInteger(32),
    'SOH_ATT_DET__BAD_RATE_TIMER' / BitsInteger(32),
    'SOH_ATT_DET__REINIT_COUNT' / BitsInteger(32),
    'SOH_ATT_DET__ATTITUDE_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
    'SOH_ATT_DET__MEAS_ATT_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
    'SOH_ATT_DET__MEAS_RATE_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
    'SOH_ATT_DET__TRACKER_USED' / BitsInteger(8),
)

SOH_ATT_CMD = BitStruct(
    'SOH_ATT_CMD__HR_CYCLE_SAFE_MODE' / BitsInteger(32),
    'SOH_ATT_CMD__ROTISSERIE_RATE' / LinearAdapter(25000, BitsInteger(16)),
    'SOH_ATT_CMD__ADCS_MODE' / Enum(BitsInteger(8), SUN_POINT=0,
                                    FINE_REF_POINT=1, SEARCH_INIT=2,
                                    SEARCHING=3, WAITING=4, CONVERGING=5,
                                    ON_SUN=6, NOT_ACTIVE=7),
    'SOH_ATT_CMD__SAFE_MODE_REASON' / Enum(BitsInteger(8), BOOT=1, COMMAND=2,
                                           ATTITUDE_INVALID=4, TIME_INVALID=8,
                                           ATTITUDE_TIME_INVALID=12,
                                           REFS_INVALID=16),
    'SOH_ATT_CMD__RECOMMEND_SUN_POINT' / Enum(BitsInteger(8), YES=1, NO=0),
)

SOH_RW_DRIVE = BitStruct(
    'SOH_RW_DRIVE__FILTERED_SPEED_RPM1' / LinearAdapter(2.5, BitsInteger(16)),
    'SOH_RW_DRIVE__FILTERED_SPEED_RPM2' / LinearAdapter(2.5, BitsInteger(16)),
    'SOH_RW_DRIVE__FILTERED_SPEED_RPM3' / LinearAdapter(2.5, BitsInteger(16)),
)

SOH_TRACKER = BitStruct(
    'SOH_TRACKER__OPERATING_MODE' / Enum(BitsInteger(8), IDLE=0, INITIALIZE=1,
                                         STARID=2, TRACK=3, PHOTO=4, CAL=5),
    'SOH_TRACKER__STAR_ID_STEP' / Enum(BitsInteger(8), IDLE=0, INITIALIZE=1,
                                       WAITING_FOR_IMAGE1=2,
                                       WAITING_FOR_IMAGE2=3, CALCULATE_RATE=4,
                                       MAKE_UNIT_VECTORS=5, AWAITING_TRISTAR=6,
                                       OK_FOUND_4=7, OK_FOUND_3=8, TIME_OUT=9,
                                       SPARE=10, NO_MATCH=11),
    'SOH_TRACKER__ATT_STATUS' / Enum(BitsInteger(8), OK=0, PENDING=1, BAD=2,
                                     TOO_FEW_STARS=3, QUEST_FAILED=4,
                                     RESIDUALS_TOO_HIGH=5, TOO_CLOSE_TO_EDGE=6,
                                     PIX_AMP_TOO_LOW=7, PIX_AMP_TOO_HIGH=8,
                                     BACKGND_TOO_HIGH=9, TRACK_FAILURE=10,
                                     PIX_SUM_TOO_LOW=11, UNUSED=12,
                                     TOO_DIM_FOR_STARID=13, TOO_MANY_GROUPS=14,
                                     TOO_FEW_GROUPS=15, CHANNEL_DISABLED=16,
                                     TRACK_BLK_OVERLAP=17, OK_FOR_STARID=18,
                                     TOO_CLOSE_TO_OTHER=19, TOO_MANY_PIXELS=20,
                                     TOO_MANY_COLUMNS=21, TOO_MANY_ROWS=22,
                                     OPEN=23, CLOSED=24, RATE_TOO_HIGH=25),
    'SOH_TRACKER__NUM_ATTITUDE_STARS' / BitsInteger(8),
)

SOH_ATT_CTRL = BitStruct(
    'SOH_ATT_CTRL__POSITION_ERROR1' / LinearAdapter(5e8, BitsInteger(32)),
    'SOH_ATT_CTRL__POSITION_ERROR2' / LinearAdapter(5e8, BitsInteger(32)),
    'SOH_ATT_CTRL__POSITION_ERROR3' / LinearAdapter(5e8, BitsInteger(32)),
    'SOH_ATT_CTRL__TIME_INTO_SEARCH' / BitsInteger(16),
    'SOH_ATT_CTRL__WAIT_TIMER' / BitsInteger(16),
    'SOH_ATT_CTRL__SUN_POINT_ANGLE_ERROR' / LinearAdapter(333.3334,
                                                          BitsInteger(16)),
    'SOH_ATT_CTRL__SUN_POINT_STATE' / Enum(BitsInteger(8), SUN_POINT=0,
                                           FINE_REF_POINT=1, SEARCH_INIT=2,
                                           SEARCHING=3, WAITING=4,
                                           CONVERGING=5, ON_SUN=6,
                                           NOT_ACTIVE=7),
)

SOH_MOMENTUM = BitStruct(
    'SOH_MOMENTUM__MOMENTUM_VECTOR_BODY1' / LinearAdapter(5000,
                                                          BitsInteger(16)),
    'SOH_MOMENTUM__MOMENTUM_VECTOR_BODY2' / LinearAdapter(5000,
                                                          BitsInteger(16)),
    'SOH_MOMENTUM__MOMENTUM_VECTOR_BODY3' / LinearAdapter(5000,
                                                          BitsInteger(16)),
    'SOH_MOMENTUM__DUTY_CYCLE1' / BitsInteger(8),
    'SOH_MOMENTUM__DUTY_CYCLE2' / BitsInteger(8),
    'SOH_MOMENTUM__DUTY_CYCLE3' / BitsInteger(8),
    'SOH_MOMENTUM__TORQUE_ROD_MODE1' / Enum(BitsInteger(8), OFF=0, ON_POS=1,
                                            ON_NEG=2, AUTO=3, MEASURED=4,
                                            MODELED=5, DELAYED_AUTO=6,
                                            NO_FIELD_VALID=7),
    'SOH_MOMENTUM__TORQUE_ROD_MODE2' / Enum(BitsInteger(8), OFF=0, ON_POS=1,
                                            ON_NEG=2, AUTO=3, MEASURED=4,
                                            MODELED=5, DELAYED_AUTO=6,
                                            NO_FIELD_VALID=7),
    'SOH_MOMENTUM__TORQUE_ROD_MODE3' / Enum(BitsInteger(8), OFF=0, ON_POS=1,
                                            ON_NEG=2, AUTO=3, MEASURED=4,
                                            MODELED=5, DELAYED_AUTO=6,
                                            NO_FIELD_VALID=7),
    'SOH_MOMENTUM__MAG_SOURCE_USED' / Enum(BitsInteger(8), OFF=0, ON_POS=1,
                                           ON_NEG=2, AUTO=3, MEASURED=4,
                                           MODELED=5, DELAYED_AUTO=6,
                                           NO_FIELD_VALID=7),
    'SOH_MOMENTUM__MOMENTUM_VECTOR_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
)

SOH_CSS = BitStruct(
    'SOH_CSS__SUN_VECTOR_BODY1' / LinearAdapter(10000, BitsInteger(16)),
    'SOH_CSS__SUN_VECTOR_BODY2' / LinearAdapter(10000, BitsInteger(16)),
    'SOH_CSS__SUN_VECTOR_BODY3' / LinearAdapter(10000, BitsInteger(16)),
    'SOH_CSS__SUN_VECTOR_STATUS' / Enum(BitsInteger(8), GOOD=0, COARSE=1,
                                        BAD=2),
    'SOH_CSS__SUN_SENSOR_USED' / BitsInteger(8),
)

SOH_MAG = BitStruct(
    'SOH_MAG__MAG_VECTOR_BODY1' / LinearAdapter(200000000, BitsInteger(16)),
    'SOH_MAG__MAG_VECTOR_BODY2' / LinearAdapter(200000000, BitsInteger(16)),
    'SOH_MAG__MAG_VECTOR_BODY3' / LinearAdapter(200000000, BitsInteger(16)),
    'SOH_MAG__MAG_VECTOR_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
)

SOH_IMU = BitStruct(
    'SOH_IMU__NEW_PACKET_COUNT' / BitsInteger(8),
    'SOH_IMU__IMU_VECTOR_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
)

SOH_CLOCK_SYNC = BitStruct(
    'SOH_CLOCK_SYNC__HR_RUN_COUNT' / BitsInteger(32),
    'SOH_CLOCK_SYNC__HR_EXEC_TIME_MS' / BitsInteger(8),
)

SOH_ANALOGS = BitStruct(
    'SOH_ANALOGS__BOX1_TEMP' / LinearAdapter(200, BitsInteger(16)),
    'SOH_ANALOGS__BUS_VOLTAGE' / LinearAdapter(1000.0, BitsInteger(16)),
    'SOH_ANALOGS__BATTERY_VOLTAGE' / LinearAdapter(500, BitsInteger(16)),
    'SOH_ANALOGS__BATTERY_CURRENT' / LinearAdapter(500, BitsInteger(16)),
)

SOH_TRACKER2 = BitStruct(
    'SOH_TRACKER2__OPERATING_MODE' / Enum(BitsInteger(8), IDLE=0, INITIALIZE=1,
                                          STARID=2, TRACK=3, PHOTO=4, CAL=5),
    'SOH_TRACKER2__STAR_ID_STEP' / Enum(BitsInteger(8), IDLE=0, INITIALIZE=1,
                                        WAITING_FOR_IMAGE1=2,
                                        WAITING_FOR_IMAGE2=3,
                                        CALCULATE_RATE=4,
                                        MAKE_UNIT_VECTORS=5,
                                        AWAITING_TRISTAR=6, OK_FOUND_4=7,
                                        OK_FOUND_3=8, TIME_OUT=9, SPARE=10,
                                        NO_MATCH=11),
    'SOH_TRACKER2__ATT_STATUS' / Enum(BitsInteger(8), OK=0, PENDING=1, BAD=2,
                                      TOO_FEW_STARS=3, QUEST_FAILED=4,
                                      RESIDUALS_TOO_HIGH=5,
                                      TOO_CLOSE_TO_EDGE=6,
                                      PIX_AMP_TOO_LOW=7, PIX_AMP_TOO_HIGH=8,
                                      BACKGND_TOO_HIGH=9, TRACK_FAILURE=10,
                                      PIX_SUM_TOO_LOW=11, UNUSED=12,
                                      TOO_DIM_FOR_STARID=13,
                                      TOO_MANY_GROUPS=14, TOO_FEW_GROUPS=15,
                                      CHANNEL_DISABLED=16,
                                      TRACK_BLK_OVERLAP=17, OK_FOR_STARID=18,
                                      TOO_CLOSE_TO_OTHER=19,
                                      TOO_MANY_PIXELS=20, TOO_MANY_COLUMNS=21,
                                      TOO_MANY_ROWS=22, OPEN=23, CLOSED=24,
                                      RATE_TOO_HIGH=25),
    'SOH_TRACKER2__NUM_ATTITUDE_STARS' / BitsInteger(8),
)

SOH_GPS = BitStruct(
    'SOH_GPS__GPS_LOCK_COUNT' / BitsInteger(16),
    'SOH_GPS__GPS_VALID' / Enum(BitsInteger(8), YES=1, NO=0),
    'SOH_GPS__GPS_ENABLE' / Enum(BitsInteger(8), YES=1, NO=0),
)

SOH_EVENT_CHECK = BitStruct(
    'SOH_EVENT_CHECK__LATCHED_RESP_FIRE_PACK1' / BitsInteger(8),
    'SOH_EVENT_CHECK__LATCHED_RESP_FIRE_PACK2' / BitsInteger(8),
)

SOH_RADIO = BitStruct(
    'SOH_RADIO__SD_MINUTE_CUR' / BitsInteger(32),
    'SOH_RADIO__SD_PERCENT_USED_TOTAL' / BitsInteger(8),
    'SOH_RADIO__SD_OK' / Enum(BitsInteger(8), YES=1, NO=0),
    'SOH_RADIO__SD_FAULT_COUNT' / BitsInteger(8),
    'SOH_RADIO__SDR_TX_TX_FRAMES' / BitsInteger(32),
    'SOH_RADIO__SDR_TX_TEMP' / BitsInteger(8),
    'SOH_RADIO__SDR_TX_COMM_ERROR' / Enum(BitsInteger(8), NO=0, YES=1),
    'SOH_RADIO__SQ_CHANNEL' / BitsInteger(8),
    'SOH_RADIO__SQ_TRAP_COUNT' / BitsInteger(8),
    'SOH_RADIO__SQ_TEMP' / BitsInteger(8),
)

SOH_TRACKER_CTRL = BitStruct(
    'SOH_TRACKER_CTRL__AID_STATUS1' / BitsInteger(8),
    'SOH_TRACKER_CTRL__AID_STATUS2' / BitsInteger(8),
    'SOH_TRACKER_CTRL__STAR_ID_STATUS' / BitsInteger(8)
)

cute_bct_soh = Struct(
    'SOH_L0' / SOH_L0,
    'SOH_COMMAND_TLM' / SOH_COMMAND_TLM,
    'SOH_GENERAL' / SOH_GENERAL,
    'SOH_TIME' / SOH_TIME,
    'SOH_REFS' / SOH_REFS,
    'SOH_ATT_DET' / SOH_ATT_DET,
    'SOH_ATT_CMD' / SOH_ATT_CMD,
    'SOH_RW_DRIVE' / SOH_RW_DRIVE,
    'SOH_TRACKER' / SOH_TRACKER,
    'SOH_ATT_CTRL' / SOH_ATT_CTRL,
    'SOH_MOMENTUM' / SOH_MOMENTUM,
    'SOH_CSS' / SOH_CSS,
    'SOH_MAG' / SOH_MAG,
    'SOH_IMU' / SOH_IMU,
    'SOH_CLOCK_SYNC' / SOH_CLOCK_SYNC,
    'SOH_ANALOGS' / SOH_ANALOGS,
    'SOH_TRACKER2' / SOH_TRACKER2,
    'SOH_GPS' / SOH_GPS,
    'SOH_EVENT_CHECK' / SOH_EVENT_CHECK,
    'SOH_RADIO' / SOH_RADIO,
    'SOH_TRACKER_CTRL' / SOH_TRACKER_CTRL,
)

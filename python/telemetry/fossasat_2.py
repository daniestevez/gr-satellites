#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 jgromes <gromes.jan@gmail.com>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from ..adapters import LinearAdapter
from .fossasat import *

fossasat_2 = Struct(
    'callsign' / Const(b"FOSSASAT-2"),
    'func_id' / FuncId,
    'opt_data_len' / Optional(Int8ul),
    'payload' / Switch(this.func_id, {
        'RESP_PONG': Pong,
        'RESP_REPEATED_MESSAGE': RepeatedMessage,
        'RESP_REPEATED_MESSAGE_CUSTOM': RepeatedMessage,
        'RESP_SYSTEM_INFO': SystemInfo,
        'RESP_PACKET_INFO': PacketInfo,
        'RESP_STATISTICS': Statistics,
        'RESP_FULL_SYSTEM_INFO': FullSystemInfo,
        'RESP_STORE_AND_FORWARD_ASSIGNED_SLOT': StoreAndForwardAssigned,
        'RESP_FORWARDED_MESSAGE': ForwardedMessage,
        'RESP_PUBLIC_PICTURE': CameraPicture,
        'RESP_DEPLOYMENT_STATE': DeploymentState,
        'RESP_CAMERA_STATE': CameraState,
        'RESP_RECORDED_IMU': RecordedIMU,
        'RESP_MANUAL_ACS_RESULT': ManualACSResult,
        'RESP_GPS_LOG': GPSLog,
        'RESP_GPS_LOG_STATE': GPSLogState,
        'RESP_FLASH_CONTENTS': FlashContents,
        'RESP_CAMERA_PICTURE': CameraPicture,
        'RESP_CAMERA_PICTURE_LENGTH': CameraPictureLength,
        'RESP_GPS_COMMAND_RESPONSE': GPSCommandResponse,
        'RESP_ACKNOWLEDGE': Acknowledge,
        }, default=HexDump(GreedyBytes)),
    )

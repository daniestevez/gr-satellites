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
from .fossasat import (
    VoltageValue, CurrentValue, TempValue, FuncId,
    StatsCurrents, StatsVoltages, StatsTemperatures, Pong, RepeatedMessage,
    SystemInfo, PacketInfo, Statistics, StoreAndForwardAssigned,
    ForwardedMessage, CameraPicture, DeploymentState)


SystemInfo = Struct(
    'v_batt' / VoltageValue,
    'i_chrg' / CurrentValue,
    'v_chrg' / VoltageValue,
    'uptime' / Int32ul,
    'power_cfg' / Struct(
        Padding(3),
        'tx_enabled' / Flag,
        'mppt_keep_alive' / Flag,
        'mppt_temp_switch' / Flag,
        'lp_enabled' / Flag,
        'lp_active' / Flag,
        ),
    'reset_ctr' / Int16ul,
    'v_panel_a' / VoltageValue,
    'v_panel_b' / VoltageValue,
    'v_panel_c' / VoltageValue,
    'batt_temp' / TempValue,
    'obc_temp' / TempValue,
    'mcu_temp' / Int8sl,
    )

Statistics = Struct(
    'flags' / BitStruct(
        'has_obc_temp' / Flag,
        'has_batt_temp' / Flag,
        'has_v_panel_c' / Flag,
        'has_v_panel_b' / Flag,
        'has_v_panel_a' / Flag,
        'has_v_batt' / Flag,
        'has_i_chrg' / Flag,
        'has_v_chrg' / Flag,
        ),
    'stats' / Struct(
        'v_chrg' / Optional(If(this._.flags.has_v_chrg, StatsVoltages)),
        'i_chrg' / Optional(If(this._.flags.has_i_chrg, StatsCurrents)),
        'v_batt' / Optional(If(this._.flags.has_v_batt, StatsVoltages)),
        'v_panel_a' / Optional(If(this._.flags.has_v_panel_a, StatsVoltages)),
        'v_panel_b' / Optional(If(this._.flags.has_v_panel_b, StatsVoltages)),
        'v_panel_c' / Optional(If(this._.flags.has_v_panel_c, StatsVoltages)),
        'batt_temp' / Optional(If(this._.flags.has_batt_temp,
                                  StatsTemperatures)),
        'obc_temp' / Optional(If(this._.flags.has_obc_temp,
                                 StatsTemperatures)),
        ),
    )

RecordedSolarCells = Struct(
    'samples' / GreedyRange(
        Struct(
            'v_panel_a' / VoltageValue,
            'v_panel_b' / VoltageValue,
            'v_panel_c' / VoltageValue,
            )
        )
    )

fossasat_1b = Struct(
    'callsign' / Const(b"FOSSASAT-1B"),
    'func_id' / FuncId,
    'opt_data_len' / Optional(Int8ul),
    'payload' / Switch(this.func_id, {
        'RESP_PONG': Pong,
        'RESP_REPEATED_MESSAGE': RepeatedMessage,
        'RESP_REPEATED_MESSAGE_CUSTOM': RepeatedMessage,
        'RESP_SYSTEM_INFO': SystemInfo,
        'RESP_PACKET_INFO': PacketInfo,
        'RESP_STATISTICS': Statistics,
        'RESP_STORE_AND_FORWARD_ASSIGNED_SLOT': StoreAndForwardAssigned,
        'RESP_FORWARDED_MESSAGE': ForwardedMessage,
        'RESP_PUBLIC_PICTURE': CameraPicture,
        'RESP_DEPLOYMENT_STATE': DeploymentState,
        'RESP_RECORDED_SOLAR_CELLS': RecordedSolarCells,
        }, default=HexDump(GreedyBytes)),
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

import datetime

from construct import *
import construct.core
from ..adapters import LinearAdapter, UNIXTimestampAdapter

# Number of sensors
VOLT_SENSORS = 7
CUR_SENSORS = 6
TEMP_SENSORS = 7
IRR_SENSORS = 6

def sensor(context):
    if context._.beacon_id == 'VoltageEvolution':
        return 'voltage'
    if context._.beacon_id == 'CurrentEvolution':
        return 'current'
    if context._.beacon_id == 'TemperatureEvolution':
        return 'temperature'
    if context._.beacon_id == 'IrradianceEvolution':
        return 'irradiance'
    if context._.beacon_id == 'StateOfChargeEvolution':
        return 'state_of_charge'
    idx = context._index
    if idx < VOLT_SENSORS:
        return 'voltage'
    idx -= VOLT_SENSORS
    if idx < CUR_SENSORS:
        return 'current'
    idx -= CUR_SENSORS
    if idx < TEMP_SENSORS:
        return 'temperature'
    return 'irradiance'

VoltOrIrrAdapter = LinearAdapter(1000, Int16ub)
TempAdapter = LinearAdapter(10, Int16ub)

class DeltaTAdapter(Adapter):
#    def _encode(self, obj, context, path = None):
# TODO
    def _decode(self, obj, context, path = None):
        if obj == 0:
            raise construct.core.StreamError
        delta_t = obj
        t1 = context._.last_timestamp
        t2 = t1 - datetime.timedelta(seconds = delta_t - 1 + context._.delta_min_delay)
        if context._.beacon_id != 'CurrentState':
            context._.last_timestamp = t2
        return t2

def set_delta_min_delay(obj, context):
    context.delta_min_delay = 0 if obj == 'CurrentState' else 300
    
def set_last_timestamp(obj, context):
    context.last_timestamp = obj

def set_context(obj, context):
    set_delta_min_delay(obj, context)
    set_last_timestamp(obj, context)

BeaconID = Enum(Int8ub,\
    CurrentState = 0xB0,\
    VoltageEvolution = 0xB1,\
    CurrentEvolution = 0xB2,\
    TemperatureEvolution = 0xB3,\
    IrradianceEvolution = 0xB4,\
    StateOfChargeEvolution = 0xB5)

Timestamp = UNIXTimestampAdapter(Int32sb)

Value = Switch(this.parameter, {'voltage' : VoltOrIrrAdapter, 'irradiance' : VoltOrIrrAdapter, 'temperature' : TempAdapter}, default = Int16ub)

LongData = Struct(\
    Const(b'\x00'),\
    'timestamp' / DeltaTAdapter(Int24ub),\
    'parameter' / Computed(sensor),\
    'value' / Value)

ShortData = Struct(\
    'timestamp' / DeltaTAdapter(Int8ub),\
    'parameter' / Computed(sensor),\
    'value' / Value)

Data = Select(LongData, ShortData)

sat_3cat_1 = Struct(\
    Const(b'\x00'),\
    'beacon_id' / BeaconID * set_delta_min_delay,\
    'sc_time' / Timestamp * set_last_timestamp,\
    'state_of_charge' / Int8ub,\
    'sensor_id' / Int8ub,\
    'data' / GreedyRange(Data))

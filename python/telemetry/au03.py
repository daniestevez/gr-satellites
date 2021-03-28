#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017,2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import datetime

from construct import *

from ..adapters import UNIXTimestampAdapter
from .csp import CSPHeader


Timestamp = UNIXTimestampAdapter(Int32sb)


class BatteryAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        return int((obj - 4420) / 16.0)

    def _decode(self, obj, context, path=None):
        return obj * 16 + 4420


Battery = BatteryAdapter(Int8ub)


class CurrInAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        return int(obj * 255.0 / 2700.0)

    def _decode(self, obj, context, path=None):
        return obj * 2700.0 / 255.0


CurrIn = CurrInAdapter(Int8ub)


class CurrOutAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        return int(obj * 255.0 / 4000.0)

    def _decode(self, obj, context, path=None):
        return obj * 4000.0 / 255.0


CurrOut = CurrOutAdapter(Int8ub)


class Curr3Adapter(Adapter):
    def _encode(self, obj, context, path=None):
        return int(obj * 255.0 / 5500.0)

    def _decode(self, obj, context, path=None):
        return obj * 5500.0 / 255.0


Curr3 = Curr3Adapter(Int8ub)


class Curr5Adapter(Adapter):
    def _encode(self, obj, context, path=None):
        return int(obj * 255.0 / 4500.0)

    def _decode(self, obj, context, path=None):
        return obj * 4500.0 / 255.0


Curr5 = Curr5Adapter(Int8ub)


au03 = Struct(
        'csp_header' / CSPHeader,
        'timestamp' / Timestamp,
        'callsign' / Bytes(6),
        'flags' / Byte,
        'batt_voltage' / Battery,
        'current_in' / CurrIn,
        'current_out' / CurrOut,
        'rail3_current' / Curr3,
        'rail5_current' / Curr5,
        'com_temp' / Int8sb,
        'eps_temp' / Int8sb,
        'bat_temp' / Int8sb
        )

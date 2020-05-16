#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
# 

from construct import *
from ..adapters import *
from .csp import CSPHeader

Timestamp = UNIXTimestampAdapter(Int32sb)

Beacon = Struct(
    'csp_header' / CSPHeader,
    'beacon_counter' / Int16ub,
    'solar_panel_voltage' / LinearAdapter(1/16.0, Int8ub)[3],
    'eps_temp' / AffineAdapter(1, 100, Int8ub)[4],
    'eps_boot_cause' / Int8ub,
    'eps_batt_mode' / Int8ub,
    'solar_panel_current' / LinearAdapter(1/10.0, Int8ub),
    'system_input_current' / LinearAdapter(1/16.0, Int8ub),
    'battery_voltage' / LinearAdapter(1/34.0, Int8ub),
    'radio_PA_temp' / AffineAdapter(1, 100, Int8ub),
    'tx_count' / Int16ub,
    'rx_count' / Int16ub,
    'obc_temp' / AffineAdapter(1, 100, Int8ub)[2],
    'ang_velocity_mag' / Int8ub,
    'magnetometer' / LinearAdapter(1/6.0, Int8sb)[3],
    'main_axis_of_rot' / Int8ub
    )

WODBeacon = Struct(
    'csp_header' / CSPHeader,
    'timestamp' / Timestamp,
    'sp_voltage' / LinearAdapter(1000, Int16ub)[3],
    'sp_regulator_temp' / Int16sb[3],
    'battery_temp' / Int16sb,
    'boot_cause' / Int16ub,
    'battery_mode' / Int16ub,
    'solar_pannel_current' / Int16sb,
    'system_current' / Int16ub,
    'battery_voltage' / LinearAdapter(1000, Int16ub),
    'eps_boot_count' / Int16ub,
    'radio_amplifier_temp' / LinearAdapter(10, Int16sb),
    'tx_count' / Int16ub,
    'rx_count' / Int16ub,
    'last_rx_rf_power' / Int16sb,
    'last_rf_error' / Int16ub,
    'radio_boot_count' / Int16ub,
    'obc_temp' / LinearAdapter(10, Int16sb)[2],
    'gyro' / LinearAdapter(100, Int16sb)[3],
    'mag' / LinearAdapter(10, Int16sb)[3],
    'sp_regulator_current' / Int16ub[3],
    'sp_temp' / LinearAdapter(10, Int16sb)[6],
    'sun_sensor' / Int16sb[6]
    )


class sat_1kuns_pf:
    @staticmethod
    def parse(packet):
        if len(packet) == 138:
            # this is most likely an image packet
            return 
        
        if len(packet) >= 92:
            return WODBeacon.parse(packet)
        else:
            return Beacon.parse(packet)

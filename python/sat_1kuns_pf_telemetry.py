#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 Daniel Estevez <daniel@destevez.net>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from construct import *

from .adapters import *

from .au03_telemetry import Timestamp

Beacon = Struct(
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 Daniel Estevez <daniel@destevez.net>.
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

import struct
from datetime import datetime

beacon_a_len = 207
beacon_b_len = 205

class gomx1_beacon(object):
    def __init__(self, payload):
        if len(payload) < 5:
            raise ValueError("Malformed beacon: too short")

        beacon_time, self.beacon_flags = struct.unpack('>IB', payload[:5])
        beacon = payload[5:]
        self.beacon_time = datetime.utcfromtimestamp(beacon_time)
        if len(beacon) == beacon_a_len:
            self.beacon = gomx1_beacon_a(beacon)
        elif len(beacon) == beacon_b_len:
            self.beacon = "Beacon B (not yet implemented)"
        else:
            raise ValueError("Malformed or unknown beacon")

    def __str__(self):
        return ("""Timestamp:\t{}
Flags:\t\t{}
""".format(self.beacon_time, hex(self.beacon_flags)) + str(self.beacon))

class gomx1_beacon_a(object):
    def __init__(self, payload):
        if len(payload) != beacon_a_len:
            raise ValueError("Malformed beacon of type A")

        self.obc_bootcount, temp1, temp2, panel_temp, self.byte_corr_tot, \
          self.rx, self.rx_err, self.tx, self.last_temp_a, self.last_temp_b, \
          self.last_rssi, self.last_rferr, last_batt_volt, \
          self.last_txcurrent, self.com_bootcount, vboost, vbatt, \
          curout, curin, self.cursun, self.cursys, \
          temp, self.output, self.counter_boot, self.counter_wdt_i2c, \
          self.counter_wdt_gnd, self.bootcause, latchup, \
          battmode, self.average_fps_5min, self.average_fps_1min, \
          self.average_fps_10sec, self.plane_count, self.frame_count, \
          self.last_icao, last_timestamp, self.last_lat, self.last_lon, \
          self.last_altitude, self.crc_corrected, self.gatoss_bootcount, \
          self.gatoss_bootcause, self.hub_temp, self.hub_bootcount, \
          self.hub_reset, self.sense_status, burns, tumblerate, \
          tumblenorm, mag, self.adcs_status, torquerduty, \
          self.ads, self.acs, sunsensor_packed = \
          struct.unpack('>H2h12s4H4h3H6sH12s6s2H12sB3HB12sB4H3I2f2I2HbH2B4s12s8s12sB12s2B8s',\
                        payload)
        self.temp1 = temp1 / 4.0
        self.temp2 = temp2 / 4.0
        self.panel_temp = [x/4.0 for x in struct.unpack('>6h', panel_temp)]
        self.last_batt_volt = last_batt_volt / 100.0
        self.vboost = [x*1e-3 for x in struct.unpack('>3H', vboost)]
        self.vbatt = vbatt * 1e-3
        self.curout = struct.unpack('>6H', curout)
        self.curin = struct.unpack('>3H', curin)
        self.temp = struct.unpack('>6h', temp)
        self.latchup = struct.unpack('>6H', latchup)
        battmode_map = ['normal', 'undervoltage', 'overvoltage']
        try:
            self.battmode = battmode_map[battmode]
        except IndexError:
            self.battmode = 'invalid mode {}'.format(battmode)
        self.last_timestamp = datetime.utcfromtimestamp(last_timestamp)
        self.burns = struct.unpack('>2H', burns)
        self.tumblerate = struct.unpack('>3f', tumblerate)
        self.tumblenorm = struct.unpack('>2f', tumblenorm)
        self.mag = struct.unpack('>3f', mag)
        self.torquerduty = struct.unpack('>3f', torquerduty)
        self.sunsensor_packed = struct.unpack('>8B', sunsensor_packed)

    def __str__(self):
        return ("""Beacon A:
    OBC:
        Boot count:\t{}
        Board temp 1:\t{}ºC
        Board temp 2:\t{}ºC
        Panel temps:\t{}ºC
    COM:
        Bytes corrected by RS:\t{}
        RX packets:\t\t{}
        RX errors:\t\t{}
        TX packets:\t\t{}
        Last temp A:\t\t{}ºC
        Last temp B:\t\t{}ºC
        Last RSSI:\t\t{}dBm
        Last RF error:\t\t{}Hz
        Last battery voltage:\t{}V
        Last TX current:\t{}mA
        Boot count:\t\t{}
    EPS:
        Boost converter voltages:\t{}V
        Battery voltage:\t\t{}V
        Current out:\t\t\t{}mA
        Current in:\t\t\t{}mA
        Boost converter current:\t{}mA
        Battery current:\t\t{}mA
        Temperature sensors:\t\t{}ºC
        Output status:\t\t\t{}
        EPS reboots:\t\t\t{}
        WDT I2C reboots:\t\t{}
        WDT GND reboots:\t\t{}
        Boot cause:\t\t\t{}
        Latchups:\t\t\t{}
        Battery mode:\t\t\t{}
    GATOSS:
        Average FPS 5min:\t{}
        Average FPS 1min:\t{}
        Average FPS 10sec:\t{}
        Plane count:\t\t{}
        Frame count:\t\t{}
        Last ICAO:\t\t{}
        Last timestamp:\t\t{}
        Last latitude:\t\t{}
        Last longitude:\t\t{}
        Last altitude:\t\t{}ft
        CRC corrected:\t\t{}
        Boot count:\t\t{}
        Boot cause:\t\t{}
    HUB:
        Temp:\t\t{}ºC
        Boot count:\t{}
        Reset cause:\t{}
        Switch status:\t{}
        Burn tries:\t{}
    ADCS:
        Tumble rate:\t{}
        Tumble norm:\t{}
        Magnetometer:\t{}
        Status:\t\t{}
        Torquer duty:\t{}
        ADS state:\t{}
        ACS state:\t{}
        Sun sensor:\t{}
        """.format(self.obc_bootcount, self.temp1, self.temp2, self.panel_temp,\
                   self.byte_corr_tot, self.rx, self.rx_err, self.tx, self.last_temp_a,\
                   self.last_temp_b, self.last_rssi, self.last_rferr, self.last_batt_volt,\
                   self.last_txcurrent, self.com_bootcount, self.vboost, self.vbatt,\
                   self.curout, self.curin, self.cursun, self.cursys, self.temp,\
                   hex(self.output), self.counter_boot, self.counter_wdt_i2c, self.counter_wdt_gnd,\
                   self.bootcause, self.latchup, self.battmode, self.average_fps_5min,\
                   self.average_fps_1min, self.average_fps_10sec, self.plane_count,\
                   self.frame_count, hex(self.last_icao), self.last_timestamp, self.last_lat,\
                   self.last_lon, self.last_altitude, self.crc_corrected,\
                   self.gatoss_bootcount, self.gatoss_bootcause, self.hub_temp,\
                   self.hub_bootcount, self.hub_reset, hex(self.sense_status), self.burns,\
                   self.tumblerate, self.tumblenorm, self.mag, hex(self.adcs_status),\
                   self.torquerduty, hex(self.ads), hex(self.acs), self.sunsensor_packed))


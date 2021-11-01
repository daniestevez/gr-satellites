#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2021 @dbusan <https://github.com/dbusan>
# Copyright 2021 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from .ax25 import Header as AX25Header


telem_params = {
    # highR, lowR, offset, scale
    'V_3V3': (10000, 10000, 0, 1),
    'V_Batt': (24500, 10000, 0, 1),
    'V_SolarPanelXX': (25000, 10000, 0, 1),
    'V_SolarPanelYY': (25000, 10000, 0, 1),
    'I_3V3': (0, 10000, 0.25, 0.8),
    'I_Batt': (0, 10000, 0.25, 0.8),
    'I_SolOutXX': (0, 10000, 0.25, 0.8),
    'I_SolInXX': (0, 10000, 0.25, 0.8),
    'I_SolOutYY': (0, 10000, 0.25, 0.8),
    'I_SolInYY': (0, 10000, 0.25, 0.8),
    'I_Magnetorquers0XX': (0, 10000, 0, 0.25),
    'I_Magnetorquers0YY': (0, 10000, 0, 0.25),
    'I_Magnetorquers0ZZ': (0, 10000, 0, 0.25),
    'I_Magnetorquers1XX': (0, 10000, 0, 0.25),
    'I_Magnetorquers1YY': (0, 10000, 0, 0.25),
    'T_SolNegXX': (0, 10000, 67.8 / 160.0, 1.0 / 160.0),
    'T_SolPosXX': (0, 10000, 67.8 / 160.0, 1.0 / 160.0),
    'T_SolNegYY': (0, 10000, 67.8 / 160.0, 1.0 / 160.0),
    'T_SolPosYY': (0, 10000, 67.8 / 160.0, 1.0 / 160.0),
    'T_BHeat12': (0, 10000, 50.0 / 100.0, 1.0 / 100.0),
    'T_BHeat34': (0, 10000, 50.0 / 100.0, 1.0 / 100.0),
}


class BinarAdapter(Adapter):
    def __init__(self, telemetry_id, *args, **kwargs):
        self.telemetry_id = telemetry_id
        return Adapter.__init__(self, *args, **kwargs)

    def _encode(self, obj, context, path=None):
        pass

    def _decode(self, obj, context, path=None):
        telem_obj_params = telem_params[self.telemetry_id]

        highR = telem_obj_params[0]
        lowR = telem_obj_params[1]
        offsetvalue = telem_obj_params[2]
        scaleratio = telem_obj_params[3]

        return generalised_decode(obj, lowR, highR, scaleratio, offsetvalue)


Voltages = Struct(
    'V_3V3' / BinarAdapter('V_3V3', Int16ul),
    'V_Batt' / BinarAdapter('V_Batt', Int16ul),
    'V_SolarPanelXX' / BinarAdapter('V_SolarPanelXX', Int16ul),
    'V_SolarPanelYY' / BinarAdapter('V_SolarPanelYY', Int16ul),
)

Currents = Struct(
    'I_3V3' / BinarAdapter('I_3V3', Int16ul),
    'I_Batt' / BinarAdapter('I_Batt', Int16ul),
    'I_SolOutXX' / BinarAdapter('I_SolOutXX', Int16ul),
    'I_SolInXX' / BinarAdapter('I_SolInXX', Int16ul),
    'I_SolOutYY' / BinarAdapter('I_SolOutYY', Int16ul),
    'I_SolInYY' / BinarAdapter('I_SolInYY', Int16ul),
    'I_Magnetorquers0XX' / BinarAdapter('I_Magnetorquers0XX', Int16ul),
    'I_Magnetorquers0YY' / BinarAdapter('I_Magnetorquers0YY', Int16ul),
    'I_Magnetorquers0ZZ' / BinarAdapter('I_Magnetorquers0ZZ', Int16ul),
    'I_Magnetorquers1XX' / BinarAdapter('I_Magnetorquers1XX', Int16ul),
    'I_Magnetorquers1YY' / BinarAdapter('I_Magnetorquers1YY', Int16ul),
)

Temperatures = Struct(
    'T_SolNegXX' / BinarAdapter('T_SolNegXX', Int16ul),
    'T_SolPosXX' / BinarAdapter('T_SolPosXX', Int16ul),
    'T_SolNegYY' / BinarAdapter('T_SolNegYY', Int16ul),
    'T_SolPosYY' / BinarAdapter('T_SolPosYY', Int16ul),
    'T_BHeat12' / BinarAdapter('T_BHeat12', Int16ul),
    'T_BHeat34' / BinarAdapter('T_BHeat34', Int16ul),
)

Telemetry = Struct(
    'Voltages' / Voltages,
    'Currents' / Currents,
    'Temperatures' / Temperatures,
    'GPSPosn' / Float32l[2],
)

StringMsg = Struct(
    'Message' / Bytes(36)
)


def generalised_decode(obj, lowR, highR, scaleratio, offsetvalue):
    vref = 3.36
    vdiv_ratio = float(lowR)/float(highR+lowR)

    val = (obj/2**16*vref/vdiv_ratio-offsetvalue)/(scaleratio)
    return val


binar1 = Struct(
    'packetlen' / Int8ub,
    'telemetry' / Telemetry,
    'message' / StringMsg,
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2017,2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr
import pmt

class sat_3cat_2:
    def parse(self, packet):
        data = packet[17:].split()
        
        status = {b'1' : 'Survival', b'2' : 'Sun-safe', b'3' : 'Nominal',\
                  b'4' : 'TX', b'5' : 'RX', b'6' : 'Payload', b'7' : 'Payload' }
        adcs = {b'0' : 'auto', b'1' : 'manual'}
        if data[5] == b'0':
            detumbling = 'Detumbling  ({},{},{})nT'.format(float(data[7]), float(data[8]), float(data[9]))
        else:
            detumbling = 'SS-nominal  Sun: ({:.2f},{:.2f},{:.2f})'.format(float(data[7]), float(data[8]), float(data[9]))

        string = status[data[0]] + '  {:.2f}V  {}mA'.format(int(data[1])/1000.0, int(data[2])) + \
        '  EPS: {}ºC   Ant: {}ºC'.format(data[3], data[4]) + \
        '  ADCS ' + adcs[data[6]] + '  ' + detumbling + \
        '  Control: ({:.1e},{:.1e},{:.1e})V'.format(float(data[10]), float(data[11]), float(data[12]))

        return string

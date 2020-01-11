#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017, 2020 Daniel Estevez <daniel@destevez.net>.
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

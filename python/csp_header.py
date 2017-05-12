#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>.
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

import struct

class CSP(object):
    def __init__(self, csp_packet):
        if len(csp_packet) < 4:
            raise ValueError("Malformed CSP packet (too short)")
        csp = struct.unpack("<I", csp_packet[0:4])[0]
        self.priority = (csp >> 30) & 0x3
        self.source = (csp >> 25) & 0x1f
        self.destination = (csp >> 20) & 0x1f
        self.dest_port = (csp >> 14) & 0x3f
        self.source_port = (csp >> 8) & 0x3f
        self.reserved = (csp >> 4) & 0xf
        self.hmac = (csp >> 3) & 1
        self.xtea = (csp >> 2) & 1
        self.rdp = (csp >> 1) & 1
        self.crc = csp & 1

    def __str__(self):
        return ("""CSP header:
        Priority:\t\t{}
        Source:\t\t\t{}
        Destination:\t\t{}
        Destination port:\t{}
        Source port:\t\t{}
        Reserved field:\t\t{}
        HMAC:\t\t\t{}
        XTEA:\t\t\t{}
        RDP:\t\t\t{}
        CRC:\t\t\t{}""".format(
            self.priority, self.source, self.destination, self.dest_port,
            self.source_port, self.reserved, self.hmac, self.xtea, self.rdp,
            self.crc))

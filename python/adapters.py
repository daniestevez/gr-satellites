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
import datetime

class AffineAdapter(Adapter):
    def __init__(self, c, a, *args, **kwargs):
        self.c = c
        self.a = a
        return Adapter.__init__(self, *args, **kwargs)
    def _encode(self, obj, context, path = None):
        return int(round(obj * self.c + self.a))
    def _decode(self, obj, context, path = None):
        return (float(obj) - self.a)/ self.c

class LinearAdapter(AffineAdapter):
    def __init__(self, c, *args, **kwargs):
        return AffineAdapter.__init__(self, c, 0, *args, **kwargs)

class UNIXTimestampAdapter(Adapter):
    def _encode(self, obj, context, path = None):
        return round(obj.timestamp())
    def _decode(self, obj, context, path = None):
        return datetime.datetime.utcfromtimestamp(obj)

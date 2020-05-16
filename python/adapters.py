#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
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

class TableAdapter(Adapter):
    def __init__(self, table, *args, **kwargs):
        self.table = table
        return Adapter.__init__(self, *args, **kwargs)
    def _encode(self, obj, context, path = None):
        try:
            return self.table.index(obj)
        except ValueError:
            return None
    def _decode(self, obj, context, path = None):
        try:
            return self.table[obj]
        except IndexError:
            return None


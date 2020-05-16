#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import subprocess

class FehOpener():
    def __init__(self, fullscreen = True, interval = 1):
        self.fullscreen = fullscreen
        self.interval = interval
    def __params(self):
        p = ['-F'] if self.fullscreen else []
        return p + ['-R', str(self.interval)]
    def open(self, filename):
        subprocess.Popen(['feh'] + self.__params() + [filename],\
                             stdin = subprocess.DEVNULL)

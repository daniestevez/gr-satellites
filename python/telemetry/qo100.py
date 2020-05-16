#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

class qo100:
    @staticmethod
    def parse(packet):
        text = packet[:-2].decode('ascii')
        lines = [text[k:k+64] for k in range(0, len(text), 64)]
        return '\n'.join(lines)

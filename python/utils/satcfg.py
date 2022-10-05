#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from pathlib import Path


def get_cfg(satellite):
    """
    Opens and returns the local configuration for selected satellite
    """
    config_dir = Path.home() / '.gr_satellites'
    config_filename = config_dir / 'sat.cfg'

    if not config_dir.exists():
        Path.mkdir(config_dir)

    if not config_filename.exists():
        return []

    with open(config_filename, encoding='utf-8') as f:
        for row in f:
            sat = row.strip().split(' ')
            if len(sat) > 1 and satellite == sat[0]:
                return sat[1:]
    return []

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 jgromes <gromes.jan@gmail.com>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from ..adapters import *
from .csp import CSPHeader


Beacon = Struct(
    Padding(8),
    'obc_timestamp' / Int32ub,
    'obc_boot_count' / Int32ub,
    'obc_reset_cause' / Int32ub,
    'eps_vbatt' / Int16ub,
    'eps_cursun' / Int16ub,
    'eps_cursys' / Int16ub,
    'eps_temp_bat' / Int16sb,
    'radio_temp_pa' / LinearAdapter(10, Int16sb),
    'radio_tot_tx_count' / Int32ub,
    'radio_tot_rx_count' / Int32ub
    )

Drop = Struct(
    'flag' / Int8ub,
    'chunk' / Int32ub,
    'time' / Int32ub,
    'data' / HexDump(GreedyBytes),
    )

vzlusat_2 = Struct(
    'csp_header' / CSPHeader,
    'cmd' / Hex(Int8ub),
    'payload' / IfThenElse(
        ((this.csp_header.source == 1)
         & (this.csp_header.destination == 26)
         & (this.csp_header.source_port == 18)
         & (this.csp_header.destination_port == 18)),
        Switch(this.cmd, {
            0x56: Beacon,
            0x03: Drop
            }, default=HexDump(GreedyBytes)),
        HexDump(GreedyBytes)
        )
    )

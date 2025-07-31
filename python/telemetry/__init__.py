#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

'''
gr-satellites telemetry definitions

These are telemetry defintions. Most of them are just a construct
object, but in more complex cases, another class supporting the
.parse method and relying on construct is used.
'''

import construct

from .aausat4 import aausat4
from .aepex_70cm import aepex_70cm
from .amicalsat import amicalsat
from .asrtu import asrtu
from .au03 import au03
from .ax25 import ax25
from .binar1 import binar1
from .by02 import by02
from .by70_1 import by70_1
from .cirbe_70cm import cirbe_70cm
from .csp import csp
from .csp import cspv2
from .ctim_70cm import ctim_70cm
from .cute_70cm import cute_70cm
from .delfic3 import delfic3
from .delfipq import delfipq
from .dstar_one import dstar_one
from .erminaz import erminaz
from .eseo import eseo
from .floripasat import floripasat
from .fossasat_1b import fossasat_1b
from .fossasat_2 import fossasat_2
from .funcube import funcube
from .gomx_1 import gomx_1
from .gomx_3 import gomx_3
from .inspiresat_1 import inspiresat_1
from .kr01 import kr01
from .lume import lume
from .mirsat1 import mirsat1
from .mysat1 import mysat1
from .nila import nila
from .picsat import picsat
from .qo100 import qo100
from .quetzal1 import quetzal1
from .sat_1kuns_pf import sat_1kuns_pf
from .sat_3cat_1 import sat_3cat_1
from .sat_3cat_2 import sat_3cat_2
from .smogp import smog1
from .smogp import smogp
from .smogp import smogp_signalling
from .snet import snet
from .suomi100 import suomi100
from .by70_1 import taurus1
from .trisat import trisat
from .tubix20 import tubix20
from .upmsat_2 import upmsat_2
from .vzlusat_2 import vzlusat_2

construct.setGlobalPrintFullStrings(True)

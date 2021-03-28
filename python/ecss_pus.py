#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *


TMSecondaryHeader = BitStruct(
    'version' / BitsInteger(4),
    'time_reference_status' / BitsInteger(4),
    'service_type_id' / BitsInteger(8),
    'message_subtype_id' / BitsInteger(8),
    'message_type_counter' / BitsInteger(16),
    'destination_id' / BitsInteger(16))

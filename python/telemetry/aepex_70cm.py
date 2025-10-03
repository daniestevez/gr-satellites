# Copyright 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024  Daniel Estevez
# <daniel@destevez.net>
# Copyright 2024 The Regents of the University of Colorado
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from construct import BitsInteger, BitStruct, GreedyBytes, If, Struct, Switch
from .ax25 import Header

from .aepex_sw_stat import aepex_sw_stat

PrimaryHeader = BitStruct(
    'VERSION' / BitsInteger(3),
    'TYPE' / BitsInteger(1),
    'SEC_HDR_FLAG' / BitsInteger(1),
    'PKT_APID' / BitsInteger(11),
    'SEQ_FLGS' / BitsInteger(2),
    'SEQ_CTR' / BitsInteger(14),
    'PKT_LEN' / BitsInteger(16),
)

SecondaryHeader = BitStruct(
    'SHCOARSE' / BitsInteger(32),
    'SHFINE' / BitsInteger(16)
)

aepex_70cm = Struct(
    'ax25_header' / Header,
    'primary_header' / PrimaryHeader,
    'secondary_header' / If(
        lambda c: c.primary_header.SEC_HDR_FLAG,
        SecondaryHeader
    ),
    'packet' / Switch(
        lambda c: c.primary_header.PKT_APID,
        {
            0x01: aepex_sw_stat
        },
        default=GreedyBytes
    )

)

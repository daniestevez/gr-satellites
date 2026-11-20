#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
from gnuradio import gr, blocks
import numpy as np
import pmt


def use_message_block(block, data_in):
    """
    Send a list of input messages 'data_in' through the GNU Radio block 'dut'.

    Returns a list of output messages.
    """
    tb = gr.top_block()
    dbg = blocks.message_debug()
    tb.msg_connect((block, 'out'), (dbg, 'store'))

    for idx, frame in enumerate(data_in):
        pdu = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(frame), frame))
        block.to_basic_block()._post(pmt.intern('in'), pdu)
    block.to_basic_block()._post(
        pmt.intern('system'),
        pmt.cons(pmt.intern('done'), pmt.from_long(1)))

    tb.start()
    tb.wait()

    data_out = [pmt.u8vector_elements(pmt.cdr(dbg.get_message(idx)))
                for idx in range(dbg.num_messages())]
    return data_out

# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later

from itertools import batched, chain

from gnuradio import gr
import pmt

from .mobitex_fec import decode, Status, unpack_2b


class mobitex_fec(gr.basic_block):
    """
    Block to perform error-correction on Mobitex data blocks.

    # Input
    PDU with encoded Mobitex data block (20 * 12 bits)

    # Output
    PDU with decoded Mobitex data block (20 * 8 bits)

    Output Tags:
    - corrected_errors (int): Number of corrected bit errors
    - uncorrected_errors (int): Number of uncorrectable bit errors
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='mobitex_fec',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        meta = pmt.car(msg_pmt)
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return

        block = pmt.u8vector_elements(msg)

        if len(block) != 30:
            print(
                '[ERROR] Received invalid Mobitex data block, '
                f'expected 30 bytes (got {len(block)} bytes).'
            )
            return

        codewords = chain(*[
            unpack_2b(bytes(item)) for item in batched(block, n=3)
        ])

        packet_out = []
        errors_corrected = 0
        errors_uncorrected = 0

        for codeword in codewords:
            corrected, _, status = decode(codeword)
            packet_out.append(corrected)

            if status == Status.NO_ERROR:
                pass
            elif status == Status.ERROR_CORRECTED:
                errors_corrected += 1
            elif status == Status.ERROR_UNCORRECTABLE:
                errors_uncorrected += 1

        meta = pmt.dict_add(
            meta,
            pmt.intern('corrected_errors'),
            pmt.from_long(errors_corrected),
        )
        meta = pmt.dict_add(
            meta,
            pmt.intern('uncorrected_errors'),
            pmt.from_long(errors_uncorrected),
        )
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(meta, pmt.init_u8vector(len(packet_out), packet_out)))

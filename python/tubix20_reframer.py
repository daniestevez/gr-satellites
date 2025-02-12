# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gnuradio import gr
import numpy as np
import pmt

from .check_eseo_crc import crc16_ccitt_zero as crc16_ccitt_zero


class tubix20_reframer(gr.basic_block):
    """
    Input:
        PDUs with decoded mobitex data blocks.
        Each PDU must have a 'block id' tag.
        The first PDU must have additionally
            - 'num_blocks' tag: Number of blocks for this frame
            - 'frame_header' tag: Header of this frame (11 bytes)
                - 2 control bytes
                - 1 control bytes FEC
                - 6 callsign bytes
                - 2 callsign CRC bytes
    Output:
        PDUs with Tubix20 "Master Frames", e.g. used for TechnoSat, Beesat-9, TUBIN
        - master frame header
            - 2 control bytes
            - 6 callsign bytes
            - 2 callsign CRC bytes
        - master frame body
            - N x 18 bytes
        - master frame footer
            - 1 byte "ground station quality byte"
            - 4 bytes "error marker"
            - 1 byte "ground station TNC temperature"

    References:
    [1] TechnoSat_TUBIN_Telemetry_Format - https://www.static.tu.berlin/fileadmin/www/10002275/Amateur_Radio/TechnoSat_Telemetry_Format.ods
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='tubix20_reframer',
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))
        self.reset()

    def reset(self):
        self.num_blocks = 0
        self.frame_header = None
        self.control_bit_errors = None
        self.callsign_bit_errors = None
        self.blocks = {}
        self.block_bit_errors = {}

    def handle_msg(self, msg_pmt):
        meta = pmt.car(msg_pmt)
        tags = pmt.to_python(meta)

        if tags['block_id'] == 0:
            if len(self.blocks) != 0:
                print('ERROR: Received new block 0 while there are still unhandled blocks in the buffer.')
                # Discard partial frame
                self.reset()

            self.num_blocks = tags['num_blocks']
            self.frame_header = tags['frame_header']
            self.control_bit_errors = tags['control_bit_errors']
            self.callsign_bit_errors = tags['callsign_bit_errors']

        packet = pmt.u8vector_elements(pmt.cdr(msg_pmt))

        self.blocks[tags['block_id']] = packet
        self.block_bit_errors[tags['block_id']] = tags['block_bit_errors']

        if tags['block_id'] + 1 == self.num_blocks:
            if (len(self.blocks) != self.num_blocks) or (self.frame_header is None):
                print('ERROR: Unexpected number of data blocks, discard partial frame.')
                return

            self.publish_frame()
            self.reset()

    def error_code_bytes(self):
        """
        For each block, check the CRC-16CCITT of the 18 data bytes against the 2 CRC bytes

        > This errorcode is a 32-bit bit-field that indicates which blocks are invalid.
        > The bits that are set indicate an invalid block.
        > The errorcode is in little-endian format,
        > so the bit number 0 of the fist byte of the error code corresponds to the first data block and so on.

        Returns the errorcode.
        """
        error_code = 0
        for block_id, block in self.blocks.items():
            crc = bytes(block[18:])
            computed_crc = crc16_ccitt_zero(block[:18]).to_bytes(length=2)

            if crc != computed_crc:
                error_code |= (1 << block_id)  # Set bit for invalid block
            pass
        error_code_bytes = error_code.to_bytes(4, byteorder='little')
        return error_code_bytes

    def publish_frame(self):
        packet_out = []

        packet_out.extend(self.frame_header[:2])      # Control Bytes
        packet_out.extend(self.frame_header[3:3 + 6]) # Callsign
        packet_out.extend(self.frame_header[9:9 + 2]) # Callsign CRC

        for i in range(self.num_blocks):
            packet_out.extend(self.blocks[i][:18])    # Data Blocks

        packet_out.extend([0xAA])                     # dummy value
        packet_out.extend(
            list(self.error_code_bytes())             # "error code" bytes
        )
        packet_out.extend([0xBB])                     # dummy value

        meta = pmt.make_dict()
        meta = pmt.dict_add(
            meta,
            pmt.intern('control_bit_errors'),
            pmt.from_long(self.control_bit_errors),
        )
        meta = pmt.dict_add(
            meta,
            pmt.intern('callsign_bit_errors'),
            pmt.from_long(self.callsign_bit_errors),
        )
        meta = pmt.dict_add(
            meta,
            pmt.intern('block_bit_errors'),
            pmt.to_pmt(sum(self.block_bit_errors.values())),
        )
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(meta, pmt.init_u8vector(len(packet_out), packet_out)))

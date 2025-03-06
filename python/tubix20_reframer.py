# Copyright 2025 Fabian P. Schmidt <kerel@mailbox.org>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""
References:
[1]: TechnoSat_TUBIN_Telemetry_Format
     <https://www.static.tu.berlin/fileadmin/www/10002275/
     Amateur_Radio/TechnoSat_Telemetry_Format.ods>
[2]: <https://destevez.net/2016/09/some-notes-on-beesat-and-mobitex-nx/>
"""
from gnuradio import gr
import pmt

from .check_eseo_crc import crc16_ccitt_zero as crc16_ccitt_zero


class tubix20_reframer(gr.basic_block):
    """
    Input:
        PDUs with decoded mobitex data blocks.
        Each PDU must have a 'block id' tag.
        The first PDU must have the following additional tags:
            - 'num_blocks' tag: Number of blocks for this frame
            - 'frame_header' tag: Header of this frame (typically 11 bytes)
                - 2 control bytes
                - 1 control bytes FEC
                - 6 callsign bytes
                - 2 callsign CRC bytes
    Output:
        PDUs with Tubix20 "Master Frames"
        - master frame header (typically 10 bytes)
            - 2 control bytes
            - 6 callsign bytes
            - 2 callsign CRC bytes
        - master frame body
            - N x 18 bytes
        - master frame appendix
            - 1 byte "ground station quality byte"
            - 4 bytes "error marker"
            - 1 byte "ground station TNC temperature"
    """
    bytemap = {
        'control_bytes': slice(0, 2),
        'control_bytes_crc': slice(2, 3),
        'callsign': slice(3, 9),
        'callsign_crc': slice(9, 11),
    }

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
        self.num_blocks_expected = 0
        self.frame_header = None

        self.block0_meta = None
        self.blocks = {}
        self.tags = {}

        self.timestamp = None

    def handle_msg(self, msg_pmt):
        meta = pmt.car(msg_pmt)
        packet = pmt.u8vector_elements(pmt.cdr(msg_pmt))
        tags = pmt.to_python(meta)

        # Reset state on block 0
        if tags['block_id'] == 0:
            if len(self.blocks) != 0:
                print('ERROR: Received new block 0 while there are still '
                      'unhandled blocks in the buffer.')
                # Discard partial frame
                self.reset()

            self.num_blocks_expected = tags['num_blocks']
            self.frame_header = tags['frame_header']

            meta = pmt.dict_delete(meta, pmt.intern('block_id'))
            meta = pmt.dict_delete(meta, pmt.intern('frame_header'))
            meta = pmt.dict_delete(meta, pmt.intern('crc_valid'))
            meta = pmt.dict_delete(meta, pmt.intern('corrected_errors'))
            meta = pmt.dict_delete(meta, pmt.intern('uncorrected_errors'))
            self.block0_meta = meta

        # Store in buffer
        self.blocks[tags['block_id']] = packet
        self.tags[tags['block_id']] = tags

        if tags['block_id'] == self.num_blocks_expected - 1:
            if (
                (len(self.blocks) != self.num_blocks_expected) or
                (self.frame_header is None)
            ):
                print('ERROR: Unexpected number of data blocks, discard '
                      'partial frame.')
                return

            self.publish_frame()
            self.reset()

    def error_code_bytes(self):
        """
        Returns the errorcode.

        > This errorcode is a 32-bit bit-field that indicates which blocks
        > are invalid. The bits that are set indicate an invalid block.
        > The errorcode is in little-endian format, so the bit number 0 of
        > the fist byte of the error code corresponds to the first data block
        > and so on.
        """
        error_code = 0
        for block_id, tags in self.tags.items():
            if not tags['crc_valid']:
                error_code |= (1 << block_id)  # Set bit for invalid block
            pass
        error_code_bytes = error_code.to_bytes(4, byteorder='little')
        return error_code_bytes

    def prepare_frame(self):
        packet_out = []

        # note: Based on convention,
        #       control_bytes_crc IS NOT added to the master frame header,
        #       but callsign_crc IS added to the master frame header.
        packet_out.extend(self.frame_header[self.bytemap['control_bytes']])
        packet_out.extend(self.frame_header[self.bytemap['callsign']])
        packet_out.extend(self.frame_header[self.bytemap['callsign_crc']])

        for i in range(len(self.blocks)):
            packet_out.extend(self.blocks[i])

        packet_out.extend([0xAA])
        packet_out.extend(list(self.error_code_bytes()))
        packet_out.extend([0xBB])

        return packet_out

    def publish_frame(self):
        packet_out = self.prepare_frame()

        num_blocks_correct = sum(
            [1 for tags in self.tags.values() if tags['crc_valid']])
        num_corrected_errors = sum(
            [tags['corrected_errors'] for tags in self.tags.values()])
        num_uncorrected_errors = sum(
            [tags['uncorrected_errors'] for tags in self.tags.values()])

        meta = pmt.dict_add(
            self.block0_meta,
            pmt.intern('num_blocks_correct'),
            pmt.from_long(num_blocks_correct),
        )
        meta = pmt.dict_add(
            meta,
            pmt.intern('num_corrected_errors'),
            pmt.from_long(num_corrected_errors),
        )
        meta = pmt.dict_add(
            meta,
            pmt.intern('num_uncorrected_errors'),
            pmt.from_long(num_uncorrected_errors),
        )
        self.message_port_pub(
            pmt.intern('out'),
            pmt.cons(meta, pmt.init_u8vector(len(packet_out), packet_out)))

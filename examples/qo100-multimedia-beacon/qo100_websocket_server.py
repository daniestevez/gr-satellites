#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2022 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import asyncio
import functools
import logging
import websockets


async def ws_recv_alive(websocket):
    async for message in websocket:
        pass


async def ws_send_data(websocket, queue):
    while True:
        item = await queue.get()
        # For some reason we need to add 3 bytes before
        # the payload
        await websocket.send(b'\x00\x00\x00' + item)


async def tcp_client(queue):
    port = 52001
    logging.info(
        'connecting to GNU Radio flowgraph at TCP port %d', port)
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', port)
    logging.info('connection to flowgraph established')
    while True:
        packet = await reader.read(221)
        packet_type = packet[1] & 0xf
        # packet_type == 8 corresponds to external data
        if packet_type != 8:
            continue
        payload = packet[2:]
        payload_type = payload[0]
        if payload_type not in [0, 1, 2, 3]:
            # unknown payload type
            continue
        if payload_type in [1, 3]:
            payload = payload[:1] + repack_8to6(payload[1:])
        await queue.put(payload)


async def handle_file(reader, writer, queue):
    max_len = 2**20
    data = await reader.read(max_len)
    logging.info('received new bulletin file')
    await queue.put(b'\x10' + data)


async def tcp_file_server(queue):
    port = 52002
    server = await asyncio.start_server(
        functools.partial(handle_file, queue=queue),
        '127.0.0.1', port)
    logging.info('starting TCP file server at port %d', port)
    async with server:
        await server.serve_forever()


def repack_8to6(data):
    """Repacks data from 8 bits/byte to 6 bits/byte"""
    out = bytearray()
    sby = 0
    sbi = 0
    dbi = 0
    byte = 0
    while True:
        bit = (data[sby] >> sbi) & 1
        byte |= bit << dbi
        sbi += 1
        if sbi == 8:
            sbi = 0
            sby += 1
            if sby == len(data):
                return bytes(out)
        dbi += 1
        if dbi == 6:
            dbi = 0
            out.append(byte)
            byte = 0


async def handle(websocket):
    logging.info('client connected')
    queue = asyncio.Queue()
    await asyncio.gather(
        tcp_client(queue),
        tcp_file_server(queue),
        ws_send_data(websocket, queue),
        ws_recv_alive(websocket))


async def main():
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        level=logging.INFO)
    logging.info('starting QO-100 multimedia beacon WebSocket server')
    async with websockets.serve(handle, 'localhost', 40134):
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())

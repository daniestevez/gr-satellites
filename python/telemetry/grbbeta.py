#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telemetry parser for GRBBeta (HA2GRB)
# UHF/VHF AX.25 beacon, ASCII messages, and digipeater/ground-station frames
#

from construct import *
from .ax25 import Header

_RawFrame = Struct(
    'header' / Header,
    'info' / GreedyBytes,
)


class GRBBeta:
    """Telemetry parser for GRBBeta (HA2GRB)"""

    def parse(self, packet):
        try:
            data = _RawFrame.parse(packet)
        except Exception:
            return None

        src = data.header.addresses[-1].callsign
        dst = data.header.addresses[0].callsign
        info = data.info

        try:
            text = info.decode('ascii', errors='replace').rstrip('\x00')
        except Exception:
            text = None

        out = []
        parts = text.split(',') if text else []

        if text and parts[0] in ('U', 'V') and len(parts) >= 14:
            band = 'UHF' if parts[0] == 'U' else 'VHF'
            out.append(f'{src} -> {dst}')
            try:
                out.append(f'GRBBeta {band} beacon')
                out.append('-' * 40)
                out.append(f'Uptime since reset   : {int(parts[1])} s')
                out.append(f'Uptime total         : {int(parts[2])} s')
                out.append(f'Radio boot count     : {parts[3]}')
                out.append(f'RF reset count       : {parts[4]}')
                out.append(
                    f'Radio MCU temp       : {int(parts[5])*0.01:.2f} degC')
                out.append(
                    f'RF chip temp         : {int(parts[6])*0.01:.2f} degC')
                out.append(
                    f'PA temp              : {int(parts[7])*0.01:.2f} degC')
                out.append(f'Digipeater fwd count : {parts[8]}')
                out.append(f'Last digipeat user   : {parts[9] or "(none)"}')
                out.append(f'RX data packets      : {parts[10]}')
                out.append(f'TX data packets      : {parts[11]}')
                out.append(
                    f'RSSI actual          : '
                    f'{int(parts[12])/2 - 134:.1f} dBm')
                out.append(
                    f'RSSI carrier         : '
                    f'{int(parts[13])/2 - 134:.1f} dBm')
            except (ValueError, IndexError):
                out.append('(malformed beacon fields)')
                out.append(text)
        elif text and text.isprintable():
            out.append(f'{src} -> {dst}')
            out.append('GRBBeta message')
            out.append('-' * 40)
            out.append(text)
        else:
            out.append('GRBBeta unknown/digipeater frame')
            out.append('-' * 40)
            out.append(f'{len(info)} raw bytes')

        out.append('')
        return '\n'.join(out)


grbbeta = GRBBeta()
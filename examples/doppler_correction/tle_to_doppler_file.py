#!/usr/bin/env python3

# Copyright 2023 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import argparse
import datetime

import numpy as np
import scipy.constants
import skyfield.api
from skyfield.api import wgs84, EarthSatellite


DAY_S = 24 * 3600


ts = skyfield.api.load.timescale()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Generates a Doppler file from a TLE')
    parser.add_argument(
        '--tle-file', required=True,
        help='Input TLE file')
    parser.add_argument(
        '--output-file', required=True,
        help='Ouptut text file')
    parser.add_argument(
        '--unix-timestamp', required=True, type=float,
        help='Initial UNIX timestamp')
    parser.add_argument(
        '--time-step', default=0.1, type=float,
        help='Time step (seconds) [default=%(default)r]')
    parser.add_argument(
        '--duration', default=15*60, type=float,
        help='Doppler file duration (seconds) [default=%(default)r]')
    parser.add_argument(
        '--f-carrier', required=True, type=float,
        help='Carrier frequency (Hz)')
    parser.add_argument(
        '--uplink', action='store_true',
        help=('Generate Doppler file for uplink correction '
              '(inverts sign of Doppler)'))
    parser.add_argument(
        '--lat', required=True, type=float,
        help='Groundstation latitude (degrees)')
    parser.add_argument(
        '--lon', required=True, type=float,
        help='Groundstation longitude (degrees)')
    parser.add_argument(
        '--alt', default=0.0, type=float,
        help='Groundstation altitude (meters) [default=%(default)r]')
    return parser.parse_args()


def main():
    args = parse_args()
    with open(args.tle_file) as f:
        lines = f.readlines()
    if len(lines) == 3:
        # drop first line (contains the name of the satellite)
        lines = lines[1:]
    if len(lines) != 2:
        raise RuntimeError('TLE file must have either 2 or 3 lines')
    unix_epoch = datetime.datetime(1970, 1, 1, tzinfo=skyfield.api.utc)
    satellite = EarthSatellite(lines[0], lines[1], 'satellite', ts)
    t0 = unix_epoch + datetime.timedelta(seconds=args.unix_timestamp)
    t0 = ts.from_datetime(t0.replace(tzinfo=skyfield.api.utc))
    t = t0 + np.arange(0, (args.duration + args.time_step) / DAY_S,
                       args.time_step / DAY_S)
    t = ts.tai_jd([s.tai for s in t])
    groundstation = wgs84.latlon(
        args.lat, args.lon, args.alt)
    topocentric = (satellite - groundstation).at(t)
    range_rate = topocentric.frame_latlon_and_rates(
        groundstation)[5].km_per_s * 1e3
    doppler = - range_rate / scipy.constants.c * args.f_carrier
    if args.uplink:
        doppler = -doppler
    with open(args.output_file, 'w') as output_file:
        for s, f in zip(t, doppler):
            s = (s.utc_datetime() - unix_epoch).total_seconds()
            print(f'{s}\t{f}', file=output_file)


if __name__ == '__main__':
    main()

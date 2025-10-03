#!/usr/bin/env python3

# Copyright 2023,2025 Daniel Estevez <daniel@destevez.net>
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
        description='Generates a delay file from a TLE')
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
        help='Delay file duration (seconds) [default=%(default)r]')
    parser.add_argument(
        '--delay-offset', default=0, type=float,
        help='Offset to add to the delay (seconds) [default=%(default)r]')
    parser.add_argument(
        '--invert-delay', action='store_true',
        help=('Invert sign, to use for correction instead of simulation '
              '(requires --delay-offset to avoid negative delays)'))
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
    satellite = EarthSatellite(lines[0], lines[1], 'satellite', ts)
    t0 = ts.from_datetime(
        datetime.datetime.fromtimestamp(args.unix_timestamp, datetime.timezone.utc)
    )
    t = t0 + np.arange(0, (args.duration + args.time_step) / DAY_S,
                       args.time_step / DAY_S)
    t = ts.tai_jd([s.tai for s in t])
    groundstation = wgs84.latlon(
        args.lat, args.lon, args.alt)
    topocentric = (satellite - groundstation).at(t)
    range_m = topocentric.altaz()[2].km * 1e3
    delay = range_m / scipy.constants.c
    with open(args.output_file, 'w') as output_file:
        for s, f in zip(t, delay):
            s = s.utc_datetime().timestamp()
            print(f'{s}\t{f}', file=output_file)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

"""Plots SMOG-P/ATL-1 spectrum data previously saved to a file"""

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import pathlib

def usage():
    print(f'Usage: sys.argv[0] input_file', file = sys.stderr)
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()
    
    filename = sys.argv[1]
    m = re.match('spectrum_start_(?P<start>\\d+?)_step_(?P<step>\\d+?)_rbw_\\d+_measid_(?P<measid>\\d+?)\Z', pathlib.Path(filename).name)
    start = int(m.group('start'))
    step = int(m.group('step'))
    measid = int(m.group('measid'))

    data = np.fromfile(filename, dtype = 'uint8')
    freq = start + step * np.arange(data.size)

    plt.figure()
    plt.plot(freq * 1e-6, data)
    plt.title(f'Spectrum measurement {measid}')
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('PSD')
    plt.savefig(pathlib.Path(filename).parent / f'spectrum_{measid}.png')

if __name__ == '__main__':
    main()

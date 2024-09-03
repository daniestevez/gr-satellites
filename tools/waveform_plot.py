#!/usr/bin/env python
import argparse
from os.path import basename

import matplotlib.pyplot as plt
import numpy as np


def parse_args():
    p = argparse.ArgumentParser(
        description='waveform_plot.py - Plot float32 waveforms.',
        prog='waveform_plot.py waveform.f32',
        argument_default=argparse.SUPPRESS)
    p.add_argument('waveform', help=argparse.SUPPRESS)
    p.add_argument('--lines', action='store_true',
                   help='Draw with lines only, faster rendering of large files.')
    return p.parse_args()


def waveform_plot(a: dict):
    assert 'waveform' in a, "waveform is not set"
    try:
        x = np.fromfile(a['waveform'], dtype='float32')
    except FileNotFoundError:
        print(f"File {a['waveform']} not found")
        return 1
    print(f"Plotting {a['waveform']}")

    fig, (sig, hst) = plt.subplots(1, 2, sharey=True, figsize=(10, 6), tight_layout=True,
                                   gridspec_kw={'width_ratios': [0.8, 0.2]})
    plt.yticks(np.arange(-5, 5, 0.1), minor=True)
    fig.subplots_adjust(hspace=0, wspace=0)

    sig.set_title(basename(a['waveform']), loc='left')
    sig.grid(axis='y', alpha=0.5)
    sig.grid(axis='y', which='minor', alpha=0.1)

    hst.set_title('histogram', loc='left')
    hst.tick_params(which='both', labelright=True, left=False, right=True)
    hst.grid(axis='y', alpha=0.5)
    hst.grid(axis='y', which='minor', alpha=0.1)

    if 'lines' in a:  # faster rendering of large files
        sig.plot(x, linestyle='-', linewidth=0.2)
    else:  # line with dots, histogram
        sig.plot(x, linestyle='-', marker='.', markersize=1.0, linewidth=0.2)
        hst.hist(x, density=True, bins=1000, orientation='horizontal')

    plt.show()


if __name__ == "__main__":
    waveform_plot(vars(parse_args()))

#!/usr/bin/env python3

import yaml
import satellites
import satellites.core as c
from gnuradio import gr, blocks
import sys
import signal
from pathlib import Path

class top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, 'Top block')

        with open(Path(satellites.__path__[0]) / 'satyaml' / '1KUNS-PF.yml') as f:
            sat = yaml.safe_load(f.read())

        self.flowgraph = c.gr_satellites_flowgraph(sat, samp_rate = 48000)
        self.wavfile = blocks.wavfile_source(sys.argv[1], False)
        self.connect(self.wavfile, self.flowgraph)

def main():
    tb = top_block()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()
        
if __name__ == '__main__':
    main()


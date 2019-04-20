#!/usr/bin/env python3

import numpy as np
import subprocess
import sys

def print_usage():
    print(f'Usage {sys.argv[0]} <jy1sat_frames.bin> <output_path>')

def seqnum(packet):
    return packet[3]*256 + packet[4]

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read 256 byte frames
    x = np.fromfile(input_file, dtype='uint8').reshape((-1,256))

    # Filter out by frame id and trim to payload
    x = x[((x[:,0] == 0xe0) | (x[:,0] == 0xe1)) & (x[:,1] == 0x10), 56:]

    # Filter SSDV packets
    x = x[(x[:,0] == 0x55) & (x[:,1] == 0x68), :]
    ids = set(x[:,2])
    
    for i in ids:
        l = list(x[x[:,2]==i,:])
        l.sort(key=seqnum)
        ssdv = '{}_{}.ssdv'.format(output_file, i)
        jpeg = '{}_{}.jpg'.format(output_file, i)
        np.array(l).tofile(ssdv)
        print('Calling SSDV decoder for image {}'.format(hex(i)))
        subprocess.call(['ssdv', '-d', '-J', ssdv, jpeg])
        print()

if __name__ == '__main__':
    main()

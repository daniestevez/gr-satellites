#!/bin/sh

grcc apps/hierarchical/ccsds_descrambler.grc

for file in apps/hierarchical/*.grc
do grcc $file
done

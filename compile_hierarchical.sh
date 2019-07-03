#!/bin/sh

grcc apps/hierarchical/ccsds_descrambler.grc

for file in apps/hierarchical/*.grc
do grcc $file
done

grcc apps/satrevolution/swiatowid_custom.grc
grcc apps/satrevolution/swiatowid_aprs.grc


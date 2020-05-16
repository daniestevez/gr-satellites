# gr-satellites

gr-satellites is a GNU Radio out-of-tree module encompassing a collection of
telemetry decoders that supports many different Amateur satellites. This
open-source project started in 2015 with the goal of providing telemetry
decoders for all the satellites that transmit on the Amateur radio bands.

It supports most popular protocols, such as AX.25, the GOMspace NanoCom U482C
and AX100 modems, an important part of the CCSDS stack, the AO-40 protocol used
in the FUNcube satellites, and several ad-hoc protocols used in other
satellites.

This out-of-tree module can be used to decode frames transmitted from most
Amateur satellites in orbit, performing demodulation, forward error correction,
etc. Decoded frames can be saved to a file or displayed in hex format. For some
satellites the telemetry format definition is included in gr-satellites, so the
decoded telemetry frames can be printed out as human-readable values such as bus
voltages and currents. Additionally, some satellites transmit files such as JPEG
images. gr-satellites can be used to reassemble these files and even display the
images in real-time as they are being received.

gr-satellites can be used as a set of building blocks to implement decoders for
other satellites or other groundstation solutions. Some of the low level blocks
in gr-satellites are also useful for other kinds RF communications protocols.

## Documentation

gr-satellites [documentation](https://gr-satellites.readthedocs.io/) is hosted in
[reathedocs.io](https://readthedocs.io/).

## Branches and releases

There are currently three development branches of gr-satellites:

* `maint-3.7` Compatible with GNU Radio 3.7 only. No future development will be
  done on this branch. Perhaps important changes, such as very popular
  satellites, will be backported from the `maint-3.8` branch.

* `maint-3.8` Compatible with GNU Radio 3.8 only. Future development is being
  doing in this branch, adding support to new satellites as they get
  launched. If contributing to gr-satellites, please send pull requests to
  `maint-3.8` if in doubt.

* `next` Branch where a large refactor of gr-satellites bringing important
  changes is being done. Active development is happening, but there are still
  several months of until the `next` branch is fully usable.

Starting in 2020, `master` is set equal to `maint-3.8` (before this, it was set
equal to `maint-3.7`).

Regarding the numbered releases, the `1.x.y` series is used for stable releases
on the `maint-3.7` branch (and so, releases supporting GNU Radio 3.7), the
`2.x.y` series is used for stable releases on the `maint-3.8` (and so, releases
supporting GNU Radio 3.8), and alpha releases are done on the `next` branch
showcasing some of the latest developments.

## Installation

The installation procedure of gr-satellites is roughly the usual of a GNU Radio
out-of-tree module. Detailed instructions about the required dependencies and
how to build and install gr-satellites are given in the
[documentation](https://gr-satellites.readthedocs.io/).

## Support

Support for gr-satellites is handled only through
[Github issues](https://github.com/daniestevez/gr-satellites/issues)
so that the whole community can benefit, rather than through private
channels such as email. Please understand this when asking for support.

## Satellite teams

Satellite teams interested in using gr-satellites for you groundstation
solution, please read
[this note](https://github.com/daniestevez/gr-satellites/blob/master/satellite_teams.md),
especially if you will be using Amateur radio spectrum.

## CCSDS TM and TC Space Datalink and SpacePacket blocks

Athanasios Theocharis made under ESA Summer of Code in Space 2019 a collection
of blocks covering several CCSDS blue books. The documentation for this blocks
can be found in
[CCSDS_README.md](https://github.com/daniestevez/gr-satellites/blob/master/CCSDS_README.md).

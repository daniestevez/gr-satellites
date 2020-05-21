# gr-satellites

TESTING PULL REQUEST BUILDBOT FROM ANOTHER ACCOUNT

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

## Releases and branches

Currently there are the following series of releases in the history of
gr-satellites:

* `v3.x.y` is the result of a large refactor that introduces a lot of
  new functionality and improvements. The refactore started on September
  2019 and was finished in May 2020.

* `v2.x.y` is a series of releases compatible with GNU Radio 3.8 that existed
  between September 2019 and May 2020. The functionality in this series is
  equivalent to the `v1.x.y` series.

* `v1.x.y` the original series of releases, which was compatible with GNU Radio
  3.7. Development in this series stopped on September 2019 with the appearance
  of the `v2.x.y` line, but some bugfix releases have been published afterward.

The repository is organized in the following branches:

* `master` is where the active development happens. From time to time, features
  will be frozen in a new release.

* `maint-3.8` is the branch where releases in the current `v3.x.y` line are
  published. This branch is compatible with GNU Radio 3.8.

* `maint-3.8-v2` is the branch where releases in the `v2.x.y` line are
  published. This branch is compatible with GNU Radio 3.8.

* `maint-3.7` is the branch where releases in the `v1.x.y` line are
  published. This branch is compatible with GNU Radio 3.7.

In general, pull requests should be submitted to `master`.

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

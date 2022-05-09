# Contributing to gr-satellites

These guidelines are based on the [contributing guidelines for GNU
Radio](https://github.com/gnuradio/gnuradio/blob/main/CONTRIBUTING.md). Since
gr-satellites is a GNU Radio out-of-tree module, we follow the same guidelines
for consistency wherever it makes sense: coding style, code of conduct, etc.

## Coding Guidelines

gr-satellites follows the same coding guidelines as GNU Radio. These are
described in [GREP1][grep1].

For C++, clang-format is used. Formatting is checked in the CI pipeline and
can also be checked locally with the `tools/clang_format.py` helper script.

For Python, we follow PEP8. In contrast to GNU Radio, which doesn't use a Python
formatting checker, since a large amount of the gr-satellites code base is
Python, we use pycodestyle to check PEP8 formatting. This is part of the
CI pipeline and can be checked locally by running pycodestyle. Note that there
are some [folders that are excluded]
(https://github.com/daniestevez/gr-satellites-pycodestyle-action/blob/main/Dockerfile)
from pycodestyle checking.

## Python or C++?

While GNU Radio has most of its code base written in C++, gr-satellites has the
majority of its code base written in Python. This allows for a faster
development, and performance is often not so critical, since small satellites
typically transmit using low data rates. In particular, telemetry parsing is
always written in Python using [construct](https://construct.readthedocs.io/).

However, some kinds of blocks are equally simple to implement in C++ or in
Python, so C++ should be preferred for those.

## Git commit messages are very important

The same guidelines as for GNU Radio apply regarding commit messages:
- Keep the lines below 72 characters
- Avoid empty git commit messages
- The git commit message explains the change, the code only explains the current
  state

## Include Unit Tests

If you have an obvious test, that might speed up the time it takes to convince
reviewers that your code is correct.

## Adding support for a new satellite

Adding support for a new satellite can be as easy as writing a [SatYAML
file](https://gr-satellites.readthedocs.io/en/latest/satyaml.html) describing
the satellite if the satellite only uses protocols already supported by
gr-satellites. Since most satellites use a custom telemetry format, a new telemetry
parser should be written using
[construct](https://construct.readthedocs.io/). See the
[python/telemetry](https://github.com/daniestevez/gr-satellites/tree/main/python/telemetry)
folder for some examples, and take note that your new parser should be added
both to `python/telemetry/__index__.py` and to
`python/telemetry/CMakeLists.txt`.

For satellites using new or ad-hoc custom protocols, some
[components](https://gr-satellites.readthedocs.io/en/latest/components.html)
will need to be written to support them. Most likely, a new deframer will need
to be written. Examples can be found in
[python/components/deframers](https://github.com/daniestevez/gr-satellites/tree/main/python/components/deframers).

See also the [note to satellite teams] planning to use gr-satellites for their
mission.

[grep1]: https://github.com/gnuradio/greps/blob/main/grep-0001-coding-guidelines.md

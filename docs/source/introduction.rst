Introduction
============

gr-satellites is a `GNU Radio`_ out-of-tree module encompassing a collection of
telemetry decoders that supports many different `Amateur satellites`_. This
open-source project started in 2015 with the goal of providing telemetry
decoders for all the satellites that transmit on the `Amateur radio bands`_.

It supports most popular protocols, such as `AX.25`_, the GOMspace NanoCom U482C
and `AX100`_ modems, an important part of the `CCSDS stack`_, the `AO-40
protocol`_ used in the `FUNcube`_ satellites, and several ad-hoc protocols used
in other satellites.

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

.. _GNU Radio: https://gnuradio.org
.. _Amateur satellites: https://en.wikipedia.org/wiki/Amateur_radio_satellite
.. _Amateur radio bands: https://en.wikipedia.org/wiki/Amateur_radio_frequency_allocations
.. _AX.25: http://www.ax25.net/
.. _AX100: https://gomspace.com/shop/subsystems/communication-systems/nanocom-ax100.aspx
.. _CCSDS stack: https://public.ccsds.org/Publications/BlueBooks.aspx
.. _AO-40 protocol: https://www.amsat.org/articles/g3ruh/125.html
.. _FUNcube: https://funcube.org.uk/

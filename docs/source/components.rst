.. _Components:

Components
==========

Components represent gr-satellite's way of decomposing the decoding process in
high-level blocks. The decoding chain is broken into a series of steps which
pass their output to the input of the next step. These are the following:

* **Data sources**. These produce the input of the decoding chain, which
  typically consists of RF signal samples.

* **Demodulators**. These turn RF samples into soft symbols. They filter the
  signal, recover the transmit clock and carrier if necessary, etc. An example
  is a BPSK demodulator, which turns RF samples of a BPSK signal into a stream
  of soft symbols.

* **Deframers**. Deframers implement the lower layer protocols related to frame
  boundary detection, descrambling, deinterleaving, FEC, error checking with a
  CRC code, etc. The output of a deframer are PDUs with the frames. An example
  is an AX.25 deframer, or a CCSDS concatenated code deframer.

* **Transports**. Transports implement higher layer protocols that might be
  needed to get to the useful information inside the frames. For example, if
  frames are fragmented, a transport will handle defragmentation. An example is
  a KISS transport, whose input are frames that contain bytes of a KISS stream,
  and its output are the packets contained in that KISS stream, regardless of
  how they are split between different frames.

* **Data sinks**. Data sinks are the consumers of packets. They might store
  them, send them to another software, or parse telemetry values.

Below, the main component blocks in each category are described.

Data sources
^^^^^^^^^^^^

Data source components can be found under *Satellites > Data sources* in GNU
Radio companion. Currently, the only data source is the "KISS File Source"
block. This block will read a file in KISS format, and output the frames in the
file as PDUs.

The usual operations involving reading RF samples from an SDR or recording can
be achieved easily with default GNU Radio blocks, so there are no specific data
sources for these. Advanced users can look at the ``setup_input()`` method of
the class ``gr_satellites_top_block`` in ``apps/gr_satellites`` to see how the
``gr_satellites`` command line tools sets up its different inputs using default
GNU Radio blocks.

Demodulators
^^^^^^^^^^^^

Deframers
^^^^^^^^^

Transports
^^^^^^^^^^

Data sinks
^^^^^^^^^^

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
  CRC code, etc. The output of a deframer are PDUs with the frames. Some examples
  are an AX.25 deframer and a CCSDS concatenated code deframer.

* **Transports**. Transports implement higher layer protocols that might be
  needed to get to the useful information inside the frames. For example, if
  frames are fragmented, a transport will handle defragmentation. An example is
  a KISS transport, whose input are frames that contain bytes of a KISS stream,
  and its output are the packets contained in that KISS stream, regardless of
  how they are split between different frames.

* **Data sinks**. Data sinks are the consumers of packets. They might store
  them, send them to another software, or parse telemetry values.

All the component blocks support :ref:`Command line options` in the same way as
the satellite decoder block. The set of available options for each component
block is different. It is possible to use the ``"--help"`` as the options of a
particular block in order to print out the available options for that block.
  
Below, the main component blocks in each category are described.

.. _Data sources:

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

Demodulator components can be found under *Satellites > Demodulators* in GNU
Radio companion. There are currently three demodulator component blocks:

* BPSK demodulator

* FSK demodulator

* AFSK demodulator

They take RF signal samples as input, and output soft symbols, as a stream of
``float`` normalized with amplitude one. The input can be either real or IQ
(complex). See :ref:`Real or IQ input` for more information.

The demodulator blocks and their parameters are described below.

.. _BPSK demodulator:

BPSK demodulator
""""""""""""""""

The BPSK demodulator expects an input which consists of RF samples of a BPSK
signal, and outputs the demodulated BPSK soft symbols. The BPSK signal can
optionally be DBPSK or Manchester encoded.

The figure below shows the example flowgraph which can be found in
``examples/components/bpsk_demodulator.grc``. This reads a WAV file from
:ref:`satellite-recordings<Downloading sample recordings>` which contains some
BPSK packets from LilacSat-1 and uses the BPSK demodulator to obtain the
symbols. The "Skip Head" and "Head" blocks are used to select a portion of the
output, which is then plotted using the "QT GUI Time Sink".

.. figure:: images/bpsk_demodulator_flowgraph.png
    :alt: Usage of BPSK demodulator in a flowgraph

    Usage of BPSK demodulator in a flowgraph

When this example flowgraph is run, it displays the output shown in the figure
below. There we can see the start of the BPSK packet. On the left side of the
plot we have noise, before the packet starts, then the packet starts, and the
clock and carrier recovery take some time to sync. After this, the symbols are
demodulated properly. This can be seen because the +1 and -1 symbols are well
separated.
    
.. figure:: images/bpsk_demodulator_output.png
    :alt: Output of the BPSK demodulator example flowgraph

    Output of the BPSK demodulator example flowgraph

The figure below shows the options allowed by the BPSK demodulator block. The
*Baudrate* option is used to set the baudrate in symbols per second. The
*Sample rate* option specifies the sample rate of the input. The *Frequency offset*
specifies at which frequency the BPSK signal is centred
(see :ref:`Frequency offsets for BPSK`).

The *Differential* option enables differential decoding of DBPSK. For differential
decoding, the phase recovery using a Costas loop is disabled and non-coherent
demodulation is used.

The *Manchester* option enables Manchester decoding. A Manchester encoded BPSK
signal is decoded as if it had twice the baudrate, and then the phase of the
Manchester clock is searched in the symbols and the Manchester clock is
"wiped-off", multiplying symbols by the clock and accumulating them by pairs.

The *IQ input* option enables IQ (complex) input.
    
.. figure:: images/bpsk_demodulator_options.png
    :alt: Options of BPSK demodulator

    Options of BPSK demodulator

.. _FSK demodulator:

FSK demodulator
"""""""""""""""

The FSK demodulator expects an input which consists of RF samples of an FSK
signal, and outputs the demodulated FSK soft symbols. Both real and IQ (complex)
input are suported, but the semantics are different: with real input, the FSK
demodulator expects an FM-demodulated signal; with IQ input, the FSK demodulator
expects the signal before FM demodulation
(see :ref:`FSK demodulation and IQ input`).

The figure below shows the example flowgraph which can be found in
``examples/components/fsk_demodulator.grc``. This reads a WAV file from
:ref:`satellite-recordings<Downloading sample recordings>` which contains a single
FSK packet from AAUSAT-4 and uses the FSK demodulator to obtain the
symbols. The output is plotted using the "QT GUI Time Sink".

.. figure:: images/fsk_demodulator_flowgraph.png
    :alt: Usage of FSK demodulator in a flowgraph

    Usage of FSK demodulator in a flowgraph

When this example flowgraph is run, it displays the output shown in the figure
below. There we can see the FSK packet, surrounded by noise on both sides.
    
.. figure:: images/fsk_demodulator_output.png
    :alt: Output of the FSK demodulator example flowgraph

    Output of the FSK demodulator example flowgraph

The figure below shows the options allowed by the FSK demodulator block. The
*Baudrate* option is used to set the baudrate in symbols per second. The
*Sample rate* option specifies the sample rate of the input. The *IQ input* option enables
IQ (complex) input. The signal is expected to be centred at baseband (0Hz) when
IQ input is selected. The *Subaudio* option enables subaudio demodulation, which
is intended for subaudio telemetry under FM voice and includes an additional
lowpass filter to filter out the voice signal.
    
.. figure:: images/fsk_demodulator_options.png
    :alt: Options of FSK demodulator

    Options of FSK demodulator

.. _AFSK demodulator:
    
AFSK demodulator
""""""""""""""""

The APSK demodulator expects an input which consists of RF samples of an AFSK
signal, and outputs the demodulated AFSK soft symbols.  Both real and IQ (complex)
input are suported, but the semantics are different: with real input, the AFSK
demodulator expects an FM-demodulated signal; with IQ input, the AFSK demodulator
expects the signal before FM demodulation (see :ref:`FSK demodulation and IQ input`).

The figure below shows the example flowgraph which can be found in
``examples/components/afsk_demodulator.grc``. This reads a WAV file from
:ref:`satellite-recordings<Downloading sample recordings>` which contains a
single AFSK packet from GOMX-1 and uses the AFSK demodulator to obtain the
symbols. The "Head" block is used to select a portion of the output, which
is then plotted using the "QT GUI Time Sink".

.. figure:: images/afsk_demodulator_flowgraph.png
    :alt: Usage of AFSK demodulator in a flowgraph

    Usage of AFSK demodulator in a flowgraph

When this example flowgraph is run, it displays the output shown in the figure
below. There we can see the AFSK packet, surrounded by noise on both sides.
    
.. figure:: images/afsk_demodulator_output.png
    :alt: Output of the AFSK demodulator example flowgraph

    Output of the AFSK demodulator example flowgraph

The figure below shows the options allowed by the AFSK demodulator block. The
*Baudrate* option is used to set the baudrate in symbols per second. The
*Sample rate* option specifies the sample rate of the input.

The *AF carrier* option specifies the audio frequency in Hz on which the FSK tones
are centred. The *Deviation* option specifies the separation in Hz between each
of the tones and the AF carrier. If the deviation is positive, the high tone is
interpreted as representing the symbol 1, while the low tone is interpreted as
representing the symbol 0 (or -1 in bipolar representation). If the deviation is
negative, the low tone is interpreted as representing the symbol 1 and the high
tone is interpreted as representing the symbol 0.

In this example, the AF carrier is 3600 Hz and the deviation is -1200 Hz. This
means that the tone representing 1 is at 2400 Hz, while the tone representing 0
is at 4800 Hz (the signal is actually 4800 baud GMSK).

The *IQ input* option enables IQ (complex) input.
    
.. figure:: images/afsk_demodulator_options.png
    :alt: Options of AFSK demodulator

    Options of AFSK demodulator

Deframers
^^^^^^^^^

Deframer components can be found under *Satellites > Deframers* in GNU
Radio companion. There is a large number of deframer component blocks, since
many satellites use ad-hoc protocols for framing, so a custom deframer is used
for those satellites.

Deframers take soft symbols, produced as the output of one of the demodulator
components, and detect frame boundaries, perform as necessary descrambling,
deinterleaving, FEC decoding, CRC checking, etc.

Here, the most popular deframers are described. For ad-hoc deframers that are
used in few satellites, the reader is referred to the documentation of each of
the blocks in GNU Radio companion.

.. _AX.25 deframer:

AX.25 deframer
""""""""""""""

The AX.25 deframer implements the `AX.25`_ protocol. It performs NRZ-I decoding,
frame boundary detection, bit de-stuffing, and CRC-16 checking. Optionally, it
can also perform G3RUH descrambling. G3RUH scrambling is typically used for
faster baudrates, such as 9k6 FSK packet radio, but not for slower baudrates,
such as 1k2 AFSK packet radio.

The figure below shows an example flowgraph of the AX.25 deframer block. This
example can be found in ``examples/components/ax25_deframer.grc``. The example
reads a WAV file from :ref:`satellite-recordings<Downloading sample recordings>`
containing 9k6 FSK AX.25 packets from US01, demodulates them
with the FSK demodulator block, deframes tham with AX.25 deframer, and prints
the output with the Message Debug block.

.. figure:: images/ax25_deframer_flowgraph.png
    :alt: Usage of AX.25 deframer in a flowgraph

    Usage of AX.25 deframer in a flowgraph

The AX.25 deframer block has a single option that indicates whether G3RUH
descrambling should be performed or not.

.. _GOMspace AX100 deframer:

GOMspace AX100 deframer
"""""""""""""""""""""""

The GOMspace AX100 deframer implements two different protocols used by the popular
`GOMspace NanoCom AX100`_ transceiver. These two protocols are:

* ASM+Golay. This uses a header encoded with a Golay(24,12) code that indicates
  the packet length. The payload is Reed-Solomon encoded with a (255,223) CCSDS
  code and scrambled with the CCSDS synchronous scrambler.

* Reed Solomon. This uses a G3RUH asynchronous scrambler. The first byte of the
  packets indicates the length of the payload and is sent unprotected. The
  packet payload is Reed-Solomon encoded with a (255,223) CCSDS code.

The figure below shows an example flowgraph of the AX100 deframer block running
in both modes. This example can be found in
``examples/components/ax100_deframer.grc``. For ASM+Golay decoding the example
reads a WAV file from :ref:`satellite-recordings<Downloading sample recordings>`
containing packets from 1KUNS-PF. For Reed Solomon decoding the
example reads a WAV file from
:ref:`satellite-recordings<Downloading sample recordings>`
which contains packets from TW-1B. The output frames are printed with Message
Debug blocks.
  
.. figure:: images/ax100_deframer_flowgraph.png
    :alt: Usage of AX100 deframer in a flowgraph

    Usage of AX100 deframer in a flowgraph

In Reed Solomon mode, the AX100 deframer only has two options:
the *Mode* option indicates the
mode, as described above, and the *Syncword threshold* option specifies how
many bit errors are allowed in the detection of the 32 bit syncword.
In ASM+Golay mode, the AX100 deframer has an additional option:
*Scrambler*, which can be used to enable or disable the CCSDS synchronous
scrambler.

.. _GOMspace U482C deframer:

GOMspace U482C deframer
"""""""""""""""""""""""

The GOMsace U482C deframer implements the protocol used by the GOMspace NanoCom
U482C tranceiver, which is an older transceiver from GOMspace that is still seen
in some satellites.

The protocol used by the U482C is similar to the ASM+Golay mode used by the
AX100. The packet payload can be optionally:

* Encoded with the CCSDS r=1/2, k=7 convolutional encoder

* Scrambled with the CCSDS synchronous scrambler

* Encoded with a CCSDS (255,223) Reed-Solomon code

The packet header has flags that indicate which of these options are in use, in
addition to the length field.

The U482C modem uses AFSK with a 4800 baud audio-frequency GMSK waveform.

The figure below shows an example flowgraph of the U482C deframer block. This
example can be found in ``examples/components/u482c_deframer.grc``. The example
reads a WAV file from :ref:`satellite-recordings<Downloading sample recordings>`
containing a packet from GOMX-1. The packet is demodulated and deframed, and the
output is printed in hex using the Message Debug block.

.. figure:: images/u482c_deframer_flowgraph.png
    :alt: Usage of U482C deframer in a flowgraph

    Usage of U482C deframer in a flowgraph

The U482C deframer has a single option, which indicates the number of bit
errors that are allowed in the syncword detection.

.. _AO-40 FEC deframer:

AO-40 FEC deframer
""""""""""""""""""

The AO-40 FEC deframer implements the protocol designed by Phil Karn KA9Q for
the `AO-40 FEC beacon`_. This protocol is currently used in the FUNcube
satellites and others.

The FEC is based on CCSDS recommendations and uses a pair of interleaved
Reed-Solomon (160,128) codes, the CCSDS synchronous scrambler, the CCSDS r=1/2,
k=7 convolutional code, interleaving and a distributed syncword.

The figure below shows an example flowgraph of the AO-40 FEC deframer
block. This example can be found in
``examples/components/ao40_fec_deframer.grc``. It reads a WAV file from
:ref:`satellite-recordings<Downloading sample recordings>` containing a packet
from AO-73 (FUNcube-1). The packet is first BPSK demodulated and then deframed
with the AO-40 FEC deframer. The output is printed out using the Message
Debug block.

.. figure:: images/ao40_fec_deframer_flowgraph.png
    :alt: Usage of AO-40 FEC deframer in a flowgraph

    Usage of AO-40 FEC deframer in a flowgraph

The AO-40 FEC deframer block has two options. The *Syncword threshold*
option indicates the number of bit errors to allow in the syncword
detection. The *Use short frames* option toggles the usage of short
frames. This is a variant of the AO-40 FEC protocol which is based on a single
Reed-Solomon codeword and is used by SMOG-P and ATL-1.

.. _CCSDS deframers:

CCSDS deframers
"""""""""""""""

The CCSDS Uncoded deframer, CCSDS Concatenated deframer, and CCSDS Reed-Solomon
deframer blocks implement some of the CCSDS protocols defined in the TM
Synchronization and Channel Coding Blue Book (see the `CCSDS Blue Books`_).

The CCSDS Uncoded deframer implements uncoded TM frames.

The CCSDS Reed-Solomon deframer implements Reed-Solomon TM frames, which use a
Reed-Solmon (255, 223) code (or a shortened version of this code) and the CCSDS
synchronous scrambler. There is support for several interleave Reed-Solomon
codewords.

The CCSDS Concatenated deframer implements concatenated TM frames, which add an
r=1/2, k=7 convolutional code as an inner coding to the Reed-Solomon frames.

The usage of all three of these deframers is very similar.

The figure below shows an example flowgraph of the CCSDS Concatenated deframer
block. This example can be found in
``examples/components/ccsds_deframer.grc``. It reads a WAV file from
:ref:`satellite-recordings<Downloading sample recordings>` containing some
packets from BY70-1. These are concatenated TM frames with a frame size of 114
bytes and differential encoding (to solve the BPSK phase ambiguity). The packet
is first BPSK demodulated and then deframed. The output is printed using the
Message Debug block.

.. figure:: images/ccsds_deframer_flowgraph.png
    :alt: Usage of CCSDS Concatenated deframer in a flowgraph

    Usage of CCSDS Concatenated deframer in a flowgraph

The figure below shows the options used by the CCSDS Concatenated
deframer. The CCSDS Reed-Solomon deframer block allows exactly the same options,
except for the *Convolutional code* option,
since all the other options refer to the Reed-Solomon outer code.

The *Frame size* option indicates the size of the frame in bytes (after
Reed-Solomon decoding). The *Precoding* option can be used enable a differential
decoder before the Reed-Solomon decoder.
This is often used to solve the BPSK 180º phase ambiguity.
The *Reed-Solomon basis* option can be used to toggle between the conventional
and dual basis definitions of the Reed-Solomon code. The CCSDS standard
specifies the dual basis, but the conventional basis is frequently used. The
*Reed-Solomon interleve depth* option can be used to enable decoding of interleaved
Reed-Solomon codewords. The *Scrambler* option can be used to enable or disable
the CCSDS synchronous scrambler.
The *Syncword threshold* option can be used to choose the number of bit
errors that are allowed in the detection of the syncword.
    
.. figure:: images/ccsds_deframer_options.png
    :alt: Options of CCSDS Concatenated deframer

    Options of CCSDS Concatenated deframer

Transports
^^^^^^^^^^

Transport components can be found under *Satellites > Transports* in GNU Radio
companion. Transports are designed to implement upper layer protocols. They take
as input the output of a demodulator, which contains physical layer or link
layer frames and process it to obtain upper layer packets. Some of the typical
functionalities implemented by these upper layer protocols include
fragmentation/defragmentation.

The only transport available so far in gr-satellites is the KISS transport.

.. _KISS transport:

KISS transport
""""""""""""""

The KISS tranport implements fragmentation/defragmentation according to the KISS
protocol for packet boundary detection. Its input should be PDUs containing
the bytes of a KISS stream. The frames are joined and the KISS stream is
followed, detecting packet boundaries and extracting the packets. The packets
are output as PDUs.

The figure below shows an example flowgraph of the KISS transport, which can be
found in ``examples/components/kiss_transport.grc``. It is based
on the CCSDS Concatenated deframer example described above. BY70-1 sends frames
which contain the bytes of a KISS stream, so the KISS transport can be used to
extract the packets from this stream. There are two Message Debug blocks that
can be enabled or disabled in order to see the input or the output of the KISS
transport block.

.. figure:: images/kiss_transport_flowgraph.png
    :alt: Usage of KISS transport in a flowgraph

    Usage of KISS transport in a flowgraph

When the example is run, the frames at the input of the input of the KISS
transport look like the one below. We see that there is a single packet embedded
into the 114 byte Reed-Solomon frame, using ``c0`` KISS idle bytes for padding.

.. code-block:: none

   pdu_length = 114
   contents = 
   0000: c0 b8 64 3d 00 12 00 00 00 00 c8 3a 00 80 00 00 
   0010: 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 
   0020: 32 32 32 32 32 32 32 32 32 32 32 32 32 32 ff c4 
   0030: 00 1f 00 00 01 05 01 01 01 01 01 01 00 00 00 00 
   0040: 00 00 00 00 01 02 03 04 05 06 07 08 09 0a 0b ff 
   0050: 18 21 00 00 db dc 4b f7 07 c0 c0 c0 c0 c0 c0 c0 
   0060: c0 c0 c0 c0 c0 c0 c0 c0 c0 c0 c0 c0 c0 c0 c0 c0 
   0070: c0 c0 

The frames at the output of the KISS transport look like the following. We see
that the ``c0`` KISS idle bytes have been stripped. The KISS transport can
also handle the case when a packet is longer than 114 bytes and has been
fragmented into several 114 byte frames.
   
.. code-block:: none

   pdu_length = 87
   contents = 
   0000: b8 64 3d 00 12 00 00 00 00 c8 3a 00 80 00 00 32 
   0010: 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 32 
   0020: 32 32 32 32 32 32 32 32 32 32 32 32 32 ff c4 00 
   0030: 1f 00 00 01 05 01 01 01 01 01 01 00 00 00 00 00 
   0040: 00 00 00 01 02 03 04 05 06 07 08 09 0a 0b ff 18 
   0050: 21 00 00 c0 4b f7 07 

The KISS transport has a single option, called *Expect control byte*. When it
is set to ``True``, the first byte before the packet payload is interpreted as a
control byte according to the KISS protocol. If it is set to ``False``, it is
assumed that there is no control byte preceeding the packet payload. When using
KISS as a means to fragment/defragment upper layer packets it is more common not
to use control bytes.

Data sinks
^^^^^^^^^^

Data sink components are the final consumers of the PDUs that contain the
decoded frames. They can be used for several things, such as printing telemetry
values, saving frames to a file, sending frames to an online telemetry database
server, and reassembling files and images. The different data sinks available in
gr-satellites are described below.

.. _Telemetry parser:

Telemetry parser
""""""""""""""""

The telemetry parser uses `construct`_ to parse a PDU containing a telemetry
frame into the different fields and prints the parsed values to the standard
output or a file.

The parser uses *telemetry definitions*, which are either ``Construct`` objects
(typically a ``Struct``) or any other object supporting the ``parse()`` method in
case more complex parsing behaviour is needed. The list of available telemetry
definitions can be seen in ``python/telemetry/__index__.py``, or by calling
``import satellites.telemetry; help(satellites.telemetry)`` in ``python3``.

The figure below shows an example flowgraph of the Telemetry parser block, which can be
found in ``examples/components/telemetry_paser.grc``. It is based
on the U482C example described above. The packets sent by GOMX-1 are deframed
and the the Telemetry parser is used to print out the telemetry values to the
standard output.

.. figure:: images/telemetry_parser_flowgraph.png
    :alt: Usage of Telemetry parser in a flowgraph

    Usage of Telemetry parser in a flowgraph

The beginning of the ouptut produced by the Telemetry parser block can be seen below.

.. code-block:: none

   Container: 
    csp_header = Container: 
        priority = 2
        source = 1
        destination = 10
        destination_port = 30
        source_port = 0
        reserved = 0
        hmac = False
        xtea = False
        rdp = False
        crc = False
    beacon_time = 2015-03-31 20:57:01
    beacon_flags = 121
    beacon = Container: 
        obc = Container: 
            boot_count = 573
            temp = ListContainer: 
                -6.0
                -4.0
            panel_temp = ListContainer: 
                0.0
                -28.5
                -26.75
                -13.25
                -28.25
                -20.0

The options used by the Telemetry parser are the following. The
*Telemetry definition* option indicates the telemetry definition object, which must be an
object in the ``satellites.telemetry`` module as described above. The *Output*
drop down list can be used to select the standard output or a file as the
destination for the parser's output. If a file is selected, an additional
option to select the file path appears. 

Telemetry submit
""""""""""""""""

The telemetry submit block implements :ref:`Telemetry submission` to several
different online telemetry servers. Its input consists of PDUs with frames,
which are then submitted to the selected telemetry server.

This block uses the gr-satellites config file located in
``~/.gr_satellites/config.ini`` to configure the different options of the
telemetry servers, such as the login credentials. See the
:ref:`information regarding the command line tool<Telemetry submission>` for how
to set up this configuration file.

The telemetry submit block has only one option, which is a drop down list
that is used to select the telemetry server to use.

Hexdump sink
""""""""""""

The hexdump sink prints PDUs in hex to the standard output. It is a wrapper over
the Message Debug standard GNU Radio block, so it uses the same output
format. This block is used internally by the ``gr_satellites`` command line tool
(see :ref:`Hex dump`), and can also be used in custom flowgraphs instead of
Message Debug.

KISS file sink
""""""""""""""

The KISS file sink can be used to store PDUs in a file using the
`KISS protocol`_. This protocol is a simple format to mark frame
boundaries. Files containing frames with the KISS protocol can then be read with
the KISS file datasource (see :ref:`Data sources`) and with the
``gr_satellites`` command line tool (see :ref:`Specifying the input source`),
as well as with external tools.

The KISS file sink block has two options. The *File* option is used to
select the path of the output file. The *Append file* option can be used to
overwrite or append to the output file.

The KISS files produced by the KISS file sink store timestamps as described in the
:ref:`KISS output` of the ``gr_satellites`` command line tool.

KISS server sink
""""""""""""""""

The KISS server sink spawns a TCP server that sends decoded PDUs to connected
clients using the `KISS protocol`_. A number of tools can act as clients using
this protocol.

The KISS file sink block has a *Port* option to specify the TCP port to listen on.

The KISS server sink sends timestamps as described in the
:ref:`KISS output` of the ``gr_satellites`` command line tool.

.. _File and Image receivers:

File and Image receivers
""""""""""""""""""""""""

The File and Image receiver blocks are used to reassemble files transmitted in
chunks, using a variety of different formats. The only difference between the
File receiver and the Image receiver is that the Image receiver is able to
display image files in realtime using `feh`_ as they are being received.

These receiver blocks use *FileReceiver definitions*, which are
classes derived from ``FileReceiver``. The list of available definitions can be
seen in ``python/filereceiver/__index__.py``, or by calling
``import satellites.filereceiver; help(satellites.filereceiver)`` in
``python3``. Classes used by the Image receiver must be derived from ``ImageReceiver``.

The figure below shows an example flowgraph of the Image receiver block, which can be
found in ``examples/components/image_receiver.grc``. The example
reads a WAV file from :ref:`satellite-recordings<Downloading sample recordings>`
containing an image transfer from LilacSat-1. The WAV file is played back in
real time using the Throttle block. The Satellite decoder block is used to
demodulate and deframe the packets. Since these packets contain a KISS stream,
the KISS transport is used to obtain the image packets. These are sent into the
Image receiver block, which will print some information to the standard output
and when the beginning of the image is receive, will launch feh to display the image.

.. figure:: images/image_receiver_flowgraph.png
    :alt: Usage of Image receiver in a flowgraph

    Usage of Image receiver in a flowgraph

The figure below shows the options of the Image receiver block. The option
*ImageReceiver class* indicates the definition to use for reassembling the image
(which is implemented by a class derived from ``ImageReceiver``). The *Path*
option specifies the path of the directory where received files are saved
to. The names of the files depend on metadata in the image packets. The *Verbose*
option enables printing information to the standard output, such as the
frames being received. The *Display* option enables the use of feh to display
the image. The *Fullscreen* option is used to run feh in fullscreen.
    
.. figure:: images/image_receiver_options.png
    :alt: Options of Image receiver

    Options of Image receiver

The options of the File receiver block are the same as those of the Image
receiver block, except for the *Display* and *Fullscreen* options, which are
specific to image reception.

Codec2 UDP sink
"""""""""""""""

The Codec2 UDP sink is used internally by the ``gr_satellites`` command line
tool when decoding LilacSat-1. The LilacSat-1 decoder supports outputting Codec2
digital voice frames by UDP. These frames can then be fed into the Codec2
command line decoder.

The Codec2 frames are 7 bytes long, and each is sent in a different UDP packet
to ensure minimum latency.

The Codec2 UDP sink has two options, which indicate the IP and port to send
the frames to. By default, address ``127.0.0.1`` and port ``7000`` are used.

The Codec2 frames can be decoded and played in real time by the Codec2 decoder as shown here.

.. code-block:: console

   $ nc -lu 7000 | c2dec 1300 - -  | play -t raw -r 8000 -e signed-integer -b 16 -c 1 -

The ``c2dec`` command line decoder can be obtained by building from source the
`codec2 library`_
   
.. _AX.25: http://www.ax25.net/
.. _GOMspace NanoCom AX100: https://gomspace.com/shop/subsystems/communication-systems/nanocom-ax100.aspx
.. _AO-40 FEC beacon: http://www.ka9q.net/papers/ao40tlm.html
.. _CCSDS Blue Books: https://public.ccsds.org/Publications/BlueBooks.aspx
.. _KISS protocol: http://www.ax25.net/kiss.aspx
.. _construct: https://construct.readthedocs.io/
.. _feh: https://feh.finalrewind.org/
.. _codec2 library: https://github.com/drowe67/codec2/

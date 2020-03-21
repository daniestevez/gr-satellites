.. _gr_satellites command line tool:

gr_satellites command line tool
===============================

The ``gr_satellites`` command line tool is a complete solution that can decode
frames using either real-time RF samples from an SDR or conventional radio or a
recording.

Basic usage
^^^^^^^^^^^

``gr_satellites`` can be run from a terminal after gr-satellites has been
installed. If run without any arguments, ``gr_satellites`` will only print some
basic information about the arguments it allows.

.. code-block:: console

   $ gr_satellites 
   usage: gr_satellites satellite [-h] [--wavfile WAVFILE] [--rawfile RAWFILE]
		                  [--rawint16 RAWINT16] [--samp_rate SAMP_RATE]
                                  [--udp] [--udp_ip UDP_IP] [--udp_port UDP_PORT]
                                  [--kiss_in KISS_IN] [--iq]
                                  [--input_gain INPUT_GAIN] [--kiss_out KISS_OUT]
                                  [--kiss_append] [--hexdump]
                                  [--dump_path DUMP_PATH]

Specifying the satellite
""""""""""""""""""""""""

The arguments that ``gr_satellites`` allows depend on the satellite that has
been selected. Therefore, to use ``gr_satellites`` is always necessary to
specify the ``satellite`` to be used as an argument immediately following
``gr_satellites``. There are three different ways to specify the satellite:

* Using the satellite name, such as *FUNcube-1* or *LilacSat-2*. This can be
  used with any :ref:`satellite officially supported by gr-satellites<Supported
  satellites>`, and it is the most simple way of specifying a satellite.

  .. code-block:: console

     $ gr_satellites FUNcube-1
     Need to specify exactly one of the following input sources: {--wavfile, --rawfile, --rawint16, --udp, --kiss_in}
     usage: gr_satellites satellite [-h] [--wavfile WAVFILE] [--rawfile RAWFILE]
                                    [--rawint16 RAWINT16] [--samp_rate SAMP_RATE]
                                    [--udp] [--udp_ip UDP_IP] [--udp_port UDP_PORT]
                                    [--kiss_in KISS_IN] [--iq]
                                    [--input_gain INPUT_GAIN] [--kiss_out KISS_OUT]
                                    [--kiss_append] [--hexdump]
                                    [--dump_path DUMP_PATH] [--f_offset F_OFFSET]
                                    [--rrc_alpha RRC_ALPHA] [--disable_fll]
                                    [--fll_bw FLL_BW] [--clk_bw CLK_BW]
                                    [--clk_limit CLK_LIMIT] [--costas_bw COSTAS_BW]
                                    [--manchester_history MANCHESTER_HISTORY]
                                    [--syncword_threshold SYNCWORD_THRESHOLD]
                                    [--verbose_rs]

   A satellite may have several different names, known as *alternative
   names*. For example, FUNcube-1 is both known as AO-73 and FUNcube-1.
				    
* Using the satellite `NORAD ID`_. This can bue used with any
  :ref:`satellite officially supported by gr-satellites<Supported satellites>`,
  and it can be useful when interfacing ``gr_satellites`` with other tools that
  use NORAD IDs to classify satellites.

  Below we show ``gr_satellites`` running with NORAD ID 39444, which corresponds
  to FUNcube-1.

  .. code-block:: console

     $ gr_satellites 39444
     Need to specify exactly one of the following input sources: {--wavfile, --rawfile, --rawint16, --udp, --kiss_in}
     usage: gr_satellites satellite [-h] [--wavfile WAVFILE] [--rawfile RAWFILE]
                                    [--rawint16 RAWINT16] [--samp_rate SAMP_RATE]
                                    [--udp] [--udp_ip UDP_IP] [--udp_port UDP_PORT]
                                    [--kiss_in KISS_IN] [--iq]
                                    [--input_gain INPUT_GAIN] [--kiss_out KISS_OUT]
                                    [--kiss_append] [--hexdump]
                                    [--dump_path DUMP_PATH] [--f_offset F_OFFSET]
                                    [--rrc_alpha RRC_ALPHA] [--disable_fll]
                                    [--fll_bw FLL_BW] [--clk_bw CLK_BW]
                                    [--clk_limit CLK_LIMIT] [--costas_bw COSTAS_BW]
                                    [--manchester_history MANCHESTER_HISTORY]
                                    [--syncword_threshold SYNCWORD_THRESHOLD]
                                    [--verbose_rs]
  
* Using a path to an ``.yml`` SatYAML file. SatYAML files are used by
  gr-satellites to specify the decoding parameters and configuration
  corresponding to each different satellite. They are described in more detail
  in the :ref:`SatYAML files` section.

  gr-satellites comes bundled with a large number of SatYAML files corresponding to all
  the officially supported satellites. They can be found in the
  ``python/satyaml/`` directory.

  Specifying the path of a SatYAML file is useful if the user has modified some
  of the files bundled with gr-satellites or has created their own ones.

    .. code-block:: console

     $ gr_satellites python/satyaml/AO-73.yml
     Need to specify exactly one of the following input sources: {--wavfile, --rawfile, --rawint16, --udp, --kiss_in}
     usage: gr_satellites satellite [-h] [--wavfile WAVFILE] [--rawfile RAWFILE]
                                    [--rawint16 RAWINT16] [--samp_rate SAMP_RATE]
                                    [--udp] [--udp_ip UDP_IP] [--udp_port UDP_PORT]
                                    [--kiss_in KISS_IN] [--iq]
                                    [--input_gain INPUT_GAIN] [--kiss_out KISS_OUT]
                                    [--kiss_append] [--hexdump]
                                    [--dump_path DUMP_PATH] [--f_offset F_OFFSET]
                                    [--rrc_alpha RRC_ALPHA] [--disable_fll]
                                    [--fll_bw FLL_BW] [--clk_bw CLK_BW]
                                    [--clk_limit CLK_LIMIT] [--costas_bw COSTAS_BW]
                                    [--manchester_history MANCHESTER_HISTORY]
                                    [--syncword_threshold SYNCWORD_THRESHOLD]
                                    [--verbose_rs]
				    
.. _NORAD ID: https://en.wikipedia.org/wiki/Satellite_Catalog_Number

Specifying the input source
"""""""""""""""""""""""""""

Besides specifying the satellite to use for decoding, it is mandatory to specify
the input source by using exactly one of the following options:

* ``--wavfile`` can be used to read a recording in WAV format. The sample rate
  of the recording needs to be specified with the ``--samprate`` argument.

  By default, the WAV file is interpreted as a one-channel file containing real
  RF samples. To read a two-channel file containing IQ RF samples, the ``--iq``
  argument needs to be specified.

  .. note::
     All the :ref:`sample recordings <Downloading sample recordings>` in
     the ``satellite-recordings/`` are real 48kHz WAV files and can be read with
     the ``--wavfile file --samprate 48e3`` arguments.

     For example, this will decode some frames from FUNcube-1:
     
     .. code-block:: console

        $ gr_satellites FUNcube-1 --wavfile satellite-recordings/ao73.wav --samprate 48e3
  
* ``--rawfile`` can be used to read a recording in ``complex64`` or ``float32``
  format (depending on whether the ``--iq`` argument is used or not). The sample rate
  of the recording needs to be specified with the ``--samprate`` argument.

  .. note::
     Files in ``complex64`` format contain a sequence of 32-bit floating point numbers in
     IEEE 754 format. The sequence alternates between the I (in-phase) and Q
     (quadrature) componentes of a stream of IQ samples. This format is used by the
     GNU Radio File Source and File Sink blocks when their type is set to
     *complex*.

     Files in ``float32`` format contain a sequence of 32-bit floating point
     numbers in IEEE 754 format. The sequence contains the elements of a stream
     of real samples. This format is used by the GNU Radio File Source and File
     Sink blocks when their type is set to *float*.

* ``--rawint16`` can be used to read a recording in ``int16`` format. The file
  is interpreted as IQ or real data according as to whether the ``--iq``
  argument is used or not.  The sample rate of the recording needs to be
  specified with the ``--samprate`` argument.

  .. note::
     Files in ``int16`` format contain a sequence of 16-bit integers in
     host endianness. This format is used by GNU Radio File Source and File Sink
     blocks when their type is set to *short*.

* ``--udp`` can be used to received RF samples streamed in real-time. The sample rate
  of the recording needs to be specified with the ``--samprate`` argument.

  The streaming format is the same as for the ``--rawint16`` and both real
  samples (by default) and IQ samples (using the ``--iq`` argument) are
  supported.

  By default, ``gr_satellites`` will listen on the IP address ``::`` (all
  addresses) and the UDP port 7355. A different IP address or port can be
  specified using the parameters ``--udp_ip`` and ``--udp_port``.

  .. note::
     `GQRX`_ can stream audio in UDP using this format and UDP port,
     and a sample rate of 48ksps by following the instructions
     `here <https://gqrx.dk/doc/streaming-audio-over-udp>`_. In this case,
     ``gr_satellites`` should be run as

     .. code-block:: console

	$ gr_satellites FUNcube-1 --udp --samprate 48e3

     This is recommended as a simple way of interfacing ``gr_satellites`` with
     SDR hardware for beginner users.

     It is also possible to use the example GNU Radio companion flographs in
     `gr-frontends`_ to stream samples by UDP from different sources.

     For advanced users, ``nc`` can also be a very useful tool for streaming.

* ``--kiss_in`` can be used to process a file containing already decoded frames
  in KISS format. All the demodulation steps are skipped and only telemetry
  parsing, file receiving, etc. are done.

  This can be useful to view the telemetry stored in files previously decoded
  with gr-satellites or other software.

Getting help
""""""""""""

``gr_satellites`` prints a detailed description of all the allowed arguments by
using the ``-h`` or ``--help`` argument. Note that a satellite needs to be
specified, since the set of allowed arguments depends on the decoders used by
that satellite.

For example, this shows all the options allowed by the FUNcube-1 decoder:

.. code-block:: console

   $ gr_satellites FUNcube-1 --help
   usage: gr_satellites satellite [-h] [--wavfile WAVFILE] [--rawfile RAWFILE]
                                  [--rawint16 RAWINT16] [--samp_rate SAMP_RATE]
                                  [--udp] [--udp_ip UDP_IP] [--udp_port UDP_PORT]
                                  [--kiss_in KISS_IN] [--iq]
                                  [--input_gain INPUT_GAIN] [--kiss_out KISS_OUT]
                                  [--kiss_append] [--hexdump]
                                  [--dump_path DUMP_PATH] [--f_offset F_OFFSET]
                                  [--rrc_alpha RRC_ALPHA] [--disable_fll]
                                  [--fll_bw FLL_BW] [--clk_bw CLK_BW]
                                  [--clk_limit CLK_LIMIT] [--costas_bw COSTAS_BW]
                                  [--manchester_history MANCHESTER_HISTORY]
                                  [--syncword_threshold SYNCWORD_THRESHOLD]
                                  [--verbose_rs]

   gr-satellites - GNU Radio decoders for Amateur satellites

   optional arguments:
     -h, --help            show this help message and exit

   input:
     --wavfile WAVFILE     WAV input file
     --rawfile RAWFILE     RAW input file (float32 or complex64)
     --rawint16 RAWINT16   RAW input file (int16)
     --samp_rate SAMP_RATE
                        Sample rate (Hz)
     --udp                 Use UDP input
     --udp_ip UDP_IP       UDP input listen IP [default='::']
     --udp_port UDP_PORT   UDP input listen port [default='7355']
     --kiss_in KISS_IN     KISS input file
     --iq                  Use IQ input
     --input_gain INPUT_GAIN
                        Input gain (can be negative to invert signal)
                        [default=1]

   output:
     --kiss_out KISS_OUT   KISS output file
     --kiss_append         Append to KISS output file
     --hexdump             Hexdump instead of telemetry parse
     --dump_path DUMP_PATH
                           Path to dump internal signals

   demodulation:
     --f_offset F_OFFSET   Frequency offset (Hz) [default=1500 or 12000]
     --rrc_alpha RRC_ALPHA
                           RRC roll-off (Hz) [default=0.35]
     --disable_fll         Disable FLL
     --fll_bw FLL_BW       FLL bandwidth (Hz) [default=25]
     --clk_bw CLK_BW       Clock recovery bandwidth (relative to baudrate)
                           [default=0.06]
     --clk_limit CLK_LIMIT
                           Clock recovery limit (relative to baudrate)
                           [default=0.02]
     --costas_bw COSTAS_BW
                           Costas loop bandwidth (Hz) [default=50]
     --manchester_history MANCHESTER_HISTORY
                           Manchester recovery history (symbols) [default=32]

   deframing:
     --syncword_threshold SYNCWORD_THRESHOLD
                           Syncword bit errors [default=8]
     --verbose_rs          Verbose RS decoder

   The satellite parameter can be specified using name, NORAD ID or path to YAML
   file

Output
""""""

By default, ``gr_satellites`` will "do its best" to provide the user the output
for the decoded frames. If the telemetry format for the satellite is implemented
in gr-satellites, the telemetry frames will be printed to the standard output in
human-readable format. Otherwise, the raw frames will be printed out in hex
format to the standard output.

File decoding, image decoding and other special output options of some
particular satellites are enabled by default.

Customization of the ouput options is described in the :ref:`Output options`
subsection below.

Examples
""""""""

The ``test.sh`` script in the ``gr-satellites/`` directory runs
``gr_satellites`` on several of the
:ref:`sample recordings <Downloading sample recordings>` in
``satellite-recordings/``. This script can be used as a series of examples on
how to run ``gr_satellites``.

.. _Output options:

Ouput options
^^^^^^^^^^^^^
   
.. _GQRX: https://gqrx.dk/
.. _gr-frontends: https://github.com/daniestevez/gr-frontends
	
Other topics
^^^^^^^^^^^^

Real or IQ input
""""""""""""""""

(also speak about FSK pre-demod / post-demod)

Frequency offsets for BPSK
""""""""""""""""""""""""""

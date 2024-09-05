.. _SatYAML files:

SatYAML files
=============

SatYAML files are used by gr-satellites to describe the properties of each
specific satellite, such as what kind of protocols and telemetry formats it
uses. They are `YAML`_ files and are based around the concept of
components. Using SatYAML files, the ``gr_satellites`` command line tool and the
Satellite decoder block can figure out which components to put together to
decode a particular satellite.


SatYAML files are stored in the ``python/satyaml`` directory. Below we show the
SatYAML file ``1KUNS-PF.yml`` to give an overall idea of the format of these
files.

.. code-block:: yaml

   name: 1KUNS-PF
   alternative_names:
   norad: 43466
   data:
     &tlm Telemetry:
       telemetry: sat_1kuns_pf
     &image JPEG Images:
       image: sat_1kuns_pf
   transmitters:
     1k2 FSK downlink:
       frequency: 437.300e+6
       modulation: FSK
       baudrate: 1200
       framing: AX100 ASM+Golay
       data:
       - *tlm
       - *image
     9k6 FSK downlink:
       frequency: 437.300e+6
       modulation: FSK
       baudrate: 9600
       framing: AX100 ASM+Golay
       data:
       - *tlm
       - *image

First we can see some fields that give basic information about the
satellite. The ``name`` field indicates the main name of the satellite, which is
used by ``gr_satellites`` and the Satellite decoder block when calling up the
satellite by name. There is an optional list of ``alternative_names`` which can
also be used to call up the satellite by name. The ``norad`` field gives the
NORAD ID of the satellite and it is used when calling up the satellite by
NORAD ID.

Additional telemetry servers used for this satellite can be specified with the
``telemetry_servers`` field (see ``python/satyaml/PW-Sat2.yml`` for an example).

The ``data`` section indicates the different kinds of data transmissions that
the satellite makes, and gives the decoders for them. The following can be used:

* ``telemetry``, which specifies a telemetry decoder giving out the telemetry
  definition (see :ref:`Telemetry parser`)

* ``file`` or ``image``, which specify a file receiver or image receiver giving
  out the ``FileReceiver`` or ``ImageReceiver`` class (see :ref:`File and Image receivers`)

* ``decoder``, which specifies a custom decoder from
  ``satellites.components.datasinks``. This is used for more complex decoders
  not covered by the above.

* ``unknown``, which specifies that the data format is not known, so hex dump
  should be used to show the data to the user

The ``transmitters`` section lists the different transmitters used by the
satellite, their properties, and ties them to the entries in the
``data`` section according as to which data is sent by each of the transmitters.
A transmitter is understood as a specific combination of a frequency,
modulation and coding.

Each transmitter has a name (such as ``1k2 FSK downlink``) which is currently
used only for documentation purposes, a ``frequency``, which gives the downlink
frequency in Hz (currently used only for documentation), a ``modulation``, that
specifies the demodulator component to use, a ``baudrate``, in symbols per
second, a ``framing``, that specifies the deframer to use, and a list of
``data`` that has entries referring to the items in the ``data`` section.

The modulations allowed in the ``modulation`` field are the following:

* ``AFSK``, for which the :ref:`AFSK demodulator` is used

* ``FSK``, for which the :ref:`FSK demodulator` with Subaudio set to ``False``
  is used

* ``FSK subaudio``, for which the :ref:`FSK demodulator` with Subaudio set to
  ``True`` is used

* ``BPSK``. Coherent BPSK, for which the :ref:`BPSK demodulator` with
  Differential and Manchester set to ``False`` is used

* ``BPSK Manchester``. Coherent Manchester-encoded BPSK, for which the
  :ref:`BPSK demodulator` with Differential set to ``False`` and Manchester set
  to ``True`` is used

* ``DBPSK``. Differentially-encoded BPSK, for which the :ref:`BPSK demodulator`
  with Differential set to ``True`` and Manchester set to ``False`` is used to
  perform non-coherent demodulation

* ``DBPSK Manchester``. Differentially-encoded and Manchester-encoded BPSK, for
  which the :ref:`BPSK demodulator` with Differential and Manchester set to
  ``True`` is used to perform non-coherent demodulation

The ``AFSK`` modulation also needs the ``deviation`` and ``af_carrier`` fields
that indicate the AFSK tone frequencies in Hz, as in the AFSK demodulator. Optionally,
it is possible to indicate the deviation of the FM modulation using the ``fm_deviation``
field. By default, an FM deviation of 3 kHz is assumed.

The framings allowed in the ``framing`` field are the following:

* ``AX.25``, `AX.25`_ with no scrambling (see :ref:`AX.25 deframer`)

* ``AX.25 G3RUH``, `AX.25`_ with G3RUH scrambling (see :ref:`AX.25 deframer`)

* ``AX100 ASM+Golay``, GOMspace NanoCom AX100 in ASM+Golay mode (see
  :ref:`GOMspace AX100 deframer`)

* ``AX100 Reed Solomon``, GOMspace NanoCom AX100 in Reed-Solomon mode (see
  :ref:`GOMspace AX100 deframer`)

* ``U482C``, the GOMspace NanoCom U482C (see :ref:`GOMspace U482C deframer`)

* ``AO-40 FEC``, the AO-40 FEC protocol (see :ref:`AO-40 FEC deframer`)

* ``AO-40 FEC short``, AO-40 FEC protocol with short frames, as used by SMOG-P
  and ATL-1

* ``AO-40 FEC CRC-16-ARC``, the AO-40 FEC protocol with an CRC-16 ARC, as used by
  SMOG-1

* ``AO-40 FEC CRC-16-ARC short``, AO-40 FEC protocol with short frames and a
  CRC-16 ARC, as used by SMOG-1

* ``CCSDS Uncoded``, uncoded CCSDS codeworks (see :ref:`CCSDS deframers`)

* ``CCSDS Reed-Solomon``, CCSDS Reed-Solomon TM codewords (see :ref:`CCSDS deframers`)

* ``CCSDS Concatenated``, CCSDS Concatenated TM codewords (see :ref:`CCSDS deframers`)

* ``3CAT-1``, custom framing used by 3CAT-1. This uses a CC1101 chip with PN9
  scrambler and a (255,223) Reed-Solomon code for the payload

* ``Astrocast FX.25 NRZ-I``, custom framing used by Astrocast 0.1. This is a
  somewhat non compliant `FX.25`_ variant.

* ``Astrocast FX.25 NRZ``, custom framing used by Astrocast 0.1. This is a
  somewhat non compliant `FX.25`_ variant that is identical to the FX.25 NRZ-I
  mode except that NRZ is used instead of NRZ-I.

* ``AO-40 uncoded``, uncoded AO-40 beacon. It uses 512 byte frames and a CRC-16

* ``TT-64``, custom framing used by QB50 AT03, which uses a Reed-Solomon (64,48)
  code and CRC16-ARC

* ``ESEO``, custom framing used by ESEO. It uses a custom protocol vaguely
  similar to AX.25 with some form of G3RUH scrambling and a (255,239)
  Reed-Solomon code

* ``Lucky-7``, custom framing used by Lucky-7, which uses a SiLabs Si4463
  transceiver with a PN9 scrambler and a CRC-16

* ``Reaktor Hello World``, custom framing used by Reaktor Hello World. It uses a
  Texas Intruments CC1125 transceiver with a PN9 scrambler and a CRC-16.

* ``Light-1``, custom framing used by Light-1 and BlueWalker 3. It is the same
  as the ``Reaktor Hello World`` framing, but uses a different syncword.

* ``S-NET``, custom framing used by S-NET, which uses BCH FEC and interleaving

* ``SALSAT``, custom framing used by SALSAT. It is like ``S-NET``, but without the bugs
  in the CRC implementation.

* ``Swiatowid``, custom framing used by Swiatowid for image transmission, which
  includes a (58,48) Reed-Solomon code and a CRC-16CCITT.

* ``NuSat``, custom framing used by ÑuSat with a (64, 60) Reed-Solomon code and a CRC-8

* ``K2SAT``, custom framing used by K2SAT for image transmission. This uses the
  CCSDS r=1/2, k=7 convolutional code and the IESS-308 (V.35) asynchronous scrambler.

* ``LilacSat-1``, low latency decoder for LilacSat-1 codec2 digital voice and
  image data. This uses the CCSDS r=1/2, k=7 convolutional code and interleaved
  telemetry and Codec2 digital voice

* ``AAUSAT-4``, custom framing used by AAUSAT-4, which is similar to the CCSDS
  Concatenated coding

* ``NGHam``, `NGHam`_ protocol

* ``NGHam no Reed Solomon``, `NGHam`_ protocol without Reed-Solomon, as used by
  FloripaSat-1

* ``SMOG-P RA``, Repeat-Accumulate FEC as used by SMOG-P and ATL-1

* ``SMOG-1 RA``, Repeat-Accumulate FEC as used by SMOG-1. The difference with
  ``SMOG-P RA`` is a longer 48 bit syncword (instead of 16 bit) and the inclusion
  of a CRC-16 ARC to check frame integrity.

* ``MRC-100 RA``, Repeat-Accumulate FEC as used by SMOG-1. The difference with
  ``SMOG-P RA`` is a 32-bit syncword, a smaller frame size, and the inclusion of
  a CRC-16-CCITT-FALSE in the second and third byte to check frame integrity.

* ``SMOG-P Signalling``, custom signalling frames as used by SMOG-P and ATL-1

* ``SMOG-1 Signalling``, custom signalling frames as used by SMOG-1. The difference
  with ``SMOG-P Signalling`` is the addition of a different PRBS to mark transitions
  to TX mode.

* ``OPS-SAT``, custom framing used by OPS-SAT, which consists of AX.25 frames
  with CCSDS Reed-Solomon codewords as payload

* ``UA01``, non-AX.25 compliant framing used by QB50 UA01, which is like regular
  AX.25 but with two layers of NRZ-I encoding

* ``Mobitex``, the Mobitex protocol, used by the D-STAR ONE satellites and some
  Russian whose communications payload has also been built by German Orbital Systems

* ``Mobitex-NX``, the Mobitex-NX protocol, used by the BEESAT and TECHNOSAT satellites
  from TU Berlin

* ``FOSSATSAT``, a custom protocol used by FOSSASAT

* ``AISTECHSAT-2``, a custom CCSDS-like protocol used by AISTECHSAT-2

* ``AALTO-1``, custom framing used by AALTO-1. It uses a
  Texas Intruments CC1125 transceiver with a PN9 scrambler and a CRC-16 CCITT
  (as in AX.25)

* ``Grizu-263A``, custom framing used by Grizu-263A. It uses a Semtech SX1268
  with a PN9 scrambler and CRC-16.

* ``IDEASSat``, custom framing used by IDEASSat. It uses NRZI encoding,
  an 1N8 UART-like encoding with MSB-bit-ordering,
  and HDLC ``0x7e`` flags to mark the frame boundaries.

* ``YUSAT``, custom framing used by YUSAT-1. It is like AX.25 but without
  bit stuffing, LSB byte endianness, and NRZ-I.

* ``AX5043``, FEC framing used by the AX5043 transceiver IC. This uses a convolutional
  code, a 4x4 interleaver, and HDLC framing with the CRC16-USB.

* ``USP``, the `Unified SPUTNIX Protocol`_, which is based on CCSDS concatenate frames
  with custom synchronization and a PLS based on DVB-S2.

* ``DIY-1``, the custom framing used by DIY-1, which uses an RFM22 chip transceiver.

* ``BINAR-1``, the custom framing used by the BINAR-1 satellite.

* ``BINAR-2``, the custom framing used by the BINAR-2, 3 and 4 satellites.

* ``Endurosat``, the custom framing used by the Endurosat modem.

* ``SanoSat``, the custom framing used by SanoSat-1.

* ``FORESAIL-1``, the custom framing used by FORESAIL-1. It is the same as the
  AX-100 ASM mode, but the ASM used is the CCSDS ASM ``0x1ACFFC1D``.

* ``HSU-SAT1``, the custom framing used by HSU-SAT1.

* ``GEOSCAN``, the custom framing used by GEOSCAN-EDELVEIS.

* ``SPINO``, the custom framing used by the SPINO payload on INSPIRE-Sat7.

* ``QUBIK``, the custom framing used by QUBIK.

* ``Hades``, the custom framing used by HADES-D.

Some framings, such as the CCSDS protocols need the additional field
``frame size`` to indicate the frame size.

The CCSDS framings need several additional fields to specify the details of the
CCSDS protocol. These are:

* ``precoding: differential`` should be used to specify differential
  precoding. It if is not specified, differential precoding will
  not used.

* ``RS basis:`` should have the value ``conventional`` or ``dual`` to specify the
  Reed-Solomon basis. This field is mandatory.

* ``RS interleaving:`` should be used to specify interleaved Reed-Solomon
  codewords. It defaults to 1 (i.e., no interleaving) if not specified.

* ``scrambler:`` should have the value ``CCSDS`` or ``none``. This field is
  optional and defaults to ``CCSDS`` if not specified.

* ``convolutional:`` should have one of the following values: ``CCSDS``,
  ``NASA-DSN``, ``CCSDS uninverted``, ``NASA-DSN uninverted``.  This field is
  optional and defaults to ``CCSDS`` if not specified.


The ``AX100 ASM+Golay`` mode also supports the ``scrambler`` field, with the
possible values ``CCSDS`` and ``none``. The default is ``CCSDS``, but the value
``none`` can be used in case the scrambler needs to be disabled (which is a
rarely used feature).

The following example shows how transports are indicated in SatYAML files.

.. code-block:: yaml

   name: KS-1Q
   norad: 41845
   data:
     &tlm Telemetry:
       telemetry: csp
   transports:
     &kiss KISS:
       protocol: KISS KS-1Q
       data:
       - *tlm
   transmitters:
     20k FSK downlink:
       frequency: 436.500e+6
       modulation: FSK
       baudrate: 20000
       framing: CCSDS Concatenated dual
       frame size: 223
       transports:
      - *kiss

Instead of specifying a ``data`` entry in the transmitter, a ``transports``
entry is used instead. Transports are defined in a section above. They have a
name, used for documentation purposes, a ``protocol``, and a list of ``data``
entries to tie them with the appropriate data decoders.

The allowable transport protocols are the following:

* ``KISS``, KISS protocol with a control byte (see :ref:`KISS transport`)

* ``KISS no control byte``, KISS protocol with no control byte (see
  :ref:`KISS transport`)

* ``KISS KS-1Q``, KISS variant used by KS-1Q, which includes a header before the
  KISS bytes

.. _YAML: https://yaml.org/
.. _AX.25: http://www.ax25.net/
.. _FX.25: https://en.wikipedia.org/wiki/FX.25_Forward_Error_Correction
.. _NGHam: https://github.com/skagmo/ngham
.. _Unified SPUTNIX Protocol: https://sputnix.ru/tpl/docs/amateurs/USP%20protocol%20description%20v1.04.pdf

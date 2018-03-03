# gr-satellites
GNU Radio decoders for several Amateur satellites.

This repository is a collection of GNU Radio decoders for the telemetry of
several satellites. The decoders don't need a graphical interface to run, so
they can be used in an embedded or remote computer. The decoders are designed to
run in real time and print the telemetry packets to the terminal as they are
received. Optionally, the telemetry packets can be uploaded in real time to the
[SatNOGS database](http://db.satnogs.org/) or any other telemetry server
that implements the SiDS (Simple Downlink Sharing Convention) protocol.

It is also possible to use the decoder with a recording (audio WAV or IQ file),
in case that the telemetry wasn't processed in real time. To do this, one has to
know the time and date at which the recording was started and the recording has
to be played back at normal speed. This allows the decoder to compute the
correct timestamps for the packets when uploading them to the telemetry
server. It also simplifies Doppler correction of the recording with Gpredict if
the recording was not Doppler corrected.

## Dependencies

gr-satellites requires the git version of GNU Radio. A stable release may be
used, but note the following:

  * The "Correlate Access Code - Tag" block has changed slightly in the git
    version (it now allows floats as well as bytes). The new block is
    incompatible with the older one, so the flowgraphs using "Correlate Access
    Code - Tag" will complain of missing blocks when using a stable release of
    GNU Radio. It is possible to replace the "Correlate Access Code - Tag" block
    by hand with the older version and the flowgraphs should then
    work. Especially, you have to look at the hierarchical blocks
    `sync_to_pdu.grc` and `sync_to_pdu_packed.grc` in gr-satellites.
  * There is a bug in the "Additive scrambler" block. The
    [bug fix](https://github.com/gnuradio/gnuradio/commit/e3ad82e6d93ea05d3b096673abf609f9e146f578)
    is only in the
    git version of GNU Radio. If using a stable release of GNU Radio, do not
    expect this block to work. However, the "Additive scrambler" is only used to
    decode CCSDS scrambling. Decoders using G3RUH scrambling or no scrambler
    should work fine.

Required dependencies:

  * Phil Karn's KA9Q `libfec`. A fork that builds in modern linux systems can be found
    [here](https://github.com/daniestevez/libfec).
  * [construct](https://construct.readthedocs.io/en/latest/), at least version 2.8.

The following GNUradio out-of-tree modules are only required for the decoder of
one particular satellite. You may install only the ones you're interested in.

  * [gr-aausat](https://github.com/daniestevez/gr-aausat) AAUSAT-4 decoder and
    telemetry parser
  * [beesat-sdr](https://github.com/daniestevez/beesat-sdr) BEESAT decoder and TNC
  * [gr-lilacsat](https://github.com/bg2bhc/gr-lilacsat) This only needs to be installed
  if you want to submit telemetry to HIT. A complete decoder which does not use gr-lilacsat
  is already included in gr-satellites.

If you want to use the realtime image decoder for BY70-1, you also need to install
[feh](https://feh.finalrewind.org/).

## Hierarchichal flowgraphs

Some of the decoders use hierarchichal flowgraphs. These are placed in the
folder `apps/hierarchical`. The hierarchical flowgraphs must be compiled and
installed before using any of the flowgraphs which include them.

To compile and install the hierarchical flowgraphs, the script
`compile_hierarchical.sh` in the root folder can be used.

## Usage

The signal is fed to the decoders using a UDP stream. The format used is the
same that [gqrx](http://gqrx.dk/doc/streaming-audio-over-udp) uses. Therefore,
you can use gqrx to feed the signal to the decoders. You will have to set the
proper frequency, mode and bandpass in gqrx for the satellite you want to
receive. This is probably the easiest way to start using the decoders from
gr-satellites. Gqrx supports Doppler correction with Gpredict.

*Note:* The exact frequency setting for optimal decoding may need to tuned to
properly center the signal within the passband.  This is especially true for
SSB signals. One way to do this is by using this the Radio Control panel within
Gpredict to make small adjustments while monitoring signals in the gqrx
passband.

It is also possible to use the frontend streamers from
[gr-frontends](https://github.com/daniestevez/gr-frontends). This allow to
stream from different SDR hardware without using a GUI SDR program. It is
possible to perform Doppler correction with Gpredict. There are also frontend
streamers to use a conventional receiver connected via soundcard and recordings
(audio WAV and IQ).

Each satellite has its own decoder in the `apps/` folder. You can open the
`.grc` file with `gnuradio-companion` and edit the parameters (they are on the
upper part of the flowgraph). You can also generate and run the corresponding
`.py` script and specify the parameters on the command line. Use the -h flag to
get help on how to specify the parameters. The decoder will printing each
telemetry packet in the terminal as soon as it receives it.

## Satellites supported

  * `sat_3cat2`
    [3CAT-2](https://nanosatlab.upc.edu/en/missions-and-projects/3cat-2), which
    transmits 9k6 AX.25 BPSK telemetry in the 2m band. You must use wide SSB
    mode to receive this satellite.
  * `aausat_4`
    [AAUSAT-4](http://www.space.aau.dk/aausat4/), which transmits 2k4 or 9k6 GFSK
    telemetry in the 70cm band. It uses the CSP protocol and FEC with an r=1/2, k=7
    convolutional code and a (255,223) Reed-Solomon code. You must use FM mode
    to receive this satellite.
  * `ao40_uncoded`
    [AO-40](https://en.wikipedia.org/wiki/OSCAR_40), which transmitted 400bps BPSK
    telemetry in several bands. This decoder is for the uncoded telemetry, which
    did not use any forward error correction. The specifications of the telemetry
    can be found [in this document](http://www.amsat-dl.org/p3d/tlmspec.txt). AO-40
    is no longer functional, but it is of high historic interest. You must use SSB
    mode to receive this satellite.
  * `ao73`
    [AO-73 (FUNcube)](https://funcube.org.uk/), which transmits 1k2 BPSK
    telemetry in the 2m band. It uses the AO-40 FEC protocol, which includes
    block interleaving, an r=1/2, k=7 convolutional code, CCSDS scrambling and
    two interleaved (160,128) Reed-Solomon codes. You must use SSB mode to
    receive this satellite.
  * `aisat`
    [AISAT](https://directory.eoportal.org/web/eoportal/satellite-missions/a/aisat),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver with the CSP protocol and FEC with a (255,223)
    Reed-Solomon code. It also uses a CCSDS scrambler. There is no telemetry
    parser yet, as the beacon format is unknown. This satellite has an AIS
    receiver on board. You must use FM mode to receive this satellite.
  * `at03`
    [QB50 AT03 (PEGASUS)](https://spacedatacenter.at/pegasus/),
    which transmits 9k6 GFSK telemetry in the 70cm band. It uses the TT-64
    protocol, which includes a CRC16-ARC and FEC with a (64,48) Reed-Solomon
    code. Reed-Solomon decoding is done with the
    [rscode](http://rscode.sourceforge.net/) library. You must use FM mode to
    receive this satellite.
  * `athenoxat-1`
    [ATHENOXAT-1](http://space.skyrocket.de/doc_sdat/athenoxat-1.htm),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and FEC with a (255,223)
    Reed-Solomon code. It also uses a CCSDS scrambler. There is no telemetry
    parser yet, as the beacon format is unknown. This satellite is on a low
    inclination orbit, so it can only be received near the equator. You must
    use FM mode to receive this satellite.
  * `au02`
    [QB50 AU02 (UNSW-EC0)](http://www.acser.unsw.edu.au/QB50),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and FEC with an r=1/2, k=7
    convolutional code and a (255,223) Reed-Solomon code. It also uses a CCSDS
    scrambler. You must use FM mode to receive this satellite.
  * `au03`
    [QB50 AU03 (i-INSPIRE II)](http://sydney.edu.au/inspire-cubesat/project/index.shtml),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and FEC with an r=1/2, k=7
    convolutional code and a (255,223) Reed-Solomon code. It also uses a CCSDS
    scrambler. You must use FM mode to receive this satellite.
  * `beesat`
    [BESAT-1,-2 and -4](http://space.skyrocket.de/doc_sdat/beesat.htm), which
    transmit 4k8 FSK telemetry in the 70cm band. They use the Mobitex-NX
    protocol, which includes FEC with a (12,8,3) linear code and CRC-16CCITT for
    error detection. You must use FM mode to receive these satellites.
  * (inactive) `by701`
    [BY70-1](http://space.skyrocket.de/doc_sdat/by70-1.htm), which transmits 9k6
    BPSK telemetry in the 70cm band. It uses FEC with an r=1/2, k=7
    convolutional code and a (255,223) Reed-Solomon code (the same as the
    LilacSat-2 9k6 BPSK telemetry). You must use wide SSB mode to receive this
    satellite. It has an optical camera on board and it transmits JPEG images
    together with the telemetry. `by701` includes a complete telemetry decoder
    and image receive software. This satellite launched on 28 December 2016 into a 520x220km
    orbit. The perigee is too low because of a problem in the launch. BY70-1 reentered
    on 18 February 2017. You must use wide SSB mode to receive this satellite.
  * `ca03`
    [QB50 CA03 (Ex-Alta 1)](https://albertasat.ca/amateur-radio-information/),
    which transmits 4k8 GFSK telemetry in the 70cm band. It uses the CSP protocol
    and FEC with a (255,223) Reed-Solomon code. It also uses a G3RUH scrambler. The
    transceiver is the GomSpace NanoCom AX100, the same transceiver used in
    GOMX-3. You must use FM mode to receive this satellite.
  * `cz02`
    [QB50 CZ02 (VZLUSAT-1)](http://vzlusat1.cz/en/),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and a (255,223) Reed-Solomon code.
    It also uses a CCSDS scrambler. You must use FM mode to receive this satellite.
  * `dsat`
    [D-SAT](https://www.dsat.space/), which transmits 4k8 AF GMSK telemetry in
    the 70cm band. It uses a NanoCom U482C transceiver with the CSP protocol and
    FEC with a (255,223) Reed-Solomon code. It also uses a CCSDS scrambler. This
    receiver supports sending frames to the D-SAT groundstation software, which
    decodes telemetry. See
    [this post](http://destevez.net/2017/08/d-sat-support-added-to-gr-satellites/)
    for detailed instructions. D-SAT transmits JPEG image from an onboard
    camera. This decoder includes an image decoder which shows the images in
    real time using feh.
  * `galassia`
    [GALASSIA](https://eoportal.org/web/eoportal/satellite-missions/content/-/article/galass-1),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver with the the CSP protocol and FEC with a (255,223)
    Reed-Solomon code. It also uses a CCSDS scrambler. There is no telemetry
    parser yet, as the beacon format is unknown. This satellite is on a low
    inclination orbit, so it can only be received near the equator. You must
    use FM mode to receive this satellite.
  * `gomx_1`
    [GOMX-1](https://directory.eoportal.org/web/eoportal/satellite-missions/g/gomx-1),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver with the CSP protocol and FEC with a (255,223)
    Reed-Solomon code. It also uses a CCSDS scrambler. The beacons
    include information from ADS-B beacons transmitted by terrestrial
    aircraft. You must use FM mode to receive this satellite.
  * (inactive) `gomx_3`
    [GOMX-3](https://directory.eoportal.org/web/eoportal/satellite-missions/g/gomx-3),
    which transmits 19k2 GFSK telemetry in the 70cm band. It uses the CSP
    protocol and FEC with a (255,223) Reed-Solomon code. It also uses a G3RUH
    scrambler. The beacons include information from ADS-B beacons transmitted by
    terrestrial aircraft. GOMX-3 reentered on 18 October 2016. You
    must use FM mode to receive this satellite.
  * `gr01`
    [QB50 GR01 (DUTHSat)](http://www.duthsat.gr/),
    which transmits 1k2 or 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. For 1k2 telemetry you must use SSB mode, while for 9k6 telemetry you
    must use wide SSB mode.
  * `il01`
    [QB50 IL01 (DUCHIFAT-2)](http://www.h-space-lab.org/php/hoopoe-en.php),
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. You must use wide SSB mode to receive this satellite.
  * `indus`
    Mystery satellite transmitting on 435.080MHz using 1k2 FSK AX.25 and the
    callsign INDUSR-10 (see [here](https://twitter.com/ea4gpz/status/952593838266298368)).
  * `kr01`
    [QB50 KR01 (LINK)](http://space.skyrocket.de/doc_sdat/link.htm),
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. Currently it transmits 1k2 telemetry (safe mode perhaps), so you
    must use SSB mode to receive this satellite.
  * `ks_1q`
    [KS-1Q](http://space.skyrocket.de/doc_sdat/cas-2t.htm), which transmits 20k
    FSK telemetry in the 70cm band. It uses KISS framed CSP packets and FEC with
    an r=1/2, k=7 convolutional code and a (255,223) Reed-Solomon code (the
    protocol is very similar to LilacSat-2). It also uses a CCSDS scrambler.
    You must use FM mode to receive this satellite.
  * `lilacsat2`
    [LilacSat-2](http://lilacsat.hit.edu.cn/?page_id=257), which transmits 9k6
    BPSK, 4k8 GFSK and FM subaudio telemetry in the 70cm band. It uses FEC with
    an r=1/2, k=7 convolutional code and a (255,223) Reed-Solomon code. The
    decoders for this satellite are organized a bit different from
    the decoders for other satellites, because LilacSat-2 transmits in several
    different frequencies using several different modes. You can use `lilacsat2`
    as a usual single-frequency single-mode decoder. You can use gqrx or one of
    the frontends from gr-frontends to feed an UDP audio stream  to `lilacsat2`.
    However, you can decode only one frequency and mode using this method. You
    should tune to 437.200MHz in wide SSB mode to receive 9k6 BPSK telemetry, to
    437.200MHz in FM mode to receive FM subaudio telemetry and to 437.225MHz in
    FM mode to receive 4k8 GFSK telemetry. `lilacsat2` will recognise the
    telemetry format automatically. To receive all the frequencies and modes at
    the same time, you need to use an SDR receiver. The receivers
    `lilacsat_fcdpp` and `lilacsat_rtlsdr` can be used with a FUNcube Dongle
    Pro+ and an RTL-SDR respectively. These are complete receivers and
    decoders. They submit telemetry to the SatNOGS database and can use Doppler
    correction with Gpredict, in the same way as the frontends from
    gr-frontends. For `lilacsat_fcdpp` and `lilacsat_rtlsdr`,
    when using Doppler correction with Gpredict, you have to set
    437.200MHz as the downlink frequency in Gpredict.
  * `nayif1`
    [Nayif-1](https://amsat-uk.org/satellites/communications/nayif-1/),
    which transmits 1k2 BPSK
    telemetry in the 2m band. It uses the AO-40 FEC protocol, which includes
    block interleaving, an r=1/2, k=7 convolutional code, CCSDS scrambling and
    two interleaved (160,128) Reed-Solomon codes. You must use SSB mode to
    receive this satellite.
  * `nusat`
    [ÑuSat-1 and -2](http://space.skyrocket.de/doc_sdat/nusat-1.htm),
    which transmit 40k FSK telemetry in the 70cm band. They use FEC with a
    (64, 60) Reed-Solomon code and a CRC-8. Since a sample rate of 48kHz is too
    low to work with 40k FSK, the flowgraph is prepared to use an IQ recording
    at 192kHz. Depending on the characteristics of your IQ recording you may
    need to edit the flowgraph. The Reed-Solomon decoder is taken from the
    [rscode](http://rscode.sourceforge.net/) library. A sample IQ recording is
    included in [satellite-recordings](https://github.com/daniestevez/satellite-recordings).
  * `picsat`
    [PicSat](http://picsat.obspm.fr/),
    which transmits 1k2 or 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. For 1k2 telemetry you must use SSB mode, while for 9k6 telemetry you
    must use wide SSB mode.
  * `tw_1a`, `tw_1b`, `tw_1c`
    [TW-1A](http://space.skyrocket.de/doc_sdat/shangkeda-2.htm),
    [TW-1B](http://space.skyrocket.de/doc_sdat/njust-2.htm),
    [TW-1C](http://space.skyrocket.de/doc_sdat/njfa-1.htm), which transmit 4k8
    GFSK telemetry in the 70cm band. They use the CSP protocol and FEC with a
    (255,223) Reed-Solomon code. They also use a G3RUH scrambler. The
    transceiver is the GomSpace NanoCom AX100, the same transceiver used in
    GOMX-3. There is no beacon parser yet, as the beacon format is unknown.
    The only difference between the 3 receivers is that the NORAD ID is set for
    the correct satellite when doing telemetry submission. You must use FM mode
    to receive these satellites.
  * `ty_2`, `ty_6`
    [TY-2](http://space.skyrocket.de/doc_sdat/xiaoxiang-1.htm)
    and [TY-6](http://space.skyrocket.de/doc_sdat/ty-6.htm), which transmit
    9k6 GMSK telemetry in the 70cm band. They use the GomSpace NanoCom AX100
    transceiver in ASM+Golay mode. This uses a CCSDS scrambler and a (255,223)
    Reed-Solomon code. The telemetry format is unknown. The only
    difference between the 2 receivers is that the NORAD ID is set for the
    correct satellite when doing telemetry submission. You must use FM mode to
    receive these satellites.
  
  * `ukube1`
    [UKube-1 (FUNcube-2)](https://amsat-uk.org/satellites/communications/ukube-1/),
    which transmits 1k2 BPSK
    telemetry in the 2m band. It uses the AO-40 FEC protocol, which includes
    block interleaving, an r=1/2, k=7 convolutional code, CCSDS scrambling and
    two interleaved (160,128) Reed-Solomon codes. You must use SSB mode to
    receive this satellite.

## Installing GNUradio OOT modules

This is the usual procedure to build and install an OOT module:

```bash
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
```

## Submitting telemetry

To sumbit telemetry to the [SatNOGS database](http://db.satnogs.org/) (or
another SiDS telemetry server), you have to specify your callsign and
coordinates. The callsign is specified using the `--callsign` parameter and the
latitude and longitude are specified using the `--latitude` and `--longitude`
parameters if you are using the `.py` script. If you are using the `.grc` file
with `gnuradio-companion`, you can set these parameters by editing the boxes on
the upper part of the flowgraph.

The format for the latitude and longitude is of the form `00.00000` or
`-00.00000`. The `-` means South (for latitude) or West (for longitude).

If you want to submit telemetry from a recording, you have to specify the UTC
date and time when the recording was started. This allows the decoder to compute
the proper timestamp for the packets. The format is `YYYY-MM-DD HH:MM:SS` and it
is specified using `--recstart` if using the `.py` script or with the parameter
box on the upper part of the flowgrah if using the `.grc` file with
`gnuradio-companion`.

It is also **very important** that the decoder and the recording streamer are
started simultaneously. This can be achieved by something like
```bash
gr-frontends/wav_48kHz.py -f recording.wav & \
gr-satellites/sat_3cat2.py --recstart="2016-01-01 00:00" --callsign=N0CALL --latitude=0.000 --longitude=0.000
```

## KISS submitter

There are many satellites that use standard packet radio AX.25 and can be
received with any software TNC such as
[Direwolf](https://github.com/wb2osz/direwolf). gr-satellites includes
`kiss_submitter` to perform telemetry submission when using a software TNC.

`kiss_submitter` connects to the software TNC as a KISS TCP client. The frames
received by the software TNC will be submitted by `kiss_submitter`. To use
`kiss_submitter`, you must specify your callsign and coordinates as when
submitting telemetry using any of the decoders. You also need to specify the
NORAD ID of the satellite you are receiving. This can be done by setting using
`--norad` if using the `.py` script or with the parameter if using the `.grc`
file. It is very important that you set the NORAD ID correctly. You can search
the NORAD ID in [celestrak](http://celestrak.com/satcat/search.asp).

You must start the software TNC first and the run the `.py` script or the `.grc`
file for `kiss_submitter`.

## Submitting telemetry to HIT severs (LilacSat, BY70-1, etc.)

It is also possible to use the flowgraphs in gr-satellites to submit telemetry
to the Harbin Institute of Technology servers using `proxy_publish.py` in
`gr-lilacsat/examples/proxy_publish`. To enable this, you must open the
flowgraphs in `gnuradio-companion` and enable the "Socket PDU" block (usually on
the lower right corner of the flowgraph). This block is disabled by default
because when it is enabled the flowgraph won't run unless `proxy_publish.py` is
running. Also see [this information](http://lilacsat.hit.edu.cn/?p=559) about
how to set the proper ports in `proxy_publish.py`.

## Hints for receiving different modes

### Wide SSB

Some modes (9k6 BPSK, for instance) need to be received using SSB mode, but the
bandwidth of the signal is larger than the usual 3kHz bandwidth of a
conventional SSB receiver. Therefore, an SDR receiver or a heavily modified
conventional SSB receiver is needed (a 9k6 BPKS signal is about 15kHz wide).

The decoders for satellites using these kind of *wide SSB* signals expect the
signal to be centred at an audio frequency of 12kHz. This means that you have to
dial in USB mode to a frequency 12kHz lower than the nominal frequency of the
satellite (+/- Doppler). If your SDR program allows this (gqrx does), the best
idea is to set an SSB audio filter from 0Hz to 24kHz and then tune the signal in
the middle of the passband. Alternatively, you can use the `--bfo` parameter if
using the `.py` file or edit the corresponding parameter in the `.grc` file to
use a frequency different from 12kHz.

If you are using the wide SSB receivers from
[gr-frontends](https://github.com/daniestevez/gr-frontends) you don't need to do
anything special, as these receivers already dial in USB mode to a frequency
12kHz than the nominal and use a 24kHz wide audio filter.

### Receiving FSK and sideband inversion

We are all used to the two SSB modes: USB (which is sideband-preserving) and LSB
(which is sideband-inverting). When receiving FM (or FSK), there is the same
concept. An FM receiver can be sideband-preserving or sideband-inverting. This
makes no difference when receiving analog FM (both sound the same) or AX.25
(which uses a differential protocol).

However, some satellites which use FSK (AAUSAT-4 and GOMX-3, for instance) need
a sideband-preserving FM receiver. If your receiver is sideband-inverting, you
can use set `--invert=-1` while running the `.py` file or edit the corresponding
parameter in the `.grc` file to invert the signal again in the decoder and
recover the original signal with the correct sidebands.

## Other hints

To run the decoder and save the output to a file, it is possible to do something
like

```bash
python2 -u aausat_4.py | tee /tmp/aausat4.log
```

This will both print the beacons in real time and also save all the output to
the text file `/tmp/aausat4.log`.

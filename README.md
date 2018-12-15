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

## Installation

First you need to install the dependencies (see below).

After this, gr-satellites must be installed as any other GNU Radio out-of-tree
module. The producedure usually boils down to doing the following:

```bash
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
```

Finally, you need to compile the hierarchical flowgraphs include in
gr-satellites (see below).

## Dependencies

gr-satellites requires GNU Radio version 3.7.12.0 or new.
An older version may be used, but note the following:

  * The "Correlate Access Code - Tag" block has changed slightly in the 3.7.12.0
    version (it now allows floats as well as bytes). The new block is
    incompatible with the older one, so the flowgraphs using "Correlate Access
    Code - Tag" will complain of missing blocks when using an older version of
    GNU Radio. It is possible to replace the "Correlate Access Code - Tag" block
    by hand with the older version and the flowgraphs should then
    work. Especially, you have to look at the hierarchical blocks
    `sync_to_pdu.grc` and `sync_to_pdu_packed.grc` in gr-satellites.
  * There is a bug in the "Additive scrambler" block. The
    [bug fix](https://github.com/gnuradio/gnuradio/commit/e3ad82e6d93ea05d3b096673abf609f9e146f578)
    was introduced in version 3.7.12.0 of GNU Radio.
    If using an older release of GNU Radio, do not
    expect this block to work completely. However, the "Additive scrambler" is only used to
    decode CCSDS scrambling. Decoders using G3RUH scrambling or no scrambler
    should work fine.

Required dependencies:

  * Phil Karn's KA9Q `libfec`. A fork that builds in modern linux systems can be found
    [here](https://github.com/daniestevez/libfec).
  * [construct](https://construct.readthedocs.io/en/latest/), at least version 2.9.
  * [requests](https://pypi.org/project/requests/2.7.0/).

The following GNUradio out-of-tree modules are only required for the decoder of
one particular satellite. You may install only the ones you're interested in.

  * [gr-aausat](https://github.com/daniestevez/gr-aausat) AAUSAT-4 decoder and
    telemetry parser
  * [beesat-sdr](https://github.com/daniestevez/beesat-sdr) BEESAT and TECHNOSAT decoder and TNC
  * [gr-lilacsat](https://github.com/bg2bhc/gr-lilacsat) This only needs to be installed
  if you want to submit telemetry to HIT. A complete decoder which does not use gr-lilacsat
  is already included in gr-satellites.
  * [PW-Sat2 FramePayloadDecoder](https://github.com/PW-Sat2/FramePayloadDecoder) This only
  needs to be installed if you want to parse frames from PW-Sat2. See the instructions
  [here](https://destevez.net/2018/12/decoding-pw-sat2-with-gr-satellites/).

If you want to use any of the realtime image decoders, you also need to install
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
Gpredict. This allows the user to make small adjustments while monitoring signals
in the gqrx passband.

It is also possible to use the frontend streamers from
[gr-frontends](https://github.com/daniestevez/gr-frontends). These allow to
stream data by UDP from different SDR hardware without using a GUI SDR program. It
remains to perform Doppler correction with Gpredict. There are also frontend
streamers to use a conventional receiver connected via soundcard and recordings
(audio WAV and IQ).

Each satellite has its own decoder in the `apps/` folder. You can open the
`.grc` file with `gnuradio-companion` and edit the parameters (they are on the
upper part of the flowgraph). You can also generate and run the corresponding
`.py` script and specify the parameters on the command line. Use the -h flag to
get help on how to specify the parameters. The decoder will printing each
telemetry packet in the terminal as soon as it receives it.

## Satellites supported

  * `sat_1kuns_pf`
    [1KUNS-PF](https://en.wikipedia.org/wiki/1KUNS-PF),
    which transmits
    1k2 GMSK telemetry in the 70cm band. It uses the GomSpace NanoCom AX100
    transceiver in ASM+Golay mode. This uses a CCSDS scrambler and a (255,223)
    Reed-Solomon code. You must use FM mode to receive this satellite (437.300 MHz).
    1KUNS-PF transmits JPEG images from an onboard
    camera. This decoder includes an image decoder which shows the images in
    real time using feh.
  * `sat_3cat_1`
    [3CAT-1](https://nanosatlab.upc.edu/en/missions-and-projects/3cat-1),
    which transmits 9k6 GFSK telemetry in the 70cm band. It uses a Texas
    Intruments CC1101 transceiver with a PN9 scrambler, and a (255,223) Reed-Solomon
    code from the [rscode](http://rscode.sourceforge.net/) library.
    You must use FM mode to receive this satellite (437.250MHz).
  * `sat_3cat2`
    [3CAT-2](https://nanosatlab.upc.edu/en/missions-and-projects/3cat-2) *(inactive)*,
    which
    transmits 9k6 AX.25 BPSK telemetry in the 2m band. You must use wide SSB
    mode to receive this satellite.
  * `aausat_4`
    [AAUSAT-4](http://www.space.aau.dk/aausat4/), which transmits 2k4 or 9k6 GFSK
    telemetry in the 70cm band. It uses the CSP protocol and FEC with an r=1/2, k=7
    convolutional code and a (255,223) Reed-Solomon code. You must use FM mode
    to receive this satellite (437.425MHz).
  * `ao40_uncoded`
    [AO-40](https://en.wikipedia.org/wiki/OSCAR_40) *(inactive)*,
    which transmitted 400bps BPSK
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
    receive this satellite (145.935MHz).
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
    receive this satellite (436.670MHz).
  * `athenoxat-1`
    [ATHENOXAT-1](http://space.skyrocket.de/doc_sdat/athenoxat-1.htm),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and FEC with a (255,223)
    Reed-Solomon code. It also uses a CCSDS scrambler. There is no telemetry
    parser yet, as the beacon format is unknown. This satellite is on a low
    inclination orbit, so it can only be received near the equator. You must
    use FM mode to receive this satellite (437.485MHz).
  * `au02`
    [QB50 AU02 (UNSW-EC0)](http://www.acser.unsw.edu.au/QB50),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and FEC with an r=1/2, k=7
    convolutional code and a (255,223) Reed-Solomon code. It also uses a CCSDS
    scrambler. You must use FM mode to receive this satellite (436.525MHz).
  * `au03`
    [QB50 AU03 (i-INSPIRE II)](http://sydney.edu.au/inspire-cubesat/project/index.shtml),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and FEC with an r=1/2, k=7
    convolutional code and a (255,223) Reed-Solomon code. It also uses a CCSDS
    scrambler. You must use FM mode to receive this satellite (436.330MHz).
  * `beesat`
    [BEESAT-1,-2 and -4](http://space.skyrocket.de/doc_sdat/beesat.htm)
    and [TECHNOSAT](https://directory.eoportal.org/web/eoportal/satellite-missions/t/technosat),
    which transmit 4k8 FSK telemetry in the 70cm band. They use the Mobitex-NX
    protocol, which includes FEC with a (12,8,3) linear code and CRC-16CCITT for
    error detection. You must use FM mode to receive these satellites (435.950MHz).
  * `by701`
    [BY70-1](http://space.skyrocket.de/doc_sdat/by70-1.htm) *(inactive)*, which transmits 9k6
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
    which transmits 4k8 GFSK telemetry in the 70cm band. Occasionaly it has been seen
    to transmit in 9k6. It uses the CSP protocol
    and FEC with a (255,223) Reed-Solomon code. It also uses a G3RUH scrambler. The
    transceiver is the GomSpace NanoCom AX100, the same transceiver used in
    GOMX-3. You must use FM mode to receive this satellite (436.705MHz).
  * `cz02`
    [QB50 CZ02 (VZLUSAT-1)](http://vzlusat1.cz/en/),
    which transmits 4k8 AF GMSK telemetry in the 70cm band. It uses a NanoCom
    U482C transceiver, with the CSP protocol and a (255,223) Reed-Solomon code.
    It also uses a CCSDS scrambler. You must use FM mode to receive this satellite (437.240MHz).
  * `dsat`
    [D-SAT](https://www.dsat.space/) *(inactive)*,
    which transmits 4k8 AF GMSK telemetry in
    the 70cm band. It uses a NanoCom U482C transceiver with the CSP protocol and
    FEC with a (255,223) Reed-Solomon code. It also uses a CCSDS scrambler. This
    receiver supports sending frames to the D-SAT groundstation software, which
    decodes telemetry. See
    [this post](http://destevez.net/2017/08/d-sat-support-added-to-gr-satellites/)
    for detailed instructions. D-SAT transmits JPEG images from an onboard
    camera. This decoder includes an image decoder which shows the images in
    real time using feh.
  * `eseo`
    [ESEO](https://www.esa.int/Education/ESEO),
    which transmits 9k6 GFSK telemetry in the 70cm band. It uses a custom protocol
    vaguely similar to AX.25 with some form of G3RUH scrambling and a
    (255,239) Reed-Solomon code. You must use FM mode to receive this satellite (437.000MHz).
  * `facsat_1`,
    [FACSAT-1](https://en.wikipedia.org/wiki/FACSAT-1), which transmits
    9k6 GMSK telemetry in the 70cm band. It uses the GomSpace NanoCom AX100
    transceiver in ASM+Golay mode. This uses a CCSDS scrambler and a (255,223)
    Reed-Solomon code. The telemetry format is unknown. You must use FM mode to
    receive this satellite (437.350MHz).
  * `fmn1`
    [FMN-1](https://space.skyrocket.de/doc_sdat/fengmaniu-1.htm),
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. You must use wide SSB mode to receive this satellite (435.350MHz).
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
    aircraft. You must use FM mode to receive this satellite (437.255MHz).
  * `gomx_3`
    [GOMX-3](https://directory.eoportal.org/web/eoportal/satellite-missions/g/gomx-3)
    *(inactive)*,
    which transmits 19k2 GFSK telemetry in the 70cm band. It uses the CSP
    protocol and FEC with a (255,223) Reed-Solomon code. It also uses a G3RUH
    scrambler. The beacons include information from ADS-B beacons transmitted by
    terrestrial aircraft. GOMX-3 reentered on 18 October 2016. You
    must use FM mode to receive this satellite.
  * `gr01`
    [QB50 GR01 (DUTHSat)](http://www.duthsat.gr/) *(inactive)*,
    which transmits 1k2 or 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. For 1k2 telemetry you must use SSB mode, while for 9k6 telemetry you
    must use wide SSB mode.
  * `il01`
    [QB50 IL01 (DUCHIFAT-2)](http://www.h-space-lab.org/php/hoopoe-en.php),
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. You must use wide SSB mode to receive this satellite (437.740MHz).
  * `indus`
    Mystery satellite transmitting on 435.080MHz using 1k2 FSK AX.25 and the
    callsign INDUSR-10 (see [here](https://twitter.com/ea4gpz/status/952593838266298368)).
  * `innosat_2`,
    [INNOSAT-2](https://space.skyrocket.de/doc_sdat/innosat-2.htm), which transmits
    4k8 GMSK telemetry in the 70cm band. It uses the GomSpace NanoCom AX100
    transceiver in ASM+Golay mode. This uses a CCSDS scrambler and a (255,223)
    Reed-Solomon code. You must use FM mode to receive this satellite (437.450MHz).
  * `itasat1`
    [ITASAT 1](http://www.itasat.ita.br/),
    which transmits 1k2 AX.25 BPSK telemetry in the 2m band.
    You must use SSB mode to receive this satellite (145.860MHz).
  * `jy1sat`
    [JY1-Sat (FUNcube-6)](https://amsat-uk.org/tag/jy1sat/),
    which transmits 1k2 BPSK
    telemetry in the 2m band. It uses the AO-40 FEC protocol, which includes
    block interleaving, an r=1/2, k=7 convolutional code, CCSDS scrambling and
    two interleaved (160,128) Reed-Solomon codes. You must use SSB mode to
    receive this satellite (145.840MHz).
  * `k2sat_image`
    [K2SAT](http://www.amsatuk.me.uk/iaru/finished_detail.php?serialnum=552),
    which transmits images using QPSK in the 13cm band. See
    [this post](http://destevez.net/2018/07/k2sat-s-band-image-receiver/).
  * `kr01`
    [QB50 KR01 (LINK)](http://space.skyrocket.de/doc_sdat/link.htm)
    *(inactive)*,
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. Currently it transmits 1k2 telemetry (safe mode perhaps), so you
    must use SSB mode to receive this satellite.
  * `ks_1q`
    [KS-1Q](http://space.skyrocket.de/doc_sdat/cas-2t.htm)
    *(inactive)*, which transmits 20k
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
    [Nayif-1 (FUNcube-5)](https://amsat-uk.org/satellites/communications/nayif-1/),
    which transmits 1k2 BPSK
    telemetry in the 2m band. It uses the AO-40 FEC protocol, which includes
    block interleaving, an r=1/2, k=7 convolutional code, CCSDS scrambling and
    two interleaved (160,128) Reed-Solomon codes. You must use SSB mode to
    receive this satellite (145.940MHz).
  * `nusat`
    [ÑuSat-1 and -2](http://space.skyrocket.de/doc_sdat/nusat-1.htm),
    which transmit 40k FSK telemetry in the 70cm band
    (ÑuSat-1 on 436.445, ÑuSat-2 on 437.455).
    They use FEC with a
    (64, 60) Reed-Solomon code and a CRC-8. Since a sample rate of 48kHz is too
    low to work with 40k FSK, the flowgraph is prepared to use an IQ recording
    at 192kHz. Depending on the characteristics of your IQ recording you may
    need to edit the flowgraph. The Reed-Solomon decoder is taken from the
    [rscode](http://rscode.sourceforge.net/) library.
    A sample IQ recording is
    included in [satellite-recordings](https://github.com/daniestevez/satellite-recordings).
  * `picsat`
    [PicSat](http://picsat.obspm.fr/),
    which transmits 1k2 or 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. For 1k2 telemetry you must use SSB mode, while for 9k6 telemetry you
    must use wide SSB mode (435.525MHz).
  * `pwsat2`
    [PW-Sat2](https://pw-sat.pl/en/home-page/),
    which transmits 1k2, 2k4, 4k8 or 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. Currently the decoder only supports 1k2 or 9k6, since it is not clear
    if the other baudrates will be ever used.
    Telemetry parsing is supported using the external PW-Sat2 software. See
    [here](https://destevez.net/2018/12/decoding-pw-sat2-with-gr-satellites/) for the
    instructions. Uploading to the [PW-Sat2 Telemetry Server](http://radio.pw-sat.pl/) is
    also supported. See
    [here](https://destevez.net/2018/12/uploading-pw-sat2-telemetry-with-gr-satellites/)
    for the instructions.
    For 1k2 telemetry you must use SSB mode, while for 9k6 telemetry you
    must use wide SSB mode (435.275MHz).
  * `reaktor_hello_world`
    [Reaktor Hello World](https://reaktorspace.com/reaktor-hello-world/),
    which transmits 9k6 GFSK telemetry in the 70cm band. It uses a Texas
    Intruments CC1125 transceiver with a PN9 scrambler and a CRC-16. You must
    use FM mode to receive this satellite (437.775MHz).
  * `shaonian_xing`
    [Shaonian Xing (MXSat-1)](https://space.skyrocket.de/doc_sdat/shaonian-xing.htm),
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. You must use wide SSB mode to receive this satellite (436.375MHz).
  * `snet`
    [S-NET A,B,C,D](http://www.raumfahrttechnik.tu-berlin.de/menue/forschung/aktuelle_projekte/s-net/),
    which transmit 1k2 AFSK telemetry in the 70cm band. They use a custom coding
    with BCH FEC and interleaving. You must use FM mode to receive these
    satellites (435.950MHz).
  * `suomi_100`
    [Suomi 100](http://www.suomi100satelliitti.fi/),
    which transmits
    9k6 GMSK telemetry in the 70cm band. It uses the GomSpace NanoCom AX100
    transceiver in ASM+Golay mode. This uses a CCSDS scrambler and a (255,223)
    Reed-Solomon code. You must use FM mode to
    receive this satellite (437.775MHz).
  * `tanusha3_pm`
    [TANUSHA-3](https://swsu.ru/space/),
    which transmits FM audio, 1k2 AX.25 AFSK telemetry and 1k2 audio frequency
    phase modulation AX.25 telemetry in the 70cm band. This decoder is for the
    phase modulation packets. For the AFSK packets you can use any regular
    packet decoder such as direwolf. You must use FM mode to receive this
    satellite (437.050MHz).
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
    to receive these satellites. TW-1A, TW-1C (435.645 MHz), TW-1B (437.645 MHz).
  * `ty_2`, `ty_4`, `ty_6`
    [TY-2](https://space.skyrocket.de/doc_sdat/ty-2.htm),
    [TY 4-01](https://space.skyrocket.de/doc_sdat/ty-4-01.htm),
    and [TY-6](http://space.skyrocket.de/doc_sdat/ty-6.htm), which transmit
    9k6 GMSK telemetry in the 70cm band. They use the GomSpace NanoCom AX100
    transceiver in ASM+Golay mode. This uses a CCSDS scrambler and a (255,223)
    Reed-Solomon code. The telemetry format is unknown. The only
    difference between the 2 receivers is that the NORAD ID is set for the
    correct satellite when doing telemetry submission. You must use FM mode to
    receive these satellites. TY-2 (435.350MHz), TY 4-01 (435.925MHz), TY-6 (436.100MHz).
  * `ua01`
    [QB50 UA01 (PolyITAN-2-SAU)](http://space.skyrocket.de/doc_sdat/polyitan-2-sau.htm),
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler and two stages of NRZI coding.
    You must use wide SSB mode to receive this satellite (436.600MHz).
  * `ukube1`
    [UKube-1 (FUNcube-2)](https://amsat-uk.org/satellites/communications/ukube-1/),
    which transmits 1k2 BPSK
    telemetry in the 2m band. It uses the AO-40 FEC protocol, which includes
    block interleaving, an r=1/2, k=7 convolutional code, CCSDS scrambling and
    two interleaved (160,128) Reed-Solomon codes. You must use SSB mode to
    receive this satellite (145.915MHz).
  * `zhou_enlai`
    [Zhou Enlai](https://space.skyrocket.de/doc_sdat/zhou_enlai.htm),
    which transmits 9k6 AX.25 BPSK telemetry in the 70cm band. It uses a G3RUH
    scrambler. You must use wide SSB mode to receive this satellite (437.644MHz).

## Generic decoders

I do not add specific decoders to gr-satellites for satellites using standard
AFSK or FSK AX.25 packet radio, since there are many satellites using these
modes and there are already very good decoders for packet radio such as
[direwolf](https://github.com/wb2osz/direwolf). However, in case someone finds
it useful, I have added `generic_4k8_fsk_ax25`, `generic_9k6_fsk_ax25` and
`generic_19k2_fsk_ax25` generic decoders for 4k8, 9k6 and 19k2 FSK AX.25 packet
radio. For the time being, I do not plan to add a 1k2 AFSK decoder, since it is not
so easy to implement a good AFSK decoder (a good AGC is a challenge, for instance).

## Submitting telemetry to SatNOGS

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

## Submitting telemetry to FUNcube

The flowgraphs for the different FUNcube satellites/payloads also support
submitting telemetry to the FUNcube server. To use this, you need to obtain the
"Site Id" (your username) and "Auth code" from your account on the FUNcube
server. These parameters can then be indicated by using the `--site-id` and
`--auth-code` if using the `.py` script or by editing the boxes in the lower
right part of the flowgraph if using the `.grc` file.

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

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [5.7.0], [4.14.0], [3.21.0] - 2025-02-10

### Added
- Check Hex String block
- OpenLST deframer
- Repeater address matching to Check AX.25 Address block
- Support for AEPEX
- Support for ARTICSAT-1
- Support for ASRTU-1
- Support for BINAR-2, -3, and -4
- Support for Bluebird-01 to -05
- Support for COLIBRI-S
- Support for DORA
- Support for HADES-R
- Support for HORIZON
- Support for HYPERVIEW-1G
- Support for MORDOVIA-IOT
- Support for RTU-MIREA1
- Support for RUZAEVKA-390
- Support for TUSUR-GO
- Support for VIZARD-ION
- Support for ZIMSAT-2
- TM KISS transport
- Vector stream IO Reed-Solomon encoder block

## Fixed
- Error when opening Doppler file fails in Doppler correction block

## Changed
- Added frame length parameter to GEOSCAN deframer
- Replaced erminaz_ssdv and jy1sat_ssdv by generic gr_satellites_ssdv script

## [5.6.0], [4.13.0], [3.20.0] - 2024-09-03

### Added
- 19k2 transmitter for RESHUCUBE
- 19k2 transmitter for ISOI
- AFSK transmitter for CUBEBUG-3
- HADES deframer in SatYAML and core flowgraph
- Support for AVION
- Support for BELIEFSAT-0
- Support for CATSAT
- Support for CUAVA-2
- Support for ERMINAZ
- Support for GRBBeta
- Support for Kashiwa
- Support for KILICSAT
- Support for MOVE-II and Nanolink transport
- Support for NANOFF-A and -B
- Support for OOV-Cube
- Support for ROBUSTA-3A
- Support for SATURN
- Support for SONATE-2
- Support for VDNH-80
- Support for WS-1
- Policy for commercial missions
- Waveform plot Python script (in tools)

### Fixed
- AHMAT-1 NORAD ID
- Astrocast 0.1 frequency
- BISONSAT NORAD ID
- CCSDS Deframer example
- Crashes when the BME Submitter fails
- Fixedlen to Pdu GRC YAML
- Hayasat NORAD ID
- IRIS NORAD ID
- KS-1Q NORAD ID
- MCUBED-2 NORAD ID
- MONITOR-2 NORAD ID and transmitters
- PDU add meta GRC YAML
- QARMAN NORAD ID
- ROBUSTA-3A NORAD ID
- SCOOB-II NORAD ID
- USP AX.25 Crop GRC YAML
- Varlen Packet Framer and Varlen Packet Tagger GRC YAML

### Changed
- FSK deviation for AALTO-1
- FSK deviation for AISTECHSAT-2 and -3
- FSK deviation for al-Farabi-2
- FSK deviation for ARCCUBE-1
- FSK deviation for Astrocast 0.1
- FSK deviation for BCCSAT 1
- FSK deviation for BDSAT-2
- FSK deviation for BEESAT-2 and -9
- FSK deviation for BISONSAT
- FSK deviation for BlueWalker 3
- FSK deviation for CIRBE
- FSK deviation for CubeBel-2
- FSK deviation for CUBEBUG-3
- FSK deviation for CUBE-L
- FSK deviation for CubeSX-HSE, -HSE-2, -HSE-3 and -Sirius-HSE
- FSK deviation for CUTE
- FSK deviation for DEKART
- FSK deviation for D-STAR One LightSat, iSat and Sparrow
- FSK deviaiton for EIRSAT-1
- FSK deviaiton for ENSO
- FSK deviation for GO-32
- FSK deviation for GRBAlpha
- FSK deviation for GREENCUBE
- FSK deviation for Hayasat
- FSK deviation for INS-2TD
- FSK deviation for INSPIRE-SAT 1 and 7
- FSK deviation for ION-MK01
- FSK deviation for IRIS-A
- FSK deviation for KAFASAT
- FSK deviation for KSU CubeSat
- FSK deviation for LEDSAT
- FSK deviation for LilacSat-2
- FSK deviation for Lucky-7
- FSK deviation for Luojia-1
- FSK deviation for MCUBED-2
- FSK deviation for MIMAN
- FSK deviation for MONITOR-3 and -4
- FSK deviation for NANOFF-A and -B
- FSK deviation for NANOZOND
- FSK deviation for NETSAT 2
- FSK deviation for NORBI
- FSK deviation for OrbiCraft-Zorkiy
- FSK deviation for PEARL-1C and -1H
- FSK deviation for POLYITAN-1
- FSK deviation for SelfieSat
- FSK deviation for Sharjahsat-1
- FSK deviation for SKOLTECH-B1
- FSK deviation for SNUGLITE
- FSK deviation for SOMP 2b
- FSK deviation for SONATE-2
- FSK deviation for SSS-2B
- FSK deviation for STRATOSAT-TK1
- FSK deviation for SUCHAI-2 and -3
- FSK deviation for Suomi 100
- FSK deviation for TIGRISAT
- FSK deviation for TTU-100
- FSK deviation for TUBIN
- FSK deviation for UmKA-1
- FSK deviation for UPMSat 2
- FSK deviation for UTMN-2
- FSK deviation for UWE-4
- FSK deviation for VERONIKA
- FSK deviation for VIZARD-METEO
- FSK deviation for VZLUSAT-2

## [5.5.0], [4.12.0], [3.19.0] - 2023-12-28

### Added
- Auto-Polarization Python block
- --fm-deviation option to AFSK Demodulator
- TLE to Doppler file Python script
- HADES-D deframer and example decoder
- Support for CLARKSAT-1
- Support for ENSO
- Support for GALASSIA-2
- Support for Hayasat
- Support for IRIS-C
- Support for KAFASAT
- Support for PEARL-1C and PEARL-1H
- Support for SCOOB-II
- Support for VELOX-AM
- Support for VERONIKA

### Fixed
- BME Telemetry Submitter GRC file
- SNET Deframer GRC file typo
- AF deviation in SALSAT SatYAML file
- Added missing SanoSat Deframer GRC file

### Changed
- Ported Manchester Sync block to C++
- CPU usage improvement for Selector block
- Final NORAD ID for EIRSAT-1

## [5.4.0], [4.11.0], [3.18.0] - 2023-08-28

### Added
- BME telemetry websocket submitter
- Modified selector block
- Support for AHMAT-1
- Support for ARCUBE-1
- Support for CubeBel-2
- Support for CUBESX-HSE-3
- Support for IRIS
- Support for KUZGTU-1
- Support for MONITOR-2, MONITOR-3 and MONITOR-4
- Support for MRC-100
- Support for NANOZOND-1
- Support for NEUDOSE
- Support for SpeiSat
- Support for SNIPE-1, SNIPE-2, SNIPE-3 and SNIPE-4
- Support for STRATOSAT-TK1
- Support for SVYATOBOR-1
- Support for VIZARD-METEO
- Support for UmKa-1
- Support for UTMN-2

### Fixed
- BER simulation
- GRC file for USP AX.25 crop
- GRC file for PDU Head/Tail
- NORAD IDs for AzaadiSAT, FOSSASAT-1B and FOSSASAT-2
- Sensitivity loss in AFSK demodulator in IQ mode
- Uninitialized variable warning in varlen_packet_tagger

### Changed
- Increased RA decoder passes to 40

## [5.3.0], [4.10.0], [3.17.0] - 2023-06-02

### Added
- 19k2 FSK mode for KUZBASS-300
- CAS-5A image receiver
- Getters and setters for Doppler Correction block
- Support for AZAADISAT-2
- Support for CIRBE
- Support for INSPIRE-SAT 7
- Support for gr-difi time tags in the Doppler Correction block
- Support for SPINO

### Fixed
- CSP packet ID endianness in csp_header.py
- Default NORAD ID in Satellite Decoder block
- Framing for CYCLOPS (USP instead of AX.25)
- Several bugs in the Doppler Correction block
- Typo in the Submit block that caused a bug when using the start time option

### Changed
- HDLC Framer passes the input metadata to the output
- Use print instead of print_pdu in Hexdump Sink
- Use start time in KISS Server Sink.

## [5.2.0], [4.9.0], [3.16.0] - 2023-01-29

### Added
- Support for BDSat-2
- Support for CAS-5A
- Support for CIRBE
- Support for HKSAT
- Support for INS-2B
- Support for MARIO
- Support for NUTSat
- Support for SharjahSat-1
- Support for SS-1
- Support for TRISAT-R

### Changed
- Doppler Correction block: use constant frequency before start of file
- Doppler Correction block: use logging instead of printing
- Marked Fixedlen Tagger block as deprecated

### Fixed
- Throttle mode when used with --wavfile
- MTCUBE-2 NORAD ID

## [5.1.1], [4.8.1], [3.15.1] - 2022-11-19

### Fixed
- RMS AGC block in aarch64 systems

## [5.1.0], [4.8.0], [3.15.0] - 2022-10-24

### Added
- Support for AzaadiSAT
- Support for BlueWalker 3
- Support for EIRSAT-1
- Support for GEOSCAN-EDELVEIS
- Support for HSU-SAT1
- Support for JAGSAT-1
- Support for Light-1
- Support for 10 Sputnix satellites in 2022-08-09 launch
- Support for SelfieSat
- Support for TUMnanoSAT
- Phase Unwrap block
- gr_satellites --satcfg to read default arguments from file

### Fixed
- AALTO deframer GRC file
- FSK demodulator with negative deviation in non-IQ mode
- Python bindings for 8APSK Costas Loop

## [5.0.0], [4.7.0], [3.14.0] - 2022-07-22

### Added
- 8APSK Costas loop block
- Custom SIDS telemetry server for PicSat
- Doppler correction block
- File receiver for QO-100
- Fixed length to PDU block
- Support for ALFACRUX
- Support for ASTROBIO
- Support for CELESTA
- Support for CTIM 70 cm sw_stat beacons
- Support for FORESAIL-1
- Support for GREENCUBE
- Support for MIMAN
- Support for MTCUBE-2
- Support for PLANETUM-1
- Support for RANDEV-1
- Support for SNUGLITE-II
- Support for STEP-CUBELAB-II
- Support for SUCHAI-1
- Support for QO-100 multimedia beacon

### Changed
- Main branch only supports GNU Radio 3.10
- Modernize logging and remove usage of Boost
- Sync to PDU blocks now use Fixed length to PDU

### Fixed
- NORAD IDs for OreSat0, PlantSat and TEVEL constellation

## [4.6.0], [3.13.0] - 2022-05-09

### Added
- Support for BDSat
- Support for D-STAR ONE LightSat
- Support for Eaglet-I in BPSK mode
- Support for INS-2TD
- Support for INSPIRESat-1
- Support for OreSat0
- Support for PlantSat
- Support for SanoSat-1
- Support for SUCHAI-3
- New generic CRC blocks
- Telemetry parsing for CSP v2

### Changed
- Improved NRZI decoder block
- Refactor code using CRCs to use the new blocks
- Updated example GRC files to GNU Radio 3.10
- Deprecate Print Header block

### Fixed
- Codec2 UDP sink under GNU Radio 3.9
- KISS server sink under GNU Radio 3.9
- UDP source under GNU Radio 3.10

### Removed
- Leftover files for D-STAR ONE telemetry parser

## [4.5.0], [3.12.0] - 2022-02-19

### Added
- Support for GNU Radio 3.10
- Support for DELFI-PQ
- Support for EXP-1
- Support for GASPACS
- Support for GT-1
- Support for HUMSAT-D
- Support for IRIS-A
- Support for TARGIT
- Support for the TEVEL satellites
- Support for XW-3
- Telemetry parser for Delfi-C3

### Changed
- Final NORAD ID for CUAVA-1
- Final NORAD ID for Grizu-263A

### Fixed
- Bug in sx12xx_packet_crop under GNU Radio 3.9
- Bug in --kiss_in mode
- NORAD ID for KSU CubeSat

## [4.4.0], [3.11.0] - 2021-11-03

### Added
- Support for BINAR-1
- Support for CUAVA-1
- Support for CUTE
- CCSDS Uncoded Deframer block

### Changed
- Default output path for file receiver changed to current directory
- Added 9k6 mode to BEESAT-1

### Fixed
- CSP header parsing in AAUSAT-4 and BY70-1 telemetry parsers
- YUSAT deframer

### Removed
- Deleted unused test_satellites.cc test code

## [4.3.1], [3.10.1] - 2021-09-11

### Changed
- Do not swap CSP header endianness in AX100 and U482C deframers
- Final NORAD ID for LEDSAT

### Fixed
- Fatal error of the image receiver if feh can't be run

## [4.3.0], [3.10.0] - 2021-08-20

### Added
- Support for DHABISAT
- Support for ION SCV-003
- Support for IT-SPINS
- Support for JAISAT-1
- Support for LEDSAT
- Support for QMR-KWT
- Support for RAMSAT
- Support for SOAR
- Support for TUBIN
- Ability to change frame length in fixedlen_tagger block

## [4.2.0], [3.9.0] - 2021-06-18

### Added
- Support for CubeSX-HSE in 1k2, 2k4 and 4k8 modes
- Support for CubeSX-Sirius-HSE in 1k2 and 2k4 modes
- Support for OrbicraftZorkiy in 2k4 mode
- Support for KAITUO-1B
- Support for DIY-1
- Support for MIR-SAT1

### Fixed
- Runtime bug in AALTO-1 deframer
- Duplicated printing with --hexdump and unknown telemetry
- Bug in FSK demodulator with IQ mode and high baudrate

## [4.1.0], [3.8.0] - 2021-04-24

### Added
- USP deframer
- Env variable GR_SATELLITES_SUBMIT_TLM to force/disable telemetry submission
- Ability to disable AX100 ASM+Golay scrambler in SatYAML and GRC block
- Support for BCCSAT 1
- Support for CUBE-L
- Support for GRBAlpha
- Support for NanosatC-BR1 and NanosatC-BR2
- Support for SIMBA
- Support for SMOG-1
- Support for SPUTNIX satellites: OrbiCraft-Zorkiy, CubeSX-HSE, CubeSX-Sirius-HSE, KSU CubeSat
- Support for STECCO
- Support for TAUSAT-1 and TSURU
- Support for UNISAT-7
- 2k4 downlink for MEZNSAT

### Changed
- In gr_satellites, do not disable non-telemetry datasinks in --hexdump mode
- Reformatting of Python code according to PEP8

### Fixed
- RS basis options swapped in CCSDS Reed-Solomon encoder GRC block

## [4.0.0] - 2021-03-06

### Added
- Support for DELFI-n3xt

### Changed
- Final NORAD for UVSQ-Sat
- Document that --wavfile allows OGG/FLAC

## [3.7.0] and [4.0.0-rc1] - 2021-02-19

### Added
- Read sample rate from WAV files automatically
- PDU Length Filter block
- Example decoder for NEXUS 19k2 pi/4-DQPSK telemetry
- Support for AALTO-1 CC1125 mode
- Support for CAPE-3
- Support for DELFI-C3
- Support for EXOCUBE-2
- Support for Grizu-263A
- Support for IDEASSat
- Support for MiTEE-1
- Support for SOMP 2b
- Support for UVSQ-SAT
- Support for YUSAT-1

### Changed
- Add filter before quadrature demod for IQ input FSK demodulator

### Fixed
- Runtime error when the baudrate is too high for the sample rate
- Errors about wrong Reed-Solomon message size with OPS-SAT deframer
- Bug in SIDS submit URL encoding
- Bug with SatYAML files in platforms not using UTF-8
- Build problems with clang

## [3.6.0] - 2020-12-04

### Added
- PDU add metadata block
- PDU Head/Tail block
- Lucky-7 image receiver
- Support for custom SIDS servers
- Support for AISTECHSAT-2 custom protocol
- Support for BOBCAT-1
- Support for BY03
- Support for FossaSat-1B and FossaSat-2
- Support for NEUTRON-1
- Support for SPOC
- Support for TTU-100
- Support for VZLUSAT-2

### Changed
- Replaced boost::bind() by C++ lambdas
- Refactored Reed-Solomon decoder C++ blocks
- Refactored CCSDS deframer blocks to allow more generality
- Make --clk_limit parameter relative to samples per symbol
- Updated AISTECHSAT-2 transmit frequency
- Definitive NORAD IDs for NETSAT 1-4

### Removed
- Deprecated Astrocast 9k6 deframer in favour of the new CCSDS Reed-Solomon deframer
- Deprecated CC11xx remove length, Header remover and Strip AX.25 header in favour of PDU Head/Tail

## [3.5.2] - 2020-10-21

### Changed
- Fixed bug in S-NET deframer

## [3.5.1] - 2020-10-17

### Changed
- Added final NORAD ID for DEKART
- Fixed bug in SALSAT CRC calculation

## [3.5.0] - 2020-10-08

### Added
- Option for generating correct recording timestamps by playing back at 1x speed
- Option for listing the supported satellites in gr_satellites
- Mobitex and Mobitex-NX deframer
- Support for SALSAT
- Support for MEZNSAT
- Support for satellites using Mobitex and Mobitex-NX (D-STAR ONE, BEESAT, TECHNOSAT,
  AMGU-1, SOKRAT, DEKART)
- Support for NETSAT 1, 2, 3, 4
- Support for NORBI
- Support for KAIDUN-1

### Fixed
- Bug with Reed-Solomon decoder that prevented building on i386 since v3.3.0

## [3.4.0] - 2020-09-12

### Added
- SatYAML file for STRAND-1
- Audio source in gr_satellites
- SatYAML file for AmicalSat
- SatYAML file for UPMSat 2
- Support for NASA-DSN convention in CCSDS concatenated frames
- Support for TRISAT
- TCP KISS server and ZMQ PUB socket to send decoded frames	
- CSP fragmentation flag
- SatYAML file for ION-MK01

### Changed
- Enable full printing of construct strings

## [3.3.0] - 2020-08-11

### Added
- Documentation for installing with conda
- SatYAML file for GO-32
- KISS output from gr_satellites and the KISS file sink includes timestamps
- Support for building with MSVC in Windows

### Changed
- Telemetry conversion formulas for BY02
- JY1SAT SSDV decoder utility now uses KISS files as input
- Removed dependence on libfec. The Reed-Solomon codes from libfec are now included in gr-satellites.
- Added 4k8 modulation to SpooQy-1

### Fixed
- Bug in Telemetry parser block when used from GRC
- Delphini-1 SatYAML file
- Stray line in Lucky7 deframer GRC block

## [3.2.0] - 2020-07-14

### Added
- Option not to add a control byte in PDU to KISS
- Connection to the Harbin Institute of Technology telemetry proxy from Telemetry Submit

### Fixed
- Bug that prevented the NORAD field from appearing in Telemetry Submit

## [3.1.0] - 2020-07-11

### Added
- Example flowgraphs from gr-kiss
- Support for CAS-6
- Option to disable scrambler in CCSDS deframers
- Note about volk_profile in the documentation
- Missing .yml grc file for LilacSat-1 deframer
- Support for BY02
- Command line options for satellite decoder block and components
- More documentation about --dump_path

### Changed
- Do not use DC-block in AFSK demodulator
- Remove second lowpass filter in BPSK demodulator
- Improvements in LilacSat-1 demuxer and deframer
- Ported NRZI encoder and decoder to C++
- Re-encode frame in SMOG-P RA decoder to check decoding correctness

### Fixed
- Cmake warning when searching for libfec
- Minor corrections to documentation
- Bug in HDLC Framer

### Removed
- Deprecated SMOG-P packet filter block

## [3.0.0] - 2020-06-03

Changes from 3.0.0-rc1

### Added
- Download instructions in documentation
- Support for AO-27
- Support for FALCONSAT-3
- Test for unknown keywords in SatYAML files

### Fixed
- Test execution in gr-satellites is not yet installed
- Minor typos in documentation
- Added missing af_carrier to AFSK SatYAML files
- swig and PythonLibs are now mandatory when running cmake
- Missing import in AFSK demodulator

### Removed
- Deprecated LilacSat-2 flowgraphs in apps/

## [3.0.0-rc1] - 2020-05-17

Large refactor release bringing new functionality and improvements. This is an overview of the main changes:

### Added
- gr_satellites command line tool
- Satellite decoder block
- Components
- SatYAML files
- File and image receiver
- Sphinx Documentation

### Changed
- Performance improvements to the demodulators

### Removed
- A number of deprecated low level blocks

## [2.3.2] - 2020-05-16
### Fixed
- Bug in telemetry submitter caused by HTTP 400 error

## [2.3.1] - 2020-04-11
### Fixed
- Bug in FUNcube telemetry parser

## [2.3.0] - 2020-02-05
### Added
- Support for SMOG-P and ATL-1 at 2500 and 12500 baud
- Support for construct 2.10
### Fixed
- Bug with DC block and AGC of SMOG-P and ATL-1 potentially causing crashes

## [2.2.0] - 2020-01-01
### Added
- Support for SMOG-P and ATL-1
- Support for DUCHIFAT-3
- Support for OPS-SAT
- Standanlone decoder for AAUSAT-4
- Support for FloripaSat-1
- BME telemetry forwarder
### Changed
- Replaced AO-40 synchronizer by more general distributed synchronizer
- Replaced AO-40 deinterleaver by more general matrix deinterleaver

## [2.1.0] - 2019-11-01
### Added
- Support for Luojia-1
### Fixed
- Corrected FACSAT NORAD ID

## [2.0.0] - 2019-10-10
### Added
- Support for GNU Radio 3.8
- Support for 4k8 in ESEO decoder

### Removed
- Support for GNU Radio 3.7

## [1.8.1] - 2019-10-07
### Fixed
- Bug with FUNcube telemetry submitter in some flowgraphs

## [1.8.0] - 2019-10-04
### Added
- Światowid image decoder
- Support for Taurus-1
- CCSDS blocks from SOCIS

### Fixed
- KISS and HDLC blocks from gr-kiss in some flowgraphs

## [1.7.0] - 2019-08-31
### Added
- Support for EntrySat
- Support for Delphini-1
- Support for AmGU-1
- Support for Sokrat
- Support for BEESAT-9
- Support for Lucky-7
- Support for Światowid 9k6 protocol

### Removed
- Telemetry submitter for EntrySat

### Fixed
- Bug in FUNcube telemetry parsing

## [1.6.0] - 2019-07-05
### Added
- Support for SpooQy-1
- Generic 1k2 AFSK AX.25 decoder

### Fixed
- Bug in AAUSAT-4 decoder

### Removed
- SatNOGS telemetry forwarders for satellites not coordinated by IARU

## [1.5.0] - 2019-05-01
### Added
- Support for AISTECHSAT-3
- JY1SAT SSDV decoder
- Support for MYSAT 1

### Fixed
- Bugs in FUNcube telemetry parser

## [1.4.0] - 2019-04-07
### Added
- Support for 1KUNS-PF in 9k6 mode
- Support for AISTECH-2
- Support for EQUiSat
- Support for QO-100
- Support for AstroCast 0.1 new protocol and 9k6 mode

### Fixed
- Bugs regarding malformed or unknown frames in Funcube tlm decoder

## [1.3.1] - 2019-01-06
### Fixed
- Bug in the Reed-Solomon decoder (affects ESEO decoder)

## [1.3.0] - 2019-01-05
### Added
- Support for FMN-1
- Support for Shaonian Xing
- Support for Zhou Enlai
- Support for TY 4-01
- Support for FACSAT-1
- Support for INNOSAT-2
- Support for Reaktor Hello World
- CC110x decoder
- Support for 3CAT-1
- Generic FSK AX.25 decoders
- Support for JY1-Sat
- Support for Suomi 100
- Support for PW-Sat2
- Support for ESEO
- Generic Reed-Solomon decoder
- FUNcube telemetry submitter
- Support for ITASAT 1
- Support for D-STAR One
- Support for Astrocast 0.1
- Support for LUME-1

### Changed
- Update to construct 2.9

### Fixed
- Miscellaneous bugs

## [1.2.0] - 2018-09-20
### Added
- feh fullscreen parameter for image decoders

## [1.1.0] - 2018-09-01
### Added
- Support for TANUSHA-3 PM
- 9k6 support for ExAlta-1
- Some extra checks in LilacSat-1 image decoder

## [1.0.0] - 2018-08-02
First gr-satellites release using semantic versioning

[Unreleased]: https://github.com/daniestevez/gr-satellites/compare/v5.7.0...main
[5.7.0]: https://github.com/daniestevez/gr-satellites/compare/v5.6.0...v5.7.0
[5.6.0]: https://github.com/daniestevez/gr-satellites/compare/v5.5.0...v5.6.0
[5.5.0]: https://github.com/daniestevez/gr-satellites/compare/v5.4.0...v5.5.0
[5.4.0]: https://github.com/daniestevez/gr-satellites/compare/v5.3.0...v5.4.0
[5.3.0]: https://github.com/daniestevez/gr-satellites/compare/v5.2.0...v5.3.0
[5.2.0]: https://github.com/daniestevez/gr-satellites/compare/v5.1.1...v5.2.0
[5.1.1]: https://github.com/daniestevez/gr-satellites/compare/v5.1.0...v5.1.1
[5.1.0]: https://github.com/daniestevez/gr-satellites/compare/v5.0.0...v5.1.0
[5.0.0]: https://github.com/daniestevez/gr-satellites/compare/v4.6.0...v5.0.0
[4.14.0]: https://github.com/daniestevez/gr-satellites/compare/v4.13.0...v4.14.0
[4.13.0]: https://github.com/daniestevez/gr-satellites/compare/v4.12.0...v4.13.0
[4.12.0]: https://github.com/daniestevez/gr-satellites/compare/v4.11.0...v4.12.0
[4.11.0]: https://github.com/daniestevez/gr-satellites/compare/v4.10.0...v4.11.0
[4.10.0]: https://github.com/daniestevez/gr-satellites/compare/v4.9.0...v4.10.0
[4.9.0]: https://github.com/daniestevez/gr-satellites/compare/v4.8.1...v4.9.0
[4.8.1]: https://github.com/daniestevez/gr-satellites/compare/v4.8.0...v4.8.1
[4.8.0]: https://github.com/daniestevez/gr-satellites/compare/v4.7.0...v4.8.0
[4.7.0]: https://github.com/daniestevez/gr-satellites/compare/v4.6.0...v4.7.0
[4.6.0]: https://github.com/daniestevez/gr-satellites/compare/v4.5.0...v4.6.0
[4.5.0]: https://github.com/daniestevez/gr-satellites/compare/v4.4.0...v4.5.0
[4.4.0]: https://github.com/daniestevez/gr-satellites/compare/v4.3.1...v4.4.0
[4.3.1]: https://github.com/daniestevez/gr-satellites/compare/v4.3.0...v4.3.1
[4.3.0]: https://github.com/daniestevez/gr-satellites/compare/v4.2.0...v4.3.0
[4.2.0]: https://github.com/daniestevez/gr-satellites/compare/v4.1.0...v4.2.0
[4.1.0]: https://github.com/daniestevez/gr-satellites/compare/v4.0.0...v4.1.0
[4.0.0]: https://github.com/daniestevez/gr-satellites/compare/v4.0.0-rc1...v4.0.0
[4.0.0-rc1]: https://github.com/daniestevez/gr-satellites/compare/v3.7.0...v4.0.0-rc1
[3.21.0]: https://github.com/daniestevez/gr-satellites/compare/v3.20.0...v3.21.0
[3.20.0]: https://github.com/daniestevez/gr-satellites/compare/v3.19.0...v3.20.0
[3.19.0]: https://github.com/daniestevez/gr-satellites/compare/v3.18.0...v3.19.0
[3.18.0]: https://github.com/daniestevez/gr-satellites/compare/v3.17.0...v3.18.0
[3.17.0]: https://github.com/daniestevez/gr-satellites/compare/v3.16.0...v3.17.0
[3.16.0]: https://github.com/daniestevez/gr-satellites/compare/v3.15.1...v3.16.0
[3.15.1]: https://github.com/daniestevez/gr-satellites/compare/v3.15.0...v3.15.1
[3.15.0]: https://github.com/daniestevez/gr-satellites/compare/v3.14.0...v3.15.0
[3.14.0]: https://github.com/daniestevez/gr-satellites/compare/v3.13.0...v3.14.0
[3.13.0]: https://github.com/daniestevez/gr-satellites/compare/v3.12.0...v3.13.0
[3.12.0]: https://github.com/daniestevez/gr-satellites/compare/v3.11.0...v3.12.0
[3.11.0]: https://github.com/daniestevez/gr-satellites/compare/v3.10.1...v3.11.0
[3.10.1]: https://github.com/daniestevez/gr-satellites/compare/v3.10.0...v3.10.1
[3.10.0]: https://github.com/daniestevez/gr-satellites/compare/v3.9.0...v3.10.0
[3.9.0]: https://github.com/daniestevez/gr-satellites/compare/v3.8.0...v3.9.0
[3.8.0]: https://github.com/daniestevez/gr-satellites/compare/v3.7.0...v3.8.0
[3.7.0]: https://github.com/daniestevez/gr-satellites/compare/v3.6.0...v3.7.0
[3.6.0]: https://github.com/daniestevez/gr-satellites/compare/v3.5.2...v3.6.0
[3.5.2]: https://github.com/daniestevez/gr-satellites/compare/v3.5.1...v3.5.2
[3.5.1]: https://github.com/daniestevez/gr-satellites/compare/v3.5.0...v3.5.1
[3.5.0]: https://github.com/daniestevez/gr-satellites/compare/v3.4.0...v3.5.0
[3.4.0]: https://github.com/daniestevez/gr-satellites/compare/v3.3.0...v3.4.0
[3.3.0]: https://github.com/daniestevez/gr-satelliites/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.com/daniestevez/gr-satellites/compare/v3.1.0...v3.2.0
[3.1.0]: https://github.com/daniestevez/gr-satellites/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/daniestevez/gr-satellites/compare/v3.0.0-rc1...v3.0.0
[3.0.0-rc1]: https://github.com/daniestevez/gr-satellites/compare/v2.3.2...v3.0.0-rc1
[2.3.2]: https://github.com/daniestevez/gr-satellites/compare/v2.3.1...v2.3.2
[2.3.1]: https://github.com/daniestevez/gr-satellites/compare/v2.3.0...v2.3.1
[2.3.0]: https://github.com/daniestevez/gr-satellites/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/daniestevez/gr-satellites/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/daniestevez/gr-satellites/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/daniestevez/gr-satellites/compare/v1.8.1...v2.0.0
[1.8.1]: https://github.com/daniestevez/gr-satellites/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/daniestevez/gr-satellites/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/daniestevez/gr-satellites/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/daniestevez/gr-satellites/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/daniestevez/gr-satellites/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/daniestevez/gr-satellites/compare/v1.3.1...v1.4.0
[1.3.1]: https://github.com/daniestevez/gr-satellites/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/daniestevez/gr-satellites/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/daniestevez/gr-satellites/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/daniestevez/gr-satellites/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/daniestevez/gr-satellites/releases/tag/v1.0.0

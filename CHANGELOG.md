# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

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

[Unreleased]: https://github.com/daniestevez/gr-satellites/compare/v5.2.0...main
[5.2.0]: https://github.com/daniestevez/gr-satellites/compare/v5.1.1...v5.2.0
[5.1.1]: https://github.com/daniestevez/gr-satellites/compare/v5.1.0...v5.1.1
[5.1.0]: https://github.com/daniestevez/gr-satellites/compare/v5.0.0...v5.1.0
[5.0.0]: https://github.com/daniestevez/gr-satellites/compare/v4.6.0...v5.0.0
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

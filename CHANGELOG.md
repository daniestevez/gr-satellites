# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Support for SMOG-P and ATL-1
- Support for DUCHIFAT-3
- Support for OPS-SAT
### Changed
- Replaced AO-40 synchronizer by more general distributed synchronizer
- Replaced AO-40 deinterleaver by more general matrix deinterleaver

### [2.1.0] - 2019-11-01
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

[Unreleased]: https://github.com/daniestevez/gr-satellites/compare/v2.1.0...maint-3.8
[2.1.0]: https://github.com/daniestevez/gr-satellites/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/daniestevez/gr-satellites/compare/v1.8.1...v2.0.0
[1.8.1]: https://github.com/daniestevez/gr-satellites/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.com/daniestevez/gr-satellites/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/daniestevez/gr-satellites/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/daniestevez/gr-satellites/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/daniestevez/gr-satellites/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/daniestevez/gr-satellites/compare/v1.3.1...v1.4.0
[1.3.0]: https://github.com/daniestevez/gr-satellites/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/daniestevez/gr-satellites/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/daniestevez/gr-satellites/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/daniestevez/gr-satellites/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/daniestevez/gr-satellites/releases/tag/v1.0.0

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Stefano Speretta <s.speretta@tudelft.nl>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *
from .ax25 import Header
from ..adapters import LinearAdapter
from ..adapters import AffineAdapter
import math


Address = Enum(BytesInteger(1),
               OBC=1,
               EPS=2,
               ADB=3,
               COMMS=4,
               ADCS=5,
               GROUND=8,
               LOBE=9,
               OBC2=10)

msgType = Enum(BytesInteger(1),
               Request=1,
               Reply=2)

service = Enum(BytesInteger(1),
               Beacon=80,
               Ping=17,
               Telemetry=3)

msgOutcome = Enum(BytesInteger(1),
                  OK=0,
                  Error=1)

EPSBusState = Enum(BytesInteger(1),
                   OFF=0,
                   ON=1)

sensorBitStatus = Enum(BytesInteger(1),
                       ERROR=0,
                       ACTIVE=1)

OBCStatus = BitStruct(
    'InternalState' / BitsInteger(4),
    'SoftwareImage' / BitsInteger(4)
    )

SubsystemStatus = BitStruct(
    Padding(4),
    'SoftwareImage' / BitsInteger(4)
    )

ResetCause = BitStruct(
    'SoftResetWDTTimerexpiration' / BitsInteger(1),
    'CPULockUp' / BitsInteger(1),
    'PORPowerSettle' / BitsInteger(1),
    'PORClockSettle' / BitsInteger(1),
    'VoltageAnomaly' / BitsInteger(1),
    'HardResetWDTWrongPassword' / BitsInteger(1),
    'HardResetWDTTimerexpiration' / BitsInteger(1),
    'SystemResetOutput' / BitsInteger(1),

    'SysCTLReboot' / BitsInteger(1),
    'NMIPin' / BitsInteger(1),
    'ExitLPM4.5' / BitsInteger(1),
    'ExitLPM3.5' / BitsInteger(1),
    'BadBandGapReference' / BitsInteger(1),
    'SupplySupervisorVccTrip' / BitsInteger(1),
    'VCCDetectorTrip' / BitsInteger(1),
    'SoftResetWDTWrongPassword' / BitsInteger(1),

    Padding(7),
    'DCOShortCircuitFault' / BitsInteger(1)
    )

# verify single bits
EPSSensorStatus = BitStruct(
    'BatteryINAStatus' / sensorBitStatus,
    'BatteryGGStatus' / sensorBitStatus,
    'InternalINAStatus' / sensorBitStatus,
    'UnregulatedINAStatus' / sensorBitStatus,
    'Bus1INAStatus' / sensorBitStatus,
    'Bus2INAStatus' / sensorBitStatus,
    'Bus3INAStatus' / sensorBitStatus,
    'Bus4INAStatus' / sensorBitStatus,
    'Bus4Error' / sensorBitStatus,
    'Bus3Error' / sensorBitStatus,
    'Bus2Error' / sensorBitStatus,
    'Bus1Error' / sensorBitStatus,
    'Bus4State' / EPSBusState,
    'Bus3State' / EPSBusState,
    'Bus2State' / EPSBusState,
    'Bus1State' / EPSBusState,
    'PanelYpINAStatus' / sensorBitStatus,
    'PanelYmINAStatus' / sensorBitStatus,
    'PanelXpINAStatus' / sensorBitStatus,
    'PanelXmINAStatus' / sensorBitStatus,
    'PanelYpTMPStatus' / sensorBitStatus,
    'PanelYmTMPStatus' / sensorBitStatus,
    'PanelXpTMPStatus' / sensorBitStatus,
    'PanelXmTMPStatus' / sensorBitStatus,
    'MpptYpINAStatus' / sensorBitStatus,
    'MpptYmINAStatus' / sensorBitStatus,
    'MpptXpINAStatus' / sensorBitStatus,
    'MpptXmINAStatus' / sensorBitStatus,
    'CellYpINAStatus' / sensorBitStatus,
    'CellYmINAStatus' / sensorBitStatus,
    'CellXpINAStatus' / sensorBitStatus,
    'CellXmINAStatus' / sensorBitStatus
    )

OBCSensorStatus = BitStruct(
    'INAStatus' / sensorBitStatus,
    'TMPStatus' / sensorBitStatus,
    Padding(6)
    )

ADBSensorStatus = BitStruct(
    'INAStatus' / sensorBitStatus,
    'TMPStatus' / sensorBitStatus,
    Padding(6)
    )

COMMSSensorStatus = BitStruct(
    'INAStatus' / sensorBitStatus,
    'TMPStatus' / sensorBitStatus,
    'TransmitINAStatus' / sensorBitStatus,
    'AmplifierINAStatus' / sensorBitStatus,
    'PhasingTMPStatus' / sensorBitStatus,
    'AmplifierTMPStatus' / sensorBitStatus,
    Padding(2)
    )

OBCTlmV2 = Struct(
    # Unit: degC
    'MCUTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    'SensorsStatus' / OBCSensorStatus,
    'BusVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'BusCurrent' / LinearAdapter(1000, BytesInteger(2)),  # unit: A
    )

EPSTlmV2 = Struct(
    # Unit: degC
    'MCUTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    'Status' / EPSSensorStatus,
    # Unit: A
    'InternalINACurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    'InternalINAVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    # Unit: A
    'UnregulatedINACurrent' / LinearAdapter(
        1000, BytesInteger(2, signed=True)),
    'UnregulatedINAVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'BatteryGGVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'BatteryINAVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    # Unit: A
    'BatteryINACurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    'BatteryGGCapacity' / LinearAdapter(10, BytesInteger(2)),  # unit: mAh
    # Unit: degC
    'BatteryGGTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    # Unit: degC
    'BatteryTMP20Temperature' / LinearAdapter(
        10, BytesInteger(2, signed=True)),

    # Unit: A
    'Bus4Current' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'Bus3Current' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'Bus2Current' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'Bus1Current' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    'Bus4Voltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'Bus3Voltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'Bus2Voltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'Bus1Voltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V

    # Unit: A
    'PanelYpCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'PanelYmCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'PanelXpCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'PanelXmCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    'PanelYpVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'PanelYmVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'PanelXpVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'PanelXmVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    # Unit: degC
    'PanelYpTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    # Unit: degC
    'PanelYmTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    # Unit: degC
    'PanelXpTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    # Unit: degC
    'PanelXmTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),

    # Unit: A
    'MpptYpCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'MpptYmCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'MpptXpCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'MpptXmCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    'MpptYpVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'MpptYmVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'MpptXpVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'MpptXmVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V

    # Unit: A
    'CellYpCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'CellYmCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'CellXpCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: A
    'CellXmCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    'CellYpVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'CellYmVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'CellXpVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    )

ADBTlmV2 = Struct(
    # Unit: degC
    'MCUTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    'SensorsStatus' / ADBSensorStatus,
    'Current' / LinearAdapter(1000, BytesInteger(2, signed=True)),  # unit: A
    'Voltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    # Unit: degC
    )

COMMSTlmV2 = Struct(
    # Unit: degC
    'MCUTemperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    'SensorsStatus' / COMMSSensorStatus,
    'Voltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    'Current' / LinearAdapter(1000, BytesInteger(2, signed=True)),  # unit: A
    # Unit: degC
    'Temperature' / LinearAdapter(10, BytesInteger(2, signed=True)),
    # Unit: dBm
    'ReceiverRSSI' / AffineAdapter(1, 21, BytesInteger(2, signed=True)),
    'TransmitVoltage' / LinearAdapter(1000, BytesInteger(2)),  # unit: V
    # Unit: A
    'TransmitCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: V
    'AmplifierVoltage' / LinearAdapter(1000, BytesInteger(2)),
    # Unit: A
    'AmplifierCurrent' / LinearAdapter(1000, BytesInteger(2, signed=True)),
    # Unit: degC
    'PhasingBoardTemperature' / LinearAdapter(
        10, BytesInteger(2, signed=True)),
    )

OBCTlm = Struct(
    'Status' / OBCStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),  # unit: s
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: OBCTlmV2})
    )

OBCTlmFull = Struct(
    'Status' / OBCStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),  # unit: s
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: OBCTlmV2}),
    'BoardTemperature' / LinearAdapter(10, BytesInteger(2, signed=True))
    )

EPSTlm = Struct(
    'Status' / SubsystemStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: EPSTlmV2})
    )

EPSTlmFull = Struct(
    'Status' / SubsystemStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: EPSTlmV2}),
    'CellXmVoltage' / LinearAdapter(1000, BytesInteger(2))  # unit: V
    )

ADBTlm = Struct(
    'Status' / SubsystemStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: ADBTlmV2})
    )

ADBTlmFull = Struct(
    'Status' / SubsystemStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: ADBTlmV2}),
    # Unit: degC
    'Temperature' / LinearAdapter(10, BytesInteger(2, signed=True))
    )

COMMSTlm = Struct(
    'Status' / SubsystemStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: COMMSTlmV2})
    )

COMMSTlmFull = Struct(
    'Status' / SubsystemStatus,
    'BootCounter' / BytesInteger(1),
    'ResetCause' / ResetCause,
    'Uptime' / BytesInteger(4),  # unit: s
    'TotalUptime' / BytesInteger(4),
    'TLMVersion' / BytesInteger(1),
    'Telemetry' / Switch(this.TLMVersion, {
        2: COMMSTlmV2}),
    # Unit: degC
    'AmplifierTemperature' / LinearAdapter(10, BytesInteger(2, signed=True))
    )

PingMsg = Struct()

Beacon = Struct(
    'Destination' / Address,
    'Size' / BytesInteger(1),
    'BeaconSource' / Address,
    'Service' / service,
    'MessageType' / msgType,
    'MessageOutcome' / msgOutcome,
    'TLMSource' / Address,
    'TelemetryHeader' / Switch(this.TLMSource, {
        Address.OBC: OBCTlm,
        Address.EPS: EPSTlm,
        Address.ADB: ADBTlm,
        Address.COMMS: COMMSTlm})
    )

DirectCommand = Struct(
    'Service' / service,
    'MessageType' / msgType,
    'TelemetryHeader' / Switch(this.Service, {
        service.Ping: PingMsg,
        service.Telemetry: COMMSTlmFull})
    )

BusOverride = Struct(
    'CommandID' / Address,
    'Size' / BytesInteger(1),
    'MessageSource' / Address,
    'Service' / service,
    'TLMSource' / Address,
    'TelemetryHeader' / Switch(this.TLMSource, {
        Address.OBC: OBCTlmFull,
        Address.EPS: EPSTlmFull,
        Address.ADB: ADBTlmFull,
        Address.COMMS: COMMSTlm})
    )

BufferedCommand = Struct(
    'CommandID' / Address,
    'Destination' / Address,
    'Size' / BytesInteger(1),
    'Source' / Address,
    'Service' / service,
    'Request' / msgType,
    'TelemetryHeader' / Switch(this.Service, {
        Address.OBC: OBCTlmFull,
        Address.EPS: EPSTlmFull,
        Address.ADB: ADBTlmFull,
        Address.COMMS: COMMSTlmFull})
    )

delfipq = Struct(
    'ax25_header' / Header,
    'FrameID' / BytesInteger(1),
    'packet' / Switch(this.FrameID, {
        0: Beacon,
        1: DirectCommand,
        2: BusOverride,
        3: BufferedCommand})
    )

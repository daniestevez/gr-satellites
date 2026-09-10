"""
Decodeur de telemetrie "geoscan2" pour la flotte Geoscan.

Definition de trame fournie par Alex Shovkoplyas (VE3NEA), auteur de
SkyRoof/SatsDecoder :
%APPDATA%\\Afreet\\Products\\SkyRoof\\TelemetryRegistry\\geoscan2.json

IMPORTANT : le deframeur GEOSCAN de gr-satellites transmet la trame COMPLETE
(adresse AX.25 sur 14 octets incluse), sans la retirer - contrairement a ce
qu'affiche SkyRoof a l'ecran, qui la masque pour la lisibilite. Confirme
empiriquement le 2026-09-09 sur une trame brute Geoscan-2 (VERBOSE PDU DEBUG
PRINT de gr_satellites) : l'adresse decodee "RS92S2 -> BEACON" et tous les
champs de telemetrie correspondent exactement a la sortie SkyRoof pour la
meme trame.

Statut de validation par satellite (trames reelles comparees a la sortie
SkyRoof et/ou au dump brut gr-satellites, correspondance exacte) :
  - Geoscan-2  (64890) : CONFIRME (2026-09-09, dump brut gr-satellites)
  - Geoscan-6  (64879) : CONFIRME (2026-09-08, dump SkyRoof)
  - 239Alferov (64881) : CONFIRME (2026-09-09, dump SkyRoof)
  - RTU MIREA1 (61785) : present dans la source VE3NEA, pas encore capture
  - Geoscan-3/4/5 (64893/64892/64891) : presents dans la source VE3NEA,
    pas encore captures
  - Geoscan-1  (64880) : NON CONFIRME, absent de la source VE3NEA. Un
    satellite tres proche (Lobachevsky/RS83S) est explicitement exclu par
    VE3NEA pour la meme raison. Active malgre ce risque connu, a la demande
    de l'utilisateur - verifier la coherence de "time" et "voltage_total"
    avant de faire confiance a la sortie.

Le framing GEOSCAN multiplexe deux types de message sur le meme canal :
- trames "beacon" AX.25 (celles decodees ici), adresse complete suivie de
  03 F0 01 puis la telemetrie ;
- trames "natives" (image/ADCS/autre), qui commencent directement par un id
  satellite puis 98 46 05 BD <mtype LE>, sans adresse AX.25. Non decodees
  ici (juste affichees en hexa).
"""

import datetime
import construct


class geoscan_beacon:
    BEACON_GATE = b'\x03\xf0\x01'
    GATE_OFFSET = 14  # confirme empiriquement le 2026-09-09

    CONFIRMED_NORAD = {64879, 64881, 64890}
    UNVERIFIED_NORAD = {61785, 64891, 64892, 64893}
    EXPERIMENTAL_NORAD = {64880}  # Geoscan-1, cf. avertissement ci-dessus

    _actuators = construct.BitStruct(
        'flywheels' / construct.Flag,
        'coils' / construct.Flag,
        'ins' / construct.Flag,
        'camera' / construct.Flag,
        'panel_x_plus' / construct.Flag,
        'panel_x_minus' / construct.Flag,
        'panel_y_plus' / construct.Flag,
        'panel_y_minus' / construct.Flag,
    )

    _beacon = construct.Struct(
        'time_unix' / construct.Int32ul,
        'eps_mode' / construct.Int8ul,
        construct.Padding(1),
        'current_total' / construct.Int16ul,
        'current_solar_panels' / construct.Int16ul,
        'voltage_per_battery' / construct.Int16ul,
        'voltage_total' / construct.Int16ul,
        construct.Padding(2),
        'temp_battery_1' / construct.Int8sl,
        'temp_battery_2' / construct.Int8sl,
        construct.Padding(7),
        'actuators' / _actuators,
        'temp_x_plus' / construct.Int8sl,
        'temp_x_minus' / construct.Int8sl,
        'temp_y_plus' / construct.Int8sl,
        'temp_y_minus' / construct.Int8sl,
        'gnss_satellites' / construct.Int8ul,
        construct.Padding(2),
        'camera_files' / construct.Int8ul,
        construct.Padding(6),
        'vbus_voltage' / construct.Int16ul,
        construct.Padding(2),
        'rssi_last' / construct.Int8sl,
        'rssi_min' / construct.Int8sl,
        construct.Padding(2),
        'tx_packets' / construct.Int8ul,
        construct.Padding(3),
        'qso_count' / construct.Int8ul,
    )

    @staticmethod
    def _decode_ax25_addr(b7):
        call = ''.join(chr(c >> 1) for c in b7[:6]).strip()
        ssid = (b7[6] >> 1) & 0x0F
        return f'{call}-{ssid}' if ssid else call

    @staticmethod
    def parse(packet):
        data = bytes(packet)
        off = geoscan_beacon.GATE_OFFSET

        if (len(data) < off + 3
                or data[off:off+3] != geoscan_beacon.BEACON_GATE):
            return (f'Geoscan: trame native ou non reconnue, '
                    f'{len(data)} octets: {data.hex()}')

        try:
            b = geoscan_beacon._beacon.parse(data[off+3:])
        except construct.ConstructError as e:
            return f'Geoscan: erreur de parsing beacon: {e}'

        lines = []
        if len(data) >= 14:
            src = geoscan_beacon._decode_ax25_addr(data[7:14])
            dst = geoscan_beacon._decode_ax25_addr(data[0:7])
            lines.append(f'address = {src} -> {dst}')

        t = datetime.datetime.fromtimestamp(b.time_unix, datetime.timezone.utc)
        act = b.actuators

        def onoff(v):
            return 'ON' if v else 'OFF'

        now = datetime.datetime.now(datetime.timezone.utc)
        delta_h = abs((now - t).total_seconds()) / 3600
        warning = ''
        if delta_h > 48 or not (5000 <= b.voltage_total <= 10000):
            warning = ('\n/!\\ valeurs suspectes (horodatage ou tension hors '
                       'plage plausible) - layout probablement incorrect '
                       'pour ce satellite')

        lines += [
            f'time = {t.isoformat()}',
            f'eps_mode = {b.eps_mode}',
            f'current_total = {b.current_total} mA',
            f'current_solar_panels = {b.current_solar_panels} mA',
            f'voltage_per_battery = {b.voltage_per_battery} mV',
            f'voltage_total = {b.voltage_total} mV',
            f'temp_battery_1 = {b.temp_battery_1} degC',
            f'temp_battery_2 = {b.temp_battery_2} degC',
            f'act_flywheels = {onoff(act.flywheels)}',
            f'act_coils = {onoff(act.coils)}',
            f'act_ins = {onoff(act.ins)}',
            f'act_camera = {onoff(act.camera)}',
            f'act_panel_x_plus = {onoff(act.panel_x_plus)}',
            f'act_panel_x_minus = {onoff(act.panel_x_minus)}',
            f'act_panel_y_plus = {onoff(act.panel_y_plus)}',
            f'act_panel_y_minus = {onoff(act.panel_y_minus)}',
            f'temp_x_plus = {b.temp_x_plus} degC',
            f'temp_x_minus = {b.temp_x_minus} degC',
            f'temp_y_plus = {b.temp_y_plus} degC',
            f'temp_y_minus = {b.temp_y_minus} degC',
            f'gnss_satellites = {b.gnss_satellites}',
            f'camera_files = {b.camera_files}',
            f'vbus_voltage = {b.vbus_voltage} mV',
            f'rssi_last = {b.rssi_last} dBm',
            f'rssi_min = {b.rssi_min} dBm',
            f'tx_packets = {b.tx_packets}',
            f'qso_count = {b.qso_count}',
        ]
        return '\n'.join(lines) + warning

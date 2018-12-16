#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Daniel Estevez <daniel@destevez.net>
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from construct import *
from adapters import LinearAdapter, AffineAdapter

# Beacon of type 1
General = Struct(
    'obd_mode' / Int8ul,
    'obd_active_task' / Int8ul,
    'obd_equipment_status' / Int32ul,
    'obd_cpu_error' / Int32ul,
    'obd_can_timeout_error' / Int32ul,
    'obd_wd_reset_count' / Int8ul,
    'obd_rs422m_err_count' / Int16ul,
    'obd_rs422r_err_count' / Int16ul,
    'obd_error_count' / Int16ul,
    'obd_tc_error' / Int32ul[2],
    'obd_rs422_status' / Int32ul,
    'obd_rs422_error' / Int32ul,
    'obd_rs485_status' / Int32ul,
    'obd_rs485_error' / Int32ul,
    'obd_status' / Int32ul,
    'acs_state' / Int8ul,
    'acs_omega' / Float32b[3],
    'pm_current_bp' / Int16sl[6],
    'pm_voltage_mb' / Int16ul,
    'pm_safe_operating_mode' / Int8ul,
    'pm_error_1' / Int32ul,
    'tt_tx_status_main' / Int8ul,
    'ttm_error' / Int16ul,
    'platform_fdir_ttm' / Int32ul,
    'tt_tx_status_redundant' / Int8ul,
    'ttr_error_ttr' / Int16ul,
    'platform_fdir_ttr' / Int32ul,
    'ss_error' / Int32ul[2],
    'ese_error' / Int16ul,
    'mwr_error' / Int16ul,
    'mwm_status' / Int32ul,
    'mm_error' / Int16ul[2],
    'mt_error' / Int16ul[2],
    'tt_tx_status' / Int8ul,
    'tt_error' / Int16ul)    

Temperature = LinearAdapter(10, Int16ul)

# Beacon of type 2
PowerSystem = Struct(
    'pm_voltage_sp' / Int16ul[6],
    'pm_shunt_section' / Int16ul[6],
    'pm_temp_sp' / Temperature[3],
    'pm_current_bp' / Int16ul[6],
    'pm_temp_pb' / Temperature[6],
    'pm_voltage_mb' / Int16ul,
    'pm_safe_operating_mode' / Int8ul,
    'pm_pdu_control' / Int8ul,
    'pm_temp' / Temperature[2],
    'pm_obdh_main_current' / Int16ul,
    'pm_rx_main_current' / Int16ul,
    'pm_tx_main_current' / Int16ul,
    'pm_ss_main_current' / Int16ul,
    'pm_mm_main_current' / Int16ul,
    'pm_mw_main_current' / Int16ul,
    'pm_mt_main_current' / Int16ul,
    'pm_mps_current' / Int16ul,
    'pm_tritel_current' / Int16ul,
    'pm_hstx_current' / Int16ul,
    'pm_gps_current' / Int16ul,
    'pm_mps_valve_m_current' / Int16ul,
    'pm_dom_1_current' / Int16ul,
    'pm_obdh_red_current' / Int16ul,
    'pm_rx_red_current' / Int16ul,
    'pm_tx_red_current' / Int16ul,
    'pm_ss_red_current' / Int16ul,
    'pm_mm_red_current' / Int16ul,
    'pm_mw_red_current' / Int16ul,
    'pm_mt_red_current' / Int16ul,
    'pm_es_current' / Int16ul,
    'pm_ucam' / Int16ul,
    'pm_amsat_current' / Int16ul,
    'pm_lmp_current' / Int16ul,
    'pm_eq_pl_status' / Int32ul,
    'pm_error' / Int32ul[2])

# Beacon of type 3
OBDH = Struct(
    'obd_mode' / Int8ul,
    'obd_old_mode' / Int8ul,
    'obd_active_task' / Int8ul,
    'obd_equipment_status' / Int32ul,
    'obd_equipment_health' / Int32ul,
    'obd_cpu_error' / Int32ul,
    'obd_can_status' / Int32ul,
    'obd_plcan_m_error' / Int32ul,
    'obd_plcan_r_error' / Int32ul,
    'obd_pycan_m_error' / Int32ul,
    'obd_pycan_r_error' / Int32ul,
    'obd_can_timeout_error' / Int32ul,
    'obd_hk_status' / Int32ul,
    'obd_power_time' / Int64ul,
    'obd_mode_transition' / Int64ul,
    'obd_wd_reset_count' / Int8ul,
    'obd_temp_pdu1' / Temperature,
    'obd_temp_bat1' / Temperature,
    'obd_temp_pmb' / Temperature,
    'obd_temp_hpa2' / Temperature,
    'obd_temp_hpa1' / Temperature,
    'obd_temp_tnk' / Temperature,
    'obd_temp_bat2' / Temperature,
    'obd_temp_mwm' / Temperature,
    'obd_temp_mwr' / Temperature,
    'obd_temp_mmm' / Temperature,
    'obd_temp_mmr' / Temperature,
    'obd_rs422m_err_count' / Int16ul,
    'obd_rs422r_err_count' / Int16ul,
    'obd_hk_error' / Int32ul,
    'obd_rs422_status' / Int32ul,
    'obd_rs422_error' / Int32ul,
    'obd_rs485_status' / Int32ul,
    'obd_rs485_error' / Int32ul,
    'obd_status' / Int32ul,
    'obd_error' / Int32ul,
    'obd_temp_error' / Int16ul,
    'obd_error2' / Int32ul,
    'obd_temp_error2' / Int16ul)

# Beacon of type 4
AOCS = Struct(
    'acs_state' / Int8ul,
    'acs_sun_mode' / Int8ul,
    'acs_err' / Int32ul,
    'acs_attitude_q' / Float32b[4],
    'acs_omega' / Float32b[3],
    'acs_orbit_xyz' / Float32b[3],
    'acs_orbit_v' / Float32b[3],
    'acs_state_transition' / Int64ul,
    'acs_fdir_mps_time_err' / Float32b,
    'pm_spin_rate' / Int32ul,
    'ssm_uc_pcb_temp' / Temperature,
    'ss_adc_pcb_temp' / Temperature[2],
    'ssm_topcase_temp' / Temperature,
    'ssm_sidecase_temp' / Temperature,
    'ssr_uc_pcb_temp' / Temperature,
    'ss_adc_pcb_temp' / Temperature[2],
    'ss_dcdc_temp' / Temperature,
    'ss_sidecase_temp' / Temperature,
    'ese_uc_pcb_temp' / Temperature,
    'ese_tau_temp' / Temperature,
    'mwr_temp' / Temperature,
    'mwr_if_temp' / Temperature,
    'mwm_temp' / Temperature[3],
    'mps_hpt' / Int16ul,
    'mps_lpt' / Int16ul,
    'mps_pvt_temp' / Temperature,
    'mm_dcdc_temp' / Temperature[2],
    'mt_temp' / Temperature[2])

# Beacon of type 5
FDIR = Struct(
    'obd_plcan_m_txerr_count' / Int16ul,
    'obd_plcan_m_rxerr_count' / Int16ul,
    'obd_plcan_r_txerr_count' / Int16ul,
    'obd_plcan_r_rxerr_count' / Int16ul,
    'obd_pycan_m_txerr_count' / Int16ul,
    'obd_pycan_m_rxerr_count' / Int16ul,
    'obd_pycan_r_txerr_count' / Int16ul,
    'obd_pycan_r_rxerr_count' / Int16ul,
    'obd_edac_error_count' / Int32ul,
    'obd_rs422m_err_count' / Int16ul,
    'obd_rs422r_err_count' / Int16ul,
    'obd_error_count' / Int16ul,
    'obd_hk_error' / Int32ul,
    'obd_tc_error' / Int32ul[2],
    'obd_rs422_status' / Int32ul,
    'obd_rs422_error' / Int32ul,
    'obd_rs485_status' / Int32ul,
    'obd_rs485_error' / Int32ul,
    'obd_error' / Int32ul,
    'obd_temp_error' / Int16ul,
    'acs_err' / Int32ul,
    'acs_fdir_mps_time_err' / Float32b,
    'pm_voltage_mb' / Int16ul,
    'pm_safe_operating_mode' / Int8ul,
    'pm_eq_pl_status' / Int32ul,
    'pm_undervoltage_status' / Int32ul,
    'tt_m_tx_status' / Int8ul,
    'tt_m_tx_status_1' / Int8ul,
    'tt_m_rx_status' / Int8ul,
    'tt_m_rx_status_1' / Int8ul,
    'tt_m_rx_rssi' / Int8sl,
    'tt_m_error' / Int16ul,
    'tt_m_temp' / Temperature[2],
    'tt_m_rx_afc' / LinearAdapter(1/16.0, Int8sl),
    'platform_m_fdir' / Int32ul,
    'tt_r_tx_status' / Int8ul,
    'tt_r_tx_status_1' / Int8ul,
    'tt_r_rx_status' / Int8ul,
    'tt_r_rx_status_1' / Int8ul,
    'tt_r_rx_rssi' / Int8sl,
    'tt_r_error' / Int16ul,
    'tt_r_temp' / Temperature[2],
    'tt_r_rx_afc' / LinearAdapter(1/16.0, Int8sl),
    'platform_r_fdir' / Int32ul[3])

TriTmp = AffineAdapter(0.5, -40, Int8ul)

# Beacon of type 6
Payload = Struct(
    'tri_tmp_xyz' / TriTmp[3],
    'tri_tmp_psu' / TriTmp,
    'tri_tmp_cpu' / TriTmp,
    'tri_tmp_adc' / TriTmp[3],
    'tri_uinput' / LinearAdapter(150, Int8ul),
    'tri_iinput' / LinearAdapter(2, Int8ul),
    'tri_60V' / LinearAdapter(300, Int8ul),
    'tri_5V' / LinearAdapter(30, Int8ul),
    'tri_3_3V' / LinearAdapter(20, Int8ul),
    'tri_neg10V' / LinearAdapter(100, Int8ul),
    'tri_6_5V' / LinearAdapter(50, Int8ul),
    'tri_neg6_5V' / LinearAdapter(50, Int8ul),
    'tri_mode' / Int8ul,
    'tri_freq' / Int8ul,
    'tri_error' / Int8ul,
    'eeprom' / Int8ul,
    'lmp_tt_psu' / Int8sl,
    'lmp_vt_p12' / LinearAdapter(1/0.078, Int8ul),
    'lmp_vt_m12' / LinearAdapter(-1/0.078, Int8ul),
    'lmp_vt_p5' / LinearAdapter(1/0.029, Int8ul),
    'lmp_vt_m5' / LinearAdapter(-1/0.029, Int8ul),
    'lmp_ct_dig' / LinearAdapter(1/1.259, Int8ul),
    'lmp_vt_dig' / LinearAdapter(1/0.02, Int8ul),
    'lmp_mem' / LinearAdapter(1/4096.0, Int8ul),
    'lmp_ofs' / LinearAdapter(1/4.88, Int8ul),
    'lmp_sw' / Int24ul,
    'pcam_mcur_curr' / Int8ul,
    'pcam_img_curr' / Int8ul,
    'pcam_mcu_temp' / Temperature,
    'pcam_img_temp' / Temperature,
    'pcam_dcdc_temp' / Temperature,
    'scam_mcur_curr' / Int8ul,
    'scam_img_curr' / Int8ul,
    'scam_ram_curr' / Int8ul,
    'scam_mcu_temp' / Temperature,
    'scam_img_temp' / Temperature,
    'scam_sdr_temp' / Temperature[2],
    'ams_obc_p_up' / Int32ul,
    'ams_obc_p_up_dropped' / Int32ul,
    'ams_obc_mem_stat_ram' / Int32ul,
    'ams_obc_mem_stat_flash' / Int32ul,
    'ams_eps_dcdc_t' / Int8ul,
    'ams_vhf_fm_pa_t' / Int8ul,
    'ams_vhf_bpsk_pa_t' / Int8ul,
    'stx_vol' / LinearAdapter(50, Int8ul)[2],
    'stx_cur' / LinearAdapter(50, Int8ul)[2],
    'stx_temp' / AffineAdapter(0.5, 230, Int8ul)[4],
    'stx_stat' / Int32ul,
    'stx_com' / Int32ul,
    'stx_mem' / Int32ul,
    'gps_current_3V3' / Int16ul,
    'gps_current_5V' / Int16ul,
    'gps_week' / Int16ul,
    'gps_temperature' / Temperature[2],
    'gps_frend_m_volt' / Int16ul,
    'gps_frend_r_volt' / Int16ul,
    'gps_seconds_of_week' / Int32ul,
    'ade_in_estimator_on' / Int8ul,
    'ade_in_omega' / Int8ul,
    'ade_oprq_q' / Float32b[3])

Beacon = Struct(
    'type' / Int8ul,
    'byte' / Int8ul,
    'data' / Switch(this.type, {3 : General, 4 : PowerSystem, 5 : OBDH, 6 : AOCS, 7 : FDIR, 8 : Payload})
    )
    
    
    
    
    
    
    
    

#!/bin/sh

export GR_SATELLITES_SUBMIT_TLM=0

echo 1KUNS-PF
gr_satellites 1KUNS-PF --wavfile satellite-recordings/1kuns_pf.wav
echo 3CAT-1
gr_satellites 3CAT-1 --wavfile satellite-recordings/sat_3cat_1.wav --hexdump
echo "Astrocast 0.1"
gr_satellites "Astrocast 0.1" --wav satellite-recordings/astrocast.wav --verbose_rs
echo EntrySat
gr_satellites EntrySat  --wav satellite-recordings/entrysat.wav
echo GOMX-3
gr_satellites GOMX-3  --wav satellite-recordings/gomx_3.wav
echo US01
gr_satellites US01  --wav satellite-recordings/us01.wav
echo "Astrocast 0.1 9k6"
gr_satellites "Astrocast 0.1" --wav satellite-recordings/astrocast_9k6.wav --input_gain -1 --clk_limit 0.05
echo AO-73
gr_satellites FUNcube-1 --wavfile satellite-recordings/ao73.wav
echo "Reaktor Hello World"
gr_satellites "Reaktor Hello World" --wavfile satellite-recordings/reaktor_hello_world.wav 
echo "S-NET A"
gr_satellites "S-NET A" --wavfile satellite-recordings/snet_a.wav
echo "Swiatowid"
gr_satellites Swiatowid --wavfile satellite-recordings/swiatowid.wav
echo "NuSat"
gr_satellites "NuSat 1" --wavfile satellite-recordings/nusat.wav --iq --samp_rate 192e3
echo KS-1Q
gr_satellites KS-1Q --wavfile satellite-recordings/ks_1q.wav --clk_bw 0.02
echo BY70-1
gr_satellites BY70-1 --wavfile satellite-recordings/by701.wav
echo LilacSat-1
gr_satellites LilacSat-1 --wavfile satellite-recordings/lilacsat1.wav
echo QO-100
gr_satellites QO-100 --wavfile satellite-recordings/qo100.wav
echo AAUSAT-4
gr_satellites AAUSAT-4 --wavfile satellite-recordings/aausat_4.wav
echo Floripasat-1
gr_satellites FloripaSat-1 --wavfile satellite-recordings/floripasat_1.wav
echo SMOG-P
gr_satellites SMOG-P --wavfile satellite-recordings/smog_p_5k.wav
gr_satellites SMOG-P --wavfile satellite-recordings/smog_p_long.wav
gr_satellites SMOG-P --wavfile satellite-recordings/smog_p.wav
echo OPS-SAT
gr_satellites OPS-SAT --wavfile satellite-recordings/ops_sat.wav
echo AISAT
gr_satellites AISAT --wavfile satellite-recordings/aisat.wav
echo AISTECHSAT-3
gr_satellites AISTECHSAT-3 --wavfile satellite-recordings/aistechsat3.wav
echo AO-40
gr_satellites AO-40 --wavfile satellite-recordings/ao40_uncoded.wav
echo ATHENOXAT-1
gr_satellites ATHENOXAT-1 --wavfile satellite-recordings/athenoxat_1.wav
echo AU02
gr_satellites AU02 --wavfile satellite-recordings/au02.wav --clk_bw 0.1
echo AU03
gr_satellites AU03 --wavfile satellite-recordings/au03.wav
echo CA03
gr_satellites CA03 --wavfile satellite-recordings/ca03.wav
gr_satellites CA03 --wavfile satellite-recordings/ca03_9k6.wav
echo CZ02
gr_satellites CZ02 --wavfile satellite-recordings/cz02.wav --clk_bw 0.001
echo D-SAT
gr_satellites D-SAT --wavfile satellite-recordings/dsat.wav
echo DUCHIFAT-3
gr_satellites DUCHIFAT-3 --wavfile satellite-recordings/duchifat_3.wav
echo FACSAT-1
gr_satellites FACSAT-1 --wavfile satellite-recordings/facsat_1.wav
echo FMN-1
gr_satellites FMN-1 --wavfile satellite-recordings/fmn1.wav
echo GALASSIA
gr_satellites GALASSIA --wavfile satellite-recordings/galassia.wav
echo GOMX-1
gr_satellites GOMX-1 --wavfile satellite-recordings/gomx_1.wav
echo IL01
gr_satellites IL01 --wavfile satellite-recordings/il01.wav
echo INNOSAT-2
gr_satellites INNOSAT-2 --wavfile satellite-recordings/innosat_2.wav
echo ITASAT 1
gr_satellites "ITASAT 1" --wavfile satellite-recordings/itasat1.wav
echo KR01
gr_satellites KR01 --wavfile satellite-recordings/kr01.wav --clk_limit 0.1
echo Luojia-1
gr_satellites Luojia-1 --wavfile satellite-recordings/luojia-1.wav
echo "MYSAT 1"
gr_satellites "MYSAT 1" --wavfile satellite-recordings/mysat1.wav --f_offset 2000 --disable_fll --clk_limit 0.1
echo PW-Sat2
gr_satellites PW-Sat2 --wavfile satellite-recordings/pwsat2.wav --clk_limit 0.1
echo "Shaonian Xing"
gr_satellites "Shaonian Xing" --wavfile satellite-recordings/shaonian_xing.wav
echo "Suomi 100"
gr_satellites "Suomi 100" --wavfile satellite-recordings/suomi_100.wav
echo TW-1B
gr_satellites TW-1B --wavfile satellite-recordings/tw_1b.wav
echo TW-1C
gr_satellites TW-1C --wavfile satellite-recordings/tw_1c.wav
echo TY-2
gr_satellites TY-2 --wavfile satellite-recordings/ty_2.wav
echo "TY 4-01"
gr_satellites "TY 4-01" --wavfile satellite-recordings/ty_4.wav
echo "Quetzal-1"
gr_satellites Quetzal-1 --wavfile satellite-recordings/quetzal1.wav
echo "UA01"
gr_satellites UA01 --wavfile satellite-recordings/ua01.wav --costas_bw 150
echo "BY02"
gr_satellites BY02 --wavfile satellite-recordings/by02.wav
echo "UPMSat 2"
gr_satellites "UPMSat 2" --wavfile satellite-recordings/upmsat_2.wav --clk_bw 0.1
echo "TRISAT"
gr_satellites TRISAT --wavfile satellite-recordings/trisat.wav
echo "SOKRAT"
gr_satellites SOKRAT --wavfile satellite-recordings/sokrat.wav
echo "BEESAT-9"
gr_satellites BEESAT-9 --wavfile satellite-recordings/beesat_9.wav
echo "IDEASSat"
gr_satellites IDEASSat --wavfile satellite-recordings/ideassat.wav
echo "CAPE-3"
gr_satellites CAPE-3 --wavfile satellite-recordings/cape3.wav
echo "SanoSat-1"
gr_satellites SanoSat-1 --wavfile satellite-recordings/sanosat1.wav

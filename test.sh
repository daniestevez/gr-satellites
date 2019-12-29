#!/bin/sh

echo 1KUNS-PF
gr_satellites 1KUNS-PF --sa 48e3 --wavfile ~/satellite-recordings/1kuns_pf.wav 
echo 3CAT-1
gr_satellites 3CAT-1 --wavfile ~/satellite-recordings/sat_3cat_1.wav --samp_rate 48000 --hexdump
echo "Astrocast 0.1"
gr_satellites "Astrocast 0.1" --samp_rate 48e3 --wav ~/satellite-recordings/astrocast.wav --gain_mu 10 --verbose_rs
echo EntrySat
gr_satellites EntrySat --samp_rate 48e3 --wav ~/satellite-recordings/entrysat.wav --clk_limit 0.03
echo GOMX-3
gr_satellites GOMX-3 --samp_rate 48e3 --wav ~/satellite-recordings/gomx_3.wav
echo US01
gr_satellites US01 --samp_rate 48e3 --wav ~/satellite-recordings/us01.wav
echo "Astrocast 0.1 9k6"
gr_satellites "Astrocast 0.1" --samp_rate 48e3 --wav ~/satellite-recordings/astrocast_9k6.wav  --input_gain -1
echo AO-73
gr_satellites FUNcube-1 --wavfile ~/satellite-recordings/ao73.wav --samp_rate 48e3 --clk_limit 0.02
echo "Reaktor Hello World"
gr_satellites "Reaktor Hello World" --wavfile ~/satellite-recordings/reaktor_hello_world.wav --samp_rate 48e3
echo "S-NET A"
gr_satellites "S-NET A" --wavfile ~/satellite-recordings/snet_a.wav --samp_rate 48e3
echo "Swiatowid"
gr_satellites Swiatowid --wavfile ~/satellite-recordings/swiatowid.wav --samp_rate 48e3
echo "NuSat"
gr_satellites "NuSat 1" --wavfile ~/satellite-recordings/nusat.wav --iq --samp_rate 192e3 --gain_mu 0.1
echo KS-1Q
gr_satellites KS-1Q --wavfile ~/satellite-recordings/ks_1q.wav --samp_rate 48e3 --clock_offset_limit 0.005 --gain_mu 0.175 --input_gain 10
echo BY70-1
gr_satellites BY70-1 --wavfile ~/satellite-recordings/by701.wav --samp_rate 48e3
echo LilacSat-1
gr_satellites LilacSat-1 --wavfile ~/satellite-recordings/lilacsat1.wav --samp_rate 48e3
echo QO-100
gr_satellites QO-100 --wavfile ~/satellite-recordings/qo100.wav --samp_rate 48e3
echo AAUSAT-4
gr_satellites AAUSAT-4 --wavfile ~/satellite-recordings/aausat_4.wav --samp_rate 48e3
echo Floripasat-1
gr_satellites FloripaSat-1 --wavfile ~/satellite-recordings/floripasat_1.wav --samp_rate 48e3
echo SMOG-P
gr_satellites SMOG-P --wavfile ~/satellite-recordings/smog_p_5k.wav --samp_rate 48e3 --input_gain 10
gr_satellites SMOG-P --wavfile ~/satellite-recordings/smog_p_long.wav --samp_rate 48e3
gr_satellites SMOG-P --wavfile ~/satellite-recordings/smog_p.wav --samp_rate 48e3
echo OPS-SAT
gr_satellites OPS-SAT --wavfile ~/satellite-recordings/ops_sat.wav --samp_rate 48e3
echo AISAT
gr_satellites AISAT --wavfile ~/satellite-recordings/aisat.wav --samp_rate 48e3
echo AISTECHSAT-3
gr_satellites AISTECHSAT-3 --wavfile ~/satellite-recordings/aistechsat3.wav --samp_rate 48e3

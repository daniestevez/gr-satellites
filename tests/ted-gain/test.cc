#include <cmath>
#include <fstream>
#include <iostream>
#include <memory>

#include <gnuradio/digital/timing_error_detector_type.h>
#include <gnuradio/filter/firdes.h>

#include "interpolating_resampler.h"
#include "timing_error_detector.h"

using namespace gr::digital;

int main(int argc, char** argv)
{
    std::unique_ptr<timing_error_detector> d_ted;
    std::unique_ptr<interpolating_resampler_ccf> d_interp;
    int n_filters = 16;
    double rrc_alpha = 0.35;
    gr_complex interp_output = gr_complex(0.0f, 0.0f);
    gr_complex interp_derivative = gr_complex(0.0f, 0.0f);
    int n_poly = 100;

    float ted_error = 0.0f;
    float ted_error_old = 0.0f;

    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " sps" << std::endl;
        exit(1);
    }

    double sps = std::stof(argv[1]);

    std::vector<float> pulse = gr::filter::firdes::root_raised_cosine(
        n_poly * sps, n_poly * sps, 1.0, rrc_alpha, ceil(11 * n_poly * sps));

    std::vector<float> taps = gr::filter::firdes::root_raised_cosine(
        n_filters, n_filters, 1.0 / sps, rrc_alpha, ceil(11 * sps * n_filters));

    gr_complex* in = new gr_complex[pulse.size()]();

    d_ted.reset(timing_error_detector::make(TED_SIGNAL_TIMES_SLOPE_ML, nullptr));
    d_interp.reset(interpolating_resampler_ccf::make(
        IR_PFB_MF, d_ted->needs_derivative(), n_filters, taps));

    // d_ted->sync_reset();
    // d_interp->sync_reset(sps);

    std::ofstream interp_output_f("interp_output.c64", std::ios::binary);
    ;
    std::ofstream interp_derivative_f("interp_derivative.c64", std::ios::binary);
    ;
    std::ofstream ted_error_f("ted_error.f32", std::ios::binary);
    ;

    const int sweep_n_symbols = 3;

    for (int ii = 0; ii < sweep_n_symbols * n_poly * sps; ii++) {
        for (int j = 0; j < 11 * sps; j++) {
            int idx = n_poly * j + ii + round(n_poly * fmod(sps, 1.0));
            if (idx < static_cast<int>(pulse.size())) {
                in[j] = gr_complex(pulse[idx], 0.0f);
            }
        }

        interp_output = d_interp->interpolate(in, d_interp->phase_wrapped());
        // std::cout << "interp_output = " << interp_output << std::endl;
        interp_output_f.write((char*)&interp_output, sizeof(interp_output));
        interp_derivative = d_interp->differentiate(in, d_interp->phase_wrapped());
        // std::cout << "interp_derivative = " << interp_derivative << std::endl;
        interp_derivative_f.write((char*)&interp_derivative, sizeof(interp_derivative));

        d_ted->input(interp_output, interp_derivative);
        ted_error = d_ted->error();
        // std::cout << "ted_error = " << ted_error << std::endl;
        ted_error_f.write((char*)&ted_error, sizeof(ted_error));

        if (ii == 1) {
            std::cout << "Gain " << (ted_error_old - ted_error) * n_poly << " sample^{-1}"
                      << std::endl;
        }

        ted_error_old = ted_error;
    }

    return 0;
}

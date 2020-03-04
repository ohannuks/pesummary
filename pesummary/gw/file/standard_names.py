# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


lalinference_map = {
    "h1_cplx_snr_amp": "H1_matched_filter_abs_snr",
    "h1_cplx_snr_arg": "H1_matched_filter_snr_angle",
    "h1_optimal_snr": "H1_optimal_snr",
    "l1_cplx_snr_amp": "L1_matched_filter_abs_snr",
    "l1_cplx_snr_arg": "L1_matched_filter_snr_angle",
    "l1_optimal_snr": "L1_optimal_snr",
    "v1_cplx_snr_amp": "V1_matched_filter_abs_snr",
    "v1_cplx_snr_arg": "V1_matched_filter_snr_angle",
    "v1_optimal_snr": "V1_optimal_snr",
    "logl": "log_likelihood",
    "logprior": "log_prior",
    "matched_filter_snr": "network_matched_filter_snr",
    "optimal_snr": "network_optimal_snr",
    "phi12": "phi_12",
    "q": "mass_ratio",
    "time": "geocent_time",
    "dist": "luminosity_distance",
    "mc": "chirp_mass",
    "a1": "a_1",
    "a2": "a_2",
    "tilt1": "tilt_1",
    "tilt2": "tilt_2",
    "m1": "mass_1",
    "m2": "mass_2",
    "eta": "symmetric_mass_ratio",
    "mtotal": "total_mass",
    "h1_end_time": "H1_time",
    "l1_end_time": "L1_time",
    "v1_end_time": "V1_time",
    "a1z": "spin_1z",
    "a2z": "spin_2z",
    "m1_source": "mass_1_source",
    "m2_source": "mass_2_source",
    "mtotal_source": "total_mass_source",
    "mc_source": "chirp_mass_source",
    "phi1": "phi_1",
    "phi2": "phi_2",
    "costilt1": "cos_tilt_1",
    "costilt2": "cos_tilt_2",
    "costheta_jn": "cos_theta_jn",
    "lambda1": "lambda_1",
    "lambda2": "lambda_2",
    "lambdaT": "lambda_tilde",
    "dLambdaT": "delta_lambda",
    "mf": "final_mass"
}

bilby_map = {
    "chirp_mass": "chirp_mass",
    "mass_ratio": "mass_ratio",
    "a_1": "a_1",
    "a_2": "a_2",
    "tilt_1": "tilt_1",
    "tilt_2": "tilt_2",
    "phi_12": "phi_12",
    "phi_jl": "phi_jl",
    "dec": "dec",
    "ra": "ra",
    "theta_jn": "theta_jn",
    "psi": "psi",
    "luminosity_distance": "luminosity_distance",
    "phase": "phase",
    "geocent_time": "geocent_time",
    "log_likelihood": "log_likelihood",
    "log_prior": "log_prior",
    "reference_frequency": "reference_frequency",
    "total_mass": "total_mass",
    "mass_1": "mass_1",
    "mass_2": "mass_2",
    "symmetric_mass_ratio": "symmetric_mass_ratio",
    "iota": "iota",
    "spin_1x": "spin_1x",
    "spin_1y": "spin_1y",
    "spin_1z": "spin_1z",
    "spin_2x": "spin_2x",
    "spin_2y": "spin_2y",
    "spin_2z": "spin_2z",
    "phi_1": "phi_1",
    "phi_2": "phi_2",
    "chi_eff": "chi_eff",
    "chi_p": "chi_p",
    "redshift": "redshift",
    "mass_1_source": "mass_1_source",
    "mass_2_source": "mass_2_source",
    "chirp_mass_source": "chirp_mass_source",
    "total_mass_source": "total_mass_source",
    "H1_optimal_snr": "H1_optimal_snr",
    "L1_optimal_snr": "L1_optimal_snr",
    "H1_matched_filter_snr_abs": "H1_matched_filter_snr_abs",
    "H1_matched_filter_snr_angle": "H1_matched_filter_snr_angle",
    "L1_matched_filter_snr_abs": "L1_matched_filter_snr_abs",
    "L1_matched_filter_snr_angle": "L1_matched_filter_snr_angle",
    "lambda_1": "lambda_1",
    "lambda_2": "lambda_2",
    "lambda_tilde": "lambda_tilde",
    "cos_iota": "cos_iota",
    "cos_theta_jn": "cos_theta_jn",
}

pesummary_map = {
    "V1_optimal_snr": "V1_optimal_snr",
    "E1_optimal_snr": "E1_optimal_snr",
    "L1_matched_filter_snr": "L1_matched_filter_snr",
    "H1_matched_filter_snr": "H1_matched_filter_snr",
    "V1_matched_filter_snr": "V1_matched_filter_snr",
    "E1_matched_filter_snr": "E1_matched_filter_snr",
    "V1_matched_filter_snr_abs": "V1_matched_filter_snr_abs",
    "E1_matched_filter_snr_abs": "E1_matched_filter_snr_abs",
    "V1_matched_filter_snr_angle": "V1_matched_filter_snr_angle",
    "E1_matched_filter_snr_angle": "E1_matched_filter_snr_angle",
    "chirp_mass_source": "chirp_mass_source",
    "delta_lambda": "delta_lambda",
    "peak_luminosity": "peak_luminosity",
    "final_mass": "final_mass",
    "final_spin": "final_spin",
    "weights": "weights"
}

other_map = {
    "logL": "log_likelihood",
    "lnL": "log_likelihood",
    "loglr": "log_likelihood",
    "tilt_spin1": "tilt_1",
    "theta_1l": "tilt_1",
    "tilt_spin2": "tilt_2",
    "theta_2l": "tilt_2",
    "l1_matched_filter_snr": "L1_matched_filter_snr",
    "h1_matched_filter_snr": "H1_matched_filter_snr",
    "v1_matched_filter_snr": "V1_matched_filter_snr",
    "H1_cplx_snr_amp": "H1_matched_filter_abs_snr",
    "H1_matched_filter_abs_snr": "H1_matched_filter_abs_snr",
    "H1_matched_filter_snr_amp": "H1_matched_filter_abs_snr",
    "L1_cplx_snr_amp": "L1_matched_filter_abs_snr",
    "L1_matched_filter_abs_snr": "L1_matched_filter_abs_snr",
    "L1_matched_filter_snr_amp": "L1_matched_filter_abs_snr",
    "V1_cplx_snr_amp": "V1_matched_filter_abs_snr",
    "V1_matched_filter_abs_snr": "V1_matched_filter_abs_snr",
    "V1_matched_filter_snr_amp": "V1_matched_filter_abs_snr",
    "E1_cplx_snr_amp": "E1_matched_filter_abs_snr",
    "E1_matched_filter_abs_snr": "E1_matched_filter_abs_snr",
    "E1_matched_filter_snr_amp": "E1_matched_filter_abs_snr",
    "H1_cplx_snr_arg": "H1_matched_filter_snr_angle",
    "L1_cplx_snr_arg": "L1_matched_filter_snr_angle",
    "V1_cplx_snr_arg": "V1_matched_filter_snr_angle",
    "E1_cplx_snr_arg": "E1_matched_filter_snr_angle",
    "chirpmass_source": "chirp_mass_source",
    "chirp_mass_source": "chirp_mass_source",
    "mass1": "mass_1",
    "m1_detector_frame_Msun": "mass_1",
    "m2_detector_frame_Msun": "mass_2",
    "mass2": "mass_2",
    "rightascension": "ra",
    "right_ascension": "ra",
    "longitude": "ra",
    "declination": "dec",
    "latitude": "dec",
    "incl": "iota",
    "inclination": "iota",
    "phi_1l": "phi_1",
    "phi_2l": "phi_2",
    "polarisation": "psi",
    "polarization": "psi",
    "phijl": "phi_jl",
    "a_spin1": "a_1",
    "spin1": "a_1",
    "spin1_a": "a_1",
    "a1x": "spin_1x",
    "a1y": "spin_1y",
    "spin1x": "spin_1x",
    "spin1y": "spin_1y",
    "spin1z": "spin_1z",
    "a_spin2": "a_2",
    "spin2": "a_2",
    "spin2_a": "a_2",
    "a2x": "spin_2x",
    "a2y": "spin_2y",
    "spin2x": "spin_2x",
    "spin2y": "spin_2y",
    "spin2z": "spin_2z",
    "phiorb": "phase",
    "phi0": "phase",
    "distance": "luminosity_distance",
    "luminosity_distance_Mpc": "luminosity_distance",
    "chirpmass": "chirp_mass",
    "tc": "geocent_time",
    "geocent_end_time": "geocent_time",
    "fref": "reference_frequency",
    "time_maxl": "marginalized_geocent_time",
    "tref": "marginalized_geocent_time",
    "phase_maxl": "marginalized_phase",
    "distance_maxl": "marginalized_distance",
    "spin1_azimuthal": "a_1_azimuthal",
    "spin1_polar": "a_1_polar",
    "spin2_azimuthal": "a_2_azimuthal",
    "spin2_polar": "a_2_polar",
    "delta_lambda_tilde": "delta_lambda",
    "logPrior": "log_prior",
    "weight": "weights",
    "V1_optimal_snr": "V1_optimal_snr",
    "E1_optimal_snr": "E1_optimal_snr",
    "L1_matched_filter_snr": "L1_matched_filter_snr",
    "H1_matched_filter_snr": "H1_matched_filter_snr",
    "V1_matched_filter_snr": "V1_matched_filter_snr",
    "E1_matched_filter_snr": "E1_matched_filter_snr",
    "V1_matched_filter_snr_abs": "V1_matched_filter_snr_abs",
    "E1_matched_filter_snr_abs": "E1_matched_filter_snr_abs",
    "V1_matched_filter_snr_angle": "V1_matched_filter_snr_angle",
    "E1_matched_filter_snr_angle": "E1_matched_filter_snr_angle",
    "delta_lambda": "delta_lambda",
    "peak_luminosity": "peak_luminosity",
    "final_mass": "final_mass",
    "final_spin": "final_spin",
    "weights": "weights",
    "inverted_mass_ratio": "inverted_mass_ratio"
}


standard_names = {}
standard_names.update(lalinference_map)
standard_names.update(bilby_map)
standard_names.update(other_map)


descriptive_names = {
    "log_likelihood": "Log Likelihood",
    "tilt_1": (
        "the angle between the total orbital angular momentum, L, and the "
        "primary spin, S1"
    ),
    "tilt_2": (
        "the angle between the total orbital angular momentum, L, and the "
        "secondary spin, S2"
    ),
    "cos_tilt_1": (
        "the cosine of the angle between the total orbital angular momentum, "
        "L, and the primary spin, S1"
    ),
    "cos_tilt_2": (
        "the cosine of the angle between the total orbital angular momentum, "
        "L, and the primary spin, S2"
    ),
    "redshift": "the redshift",
    "L1_optimal_snr": "",
    "H1_optimal_snr": "",
    "V1_optimal_snr": "",
    "E1_optimal_snr": "",
    "network_optimal_snr": "",
    "L1_matched_filter_snr": "",
    "H1_matched_filter_snr": "",
    "V1_matched_filter_snr": "",
    "E1_matched_filter_snr": "",
    "network_matched_filter_snr": "",
    "H1_matched_filter_abs_snr": "",
    "H1_matched_filter_snr_abs": "",
    "L1_matched_filter_abs_snr": "",
    "L1_matched_filter_snr_abs": "",
    "V1_matched_filter_abs_snr": "",
    "V1_matched_filter_snr_abs": "",
    "E1_matched_filter_abs_snr": "",
    "E1_matched_filter_snr_abs": "",
    "H1_matched_filter_snr_angle": "",
    "L1_matched_filter_snr_angle": "",
    "V1_matched_filter_snr_angle": "",
    "E1_matched_filter_snr_angle": "",
    "chirp_mass_source": "",
    "symmetric_mass_ratio": "",
    "mass_1": "the mass of the heavier object in the binary",
    "mass_2": "the mass of the lighter object in the binary",
    "ra": "the right ascension of the source",
    "dec": "the declination of the source",
    "iota": (
        "the angle between the total orbital angular momentum, L, and the "
        "line of sight, N"
    ),
    "cos_iota": (
        "the cosine of the angle between the total orbital angular momentum, L "
        ", and the line of sight, N"
    ),
    "mass_2_source": "the source mass of the lighter object in the binary",
    "mass_1_source": "the source mass of the heavier object in the binary",
    "phi_1": "",
    "phi_2": "",
    "psi": "",
    "phi_12": "",
    "phi_jl": "",
    "a_1": "",
    "spin_1x": "",
    "spin_1y": "",
    "spin_1z": "",
    "a_2": "",
    "spin_2x": "",
    "spin_2y": "",
    "spin_2z": "",
    "chi_p": "",
    "phase": "",
    "luminosity_distance": "the luminosity distance of the source",
    "chirp_mass": "",
    "chi_eff": "",
    "total_mass_source": "the total mass of the binary in the source frame",
    "total_mass": "the total mass of the binary",
    "mass_ratio": (
        "the ratio of the binary component masses. We use the convention that "
        "the mass ratio is always less than 1"
    ),
    "inverted_mass_ratio": (
        "The inverted ratio of the binary component masses. Note that normal "
        "convention is mass ratio less than 1, but here the inverted mass ratio "
        "is always bigger than 1"
    ),
    "geocent_time": "",
    "theta_jn": (
        "the angle between the total angular momentum, J, and the line of "
        "sight, N"
    ),
    "cos_theta_jn": (
        "the cosine of the angle between the total angular momentum, J, and "
        "the line of sight, N"
    ),
    "reference_frequency": "",
    "H1_time": "",
    "L1_time": "",
    "V1_time": "",
    "a_1_azimuthal": "",
    "a_1_polar": "",
    "a_2_azimuthal": "",
    "a_2_polar": "",
    "lambda_1": "",
    "lambda_2": "",
    "lambda_tilde": "",
    "delta_lambda": "",
    "peak_luminosity": "",
    "final_mass": "",
    "final_spin": "",
}

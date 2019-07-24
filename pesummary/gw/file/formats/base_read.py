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

import numpy as np
from scipy import interpolate
from pesummary.gw.file.standard_names import standard_names
from pesummary.core.file.formats.base_read import Read
from pesummary.utils.utils import logger
from pesummary.gw.file import conversions as con


class GWRead(Read):
    """Base class to read in a results file
    """
    def __init__(self, path_to_results_file):
        super(GWRead, self).__init__(path_to_results_file)

    def load(self, function, **kwargs):
        """Load a results file according to a given function

        Parameters
        ----------
        function: func
            callable function that will load in your results file
        """
        data = self.load_from_function(
            function, self.path_to_results_file, **kwargs)
        self.data = list(self.translate_parameters(data[0], data[1]))
        self.data.append(data[2])

    @staticmethod
    def check_for_calibration_data(function, path_to_results_file):
        """Check to see if there is any calibration data in the results file

        Parameters
        ----------
        function: func
            callable function that will check to see if calibration data is in
            the results file
        path_to_results_file: str
            path to the results file
        """
        return function(path_to_results_file)

    @staticmethod
    def grab_calibration_data(function, path_to_results_file):
        """Grab the calibration data from the results file

        Parameters
        ----------
        function: func
            callable function that will grab the calibration data from the
            results file
        path_to_results_file: str
            path to the results file
        """
        log_frequencies, amp_params, phase_params = function(path_to_results_file)
        total = []
        for key in log_frequencies.keys():
            f = np.exp(log_frequencies[key])
            fs = np.linspace(np.min(f), np.max(f), 100)
            data = [interpolate.spline(log_frequencies[key], samp, np.log(fs)) for samp
                    in np.column_stack(amp_params[key])]
            amplitude_upper = 1. - np.percentile(data, 90, axis=0)
            amplitude_lower = 1. - np.percentile(data, 10, axis=0)
            amplitude_median = 1. - np.median(data, axis=0)

            data = [interpolate.spline(log_frequencies[key], samp, np.log(fs)) for samp
                    in np.column_stack(phase_params[key])]

            phase_upper = np.percentile(data, 90, axis=0)
            phase_lower = np.percentile(data, 10, axis=0)
            phase_median = np.median(data, axis=0)
            total.append(np.column_stack(
                [fs, amplitude_median, phase_median, amplitude_lower,
                 phase_lower, amplitude_upper, phase_upper]))
        return total, log_frequencies.keys()

    @staticmethod
    def load_strain_data(path_to_strain_file):
        """Load the strain data

        Parameters
        ----------
        path_to_strain_file: str
            path to the strain file that you wish to load
        """
        func_map = {"lcf": GWRead._timeseries_from_cache_file}
        ext = GWRead.extension_from_path(path_to_strain_file)
        function = func_map[ext]
        return GWRead.load_from_function(function, path_to_strain_file)

    def _timeseries_from_cache_file(self, channel, cached_file):
        """Return a time series from a cache file

        Parameters
        ----------
        channel: str
            the name of the channel for the cache file
        cached_file: str
            path to the cached file
        """
        from gwpy.timeseries import TimeSeries

        try:
            from glue.lal import Cache
            GLUE = True
        except ImportError:
            GLUE = False

        if not GLUE:
            raise Exception("lscsoft-glue is required to read from a cached "
                            "file. Please install this package")
        with open(cached_file, "r") as f:
            data = Cache.fromfile(f)
        try:
            strain_data = TimeSeries.read(data, channel)
        except Exception as e:
            raise Exception("Failed to read in the cached file because %s" % (
                            e))
        return strain_data

    @staticmethod
    def translate_parameters(parameters, samples):
        """Translate parameters to a standard names

        Parameters
        ----------
        parameters: list
            list of parameters used in the analysis
        samples: list
            list of samples for each parameters
        """
        path = ("https://git.ligo.org/lscsoft/pesummary/blob/master/pesummary/"
                "gw/file/standard_names.py")
        standard_params = [i for i in parameters if i in standard_names.keys()]
        parameters_not_included = [
            i for i in parameters if i not in standard_params]
        standard_samples = []
        for i in samples:
            standard_samples.append(
                [i[parameters.index(j)] for j in standard_params])
        standard_params = [standard_names[i] for i in standard_params]
        return standard_params, standard_samples

    @staticmethod
    def _check_definition_of_inclination(parameters):
        """Check the definition of inclination given the other parameters

        Parameters
        ----------
        parameters: list
            list of parameters used in the study
        """
        theta_jn = False
        spin_angles = ["tilt_1", "tilt_2", "a_1", "a_2"]
        names = [
            standard_names[i] for i in parameters if i in standard_names.keys()]
        if all(i in names for i in spin_angles):
            theta_jn = True
        if theta_jn:
            if "theta_jn" not in names and "inclination" in parameters:
                logger.warn("Because the spin angles are in your list of "
                            "parameters, the angle 'inclination' probably "
                            "refers to 'theta_jn'. If this is a mistake, "
                            "please change the definition of 'inclination' to "
                            "'iota' in your results file")
                index = parameters.index("inclination")
                parameters[index] = "theta_jn"
        else:
            if "inclination" in parameters:
                index = parameters.index("inclination")
                parameters[index] = "iota"
        return parameters

    def add_fixed_parameters_from_config_file(self, config_file):
        """Search the conifiguration file and add fixed parameters to the
        list of parameters and samples

        Parameters
        ----------
        config_file: str
            path to the configuration file
        """
        self._add_fixed_parameters_from_config_file(
            config_file, self._add_fixed_parameters)

    @staticmethod
    def _add_fixed_parameters(parameters, samples, config_file):
        """Open a LALInference configuration file and add the fixed parameters
        to the list of parameters and samples

        Parameters
        ----------
        parameters: list
            list of existing parameters
        samples: list
            list of existing samples
        config_file: str
            path to the configuration file
        """
        import configparser
        from pesummary.gw.file.standard_names import standard_names

        config = configparser.ConfigParser()
        try:
            config.read(config_file)
            fixed_data = None
            if "engine" in config.sections():
                fixed_data = {
                    key.split("fix-")[1]: item for key, item in
                    config.items("engine") if "fix" in key}
            for i in fixed_data.keys():
                fixed_parameter = i
                fixed_value = fixed_data[i]
                try:
                    param = standard_names[fixed_parameter]
                    if param in parameters:
                        pass
                    else:
                        parameters.append(param)
                        for num in range(len(samples)):
                            samples[num].append(float(fixed_value))
                except Exception:
                    if fixed_parameter == "logdistance":
                        if "luminosity_distance" not in parameters:
                            parameters.append(standard_names["distance"])
                            for num in range(len(samples)):
                                samples[num].append(float(fixed_value))
                    if fixed_parameter == "costheta_jn":
                        if "theta_jn" not in parameters:
                            parameters.append(standard_names["theta_jn"])
                            for num in range(len(samples)):
                                samples[num].append(float(fixed_value))
            return parameters, samples
        except Exception:
            return parameters, samples

    def _specific_parameter_samples(self, param):
        """Return the samples for a specific parameter

        Parameters
        ----------
        param: str
            the parameter that you would like to return the samples for
        """
        ind = self.parameters.index(param)
        samples = np.array([i[ind] for i in self.samples])
        return samples

    def specific_parameter_samples(self, param):
        """Return the samples for either a list or a single parameter

        Parameters
        ----------
        param: list/str
            the parameter/parameters that you would like to return the samples
            for
        """
        if type(param) == list:
            samples = [self._specific_parameter_samples(i) for i in param]
        else:
            samples = self._specific_parameter_samples(param)
        return samples

    def append_data(self, samples):
        """Add a list of samples to the existing samples data object

        Parameters
        ----------
        samples: list
            the list of samples that you would like to append
        """
        for num, i in enumerate(self.samples):
            self.samples[num].append(samples[num])

    def _mchirp_from_mchirp_source_z(self):
        self.parameters.append("chirp_mass")
        samples = self.specific_parameter_samples(["chirp_mass_source", "redshift"])
        chirp_mass = con.mchirp_from_mchirp_source_z(samples[0], samples[1])
        self.append_data(chirp_mass)

    def _q_from_eta(self):
        self.parameters.append("mass_ratio")
        samples = self.specific_parameter_samples("symmetric_mass_ratio")
        mass_ratio = con.q_from_eta(samples)
        self.append_data(mass_ratio)

    def _q_from_m1_m2(self):
        self.parameters.append("mass_ratio")
        samples = self.specific_parameter_samples(["mass_1", "mass_2"])
        mass_ratio = con.q_from_m1_m2(samples[0], samples[1])
        self.append_data(mass_ratio)

    def _invert_q(self):
        ind = self.parameters.index("mass_ratio")
        for num, i in enumerate(self.samples):
            self.samples[num][ind] = 1. / self.samples[num][ind]

    def _mchirp_from_mtotal_q(self):
        self.parameters.append("chirp_mass")
        samples = self.specific_parameter_samples(["total_mass", "mass_ratio"])
        chirp_mass = con.mchirp_from_mtotal_q(samples[0], samples[1])
        self.append_data(chirp_mass)

    def _m1_from_mchirp_q(self):
        self.parameters.append("mass_1")
        samples = self.specific_parameter_samples(["chirp_mass", "mass_ratio"])
        mass_1 = con.m1_from_mchirp_q(samples[0], samples[1])
        self.append_data(mass_1)

    def _m2_from_mchirp_q(self):
        self.parameters.append("mass_2")
        samples = self.specific_parameter_samples(["chirp_mass", "mass_ratio"])
        mass_2 = con.m2_from_mchirp_q(samples[0], samples[1])
        self.append_data(mass_2)

    def _reference_frequency(self):
        self.parameters.append("reference_frequency")
        nsamples = len(self.samples)
        self.append_data([20.] * nsamples)

    def _mtotal_from_m1_m2(self):
        self.parameters.append("total_mass")
        samples = self.specific_parameter_samples(["mass_1", "mass_2"])
        m_total = con.m_total_from_m1_m2(samples[0], samples[1])
        self.append_data(m_total)

    def _mchirp_from_m1_m2(self):
        self.parameters.append("chirp_mass")
        samples = self.specific_parameter_samples(["mass_1", "mass_2"])
        chirp_mass = con.m_total_from_m1_m2(samples[0], samples[1])
        self.append_data(chirp_mass)

    def _eta_from_m1_m2(self):
        self.parameters.append("symmetric_mass_ratio")
        samples = self.specific_parameter_samples(["mass_1", "mass_2"])
        eta = con.eta_from_m1_m2(samples[0], samples[1])
        self.append_data(eta)

    def _phi_12_from_phi1_phi2(self):
        self.parameters.append("phi_12")
        samples = self.specific_parameter_samples(["phi_1", "phi_2"])
        phi_12 = con.phi_12_from_phi1_phi2(samples[0], samples[1])
        self.append_data(phi_12)

    def _spin_angles(self):
        spin_angles = ["theta_jn", "phi_jl", "tilt_1", "tilt_2", "phi_12",
                       "a_1", "a_2"]
        spin_angles_to_calculate = [
            i for i in spin_angles if i not in self.parameters]
        for i in spin_angles_to_calculate:
            self.parameters.append(i)
        spin_components = [
            "mass_1", "mass_2", "iota", "spin_1x", "spin_1y", "spin_1z",
            "spin_2x", "spin_2y", "spin_2z", "reference_frequency"]
        samples = self.specific_parameter_samples(spin_components)
        if "phase" in self.parameters:
            spin_components.append("phase")
            samples.append(self.specific_parameter_samples("phase"))
        else:
            logger.warn("Phase it not given, we will be assuming that a "
                        "reference phase of 0 to calculate all the spin angles")
            samples.append([0] * len(samples[0]))
        spin_angles = con.spin_angles(
            samples[0], samples[1], samples[2], samples[3], samples[4],
            samples[5], samples[6], samples[7], samples[8], samples[9],
            samples[10])

        for i in spin_angles_to_calculate:
            ind = spin_angles_to_calculate.index(i)
            data = np.array([i[ind] for i in spin_angles])
            self.append_data(data)

    def _non_precessing_component_spins(self):
        spins = ["iota", "spin_1x", "spin_1y", "spin_1z", "spin_2x", "spin_2y",
                 "spin_2z"]
        spin_angles = ["a_1", "a_2", "theta_jn", "tilt_1", "tilt_2"]
        if all(i in self.parameters for i in spin_angles):
            samples = self.specific_parameter_samples(spin_angles)
            cond1 = all(i in [0, np.pi] for i in samples[3])
            cond2 = all(i in [0, np.pi] for i in samples[4])
            spins_to_calculate = [
                i for i in spins if i not in self.parameters]
            if cond1 and cond1:
                spin_1x = np.array([0.] * len(samples[0]))
                spin_1y = np.array([0.] * len(samples[0]))
                spin_1z = samples[0] * np.cos(samples[3])
                spin_2x = np.array([0.] * len(samples[0]))
                spin_2y = np.array([0.] * len(samples[0]))
                spin_2z = samples[1] * np.cos(samples[4])
                iota = np.array(samples[2])
                data = [
                    iota, spin_1x, spin_1y, spin_1z, spin_2x, spin_2y, spin_2z]

                for num, i in enumerate(spins_to_calculate):
                    self.parameters.append(i)
                    self.append_data(data[num])

    def _component_spins(self):
        spins = ["iota", "spin_1x", "spin_1y", "spin_1z", "spin_2x", "spin_2y",
                 "spin_2z"]
        spins_to_calculate = [
            i for i in spins if i not in self.parameters]
        for i in spins_to_calculate:
            self.parameters.append(i)
        spin_angles = [
            "theta_jn", "phi_jl", "tilt_1", "tilt_2", "phi_12", "a_1", "a_2",
            "mass_1", "mass_2", "reference_frequency"]
        samples = self.specific_parameter_samples(spin_angles)
        if "phase" in self.parameters:
            spin_angles.append("phase")
            samples.append(self.specific_parameter_samples("phase"))
        else:
            logger.warn("Phase it not given, we will be assuming that a "
                        "reference phase of 0 to calculate all the spin angles")
            samples.append([0] * len(samples[0]))
        spin_components = con.component_spins(
            samples[0], samples[1], samples[2], samples[3], samples[4],
            samples[5], samples[6], samples[7], samples[8], samples[9],
            samples[10])

        for i in spins_to_calculate:
            ind = spins.index(i)
            data = np.array([i[ind] for i in spin_components])
            self.append_data(data)

    def _component_spins_from_azimuthal_and_polar_angles(self):
        spins = ["spin_1x", "spin_1y", "spin_1z", "spin_2x", "spin_2y",
                 "spin_2z"]
        spins_to_calculate = [
            i for i in spins if i not in self.parameters]
        for i in spins_to_calculate:
            self.parameters.append(i)
        spin_angles = [
            "a_1", "a_2", "a_1_azimuthal", "a_1_polar", "a_2_azimuthal",
            "a_2_polar"]
        samples = self.specific_parameter_samples(spin_angles)
        spin_components = con.spin_angles_from_azimuthal_and_polar_angles(
            samples[0], samples[1], samples[2], samples[3], samples[4],
            samples[5])
        for i in spins_to_calculate:
            ind = spins.index(i)
            data = np.array([i[ind] for i in spin_components])
            self.append_data(data)

    def _chi_p(self):
        self.parameters.append("chi_p")
        parameters = [
            "mass_1", "mass_2", "spin_1x", "spin_1y", "spin_2x", "spin_2y"]
        samples = self.specific_parameter_samples(parameters)
        chi_p_samples = con.chi_p(
            samples[0], samples[1], samples[2], samples[3], samples[4],
            samples[5])
        self.append_data(chi_p_samples)

    def _chi_eff(self):
        self.parameters.append("chi_eff")
        parameters = ["mass_1", "mass_2", "spin_1z", "spin_2z"]
        samples = self.specific_parameter_samples(parameters)
        chi_eff_samples = con.chi_eff(
            samples[0], samples[1], samples[2], samples[3])
        self.append_data(chi_eff_samples)

    def _cos_tilt_1_from_tilt_1(self):
        self.parameters.append("cos_tilt_1")
        samples = self.specific_parameter_samples("tilt_1")
        cos_tilt_1 = np.cos(samples)
        self.append_data(cos_tilt_1)

    def _cos_tilt_2_from_tilt_2(self):
        self.parameters.append("cos_tilt_2")
        samples = self.specific_parameter_samples("tilt_2")
        cos_tilt_2 = np.cos(samples)
        self.append_data(cos_tilt_2)

    def _dL_from_z(self):
        self.parameters.append("luminosity_distance")
        samples = self.specific_parameter_samples("redshift")
        distance = con.dL_from_z(samples)
        self.append_data(distance)

    def _z_from_dL(self):
        self.parameters.append("redshift")
        samples = self.specific_parameter_samples("luminosity_distance")
        redshift = con.z_from_dL_approx(samples)
        self.append_data(redshift)

    def _comoving_distance_from_z(self):
        self.parameters.append("comoving_distance")
        samples = self.specific_parameter_samples("redshift")
        distance = con.comoving_distance_from_z(samples)
        self.append_data(distance)

    def _m1_source_from_m1_z(self):
        self.parameters.append("mass_1_source")
        samples = self.specific_parameter_samples(["mass_1", "redshift"])
        mass_1_source = con.m1_source_from_m1_z(samples[0], samples[1])
        self.append_data(mass_1_source)

    def _m2_source_from_m2_z(self):
        self.parameters.append("mass_2_source")
        samples = self.specific_parameter_samples(["mass_2", "redshift"])
        mass_2_source = con.m2_source_from_m2_z(samples[0], samples[1])
        self.append_data(mass_2_source)

    def _mtotal_source_from_mtotal_z(self):
        self.parameters.append("total_mass_source")
        samples = self.specific_parameter_samples(["total_mass", "redshift"])
        total_mass_source = con.m_total_source_from_mtotal_z(samples[0], samples[1])
        self.append_data(total_mass_source)

    def _mchirp_source_from_mchirp_z(self):
        self.parameters.append("chirp_mass_source")
        samples = self.specific_parameter_samples(["chirp_mass", "redshift"])
        chirp_mass_source = con.mchirp_source_from_mchirp_z(samples[0], samples[1])
        self.append_data(chirp_mass_source)

    def _time_in_each_ifo(self):
        detectors = []
        for i in self.parameters:
            if "optimal_snr" in i and i != "network_optimal_snr":
                det = i.split("_optimal_snr")[0]
                detectors.append(det)

        samples = self.specific_parameter_samples(["ra", "dec", "geocent_time"])
        for i in detectors:
            time = con.time_in_each_ifo(i, samples[0], samples[1], samples[2])
            self.append_data(time)
            self.parameters.append("%s_time" % (i))

    def _lambda1_from_lambda_tilde(self):
        self.parameters.append("lambda_1")
        samples = self.specific_parameter_samples([
            "lambda_tilde", "mass_1", "mass_2"])
        lambda_1 = con.lambda1_from_lambda_tilde(samples[0], samples[1], samples[2])
        self.append_data(lambda_1)

    def _lambda2_from_lambda1(self):
        self.parameters.append("lambda_2")
        samples = self.specific_parameter_samples([
            "lambda_1", "mass_1", "mass_2"])
        lambda_2 = con.lambda2_from_lambda1(samples[0], samples[1], samples[2])
        self.append_data(lambda_2)

    def _lambda_tilde_from_lambda1_lambda2(self):
        self.parameters.append("lambda_tilde")
        samples = self.specific_parameter_samples([
            "lambda_1", "lambda_2", "mass_1", "mass_2"])
        lambda_tilde = con.lambda_tilde_from_lambda1_lambda2(
            samples[0], samples[1], samples[2], samples[3])
        self.append_data(lambda_tilde)

    def _delta_lambda_from_lambda1_lambda2(self):
        self.parameters.append("delta_lambda")
        samples = self.specific_parameter_samples([
            "lambda_1", "lambda_2", "mass_1", "mass_2"])
        delta_lambda = con.delta_lambda_from_lambda1_lambda2(
            samples[0], samples[1], samples[2], samples[3])
        self.append_data(delta_lambda)

    def _optimal_network_snr(self):
        snrs = [i for i in self.parameters if "_optimal_snr" in i]
        samples = self.specific_parameter_samples(snrs)
        self.parameters.append("network_optimal_snr")
        network_snr = con.network_snr(samples)
        self.append_data(network_snr)

    def _matched_filter_network_snr(self):
        snrs = [i for i in self.parameters if "_matched_filter_snr" in i]
        samples = self.specific_parameter_samples(snrs)
        self.parameters.append("network_matched_filter_snr")
        network_snr = con.network_snr(samples)
        self.append_data(network_snr)

    def generate_all_posterior_samples(self):
        logger.debug("Starting to generate all derived posteriors")
        if "chirp_mass" not in self.parameters and "chirp_mass_source" in \
                self.parameters and "redshift" in self.parameters:
            self._mchirp_from_mchirp_source_z()
        if "mass_ratio" not in self.parameters and "symmetric_mass_ratio" in \
                self.parameters:
            self._q_from_eta()
        if "mass_ratio" not in self.parameters and "mass_1" in self.parameters \
                and "mass_2" in self.parameters:
            self._q_from_m1_m2()
        if "mass_ratio" in self.parameters:
            ind = self.parameters.index("mass_ratio")
            median = np.median([i[ind] for i in self.samples])
            if median > 1.:
                self._invert_q()
        if "chirp_mass" not in self.parameters and "total_mass" in self.parameters:
            self._mchirp_from_mtotal_q()
        if "mass_1" not in self.parameters and "chirp_mass" in self.parameters:
            self._m1_from_mchirp_q()
        if "mass_2" not in self.parameters and "chirp_mass" in self.parameters:
            self._m2_from_mchirp_q()
        if "reference_frequency" not in self.parameters:
            self._reference_frequency()

        condition1 = "phi_12" not in self.parameters
        condition2 = "phi_1" in self.parameters and "phi_2" in self.parameters
        if condition1 and condition2:
            self._phi_12_from_phi1_phi2()
        spin_angles = [
            "a_1", "a_2", "a_1_azimuthal", "a_1_polar", "a_2_azimuthal",
            "a_2_polar"]
        if all(i in self.parameters for i in spin_angles):
            self._component_spins_from_azimuthal_and_polar_angles()
        if "mass_1" in self.parameters and "mass_2" in self.parameters:
            if "total_mass" not in self.parameters:
                self._mtotal_from_m1_m2()
            if "chirp_mass" not in self.parameters:
                self._mchirp_from_m1_m2()
            if "symmetric_mass_ratio" not in self.parameters:
                self._eta_from_m1_m2()
            spin_components = [
                "spin_1x", "spin_1y", "spin_1z", "spin_2x", "spin_2y", "spin_2z"]
            spin_angles = ["a_1", "a_2", "tilt_1", "tilt_2", "theta_jn"]
            if all(i in self.parameters for i in spin_components):
                self._spin_angles()
            if all(i in self.parameters for i in spin_angles):
                samples = self.specific_parameter_samples(["tilt_1", "tilt_2"])
                cond1 = all(i in [0, np.pi] for i in samples[0])
                cond2 = all(i in [0, np.pi] for i in samples[1])
                if cond1 and cond1:
                    self._non_precessing_component_spins()
                else:
                    spin_angles = [
                        "phi_jl", "phi_12", "reference_frequency"]
                    if all(i in self.parameters for i in spin_angles):
                        self._component_spins()
            if "chi_p" not in self.parameters and "chi_eff" not in self.parameters:
                if all(i in self.parameters for i in spin_components):
                    self._chi_p()
                    self._chi_eff()
            if "lambda_tilde" in self.parameters and "lambda_1" not in self.parameters:
                self._lambda1_from_lambda_tilde()
            if "lambda_2" not in self.parameters and "lambda_1" in self.parameters:
                self._lambda2_from_lambda1()
            if "lambda_1" in self.parameters and "lambda_2" in self.parameters:
                if "lambda_tilde" not in self.parameters:
                    self._lambda_tilde_from_lambda1_lambda2()
                if "delta_lambda" not in self.parameters:
                    self._delta_lambda_from_lambda1_lambda2()
        if "cos_tilt_1" not in self.parameters and "tilt_1" in self.parameters:
            self._cos_tilt_1_from_tilt_1()
        if "cos_tilt_2" not in self.parameters and "tilt_2" in self.parameters:
            self._cos_tilt_2_from_tilt_2()
        if "luminosity_distance" not in self.parameters and "redshift" in self.parameters:
            self._dL_from_z()
        if "redshift" not in self.parameters and "luminosity_distance" in self.parameters:
            self._z_from_dL()
        if "comoving_distance" not in self.parameters and "redshift" in self.parameters:
            self._comoving_distance_from_z()
        if "redshift" in self.parameters:
            if "mass_1_source" not in self.parameters and "mass_1" in self.parameters:
                self._m1_source_from_m1_z()
            if "mass_2_source" not in self.parameters and "mass_2" in self.parameters:
                self._m2_source_from_m2_z()
            if "total_mass_source" not in self.parameters and "total_mass" in self.parameters:
                self._mtotal_source_from_mtotal_z()
            if "chirp_mass_source" not in self.parameters and "chirp_mass" in self.parameters:
                self._mchirp_source_from_mchirp_z()

        location = ["geocent_time", "ra", "dec"]
        if all(i in self.parameters for i in location):
            try:
                self._time_in_each_ifo()
            except Exception as e:
                logger.warn("Failed to generate posterior samples for the time in each "
                            "detector because %s" % (e))
        if any("_optimal_snr" in i for i in self.parameters):
            if "network_optimal_snr" not in self.parameters:
                self._optimal_network_snr()
        if any("_matched_filter_snr" in i for i in self.parameters):
            if "network_matched_filter_snr" not in self.parameters:
                self._matched_filter_network_snr()

        if "reference_frequency" in self.parameters:
            ind = self.parameters.index("reference_frequency")
            self.parameters.remove(self.parameters[ind])
            for i in self.samples:
                del i[ind]
        if "minimum_frequency" in self.parameters:
            ind = self.parameters.index("minimum_frequency")
            self.parameters.remove(self.parameters[ind])
            for i in self.samples:
                del i[ind]
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

import os
import numpy as np
from pesummary.gw.file.formats.base_read import GWRead


class Bilby(GWRead):
    """PESummary wrapper of `bilby` (https://git.ligo.org/lscsoft/bilby). The
    path_to_results_file argument will be passed directly to
    `bilby.core.result.read_in_result`. All functions therefore use `bilby`
    methods and requires `bilby` to be installed.

    Attributes
    ----------
    path_to_results_file: str
        path to the results file that you wish to read in with `bilby`.
    kwargs: dict
        additional arguments that will be passed directly to `bilby`
    """
    def __init__(self, path_to_results_file, **kwargs):
        super(Bilby, self).__init__(path_to_results_file)
        self.load(self._grab_data_from_bilby_file)

    @classmethod
    def load_file(cls, path):
        if not os.path.isfile(path):
            raise Exception("%s does not exist" % (path))
        return cls(path)

    @staticmethod
    def _check_for_calibration_data_in_bilby_file(path):
        """
        """
        from bilby.core.result import read_in_result

        bilby_object = read_in_result(filename=path)
        parameters = bilby_object.search_parameter_keys
        if any("recalib_" in i for i in parameters):
            return True
        return False

    @property
    def calibration_data_in_results_file(self):
        """
        """
        check = Bilby._check_for_calibration_data_in_bilby_file
        grab = Bilby._grab_calibration_data_from_bilby_file
        if self.check_for_calibration_data(check, self.path_to_results_file):
            return self.grab_calibration_data(grab, self.path_to_results_file)
        return None

    @staticmethod
    def _grab_calibration_data_from_bilby_file(path):
        """
        """
        from bilby.core.result import read_in_result

        bilby_object = read_in_result(filename=path)
        posterior = bilby_object.posterior
        parameters = list(posterior.keys())
        ifos = np.unique(
            [param.split('_')[1] for param in parameters if 'recalib_' in param])

        amp_params, phase_params, log_freqs = {}, {}, {}
        for ifo in ifos:
            amp_params[ifo], phase_params[ifo] = [], []
            freq_params = np.sort(
                [param for param in parameters if 'recalib_%s_frequency_' % (ifo)
                 in param])
            log_freqs[ifo] = np.log([posterior[param].iloc[0] for param in freq_params])
            amp_parameters = np.sort(
                [param for param in parameters if 'recalib_%s_amplitude_' % (ifo)
                 in param])
            amplitude = np.array([posterior[param] for param in amp_parameters])
            phase_parameters = np.sort(
                [param for param in parameters if 'recalib_%s_phase_' % (ifo)
                 in param])
            phase = np.array([posterior[param] for param in phase_parameters])
            for num, i in enumerate(amplitude):
                amp_params[ifo].append(i)
                phase_params[ifo].append(phase[num])
        return log_freqs, amp_params, phase_params

    @staticmethod
    def load_strain_data(path_to_strain_file):
        """Load the strain data

        Parameters
        ----------
        path_to_strain_file: str
            path to the strain file that you wish to load
        """
        Bilby.load_from_function(
            Bilby._timeseries_from_bilby_pickle, path_to_strain_file)

    @staticmethod
    def _timeseries_from_bilby_pickle(path_to_strain_file):
        """Load a bilby pickle file containing the strain data

        Parameters
        ----------
        path_to_strain_file: str
            path to the strain file that you wish to load
        """
        import pickle
        import gwpy

        with open(path_to_strain_file, "rb") as f:
            data = pickle.load(f)

        strain_data = {}
        for i in data.interferometers:
            strain_data[i.name] = gwpy.timeseries.TimeSeries(
                data=i.strain_data.time_domain_strain,
                times=i.strain_data.time_array)
        return strain_data

    @staticmethod
    def _grab_data_from_bilby_file(path):
        """Load the results file using the `bilby` library
        """
        from bilby.core.result import read_in_result

        bilby_object = read_in_result(filename=path)
        posterior = bilby_object.posterior
        parameters = list(posterior.keys())
        number = len(posterior[parameters[0]])
        samples = [[np.real(posterior[param][i]) for param in parameters] for i in range(number)]
        injection = bilby_object.injection_parameters
        if injection is None:
            injection = {i: j for i, j in zip(
                parameters, [float("nan")] * len(parameters))}
        else:
            for i in parameters:
                if i not in injection.keys():
                    injection[i] = float("nan")
        return parameters, samples, injection

    def add_marginalized_parameters_from_config_file(self, config_file):
        """Search the configuration file and add the marginalized parameters
        to the list of parameters and samples

        Parameters
        ----------
        config_file: str
            path to the configuration file
        """
        pass
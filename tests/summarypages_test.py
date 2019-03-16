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
import shutil
from glob import glob

from pesummary.command_line import command_line
from pesummary.inputs import Input
from pesummary.summarypages import WebpageGeneration

import pytest


class TestWebpageGeneration(object):

    def setup(self):
        directories = ["./.outdir_cbc", "./.outdir_bilby",
                       "./.outdir_lalinference", "./.outdir_comparison"]
        for i in directories:
            if os.path.isdir(i):
                shutil.rmtree(i)
            os.makedirs(i)

    def test_webpage_generation_for_bilby_structure(self):
        parser = command_line()
        default_arguments = [
            "--approximant", "IMRPhenomPv2",
            "--webdir", "./.outdir_bilby",
            "--samples", "./tests/files/bilby_example.h5",
            "--config", "./tests/files/config_bilby.ini"]
        opts = parser.parse_args(default_arguments)
        inputs = Input(opts)
        webpage = WebpageGeneration(inputs)
        html = sorted(glob("./.outdir_bilby/html/*"))
        expected_html = ['./.outdir_bilby/html/H1_IMRPhenomPv2_config.html',
                         './.outdir_bilby/html/H1_IMRPhenomPv2_multiple.html',
                         './.outdir_bilby/html/H1_IMRPhenomPv2.html',
                         './.outdir_bilby/html/H1_IMRPhenomPv2_mass_1.html',
                         './.outdir_bilby/html/H1_IMRPhenomPv2_log_likelihood.html',
                         './.outdir_bilby/html/H1_IMRPhenomPv2_corner.html',
                         './.outdir_bilby/html/H1_IMRPhenomPv2_H1_optimal_snr.html',
                         './.outdir_bilby/html/error.html']
        assert all(i == j for i,j in zip(sorted(expected_html), sorted(html)))

    def test_webpage_generation_for_lalinference_structure(self):
        parser = command_line()
        default_arguments = [
            "--approximant", "IMRPhenomPv2",
            "--webdir", "./.outdir_lalinference",
            "--samples", "./tests/files/lalinference_example.h5",
            "--config", "./tests/files/config_lalinference.ini"]
        opts = parser.parse_args(default_arguments)
        inputs = Input(opts)
        webpage = WebpageGeneration(inputs)
        html = sorted(glob("./.outdir_lalinference/html/*"))
        expected_html = ['./.outdir_lalinference/html/H1_IMRPhenomPv2_corner.html',
                         './.outdir_lalinference/html/H1_IMRPhenomPv2.html',
                         './.outdir_lalinference/html/H1_IMRPhenomPv2_multiple.html',
                         './.outdir_lalinference/html/H1_IMRPhenomPv2_log_likelihood.html',
                         './.outdir_lalinference/html/H1_IMRPhenomPv2_mass_1.html',
                         './.outdir_lalinference/html/H1_IMRPhenomPv2_config.html',
                         './.outdir_lalinference/html/H1_IMRPhenomPv2_H1_optimal_snr.html',
                         './.outdir_lalinference/html/error.html']
        assert all(i == j for i,j in zip(sorted(expected_html), sorted(html)))

    def test_webpage_generation_for_comparison(self):
        parser = command_line()
        default_arguments = [
            "--approximant", "IMRPhenomPv2", "IMRPhenomP",
            "--webdir", "./.outdir_comparison",
            "--samples", "./tests/files/bilby_example.h5",
            "./tests/files/lalinference_example.h5"]
        opts = parser.parse_args(default_arguments)
        inputs = Input(opts)
        webpage = WebpageGeneration(inputs)
        html = sorted(glob("./.outdir_comparison/html/*"))
        expected_html = ['./.outdir_comparison/html/H1_IMRPhenomP_corner.html',
                         './.outdir_comparison/html/Comparison_log_likelihood.html',
                         './.outdir_comparison/html/H1_IMRPhenomPv2_corner.html',
                         './.outdir_comparison/html/H1_IMRPhenomP.html',
                         './.outdir_comparison/html/H1_IMRPhenomPv2.html',
                         './.outdir_comparison/html/H1_IMRPhenomP_config.html',
                         './.outdir_comparison/html/H1_IMRPhenomPv2_multiple.html',
                         './.outdir_comparison/html/Comparison.html',
                         './.outdir_comparison/html/Comparison_multiple.html',
                         './.outdir_comparison/html/H1_IMRPhenomPv2_log_likelihood.html',
                         './.outdir_comparison/html/H1_IMRPhenomP_mass_1.html',
                         './.outdir_comparison/html/Comparison_mass_1.html',
                         './.outdir_comparison/html/Comparison_H1_optimal_snr.html',
                         './.outdir_comparison/html/H1_IMRPhenomPv2_mass_1.html',
                         './.outdir_comparison/html/H1_IMRPhenomP_multiple.html',
                         './.outdir_comparison/html/H1_IMRPhenomP_log_likelihood.html',
                         './.outdir_comparison/html/H1_IMRPhenomPv2_config.html',
                         './.outdir_comparison/html/H1_IMRPhenomPv2_H1_optimal_snr.html',
                         './.outdir_comparison/html/H1_IMRPhenomP_H1_optimal_snr.html',
                         './.outdir_comparison/html/error.html']
        assert all(i == j for i,j in zip(sorted(html), sorted(expected_html)))

    def test_webpage_generation_for_full_cbc(self):
        parser = command_line()
        default_arguments = [
            "--approximant", "IMRPhenomPv2",
            "--webdir", "./.outdir_cbc",
            "--samples", "./tests/files/GW150914_result.h5"]
        opts = parser.parse_args(default_arguments)
        inputs = Input(opts)
        webpage = WebpageGeneration(inputs)
        html = glob("./.outdir_cbc/html/*")
        expected_html = ['./.outdir_cbc/html/0_IMRPhenomPv2_dec.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_luminosity_distance.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_phase.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_spin_1z.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_ra.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_phi_jl.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_spin_2x.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_corner.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_phi_12.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_mass_2.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_symmetric_mass_ratio.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_tilt_2.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_multiple.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_chi_p.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_spin_1y.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_mass_ratio.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_log_likelihood.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_total_mass.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_a_2.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_psi.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_mass_1.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_spin_2z.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_chi_eff.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_geocent_time.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_spin_1x.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_cos_tilt_2.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_chirp_mass.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_tilt_1.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_iota.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_a_1.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_spin_2y.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_cos_tilt_1.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_config.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_redshift.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_comoving_distance.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_mass_1_source.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_mass_2_source.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_total_mass_source.html',
                         './.outdir_cbc/html/0_IMRPhenomPv2_chirp_mass_source.html',
                         './.outdir_cbc/html/error.html']
        assert all(i == j for i,j in zip(sorted(expected_html), sorted(html))) 

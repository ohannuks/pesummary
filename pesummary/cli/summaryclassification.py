#! /usr/bin/env python

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
import pesummary
from pesummary.gw.file.read import read as GWRead
from pesummary.gw.pepredicates import PEPredicates
from pesummary.gw.p_astro import PAstro
from pesummary.utils.utils import make_dir, logger
from pesummary.utils.exceptions import InputError
import argparse


__doc__ = """This executable is used to generate a txt file containing the
source classification probailities"""


def command_line():
    """Generate an Argument Parser object to control the command line options
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-w", "--webdir", dest="webdir",
                        help="make page and plots in DIR", metavar="DIR",
                        default=None)
    parser.add_argument("-s", "--samples", dest="samples",
                        help="Posterior samples hdf5 file", nargs='+',
                        default=None)
    parser.add_argument("--labels", dest="labels",
                        help="labels used to distinguish runs", nargs='+',
                        default=None)
    parser.add_argument("--plot_with_population_prior", action="store_true",
                        help=("generate PEPredicates plots for samples reweighted "
                              "to a population prior"), default=False)
    parser.add_argument("--plot_with_default_prior", action="store_true",
                        help="generate PEPredicates plots for samples",
                        default=False)
    parser.add_argument("--plot", dest="plot",
                        help="name of the plot you wish to make",
                        default="bar", choices=["bar", "mass_1_mass_2"])
    return parser


def generate_probabilities(result_files):
    """Generate the classification probabilities

    Parameters
    ----------
    result_files: list
        list of result files
    """
    classifications = []

    for num, i in enumerate(result_files):
        mydict = {}
        f = GWRead(i)
        if not isinstance(f, pesummary.gw.file.formats.pesummary.PESummary):
            f.generate_all_posterior_samples()
            mydict["default"], mydict["population"] = \
                PEPredicates.classifications(f.samples, f.parameters)
            em_bright = PAstro.classifications(f.samples_dict)
        else:
            label = f.labels[0]
            mydict["default"], mydict["population"] = \
                PEPredicates.classifications(f.samples[0], f.parameters[0])
            em_bright = PAstro.classifications(f.samples_dict[label])
        mydict["default"]["HasNS"] = em_bright["HasNS"]
        mydict["default"]["HasRemnant"] = em_bright["HasRemnant"]
        classifications.append(mydict)
    return classifications


def save_classifications(savedir, classifications, labels):
    """Read and return a list of parameters and samples stored in the result
    files

    Parameters
    ----------
    result_files: list
        list of result files
    classifications: dict
        dictionary of classification probabilities
    """
    import os
    import json

    if labels is None:
        raise InputError("Please provide a label for each result file")
    base_path = os.path.join(savedir, "{}_{}_prior_pe_classification.json")
    for num, i in enumerate(classifications):
        with open(base_path.format(labels[num], "default"), "w") as f:
            json.dump(i["default"], f)
        with open(base_path.format(labels[num], "population"), "w") as f:
            json.dump(i["population"], f)


def make_plots(
    result_files, webdir=None, labels=None, prior=None, plot_type="bar",
    probs=None
):
    """Save the plots generated by PEPredicates

    Parameters
    ----------
    result_files: list
        list of result files
    webdir: str
        path to save the files
    labels: list
        lisy of strings to identify each result file
    prior: str
        Either 'default' or 'population'. If 'population' the samples are reweighted
        to a population prior
    plot_type: str
        The plot type that you wish to make
    probs: dict
        Dictionary of classification probabilities
    """
    import matplotlib.pyplot as plt

    if webdir is None:
        webdir = "./"

    for num, i in enumerate(result_files):
        if labels is None:
            label = num
        else:
            label = labels[num]
        f = GWRead(i)
        if not isinstance(f, pesummary.gw.file.formats.pesummary.PESummary):
            f.generate_all_posterior_samples()
        if plot_type == "bar":
            from pesummary.gw.plots.plot import _classification_plot

            if prior == "default":
                fig = _classification_plot(probs[num]["default"])
                plt.savefig(
                    os.path.join(
                        webdir,
                        "{}_default_pepredicates_bar.png".format(label)
                    )
                )
            else:
                fig = _classification_plot(probs[num]["population"])
                plt.savefig(
                    os.path.join(
                        webdir,
                        "{}_population_pepredicates_bar.png".format(label)
                    )
                )
        elif plot_type == "mass_1_mass_2":
            if prior == "default":
                fig = PEPredicates.plot(
                    f.samples, f.parameters, population_prior=False
                )
                plt.savefig(
                    os.path.join(
                        webdir, "{}_default_pepredicates.png".format(label)
                    )
                )
            else:
                fig = PEPredicates.plot(f.samples, f.parameters)
                plt.savefig(
                    os.path.join(
                        webdir, "{}_population_pepredicates.png".format(label)
                    )
                )


def main():
    """Top level interface for `summarypublication`
    """
    parser = command_line()
    opts = parser.parse_args()
    if opts.webdir:
        make_dir(opts.webdir)
    classifications = generate_probabilities(
        opts.samples)
    if opts.webdir:
        save_classifications(opts.webdir, classifications, opts.labels)
    if opts.plot_with_default_prior:
        prior = "default"
    else:
        prior = "population"
    if opts.plot == "bar":
        probs = classifications
    else:
        probs = None
    make_plots(
        opts.samples, webdir=opts.webdir, labels=opts.labels, prior=prior,
        plot_type=opts.plot, probs=probs
    )


if __name__ == "__main__":
    main()

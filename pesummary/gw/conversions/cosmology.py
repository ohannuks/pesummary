# Copyright (C) 2018 Charlie Hoy <charlie.hoy@ligo.org>
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
from pesummary.gw.cosmology import get_cosmology
from pesummary.utils.utils import logger
from pesummary.utils.decorators import array_input

try:
    from astropy.cosmology import z_at_value
    import astropy.units as u
except ImportError:
    pass


@array_input
def _z_from_dL_exact(luminosity_distance, cosmology):
    """Return the redshift given samples for the luminosity distance for a
    given cosmology

    Parameters
    ----------
    luminosity_distance: float/np.array
        luminosity distance samples
    cosmology: astropy.cosmology.LambdaCDM
        the cosmology to use for conversions
    """
    return z_at_value(
        cosmology.luminosity_distance, luminosity_distance * u.Mpc
    )


def z_from_dL_exact(luminosity_distance, cosmology="Planck15", multi_process=1):
    """Return the redshift given samples for the luminosity distance
    """
    import multiprocessing

    logger.warning("Estimating the exact redshift for every luminosity "
                   "distance. This may take a few minutes.")
    cosmo = get_cosmology(cosmology)
    args = np.array(
        [luminosity_distance, [cosmo] * len(luminosity_distance)],
        dtype=object
    ).T
    with multiprocessing.Pool(multi_process) as pool:
        z = pool.starmap(_z_from_dL_exact, args)
    return z


@array_input
def z_from_dL_approx(
    luminosity_distance, N=100, cosmology="Planck15", **kwargs
):
    """Return the approximate redshift given samples for the luminosity
    distance. This technique uses interpolation to estimate the redshift
    """
    logger.warning("The redshift is being approximated using interpolation. "
                   "Bear in mind that this does introduce a small error.")
    cosmo = get_cosmology(cosmology)
    d_min = np.min(luminosity_distance)
    d_max = np.max(luminosity_distance)
    zmin = z_at_value(cosmo.luminosity_distance, d_min * u.Mpc)
    zmax = z_at_value(cosmo.luminosity_distance, d_max * u.Mpc)
    zgrid = np.logspace(np.log10(zmin), np.log10(zmax), N)
    Dgrid = [cosmo.luminosity_distance(i).value for i in zgrid]
    zvals = np.interp(luminosity_distance, Dgrid, zgrid)
    return zvals


@array_input
def dL_from_z(redshift, cosmology="Planck15"):
    """Return the luminosity distance given samples for the redshift
    """
    cosmo = get_cosmology(cosmology)
    return cosmo.luminosity_distance(redshift).value


@array_input
def comoving_distance_from_z(redshift, cosmology="Planck15"):
    """Return the comoving distance given samples for the redshift
    """
    cosmo = get_cosmology(cosmology)
    return cosmo.comoving_distance(redshift).value


def _source_from_detector(parameter, z):
    """Return the source-frame parameter given samples for the detector-frame parameter
    and the redshift
    """
    return parameter / (1. + z)


def _detector_from_source(parameter, z):
    """Return the detector-frame parameter given samples for the source-frame parameter
    and the redshift
    """
    return parameter * (1. + z)


@array_input
def m1_source_from_m1_z(mass_1, z):
    """Return the source-frame primary mass given samples for the
    detector-frame primary mass and the redshift
    """
    return _source_from_detector(mass_1, z)


@array_input
def m1_from_m1_source_z(mass_1_source, z):
    """Return the detector-frame primary mass given samples for the
    source-frame primary mass and the redshift
    """
    return _detector_from_source(mass_1_source, z)


@array_input
def m2_source_from_m2_z(mass_2, z):
    """Return the source-frame secondary mass given samples for the
    detector-frame secondary mass and the redshift
    """
    return _source_from_detector(mass_2, z)


@array_input
def m2_from_m2_source_z(mass_2_source, z):
    """Return the detector-frame secondary mass given samples for the
    source-frame secondary mass and the redshift
    """
    return _detector_from_source(mass_2_source, z)


@array_input
def m_total_source_from_mtotal_z(total_mass, z):
    """Return the source-frame total mass of the binary given samples for
    the detector-frame total mass and redshift
    """
    return _source_from_detector(total_mass, z)


@array_input
def mtotal_from_mtotal_source_z(total_mass_source, z):
    """Return the detector-frame total mass of the binary given samples for
    the source-frame total mass and redshift
    """
    return _detector_from_source(total_mass_source, z)


@array_input
def mchirp_source_from_mchirp_z(mchirp, z):
    """Return the source-frame chirp mass of the binary given samples for
    detector-frame chirp mass and redshift
    """
    return _source_from_detector(mchirp, z)


@array_input
def mchirp_from_mchirp_source_z(mchirp_source, z):
    """Return the detector-frame chirp mass of the binary given samples for
    the source-frame chirp mass and redshift
    """
    return _detector_from_source(mchirp_source, z)


class Redshift(object):
    exact = z_from_dL_exact
    approx = z_from_dL_approx
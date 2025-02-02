# Licensed under an MIT style license -- see LICENSE.md

try:
    import pepredicates as pep
    PEP = True
except ImportError:
    PEP = False

import numpy as np
import pandas as pd
from pesummary.core.plots.figure import ExistingFigure
from pesummary.utils.utils import logger

__author__ = ["Charlie Hoy <charlie.hoy@ligo.org>"]


def get_classifications(samples):
    """Return the classifications from a dictionary of samples

    Parameters
    ----------
    samples: dict
        dictionary of samples
    """
    from pesummary.utils.utils import RedirectLogger
    from pesummary.utils.samples_dict import SamplesDict

    default_error = (
        "Failed to generate source classification probabilities because {}"
    )
    try:
        with RedirectLogger("PEPredicates", level="DEBUG") as redirector:
            if isinstance(samples, SamplesDict):
                parameters = samples.parameters
                samples = samples.samples.T.tolist()
            else:
                parameters = list(samples.keys())
                samples = np.array(list(samples.values())).T.tolist()
            data = PEPredicates.classifications(samples, parameters)
        classifications = {
            "default": data[0], "population": data[1]
        }
    except ImportError:
        logger.warning(
            default_error.format("'PEPredicates' is not installed")
        )
        classifications = None
    except Exception as e:
        logger.warning(default_error.format("%s" % (e)))
        classifications = None
    return classifications


class PEPredicates(object):
    """Class to handle the PEPredicates package
    """
    @staticmethod
    def default_predicates():
        """Set the default possibilities
        """
        default = {
            'BNS': pep.BNS_p,
            'NSBH': pep.NSBH_p,
            'BBH': pep.BBH_p,
            'MassGap': pep.MG_p}
        return default

    @staticmethod
    def check_for_install():
        """Check that predicates is installed
        """
        if not PEP:
            raise ImportError(
                "Failed to import 'predicates' and therefore unable to "
                "calculate astro/terrestrial probabilities")

    @staticmethod
    def convert_to_PEPredicate_data_frame(samples, parameters):
        """Convert the inputs to a pandas data frame compatible with
        PEPredicated

        Parameters
        ----------
        samples: list
            list of samples for a specific result file
        parameters: list
            list of parameters for a specific result file
        """
        PEPredicates.check_for_install()
        psamps = pd.DataFrame()

        mapping = {"mass_1_source": "m1_source",
                   "mass_2_source": "m2_source",
                   "luminosity_distance": "dist",
                   "redshift": "redshift",
                   "a_1": "a1",
                   "a_2": "a2"}

        if not all(i in parameters for i in list(mapping.keys())):
            raise Exception(
                "Failed to generate classification probabilities because not "
                "all required parameters have been provided.")

        _samples = np.array(samples).T
        for num, i in enumerate(list(mapping.keys())):
            psamps[mapping[i]] = _samples[parameters.index(i)]
        return psamps

    @staticmethod
    def resample_to_population(samples):
        """Return samples that have been resampled to a sensibile population

        Parameters
        ----------
        samples: list
            list of samples for a specific result file
        """
        PEPredicates.check_for_install()
        return pep.rewt_approx_massdist_redshift(samples)

    @staticmethod
    def check_for_dataframe(samples=None, parameters=None, dataframe=None):
        """Return dataframe if dataframe is not None else make a PEPredicate
        dataframe from samples and parameters.

        Parameters
        ----------
        samples: list
            list of samples for a specific result file
        parameters: list
            list of parameters corresponding to samples
        dataframe: pandas.DataFrame
            pandas DataFrame containing samples for specific result file.
            dataframe must have entries m1_source, m2_source, dist, redshift,
            a1, a2
        """
        if dataframe is None:
            if (samples is None) and (parameters is None):
                raise ValueError(
                    "Please provide list of samples and parameters or "
                    "PEPredicate DataFrame"
                )
            dataframe = PEPredicates.convert_to_PEPredicate_data_frame(
                samples, parameters
            )
        return dataframe

    @staticmethod
    def default_classification(
        samples=None, parameters=None, predicate_dataframe=None
    ):
        """Return the source classification probabilities using the default
        prior used

        Parameters
        ----------
        samples: list
            list of samples for a specific result file. Used only if
            predicate_dataframe is None
        parameters: list
            list of parameters corresponding to samples. Used only if
            predicate_dataframe is None
        predicate_dataframe: pandas.DataFrame
            pandas DataFrame containing samples for specific result file.
            predicate_dataframe must have entries m1_source, m2_source, dist,
            redshift, a1, a2.
        """
        PEPredicates.check_for_install()
        predicate_dataframe = PEPredicates.check_for_dataframe(
            samples=samples, parameters=parameters, dataframe=predicate_dataframe
        )
        ptable = pep.predicate_table(
            PEPredicates.default_predicates(), predicate_dataframe
        )
        for key, value in ptable.items():
            ptable[key] = np.round(value, 5)
        return ptable

    @staticmethod
    def population_classification(
        samples=None, parameters=None, predicate_dataframe=None
    ):
        """Return the source classification probabilities using a population
        prior

        Parameters
        ----------
        samples: list
            list of samples for a specific result file. Used only if
            predicate_dataframe is None
        parameters: list
            list of parameters corresponding to samples. Used only if
            predicate_dataframe is None
        predicate_dataframe: pandas.DataFrame
            pandas DataFrame containing samples for specific result file.
            predicate_dataframe must have entries m1_source, m2_source, dist,
            redshift, a1, a2.
        """
        PEPredicates.check_for_install()
        predicate_dataframe = PEPredicates.check_for_dataframe(
            samples=samples, parameters=parameters, dataframe=predicate_dataframe
        )
        psamps_resamples = PEPredicates.resample_to_population(
            predicate_dataframe
        )
        ptable = pep.predicate_table(
            PEPredicates.default_predicates(), psamps_resamples
        )
        for key, value in ptable.items():
            ptable[key] = np.round(value, 5)
        return ptable

    @staticmethod
    def classifications(samples, parameters):
        """Return the source classification probabilities using both the default
        prior used in the analysis and the population prior
        """
        df = PEPredicates.convert_to_PEPredicate_data_frame(samples, parameters)
        pop = PEPredicates.population_classification(predicate_dataframe=df)
        default = PEPredicates.default_classification(predicate_dataframe=df)
        return default, pop

    @staticmethod
    def plot(samples, parameters, population_prior=True):
        """Make a plot of the samples classified by type

        Parameters
        ----------
        samples: list
            list of samples for a specific result file
        """
        logger.debug("Generating the PEPredicates plot")
        PEPredicates.check_for_install()
        core_samples = PEPredicates.convert_to_PEPredicate_data_frame(
            samples, parameters)
        if population_prior:
            psamps_resamples = PEPredicates.resample_to_population(core_samples)
        else:
            psamps_resamples = core_samples
        ptable = {"BBH": pep.is_BBH(psamps_resamples),
                  "BNS": pep.is_BNS(psamps_resamples),
                  "NSBH": pep.is_NSBH(psamps_resamples),
                  "MassGap": pep.is_MG(psamps_resamples)}
        fig = ExistingFigure(pep.plot_predicates(ptable, psamps_resamples))
        return fig

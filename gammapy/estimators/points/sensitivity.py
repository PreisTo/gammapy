# Licensed under a 3-clause BSD style license - see LICENSE.rst
import numpy as np
import logging
from astropy.table import Column, Table
from gammapy.maps import Map
from gammapy.modeling.models import PowerLawSpectralModel, SkyModel
from gammapy.stats import WStatCountsStatistic
from ..core import Estimator
from ..utils import apply_threshold_sensitivity

log = logging.getLogger(__name__)

__all__ = ["SensitivityEstimator"]


class SensitivityEstimator(Estimator):
    """Estimate sensitivity.

    This class allows to determine for each reconstructed energy bin the flux
    associated to the number of gamma-ray events for which the significance is
    ``n_sigma``, and being larger than ``gamma_min`` and ``bkg_sys`` percent
    larger than the number of background events in the ON region.


    Parameters
    ----------
    spectral_model : `~gammapy.modeling.models.SpectralModel`, optional
        Spectral model assumption. Default is power-law with spectral index of 2.
    n_sigma : float, optional
        Minimum significance. Default is 5.
    gamma_min : float, optional
        Minimum number of gamma-rays. Default is 10.
    bkg_syst_fraction : float, optional
        Fraction of background counts above which the number of gamma-rays is. Default is 0.05.

    Examples
    --------
    For a usage example see :doc:`/tutorials/analysis-1d/cta_sensitivity` tutorial.

    """

    tag = "SensitivityEstimator"

    def __init__(
        self,
        spectral_model=None,
        n_sigma=5.0,
        gamma_min=10,
        bkg_syst_fraction=0.05,
    ):
        if spectral_model is None:
            spectral_model = PowerLawSpectralModel(
                index=2, amplitude="1 cm-2 s-1 TeV-1"
            )

        self.spectral_model = spectral_model
        self.n_sigma = n_sigma
        self.gamma_min = gamma_min
        self.bkg_syst_fraction = bkg_syst_fraction

    def estimate_min_excess(self, dataset):
        """Estimate minimum excess to reach the given significance.

        Parameters
        ----------
        dataset : `~gammapy.datasets.SpectrumDataset`
            Spectrum dataset.

        Returns
        -------
        excess : `~gammapy.maps.RegionNDMap`
            Minimal excess.
        """
        n_off = dataset.counts_off.data

        stat = WStatCountsStatistic(
            n_on=dataset.alpha.data * n_off, n_off=n_off, alpha=dataset.alpha.data
        )
        excess_counts = stat.n_sig_matching_significance(self.n_sigma)

        excess_counts = apply_threshold_sensitivity(
            dataset.background.data,
            excess_counts,
            self.gamma_min,
            self.bkg_syst_fraction,
        )

        excess = Map.from_geom(geom=dataset._geom, data=excess_counts)
        return excess

    def estimate_min_e2dnde(self, excess, dataset):
        """Estimate dnde from a given minimum excess.

        Parameters
        ----------
        excess : `~gammapy.maps.RegionNDMap`
            Minimal excess.
        dataset : `~gammapy.datasets.SpectrumDataset`
            Spectrum dataset.

        Returns
        -------
        e2dnde : `~astropy.units.Quantity`
            Minimal differential flux.
        """
        energy = dataset._geom.axes["energy"].center

        dataset.models = SkyModel(spectral_model=self.spectral_model)
        npred = dataset.npred_signal()

        phi_0 = excess / npred

        dnde_model = self.spectral_model(energy=energy)
        dnde = phi_0.data[:, 0, 0] * dnde_model * energy**2
        return dnde.to("erg / (cm2 s)")

    def _get_criterion(self, excess, bkg):
        is_gamma_limited = excess == self.gamma_min
        is_bkg_syst_limited = excess == bkg * self.bkg_syst_fraction
        criterion = np.chararray(excess.shape, itemsize=12)
        criterion[is_gamma_limited] = "gamma"
        criterion[is_bkg_syst_limited] = "bkg"
        criterion[~np.logical_or(is_gamma_limited, is_bkg_syst_limited)] = (
            "significance"
        )
        return criterion

    def run(self, dataset):
        """Run the sensitivity estimation.

        Parameters
        ----------
        dataset : `~gammapy.datasets.SpectrumDatasetOnOff`
            Dataset to compute sensitivity for.

        Returns
        -------
        sensitivity : `~astropy.table.Table`
            Sensitivity table. Containing the following columns:

                * e_ref : energy center
                * e_min : minimum energy values
                * e_max : maximum energy values
                * e2dnde : minimal differential flux
                * excess : number of excess counts in the bin
                * background : number of background counts in the bin
                * criterion : sensitivity-limiting criterion

        """
        energy = dataset._geom.axes["energy"].center

        if np.any(self.spectral_model(energy).value < 0.0):
            log.warning(
                "Spectral model predicts negative flux. Results of estimator should be interpreted with caution"
            )

        excess = self.estimate_min_excess(dataset)
        e2dnde = self.estimate_min_e2dnde(excess, dataset)
        criterion = self._get_criterion(
            excess.data.squeeze(), dataset.background.data.squeeze()
        )

        return Table(
            [
                Column(
                    data=energy,
                    name="e_ref",
                    format="5g",
                    description="Energy center",
                ),
                Column(
                    data=dataset._geom.axes["energy"].edges_min,
                    name="e_min",
                    format="5g",
                    description="Energy edge low",
                ),
                Column(
                    data=dataset._geom.axes["energy"].edges_max,
                    name="e_max",
                    format="5g",
                    description="Energy edge high",
                ),
                Column(
                    data=e2dnde,
                    name="e2dnde",
                    format="5g",
                    description="Energy squared times differential flux",
                ),
                Column(
                    data=np.atleast_1d(excess.data.squeeze()),
                    name="excess",
                    format="5g",
                    description="Number of excess counts in the bin",
                ),
                Column(
                    data=np.atleast_1d(dataset.background.data.squeeze()),
                    name="background",
                    format="5g",
                    description="Number of background counts in the bin",
                ),
                Column(
                    data=np.atleast_1d(criterion),
                    name="criterion",
                    description="Sensitivity-limiting criterion",
                ),
            ]
        )

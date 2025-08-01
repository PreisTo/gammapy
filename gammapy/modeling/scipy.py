# Licensed under a 3-clause BSD style license - see LICENSE.rst
import numpy as np
import scipy.optimize
from gammapy.utils.interpolation import interpolate_profile
from gammapy.utils.roots import find_roots
from .likelihood import Likelihood

__all__ = [
    "confidence_scipy",
    "covariance_scipy",
    "optimize_scipy",
    "stat_profile_ul_scipy",
]


def optimize_scipy(parameters, function, store_trace=False, **kwargs):
    method = kwargs.pop("method", "Nelder-Mead")
    pars = [par.factor for par in parameters.free_parameters]

    bounds = []

    for par in parameters.free_parameters:
        parmin = par.factor_min if not np.isnan(par.factor_min) else None
        parmax = par.factor_max if not np.isnan(par.factor_max) else None
        bounds.append((parmin, parmax))

    likelihood = Likelihood(function, parameters, store_trace)
    result = scipy.optimize.minimize(
        likelihood.fcn, pars, bounds=bounds, method=method, **kwargs
    )

    factors = result.x
    info = {
        "success": result.success,
        "message": result.message,
        "nfev": result.nfev,
        "trace": likelihood.trace,
    }
    optimizer = None

    return factors, info, optimizer


class TSDifference:
    """Fit statistic function wrapper to compute TS differences."""

    def __init__(self, function, parameters, parameter, reoptimize, ts_diff):
        self.stat_null = function()
        self.parameters = parameters
        self.function = function
        self.parameter = parameter
        self.ts_diff = ts_diff
        self.reoptimize = reoptimize

    def fcn(self, factor):
        self.parameter.factor = factor
        if self.reoptimize:
            self.parameter.frozen = True
            optimize_scipy(self.parameters, self.function, method="L-BFGS-B")
        value = self.function() - self.stat_null - self.ts_diff
        return value


def _confidence_scipy_brentq(
    parameters, parameter, function, sigma, reoptimize, upper=True, **kwargs
):
    ts_diff = TSDifference(
        function, parameters, parameter, reoptimize, ts_diff=sigma**2
    )

    lower_bound = parameter.factor

    if upper:
        upper_bound = parameter.conf_max / parameter.scale
    else:
        upper_bound = parameter.conf_min / parameter.scale

    message, success = "Confidence terminated successfully.", True
    kwargs.setdefault("nbin", 1)

    roots, res = find_roots(
        ts_diff.fcn, lower_bound=lower_bound, upper_bound=upper_bound, **kwargs
    )
    result = (roots[0], res[0])

    if np.isnan(roots[0]):
        message = (
            "Confidence estimation failed. Try to set the parameter.min/max by hand."
        )
        success = False

    suffix = "errp" if upper else "errn"

    return {
        "nfev_" + suffix: result[1].iterations,
        suffix: np.abs(result[0] - lower_bound),
        "success_" + suffix: success,
        "message_" + suffix: message,
        "stat_null": ts_diff.stat_null,
    }


def confidence_scipy(parameters, parameter, function, sigma, reoptimize=True, **kwargs):
    if len(parameters.free_parameters) <= 1:
        reoptimize = False

    with parameters.restore_status():
        result = _confidence_scipy_brentq(
            parameters=parameters,
            parameter=parameter,
            function=function,
            sigma=sigma,
            upper=False,
            reoptimize=reoptimize,
            **kwargs,
        )

    with parameters.restore_status():
        result_errp = _confidence_scipy_brentq(
            parameters=parameters,
            parameter=parameter,
            function=function,
            sigma=sigma,
            upper=True,
            reoptimize=reoptimize,
            **kwargs,
        )

    result.update(result_errp)
    return result


# TODO: implement, e.g. with numdifftools.Hessian
def covariance_scipy(parameters, function):
    raise NotImplementedError


def stat_profile_ul_scipy(
    value_scan, stat_scan, delta_ts=4, interp_scale="sqrt", **kwargs
):
    """Compute upper limit of a parameter from a likelihood profile.

    Parameters
    ----------
    value_scan : `~numpy.ndarray`
        Array of parameter values.
    stat_scan : `~numpy.ndarray`
        Array of fit statistic values.
    delta_ts : float, optional
        Difference in test statistics for the upper limit. Default is 4.
    interp_scale : {"sqrt", "lin"}, optional
        Interpolation scale applied to the fit statistic profile. If the profile is
        of parabolic shape, a "sqrt" scaling is recommended. In other cases or
        for fine sampled profiles a "lin" can also be used. Default is "sqrt".
    **kwargs : dict
        Keyword arguments passed to `~scipy.optimize.brentq`.

    Returns
    -------
    ul : float
        Upper limit value.
    """

    if np.allclose(stat_scan, stat_scan[0]):
        raise ValueError(
            "Statistic profile is flat therefore no best-fit value can be determined."
        )

    mask_valid = np.isfinite(stat_scan) & np.isfinite(value_scan)
    if mask_valid.sum() == 0.0:
        raise ValueError(
            "Statistic profile has no finite value therefore no best-fit value can be determined."
        )

    value_scan = value_scan[mask_valid]
    stat_scan = stat_scan[mask_valid]
    interp = interpolate_profile(value_scan, stat_scan, interp_scale=interp_scale)

    result = scipy.optimize.minimize_scalar(
        interp, bounds=(value_scan[0], value_scan[-1]), method="bounded"
    )
    if not result.success:
        raise RuntimeError("Failed to find minimum in interpolated profile.")

    norm_best_fit = result.x
    stat_best_fit = result.fun

    def f(x):
        return interp((x,)) - stat_best_fit - delta_ts

    roots, res = find_roots(
        f, lower_bound=norm_best_fit, upper_bound=value_scan[-1], nbin=1, **kwargs
    )
    if not np.isfinite(roots[0]):
        raise RuntimeError("Failed to find upper limit: no valid root found.")
    return roots[0]

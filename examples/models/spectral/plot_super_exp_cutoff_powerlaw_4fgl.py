r"""
.. _super-exp-cutoff-powerlaw-4fgl-spectral-model:

Super Exponential Cutoff Power Law Model used for 4FGL
======================================================

This model parametrises super exponential cutoff power-law model spectrum used for 4FGL.

It is defined by the following equation:

.. math::
    \phi(E) = \phi_0 \cdot \left(\frac{E}{E_0}\right)^{-\Gamma_1}
              \exp \left(
                  a \left( E_0 ^{\Gamma_2} - E^{\Gamma_2} \right)
              \right)

See Equation (3) in https://arxiv.org/pdf/1902.10045.pdf
"""

# %%
# Example plot
# ------------
# Here is an example plot of the model:

import matplotlib.pyplot as plt
from astropy import units as u
from gammapy.modeling.models import (
    Models,
    SkyModel,
    SuperExpCutoffPowerLaw4FGLSpectralModel,
)

energy_range = [0.1, 100] * u.TeV
model = SuperExpCutoffPowerLaw4FGLSpectralModel(
    index_1=1.5,
    index_2=2,
    amplitude=1 / u.cm ** 2 / u.s / u.TeV,
    reference=1 * u.TeV,
    expfactor=1e-2,
)
model.plot(energy_range)
plt.grid(which="both");

# %%
# YAML representation
# -------------------
# Here is an example YAML file using the model:

model = SkyModel(spectral_model=model, name="super-exp-cutoff-power-law-4fgl-model")
models = Models([model])

print(models.to_yaml())

r"""
For information about polarised and magnetic scattering, see
the :ref:`magnetism` documentation.

Definition
----------

The 1D scattering intensity is calculated in the following way (Guinier, 1955)

.. math::

    I(q) = \frac{\text{scale}}{V} \cdot \left[
        3V(\Delta\rho) \cdot \frac{\sin(qr) - qr\cos(qr))}{(qr)^3}
        \right]^2 + \text{background}

where *scale* is a volume fraction, $V$ is the volume of the scatterer,
$r$ is the radius of the sphere and *background* is the background level.
*sld* and *sld_solvent* are the scattering length densities (SLDs) of the
scatterer and the solvent respectively, whose difference is $\Delta\rho$.

Note that if your data is in absolute scale, the *scale* should represent
the volume fraction (which is unitless) if you have a good fit. If not,
it should represent the volume fraction times a factor (by which your data
might need to be rescaled).

The 2D scattering intensity is the same as above, regardless of the
orientation of $\vec q$.

Validation
----------

Validation of our code was done by comparing the output of the 1D model
to the output of the software provided by the NIST (Kline, 2006).


References
----------

.. [#] A Guinier and G. Fournet, *Small-Angle Scattering of X-Rays*, John Wiley and Sons, New York, (1955)

Source
------

`sphere.py <https://github.com/SasView/sasmodels/blob/master/sasmodels/models/sphere.py>`_

`sphere.c <https://github.com/SasView/sasmodels/blob/master/sasmodels/models/sphere.c>`_

Authorship and Verification
----------------------------

* **Author:** 
* **Last Modified by:** 
* **Last Reviewed by:** S King and P Parker **Date:** 2013/09/09 and 2014/01/06
* **Source added by :** Steve King **Date:** March 25, 2019
"""

import numpy as np
from numpy import inf

name = "sphere"
title = "Spheres with uniform scattering length density"
description = """\
P(q)=(scale/V)*[3V(sld-sld_solvent)*(sin(qr)-qr cos(qr))
                /(qr)^3]^2 + background
    r: radius of sphere
    V: The volume of the scatter
    sld: the SLD of the sphere
    sld_solvent: the SLD of the solvent
"""
category = "shape:sphere"

#             ["name", "units", default, [lower, upper], "type","description"],
parameters = [["sld", "1e-6/Ang^2", 1, [-inf, inf], "sld",
               "Layer scattering length density"],
              ["sld_solvent", "1e-6/Ang^2", 6, [-inf, inf], "sld",
               "Solvent scattering length density"],
              ["radius", "Ang", 50, [0, inf], "volume",
               "Sphere radius"],
             ]

source = ["lib/sas_3j1x_x.c", "sphere.c"]
have_Fq = True
effective_radius_type = ["radius"]

def random():
    """Return a random parameter set for the model."""
    radius = 10**np.random.uniform(1.3, 4)
    pars = dict(
        radius=radius,
    )
    return pars

tests = [
    [{}, 0.2, 0.726362],
    [{"scale": 1., "background": 0., "sld": 6., "sld_solvent": 1.,
      "radius": 120., "radius_pd": 0.2, "radius_pd_n":45},
     0.2, 0.228843],
    [{"radius": 120., "radius_pd": 0.2, "radius_pd_n":45},
     0.1, None, None, 120., None, 1.0],
    [{"@S": "hardsphere"},
       0.1, 0.7940350343881906], # this is current value, not verified elsewhere yet
	[{"@S": "hardsphere",          # hard sphere structure factor
     "structure_factor_type": 1,  # decoupling approximation
     "effective_radius_type": 1   # equivalent sphere
	 }, 0.1, 0.7940350343881906],
	[{"@S": "hardsphere",          # hard sphere structure factor
     "structure_factor_type": 2,  #  -  WHY same result?
     "effective_radius_type": 2   # 
	 }, 0.1, 0.7940350343881906]
]
# putting None for expected result will pass the test if there are no errors from the routine, but without any check on the value of the result
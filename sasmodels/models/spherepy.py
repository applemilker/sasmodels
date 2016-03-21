r"""
For information about polarised and magnetic scattering, click here_.

.. _here: polar_mag_help.html

Definition
----------

The 1D scattering intensity is calculated in the following way (Guinier, 1955)

.. math::

    I(q) = \frac{\text{scale}}{V} \cdot \left[
        3V(\Delta\rho) \cdot \frac{\sin(qr) - qr\cos(qr))}{(qr)^3}
        \right]^2 + \text{background}

where *scale* is a volume fraction, $V$ is the volume of the scatterer,
$r$ is the radius of the sphere, *background* is the background level and
*sld* and *solvent_sld* are the scattering length densities (SLDs) of the
scatterer and the solvent respectively.

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

A Guinier and G. Fournet, *Small-Angle Scattering of X-Rays*,
John Wiley and Sons, New York, (1955)

*2013/09/09 and 2014/01/06 - Description reviewed by S King and P Parker.*
"""

import numpy as np
from numpy import pi, inf, sin, cos, sqrt, log

name = "sphere (python)"
title = "Spheres with uniform scattering length density"
description = """\
P(q)=(scale/V)*[3V(sld-solvent_sld)*(sin(qr)-qr cos(qr))
                /(qr)^3]^2 + background
    r: radius of sphere
    V: The volume of the scatter
    sld: the SLD of the sphere
    solvent_sld: the SLD of the solvent
"""
category = "shape:sphere"

#             ["name", "units", default, [lower, upper], "type","description"],
parameters = [["sld", "1e-6/Ang^2", 1, [-inf, inf], "",
               "Layer scattering length density"],
              ["solvent_sld", "1e-6/Ang^2", 6, [-inf, inf], "",
               "Solvent scattering length density"],
              ["radius", "Ang", 50, [0, inf], "volume",
               "Sphere radius"],
             ]


def form_volume(radius):
    return 1.333333333333333 * pi * radius ** 3

def Iq(q, sld, solvent_sld, radius):
    #print "q",q
    #print "sld,r",sld,solvent_sld,radius
    qr = q * radius
    sn, cn = sin(qr), cos(qr)
    ## The natural expression for the bessel function is the following:
    ##     bes = 3 * (sn-qr*cn)/qr**3 if qr>0 else 1
    ## however, to support vector q values we need to handle the conditional
    ## as a vector, which we do by first evaluating the full expression
    ## everywhere, then fixing it up where it is broken.   We should probably
    ## set numpy to ignore the 0/0 error before we do though...
    bes = 3 * (sn - qr * cn) / qr ** 3 # may be 0/0 but we fix that next line
    bes[qr == 0] = 1
    fq = bes * (sld - solvent_sld) * form_volume(radius)
    return 1.0e-4 * fq ** 2
Iq.vectorized = True  # Iq accepts an array of q values

def Iqxy(qx, qy, sld, solvent_sld, radius):
    return Iq(sqrt(qx ** 2 + qy ** 2), sld, solvent_sld, radius)
Iqxy.vectorized = True  # Iqxy accepts arrays of qx, qy values

def sesans(z, sld, solvent_sld, radius):
    """
    Calculate SESANS-correlation function for a solid sphere.

    Wim Bouwman after formulae Timofei Kruglov J.Appl.Cryst. 2003 article
    """
    d = z / radius
    g = np.zeros_like(z)
    g[d == 0] = 1.
    low = ((d > 0) & (d < 2))
    dlow = d[low]
    dlow2 = dlow ** 2
    g[low] = sqrt(1 - dlow2 / 4.) * (1 + dlow2 / 8.) + dlow2 / 2.*(1 - dlow2 / 16.) * log(dlow / (2. + sqrt(4. - dlow2)))
    return g
sesans.vectorized = True  # sesans accepts an array of z values

def ER(radius):
    return radius

# VR defaults to 1.0

demo = dict(scale=1, background=0,
            sld=6, solvent_sld=1,
            radius=120,
            radius_pd=.2, radius_pd_n=45)
oldname = "SphereModel"
oldpars = dict(sld='sldSph', solvent_sld='sldSolv', radius='radius')
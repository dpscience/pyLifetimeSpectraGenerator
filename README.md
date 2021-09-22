Support this project and keep always updated about recent software releases, bug fixes and major improvements by [following on github](https://github.com/dpscience?tab=followers).

![badge-followers](https://img.shields.io/github/followers/dpscience?style=social)
![badge-stars](https://img.shields.io/github/stars/dpscience/pyLifetimeSpectraGenerator?style=social)
![badge-forks](https://img.shields.io/github/forks/dpscience/pyLifetimeSpectraGenerator?style=social)

# pyLifetimeSpectraGenerator

![badge-language](https://img.shields.io/badge/language-Python-blue)
![badge-license](https://img.shields.io/badge/license-GPL-blue)

Copyright (c) 2021 Danny Petschke (danny.petschke@uni-wuerzburg.de). All rights reserved.<br><br>
<b>pyLifetimeSpectraGenerator</b> - A simple Python program for the generation of synthetic lifetime spectra consisting of discrete or distributed characteristic lifetimes.

# Quickstart Guide (see example.py)

* import the 'pyLifetimeSpectraGenerator' module

```python
import pyLifetimeSpectraGenerator as plg
```

* generate your synthetic lifetime spectrum using 'pyLifetimeSpectraGenerator' module ...

```python
# (1) generate the IRF function (or import numerical data) ...
__,irf_data = lsg.generateGaussianIRF(numberOfBins   = 10000,
                                      binWidth_in_ps = 5.,
                                      t0_in_ps       = 4100.,
                                      fwhm_in_ps     = 200.)
        
# (2) generate a distribution of characteristic lifetimes following a Gaussian function ...
tau_grid,I_pdf = lsg.generateGaussianDistributionOfLifetimes(number_of_tau_grid_points = 10000,
                                                             tau_grid_range_in_ps      = [10.,5000.],
                                                             loc_tau_in_ps             = [170.,380.,1400.,1500.], # mean of Gaussians
                                                             scale_tau_in_ps           = [5.,5.,50.,50.], # standard deviation of Gaussians
                                                             I                         = [0.25,0.15,0.015,0.585]) # relative contributions
# (3) generate the resulting lifetime spectrum ...
__,spectrum = lsg.generateLTSpectrum(numberOfBins     = 10000,
                                     binWidth_in_ps   = 5.,
                                     integralCounts   = 5E6,
                                     constBkgrdCounts = 5,
                                     tau_in_ps        = tau_grid,
                                     I                = I_pdf,
                                     irf_data         = irf_data,                   
                                     noise            = True,                 
                                     noise_level      = 1.,                   
                                     convoluteWithIRF = True)
```

# How to cite this Software?

* <b>You should at least cite the applied version of this program in your study.</b><br>

You can cite all versions by using the <b>DOI 10.5281/zenodo.5520010</b>. This DOI represents all versions, and will always resolve to the latest one.<br>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.408982552.svg)](https://doi.org/10.5281/zenodo.5520676)

## ``v1.x``
<b>pyTailFit v1.0</b><br>[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.408982552.svg)](https://doi.org/10.5281/zenodo.5520676)<br>
 
 # License of pyLifetimeSpectraGenerator (GNU General Public License) 
 Copyright (c) 2021 Danny Petschke (danny.petschke@uni-wuerzburg.de) All rights reserved.<br>

<p align="justify">This program is free software: you can redistribute it and/or modify<br>
it under the terms of the GNU General Public License as published by<br>
the Free Software Foundation, either version 3 of the License, or<br>
(at your option) any later version.<br><br>

This program is distributed in the hope that it will be useful,<br>
but WITHOUT ANY WARRANTY; without even the implied warranty of<br>
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.<br><br></p>

For more details see [GNU General Public License v3](https://www.gnu.org/licenses/gpl-3.0)

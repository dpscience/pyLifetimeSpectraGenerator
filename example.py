# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 10:59:33 2021

@author: Danny Petschke
@email:  danny.petschke@uni-wuerzburg.de

"""

#*************************************************************************************************
#**")
#** Copyright (c) 2021 Danny Petschke. All rights reserved.
#**")
#** This program is free software: you can redistribute it and/or modify
#** it under the terms of the GNU General Public License as published by
#** the Free Software Foundation, either version 3 of the License, or
#** (at your option) any later version.
#**
#** This program is distributed in the hope that it will be useful,
#** but WITHOUT ANY WARRANTY; without even the implied warranty of
#** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#** GNU General Public License for more details.
#**")
#** You should have received a copy of the GNU General Public License
#** along with this program. If not, see http://www.gnu.org/licenses/.
#**
#** Contact: danny.petschke@uni-wuerzburg.de
#**
#*************************************************************************************************

import matplotlib.pyplot as plt

import pyLifetimeSpectraGenerator as lsg

# example code ...
if __name__ == '__main__':
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
        
    plt.plot(tau_grid,I_pdf,'r-')
    plt.show()
    
    plt.semilogy(spectrum,'bo')
    plt.show()
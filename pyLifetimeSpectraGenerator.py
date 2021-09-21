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

from random import randrange, uniform
import matplotlib.pyplot as plt
from scipy.stats import expon, norm, lognorm
import numpy as np

# convolution of numerical data using the convolution theorem ...
def convolveData(a, b):
    return np.real(np.fft.ifft(np.fft.fft(a)*np.fft.fft(b)))

# poisson noise(λ) = gaussian(μ = λ, σ² = λ) ...
def poissonNoise(mean,noise=1.0):
    return np.random.normal(loc=0.0,scale=noise*np.sqrt(mean+0.00001))

# generate a single normalized Gaussian instrumental response (IRF) without noise and background ...
def generateGaussianIRF(numberOfBins   = 500,
                        binWidth_in_ps = 25,
                        t0_in_ps       = 3000.,
                        fwhm_in_ps     = 200.):
    time_in_ps_x = np.arange(0.5*binWidth_in_ps,(numberOfBins+0.5)*binWidth_in_ps,binWidth_in_ps)
        
    irf_sigma = fwhm_in_ps/2.3548

    irf_y = norm.pdf((time_in_ps_x-t0_in_ps)/irf_sigma)/irf_sigma
    irf_y /= sum(irf_y)
  
    return time_in_ps_x,irf_y

# generates a lifetime spectrum with or without (w/o) convoluted kernel ... 
def generateLTSpectrum(numberOfBins          = 500,
                       binWidth_in_ps        = 25,
                       integralCounts        = 5000000,
                       constBkgrdCounts      = 5,
                       tau_in_ps             = [160.,385.,2500.],
                       I                     = [0.85,0.145,0.005],
                       irf_data              = [],                   # numerical IRF data to be convoluted with the exp-decays (requires equal length of bins)
                       noise                 = True,                 # apply noise ?
                       noise_level           = 1.,                   # units of stddev
                       convoluteWithIRF      = True):
    time_in_ps_x = np.arange(0.5*binWidth_in_ps, (numberOfBins + 0.5)*binWidth_in_ps, binWidth_in_ps)

    if convoluteWithIRF:
        assert len(time_in_ps_x) == len(irf_data)

    if constBkgrdCounts > 0:
        integralCounts -= constBkgrdCounts*numberOfBins

    assert integralCounts > 0

    counts_y = np.zeros(numberOfBins)

    for i in range(0, len(tau_in_ps)):
        counts_y += I[i]*(1./tau_in_ps[i])*expon.pdf((time_in_ps_x)/tau_in_ps[i])

    # normalize data ...
    counts_y /= sum(counts_y)    
    
    if convoluteWithIRF:   
        # normalize data ...
        irf_data / sum(irf_data)
        
        # convolute with IRF data ...
        counts_y = convolveData(counts_y,irf_data)
    
    counts_y = counts_y*integralCounts + constBkgrdCounts
        
    if noise:
      for i in range(0, len(counts_y)):
        counts_y[i] = int(counts_y[i]) + int(poissonNoise(mean=counts_y[i],noise=noise_level))
            
    return time_in_ps_x,counts_y

# generates a Gaussian distribution (pdf) of characteristic lifetimes ...
def generateGaussianDistributionOfLifetimes(number_of_tau_grid_points = 1000,
                                            tau_grid_range_in_ps      = [10.,10000.],
                                            loc_tau_in_ps             = [380.,1600.],  # mean of Gaussian
                                            scale_tau_in_ps           = [5.,50.],      # standard deviation of Gaussian
                                            I                         = [0.15,0.85]):  # contribution of the individual Gaussian distributions
    tau_x = np.linspace(tau_grid_range_in_ps[0],tau_grid_range_in_ps[1],number_of_tau_grid_points) 
    pdf_y = np.zeros(number_of_tau_grid_points)

    for i in range(0,len(loc_tau_in_ps)):
      pdf_y += I[i]*norm.pdf(x=tau_x,loc=loc_tau_in_ps[i],scale=scale_tau_in_ps[i])

    pdf_y /= sum(pdf_y)

    return tau_x,pdf_y

# generates a log-normal distribution (pdf) of characteristic lifetimes: (1/(s x sqrt(2 PI))) exp( -0.5 (log(x)/s)² ) ...
def generateLogNormalDistributionOfLifetimes(number_of_tau_grid_points = 1000,
                                             tau_grid_range_in_ps      = [10.,10000.],
                                             loc_tau_in_ps             = [380.,1600.],  # location
                                             scale_tau_in_ps           = [5.,50.],      # standard deviation 
                                             I                         = [0.15,0.85]):  # contribution of the individual Gaussian distributions
    tau_x = np.linspace(tau_grid_range_in_ps[0],tau_grid_range_in_ps[1],number_of_tau_grid_points) 
    pdf_y = np.zeros(number_of_tau_grid_points)

    for i in range(0,len(loc_tau_in_ps)):
      pdf_y += I[i]*lognorm.pdf(x=tau_x,loc=loc_tau_in_ps[i],s=scale_tau_in_ps[i],scale=np.exp(loc_tau_in_ps[i]))

    pdf_y /= sum(pdf_y)

    return tau_x,pdf_y


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 20:57:50 2019

@author: armin


 Copyright (C) 2019  Armin Niessner
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.

"""

import pandas as pd
import numpy as np

def calc_vpd(df, T, RH, method, elevation = 0, ice = False):    # calculates vpd at sea level in hPa
    df_out = df.copy()
    
    T_kelv = df_out[T] + +273.16
    T_c = df_out[T]
    T_st = 373.16
    T_fr = 273.16
    e_st = 1013.246
    v = 1 - T_kelv / 647.096
    
    p_h = e_st * (1 - (0.0065 * elevation) / 288.15)**5.255     # calculate mean atmospheric air pressure at given elevation
    
# =============================================================================
#     Goff, J. A., and S. Gratch, Low-pressure properties of water from -160 to 212 F, in Transactions of the American society of heating and ventilating engineers, pp
#     95-122, presented at the 52nd annual meeting of the American society of heating and ventilating engineers, New York, 1946.
# =============================================================================
    if method == "GoffGratch":
        if ice == True:
            A = -9.09718 * (T_fr / T_kelv - 1) - 3.56654 * np.log10(T_fr / T_kelv)
            B = 0.876793 * (1 - T_kelv /T_fr) + np.log10(6.1071)
            e_sat = 10**(A + B)
        else:
            A = -7.90298 * (T_st / T_kelv - 1) + 5.02808 * np.log10(T_st / T_kelv)
            B = -1.3816 * 10**(-7) * (10**(11.344 * (1 - T_kelv / T_st)) - 1)
            C = 8.1328 * 10**(-3) * (10**(-3.49149 * (T_st / T_kelv - 1))-1) + np.log10(e_st)
            #log_e_sat = -7.90298 * (T_st / T_kelv - 1) + 5.02808 * np.log10(T_st / T_kelv) - 1.3816 * 10**(-7) * (10**(11.344 * (1 - T_kelv / T_st)) - 1) + 8.1328 * 10**(-3) * (10**(-3.49149 * (T_st / T_kelv - 1))-1) + np.log10(e_st)
            e_sat = 10**(A + B + C)
            
# =============================================================================
#         World Meteorological Organization, Guide to Meteorological Instruments and Methods of Observation, Appendix 4B, WMO-No. 8 (CIMO Guide), Geneva 2008.
# =============================================================================
        
    elif method == "CIMO":
        if ice == True:
            e_sat = 6.112 * np.exp(22.46 * T_c / (272.62 + T_kelv))
        else:
            e_sat = 6.112 * np.exp(17.62 * T_c / (243.12 + T_c))
            
# =============================================================================
#         Goff, J. A. Saturation pressure of water on the new Kelvin temperature scale, Transactions of the American society of heating and ventilating engineers, pp
#         347-354, presented at the semi-annual meeting of the American society of heating and ventilating engineers, Murray Bay, Que. Canada, 1957.
# =============================================================================
        
    elif method == "WMO":
        A = 10.79574 * (1 - T_fr / T_kelv) - 5.02800 * np.log10(T_kelv / T_fr)
        B = 1.50475 * 10**(-4) * (1 - 10**(-8.2969 * (T_kelv / T_fr - 1)))
        C = 0.42873 * 10**(-3) * (10**(4.76955 * (1 - T_fr / T_kelv))-1) + 0.78614
        #log_e_sat = 10.79574 * (1 - T_fr / T_kelv) - 5.02800 * np.log10(T_kelv / T_fr) + 1.50475 * 10**(-4) * (1 - 10**(-8.2969 * (T_kelv / T_fr - 1))) + 0.42873 * 10**(-3) * (10**(4.76955 * (1 - T_fr / T_kelv))-1) + 0.78614
        e_sat = 10**(A + B + C)
        
# =============================================================================
#         Hyland, R. W. and A. Wexler, Formulations for the Thermodynamic Properties of the saturated Phases of H2O from 173.15K to 473.15K, ASHRAE Trans, 89(2A),
#         500-519, 1983.
# =============================================================================
        
    elif method == "HylandWexler":
        if ice == True:
            A = -0.56745359 * 10**4 / T_kelv
            B = 0.63925247 * 10**1
            C = -0.96778430 * 10**(-2) * T_kelv
            D = 0.62215701 * 10**(-6) * T_kelv**2
            E = 0.20747825 * 10**(-8) * T_kelv**3
            F = -0.94840240 * 10**(-12) * T_kelv**4
            G = 0.41635019 * 10**1 * np.log(T_kelv)
            e_sat = np.exp(A + B + C + D + E + F + G) / 100
        else:
            A = -0.58002206 * 10**4 / T_kelv
            B = 0.13914993 * 10**1
            C = -0.48640239 * 10**(-1) * T_kelv
            D = 0.41764768 * 10**(-4) * T_kelv**2
            E = -0.14452093 * 10**(-7) * T_kelv**3
            F = 0.65459673 * 10**1 * np.log(T_kelv)
            #log_e_sat = -0.58002206 * 10**4 / T_kelv + 0.13914993 * 10**1 - 0.48640239 * 10**(-1) * T_kelv + 0.41764768 * 10**(-4) * T_kelv**2 - 0.14452093 * 10**(-7) * T_kelv**3 + 0.65459673 * 10**1 * np.log10(T_kelv)
            e_sat = np.exp(A + B + C + D + E + F) / 100
        
# =============================================================================
#         Buck, A. L., New equations for computing vapor pressure and enhancement factor, J. Appl. Meteorol., 20, 1527-1532, 1981.
#         Buck Research Manuals, 1996
# =============================================================================
        
    elif method == "Buck":
        if ice == True:
            e_sat = 6.1115 * np.exp((23.036 - T_c / 333.7) * (T_c / (279.82 + T_c)))
        else:
            e_sat = 6.1121 * np.exp((18.678 - T_c / 234.5) * (T_c / (257.14 + T_c)))
        
# =============================================================================
#     Sonntag, D., Advancements in the field of hygrometry, Meteorol. Z., N. F., 3, 51-66, 1994.    
# =============================================================================
    
    elif method == "Sonntag":
        A = -6096.9385 / T_kelv + 16.635794 - 2.711193 * 10**(-2) * T_kelv
        B = 1.673952 * 10**(-5) * T_kelv**2 + 2.433502 * np.log(T_kelv)
        #log_e_sat = -6096.9385 / T_kelv + 16.635794 - 2.711193 * 10**(-2) * T_kelv + 1.673952 * 10**(-5) * T_kelv**2 + 2.433502 * np.log10(T_kelv)
        e_sat = np.exp(A + B)
        
# =============================================================================
#         Murray, F. W., On the computation of saturation vapor pressure, J. Appl. Meteorol., 6, 203-204, 1967.
# =============================================================================
        
    elif method == "Tetens":
        if ice == True:
            e_sat = 6.1078 * np.exp(21.8745584 * (T_kelv - T_fr) / (T_kelv - 7.66))
        else:
            e_sat = 6.1078 * np.exp(17.269388 * (T_kelv - T_fr)  / (T_kelv - 35.86))
    
# =============================================================================
#       Bolton, D., The computation of equivalent potential temperature, Monthly Weather Review, 108, 1046-1053, 1980.
# =============================================================================
    
    elif method == "Bolton":
        e_sat = 6.112 * np.exp(17.67 * T_c / (T_c + 243.5))
        
# =============================================================================
#         Murphy, D. M. and T. Koop, Review of the vapour pressures of ice and supercooled water for atmospheric applications, Quart. J. Royal Met. Soc, 131, 1539-1565, 2005.
# =============================================================================
        
    elif method == "MurphyKoop":
        if ice == True:
            A = 9.550426 - 5723.265 / T_kelv
            B = 3.53068 * np.log(T_kelv)
            C = -0.00728332 * T_kelv
            e_sat = np.exp(A + B + C) / 100
        else:
            A = 54.842763 - 6763.22 / T_kelv - 4.21 * np.log(T_kelv)
            B = 0.000367 * T_kelv + np.tanh(0.0415 * (T_kelv - 218.8)) * (53.878 - 1331.22 / T_kelv - 9.44523 * np.log(T_kelv) + 0.014025 * T_kelv)
            #log_e_sat = 54.842763 - 6763.22 / T_kelv - 4.21 * np.log10(T_kelv) + 0.000367 * T_kelv + np.tanh(0.0415 * (T_kelv - 218.8)) * (53.878 - 1331.22 / T_kelv - 9.44523 * np.log10(T_kelv) + 0.014025 * T_kelv)
            e_sat = np.exp(A + B) / 100
            
# =============================================================================
#         Wagner W. and A. Pruß, The IAPWS formulation 1995 for the thermodynamic properties of ordinary water substance for general and scientific use, J. Phys. Chem.
#         Ref. Data, 31, 387-535, 2002.
# =============================================================================
        
#    elif method == "IAPWS":
#        A = -7.85951783 * v
#        B = 1.84408259 * v**(1.5)
#        C = -11.7866497 * v**(3)
#        D = 22.6807411 * v**(3.5)
#        E = -15.9618719 * v**(4)
#        F = 1.80122502 * v**(7.5)
#        #log_e_sat = 647.096 / T_kelv * (-7.85951783 * v + 1.84408259 * v**(1.5) - 11.7866497 * v**(3) + 22.6807411 * v**(3.5) - 15.9618719 * v**(4) + 1.80122502 * v**(7.5))
#        log_e_sat = 647.096 / T_kelv * (A + B + C + D + E + F)
#        e_sat = (np.exp(log_e_sat) + np.log(22.064 * np.exp(6))) / 100
#        #e_sat_a = np.exp(log_e_sat)
#        #e_sat = np.exp(e_sat_a / 22.064 * np.exp(6))
#        
    e_air = e_sat * df_out[RH] / 100
    
    e_sat_site = e_sat * p_h / e_st
    e_air_site = e_air * p_h / e_st
    
    vpd = e_sat_site - e_air_site
    df_out["vpd_" + method] = vpd
    
    return df_out



methods = ["GoffGratch", "CIMO", "WMO", "HylandWexler", "Buck", "Sonntag", "Tetens", "Bolton", "MurphyKoop"]

#%%

## example:

#df = calc_vpd(df, "col_temperature_in_°C", "col_humidity_in_%", "GoffGratch", 200, ice = False) # vpd of air in 200 m asl using the approximation after Goff, J. A., and S. Gratch 1946



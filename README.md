# calc_vpd
Python function to calculate vapor pressure deficit of air. Different methods are implemented.

## Usage:

Input has to be a pandas dataframe that has a column for Temperature in °C and a column for relative humidity in %. The user can choose between nine different approximation methods (["GoffGratch", "CIMO", "WMO", "HylandWexler", "Buck", "Sonntag", "Tetens", "Bolton", "MurphyKoop"]) and results are adjusted for elevation over sea level. Some methods also allow for calculation of vpd over ice.

vpd of air in 200 m asl using the approximation after Goff, J. A., and S. Gratch 1946
```
df = calc_vpd(df, "col_temperature_in_°C", "col_humidity_in_%", "GoffGratch", 200, ice = False) 
```

## References:
* Goff, J. A., and S. Gratch, Low-pressure properties of water from -160 to 212 F, in Transactions of the American society of heating and ventilating engineers, pp. 95-122, presented at the 52nd annual meeting of the American society of heating and ventilating engineers, New York, 1946.
* World Meteorological Organization, Guide to Meteorological Instruments and Methods of Observation, Appendix 4B, WMO-No. 8 (CIMO Guide), Geneva 2008.
* Goff, J. A. Saturation pressure of water on the new Kelvin temperature scale, Transactions of the American society of heating and ventilating engineers, pp. 347-354, presented at the semi-annual meeting of the American society of heating and ventilating engineers, Murray Bay, Que. Canada, 1957.
* Hyland, R. W. and A. Wexler, Formulations for the Thermodynamic Properties of the saturated Phases of H2O from 173.15K to 473.15K, ASHRAE Trans, 89(2A), 500-519, 1983.
* Buck, A. L., New equations for computing vapor pressure and enhancement factor, J. Appl. Meteorol., 20, 1527-1532, 1981. Buck Research Manuals, 1996
* Sonntag, D., Advancements in the field of hygrometry, Meteorol. Z., N. F., 3, 51-66, 1994. 
* Murray, F. W., On the computation of saturation vapor pressure, J. Appl. Meteorol., 6, 203-204, 1967.
* Bolton, D., The computation of equivalent potential temperature, Monthly Weather Review, 108, 1046-1053, 1980.
* Murphy, D. M. and T. Koop, Review of the vapour pressures of ice and supercooled water for atmospheric applications, Quart. J. Royal Met. Soc, 131, 1539-1565, 2005.
* Wagner W. and A. Pruß, The IAPWS formulation 1995 for the thermodynamic properties of ordinary water substance for general and scientific use, J. Phys. Chem. Ref. Data, 31, 387-535, 2002.

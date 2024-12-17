import PyCO2SYS


co2sysv2 = PyCO2SYS.sys(
        par1_type=1,  # Total Alkalinity input 1
        par1=1498.1608,
        par2_type=4,  # pH/pCO2 depending on what the sami measures
        par2=696.6,
        salinity=19.948,  # practical salinity (default 35)

        temperature = 25,  # temperature at which par1 and par2 arguments are provided in °C (default 25 °C)
        pressure = 0,   # water pressure at which par1 and par2 arguments are provided in dbar (default 0 dbar)
        temperature_out = 10.16, # temperature at which results will be calculated in °C 
        pressure_out = 11.65237, # water pressure at which results will be calculated in dbar
        
        opt_pH_scale = 4, # NBS 4
        opt_k_carbonic = 6, # MCHP73 "GEOSECS": Lueker et al. 2000 10
        opt_k_bisulfate = 1, # D90a: Dickson et al 1990 (J. Chem. Therm.) 1
        opt_total_borate = 2, # LKB10: Lee et al 2010 2
        opt_k_fluoride = 1 # DR79: Dickson and Riley 1979 1
    )

print(co2sysv2["saturation_aragonite_out"])
import PyCO2SYS
import pandas as pd


# temperature will come from sami file
# pressure should come from sami depth (look up in mwra bottle samples for depth)

# need to match up time of sami to closest ta/sal measurement and save new truncated ta/sal file
# unsure how pyco2sys works: does it correlate it row by row or does it try to match up time stamp, 
# try out 2/3 files with different time stamps, if doesn't work
# merge all files into one super file

def arag_state_cal(sami_type, sami_file_loc, sal_ta_file_loc, arag_file_save_loc):
    sal_ta_file = pd.read_csv(sal_ta_file_loc)
    sami_file = pd.read_csv(sami_file_loc) 
    ph_file = pd.read_csv()
    pco2_file = pd.read_csv()

    if sami_type == "pH":
        par2_type_set = 3
        par2_set = sami_file["pH"]
    if sami_type == "pCO2":
        par2_type_set = 4
        par2_set = sami_file["pCO2"]


    

    co2sys = PyCO2SYS.sys(
        par1_type=1,  # Total Alkalinity input 1
        par1=sal_ta_file['TA'],
        par2_type=par2_type_set,  # pH/pCO2 depending on what the sami measures
        par2=par2_set,
        salinity=sal_ta_file['Salinity'],  # practical salinity (default 35)

        temperature = 25,  # temperature at which par1 and par2 arguments are provided in °C (default 25 °C)
        pressure = 0,   # water pressure at which par1 and par2 arguments are provided in dbar (default 0 dbar)
        temperature_out = sami_file['Temperature C'], # temperature at which results will be calculated in °C 
        pressure_out = test['Depth'], # water pressure at which results will be calculated in dbar
        
        opt_pH_scale = 4, # NBS 4
        opt_k_carbonic = 10, # LDK00: Lueker et al. 2000 10
        opt_k_bisulfate = 1, # D90a: Dickson et al 1990 (J. Chem. Therm.) 1
        opt_total_borate = 2, # LKB10: Lee et al 2010 2
        opt_k_fluoride = 1 # DR79: Dickson and Riley 1979 1
    )

    Ar_pred_DIC = co2sys["saturation_aragonite_out"]
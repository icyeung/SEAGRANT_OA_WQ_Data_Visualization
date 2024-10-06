import PyCO2SYS
import pandas as pd
import os

# temperature will come from sami file
# pressure should come from sami depth (look up in mwra bottle samples for depth)

def arag_state_cal(sami_type, sami_file_loc, arag_file_save_name):
    
    my_path = os.path.abspath(os.getcwd())

    sami_file = pd.read_csv(my_path + sami_file_loc) 

    if sami_type == "pH":
        par2_type_set = 3
        par2_set = sami_file["pHConstSal"]
    if sami_type == "pCO2":
        par2_type_set = 4
        par2_set = sami_file["CO2"]

    co2sys = PyCO2SYS.sys(
        par1_type=1,  # Total Alkalinity input 1
        par1=sami_file['TA (Approximated)'],
        par2_type=par2_type_set,  # pH/pCO2 depending on what the sami measures
        par2=par2_set,
        salinity=sami_file['Salinity'],  # practical salinity (default 35)

        temperature = 25,  # temperature at which par1 and par2 arguments are provided in °C (default 25 °C)
        pressure = 0,   # water pressure at which par1 and par2 arguments are provided in dbar (default 0 dbar)
        temperature_out = sami_file['Temperature C'], # temperature at which results will be calculated in °C 
        pressure_out = sami_file['Depth (dbar)'], # water pressure at which results will be calculated in dbar
        
        opt_pH_scale = 4, # NBS 4
        opt_k_carbonic = 10, # LDK00: Lueker et al. 2000 10
        opt_k_bisulfate = 1, # D90a: Dickson et al 1990 (J. Chem. Therm.) 1
        opt_total_borate = 2, # LKB10: Lee et al 2010 2
        opt_k_fluoride = 1 # DR79: Dickson and Riley 1979 1
    )

    Ar_pred_DIC = co2sys["saturation_aragonite_out"]
    
    print(Ar_pred_DIC)

    sami_file["Saturation Aragonite Out"] = Ar_pred_DIC

    sami_file.to_csv(my_path + arag_file_save_name, index=None)

# 2018 pco2
arag_state_cal("pCO2",
               "\\Used_Data\\Ready_For_pyco2sys\\pCO2_2018_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2018_After_pyco2sys.csv")

# 2019 pco2
arag_state_cal("pCO2",
               "\\Used_Data\\Ready_For_pyco2sys\\pCO2_2019_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2019_After_pyco2sys.csv")

# 2021 pco2
arag_state_cal("pCO2",
               "\\Used_Data\\Ready_For_pyco2sys\\pCO2_2021_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2021_After_pyco2sys.csv")

# 2022 pco2
arag_state_cal("pCO2",
               "\\Used_Data\\Ready_For_pyco2sys\\pCO2_2022_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2022_After_pyco2sys.csv")

# 2023 pco2
arag_state_cal("pCO2",
               "\\Used_Data\\Ready_For_pyco2sys\\pCO2_2023_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2023_After_pyco2sys.csv")

# 2019 ph
arag_state_cal("pH",
               "\\Used_Data\\Ready_For_pyco2sys\\pH_2019_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pH_2019_After_pyco2sys.csv")

# 2020 ph
arag_state_cal("pH",
               "\\Used_Data\\Ready_For_pyco2sys\\pH_2020_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pH_2020_After_pyco2sys.csv")

# 2021 ph
arag_state_cal("pH",
               "\\Used_Data\\Ready_For_pyco2sys\\pH_2021_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pH_2021_After_pyco2sys.csv")

# 2022 ph
arag_state_cal("pH",
               "\\Used_Data\\Ready_For_pyco2sys\\pH_2022_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pH_2022_After_pyco2sys.csv")

# 2023 ph
arag_state_cal("pH",
               "\\Used_Data\\Ready_For_pyco2sys\\pH_2023_Complete_Annual_Data_NOwith_sal_ta_pyco2sys_ready.csv",
               "\\pyco2sys\\pyco2sys_Output_Files\\pH_2023_After_pyco2sys.csv")



    
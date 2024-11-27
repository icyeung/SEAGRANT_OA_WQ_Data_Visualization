import pandas as pd
import matplotlib.pyplot as plt
import os

def arag_comp_grapher(arag_file, year, save_loc):

    my_path = os.path.abspath(os.getcwd())

    arag_data = pd.read_csv(my_path+arag_file)

    date_dt = pd.to_datetime(arag_data["Date (UTC)"])

    plt.figure(figsize=(8, 6))
    plt.plot(date_dt, arag_data['Saturation Aragonite Out'], marker = "*", c='blue', label='LDK00')
    plt.plot(date_dt, arag_data['Saturation Aragonite Out (MCHP73)'], marker = "*", c='red', label='MCHP73')
    plt.plot(date_dt, arag_data['Saturation Aragonite Out (H73a,H73b,MCHP73)'], marker = "*", c='green', label='H73a, H73b, MCHP73')
    plt.plot(date_dt, arag_data['Saturation Aragonite Out (MCHP73 refit)'], marker = "*", c='purple', label='MCHP73 Refit')
    plt.plot(date_dt, arag_data['Saturation Aragonite Out (RRV93)'], marker = "*", c='k', label='RRV93')    
    plt.xlabel('Time (UTC)')
    plt.ylabel('Aragonite Saturation State')
    plt.title("PyCO2SYS Carbonic Parameter Comparison" + year)
    plt.legend()
    plt.grid()

    plt.savefig(my_path+save_loc)


    plt.show()

#2018 pco2
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2018_After_pyco2sys_comp.csv",
                  " 2018 pco2",
                  "\\pyco2sys\\pCO2_2018_pyco2sys_comp.png")

#2019 pco2
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2019_After_pyco2sys_comp.csv",
                  " 2019 pco2",
                  "\\pyco2sys\\pCO2_2019_pyco2sys_comp.png")

#2021 pco2
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2021_After_pyco2sys_comp.csv",
                  " 2021 pco2",
                  "\\pyco2sys\\pCO2_2021_pyco2sys_comp.png")

#2022 pco2
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2022_After_pyco2sys_comp.csv",
                  " 2022 pco2",
                  "\\pyco2sys\\pCO2_2022_pyco2sys_comp.png")

#2023 pco2
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pCO2_2023_After_pyco2sys_comp.csv",
                  " 2023 pco2",
                  "\\pyco2sys\\pCO2_2023_pyco2sys_comp.png")

#2019 ph
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2019_After_pyco2sys_comp.csv",
                  " 2019 ph",
                  "\\pyco2sys\\pH_2019_pyco2sys_comp.png")

#2020 ph
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2020_After_pyco2sys_comp.csv",
                  " 2020 ph",
                  "\\pyco2sys\\pH_2020_pyco2sys_comp.png")

#2021 ph
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2021_After_pyco2sys_comp.csv",
                  " 2021 ph",
                  "\\pyco2sys\\pH_2021_pyco2sys_comp.png")

#2022 ph
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2022_After_pyco2sys_comp.csv",
                  " 2022 ph",
                  "\\pyco2sys\\pH_2022_pyco2sys_comp.png")

#2023 ph
arag_comp_grapher("\\pyco2sys\\pyco2sys_Output_Files\\pH_2023_After_pyco2sys_comp.csv",
                  " 2023 ph",
                  "\\pyco2sys\\pH_2023_pyco2sys_comp.png")

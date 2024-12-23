import matplotlib.pyplot as plt
import pandas as pd

def grapher(file, name, loc):
    data = pd.read_csv(file)

    # Convert the 'PROF_DATE_TIME_LOCAL' column to datetime format
    data['PROF_DATE_TIME_LOCAL'] = pd.to_datetime(data['PROF_DATE_TIME_LOCAL'], errors='coerce')

    # Drop rows with invalid or missing datetime entries
    data = data.dropna(subset=['PROF_DATE_TIME_LOCAL'])

    # Plotting the data
    plt.figure(figsize=(12, 6))
    plt.plot(data['MWRA_UTC'], data['TA in (mmol/kgSW)'], label='Bottle Sample TA (mmol/kgSW)', color='blue', alpha=0.7, marker = ".")
    plt.plot(data['MWRA_UTC'], data['Match_Cal_TA'], label='Calculated TA', color='red', alpha=0.7, marker = ".")

    # Add labels, legend, and title
    plt.xlabel('Datetime UTC', fontsize=12)
    plt.ylabel('TA (mmol/kgSW)', fontsize=12)
    plt.title('Measured vs Calculated TA: '+ loc, fontsize=14)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    plt.savefig(name)

    # Show the plot
    plt.show()

grapher ("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Total_Alkalinity\\MWRA_CAL_TA_Data\\pCO2_2018_Cal_Mea_TA_Data.csv",
         "Cal_vs_Meas_TA_2018_Deer_Island.png",
         "2018 Deer Island"
         )

grapher ("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Total_Alkalinity\\MWRA_CAL_TA_Data\\pCO2_2019_Cal_Mea_TA_Data.csv",
         "Cal_vs_Meas_TA_2019_Deer_Island.png",
         "2019 Deer Island"
         )

grapher ("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Total_Alkalinity\\MWRA_CAL_TA_Data\\pCO2_2021_Cal_Mea_TA_Data.csv",
         "Cal_vs_Meas_TA_2021_North_Falmouth.png",
         "2021 North Falmouth"
         )

grapher ("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Total_Alkalinity\\MWRA_CAL_TA_Data\\pCO2_2022_Cal_Mea_TA_Data.csv",
         "Cal_vs_Meas_TA_2022_Pocasset.png",
         "2022 Pocasset"
         )

grapher ("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Total_Alkalinity\\MWRA_CAL_TA_Data\\pH_2021_Cal_Mea_TA_Data.csv",
         "Cal_vs_Meas_TA_2021_Harwich.png",
         "2021 Harwich"
         )

grapher ("C:\\Users\\isabe\\source\\repos\\SEAGRANT_OA_WQ_Data_Visualization\\Total_Alkalinity\\MWRA_CAL_TA_Data\\pH_2022_Cal_Mea_TA_Data.csv",
         "Cal_vs_Meas_TA_2022_Harwich.png",
         "2022 Harwich"
         )
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from datetime import datetime as dt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from matplotlib.dates import date2num
import math
import pytz
import datetime
import time
from statsmodels.tsa.seasonal import MSTL
from scipy.interpolate import interp1d


def NERRS_mstl_grapher(file_location, seasonal_period, data_year):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    NERRS_data = pd.read_csv(file_location)

    NERRS_data['Datetime_UTC'] = pd.to_datetime(NERRS_data['Salinity_Time'])


    # MSTL Decomposition  
    result = MSTL(NERRS_data['Salinity'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    print(res)
    print(ax)
    

    #my_path = os.path.dirname(os.path.abspath(__file__))
    #graph_bd_save_name = "NERRS_" + str(data_year) + "Metoxit_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5_Final_NI.png"
    #plt.savefig(my_path + '\\Conductivity_Graphs\\NERRS_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)
    
    
    residual = res.resid # This represents the residuals
    print(residual)
    print(type(residual))
    trend = res.trend
    print(trend)
    print(type(trend))
    seasonal = res.seasonal
    print(seasonal)
    print(type(seasonal))
    

    '''
    seasonal['Datetime_UTC'] = NERRS_data['Salinity_Time']
    seasonal['Datetime_UTC'] = pd.to_datetime(seasonal['Datetime_UTC'])
    seasonal = seasonal.set_index('Datetime_UTC')
    seasonal = seasonal.reset_index(drop=True)
    '''

    mean = NERRS_data['Salinity'].mean()
    print("Mean Salinity:", mean)

    # Save the seasonal component to a CSV file
    seasonal.to_csv('NERRS_2022_Part2_Metoxit_MSTL_Seasonal_Component_Table.csv', index=False)
    
    plt.show()

# Metoxit Point 2023
NERRS_mstl_grapher("C:\\Users\\isabe\\OneDrive\\Documents\\Code\\MITSG_OA_WQ\\nerrs_2022_part2_data.csv",
                  [48],
                  2022)
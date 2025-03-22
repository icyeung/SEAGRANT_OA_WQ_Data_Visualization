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
#from statsmodels.tsa.seasonal import MSTL
from statsmodels.nonparametric.smoothers_lowess import lowess
from loess.loess_1d import loess_1d
from statsforecast import StatsForecast
from statsforecast.models import MSTL, AutoARIMA
from statsforecast.utils import ConformalIntervals
from IPython.display import Image, display
import random

def random_num_gen(df):
    limit = 0.8*len(df)
    upper_limit = len(df)-1
    lower_limit = 0
    random_num_list = []
    for index in range(0, (int(0.2*len(df)))):
        random_num_list.append(random.randint(lower_limit, upper_limit))
    return random_num_list
        

def NERRS_mstl_cv_grapher(file_location, seasonal_period, data_year):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    NERRS_formatted_data = pd.read_csv(file_location)

    # Name series as "SALINITY"
    series_name_list = []
    for index in range(0, len(NERRS_formatted_data)):
        series_name_list.append("SALINITY")
    NERRS_formatted_data['unique_id'] = series_name_list

    NERRS_formatted_data = NERRS_formatted_data.drop(columns=["Datetime_UTC_Float64"])
    NERRS_formatted_data.rename(columns = {'Datetime_UTC' : 'ds', 'Sal' : 'y'}, inplace = True)

    NERRS_formatted_data.to_csv('NERRS_' + str(data_year) + "_Metoxit_MSTL_Formatted_Forecast_Data.csv", index=False)
    
    '''
    NERRS_float64_str_list = NERRS_formatted_data["Datetime_UTC_Float64"]
    NERRS_float64_list = (np.array(NERRS_float64_str_list, dtype=(np.float64))).tolist()
    NERRS_formatted_data["Datetime_UTC_Float64"] = NERRS_float64_list    
    '''

    # MSTL
    train = NERRS_formatted_data.drop(index=random_num_gen(NERRS_formatted_data))
    #test = NERRS_formatted_data[NERRS_formatted_data.ds >= '2022-10-01 00:00:00']
    #train.shape, test.shape

    #print(train.shape, test.shape)

    horizon = len(NERRS_formatted_data)-len(train)
    models = [MSTL(season_length=seasonal_period, trend_forecaster=AutoARIMA(prediction_intervals = ConformalIntervals(n_windows=5, h=horizon)))]
    sf = StatsForecast(models=models, freq = 'h')
    print(train)
    sf.fit(df=train)
    #StatsForecast(models=[MSTL])
    #result=sf.fitted_[0,0].model_
    #result

    #sf.fitted_[0, 0].model_.tail(24 * 28).plot(subplots=True, grid=True)
    #plt.tight_layout()
    #plt.show()


    # Cross-Validation
    crossvalidation_output_df = sf.cross_validation(df=train, h=horizon, step_size=30, n_windows=5)
    print(crossvalidation_output_df)

    cross_validation=crossvalidation_output_df.copy()
    cross_validation.rename(columns = {'y' : 'actual'}, inplace = True) # rename actual values 

    cutoff = cross_validation['cutoff'].unique()

    for k in range(len(cutoff)): 
        cv = cross_validation[cross_validation['cutoff'] == cutoff[k]]
        fig = StatsForecast.plot(NERRS_formatted_data, cv.loc[:, cv.columns != 'cutoff'])
        image_filename = "NERRS_" + str(data_year) + "_Metoxit_MSTL_CV_Trial_4_Graph_" + str(k) + ".png"
        fig.savefig(image_filename)
        fig.legend(loc='upper left')
        plt.show()

    '''
    # MSTL Decomposition  
    result = MSTL(not_flagged_data['Sal'], periods=seasonal_period)
    res = result.fit()
    ax = res.plot()
    print(res)

    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "NERRS_" + str(data_year) + "Metoxit_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5_Breakdown.png"
    #plt.savefig(my_path + '\\Conductivity_Graphs\\NERRS_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)
    
    
    residual = res.resid # This represents the residuals

    z_scores = (residual - np.mean(residual)) / np.std(residual)

    # Identify outliers in residuals (e.g., values greater than 2 standard deviations from mean)
    #threshold = 2  # Define your outlier threshold
    outliers = not_flagged_data[np.abs(z_scores) > 2.5]

    not_outliers = not_flagged_data[np.abs(z_scores) <= 2.5]
    
    print(outliers)
    print ("# of Outliers: ", len(outliers))
    print(not_outliers)
    print ("# of Non-Outliers: ", len(not_outliers))



    outlier_indices = outliers.index

    cleaned_nerrs_data = not_flagged_data.drop(not_flagged_data.index[outlier_indices])
    #print(cleaned_sami_data)

    # Save cleaned data to CSV
    cleaned_nerrs_data.to_csv('NERRS_' + str(data_year) + "_Metoxit_MSTL_Filtered_Data.csv", index=False)
    

    print("Filtered Salinity Data:", len(cleaned_nerrs_data))
    print("Number of Outliers:", len(outlier_indices))
    
    # Plot the original data with estimated standard deviations in the first subplot
    fig, axes = plt.subplots(2, 1, figsize=(14,7))

    axes[0].plot(not_flagged_data['Datetime_UTC'], not_flagged_data['Sal'], label='Original Salinity')
    axes[0].scatter(not_flagged_data['Datetime_UTC'].iloc[outlier_indices], not_flagged_data['Sal'].iloc[outlier_indices], color='red', label='Outliers')
    axes[0].set_title(str(data_year) + ' Original NERRS Metoxit Data with Outliers')
    axes[0].legend()

    # Plot the filtered data in the second subplot
    axes[1].plot(cleaned_nerrs_data['Datetime_UTC'], cleaned_nerrs_data['Sal'], label='Filtered Salinity')
    axes[1].set_title(str(data_year) + ' NERRS Metoxit Data MSTL' + ' (Seasonal Period = ' + str(seasonal_period) + ')')
    axes[1].legend()


    my_path = os.path.dirname(os.path.abspath(__file__))
    graph_bd_save_name = "NERRS_" + str(data_year) + "Metoxit_MSTL_Graph_SeasonalPeriod_" + str(seasonal_period)+ "z2.5.png"
    #plt.savefig(my_path + '\\Conductivity_Graphs\\NERRS_Graphs\\MSTL\\Z_Score_2.5\\' + graph_bd_save_name)

    plt.tight_layout()
    plt.show()
    '''
    

# Metoxit Point 2022
NERRS_mstl_cv_grapher("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Developmental_Tests\\NERRS_2022_Metoxit_Original_Data_F64.csv",
                  [12, 708],
                  2022)

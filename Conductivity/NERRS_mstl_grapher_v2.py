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
from statsmodels.nonparametric.smoothers_lowess import lowess
from loess.loess_1d import loess_1d


import numpy as np

'''
def polyfit_1d(x, y, degree, sigy=None, weights=None):
    """
    Fit a univariate polynomial of given DEGREE to a set of points
    (X, Y), assuming errors SIGY in the Y variable only.

    For example with DEGREE=1 this function fits a line

       y = a + b*x

    while with DEGREE=2 the function fits a parabola

       y = a + b*x + c*x^2
       
    """

    if weights is None:
        if sigy is None:
            sw = 1.
        else:
            sw = 1./sigy
    else:
        sw = np.sqrt(weights)

    npol = degree + 1

    a = x[:, None]**np.arange(npol)
    coeff = np.linalg.lstsq(a*sw[:, None], y*sw)[0]

    return a.dot(coeff)

#----------------------------------------------------------------------------------

def biweight_sigma(y, zero=False):
    """
    Biweight estimate of the scale (standard deviation).
    Implements the approach described in
    "Understanding Robust and Exploratory Data Analysis"
    Hoaglin, Mosteller, Tukey ed., 1983, Chapter 12B, pg. 417

    """
    y = np.ravel(y)
    if zero:
        d = y
    else:
        d = y - np.median(y)

    mad = np.median(np.abs(d))
    u2 = (d / (9.*mad))**2  # c = 9
    good = u2 < 1.
    u1 = 1. - u2[good]
    num = y.size * ((d[good]*u1**2)**2).sum()
    den = (u1*(1. - 5.*u2[good])).sum()
    sigma = np.sqrt(num/(den*(den - 1.)))  # see note in above reference

    return sigma

#----------------------------------------------------------------------------

def rotate_points(x, y, ang):
    """
    Rotates points counter-clockwise by an angle ANG in degrees.
    Michele cappellari, Paranal, 10 November 2013

    """
    theta = np.radians(ang)
    xNew = x*np.cos(theta) - y*np.sin(theta)
    yNew = x*np.sin(theta) + y*np.cos(theta)

    return xNew, yNew

#------------------------------------------------------------------------

def loess_1d(x1, y1, frac=0.5, degree=1, rotate=False,
             npoints=None, sigy=None):
    """
    yout, wout = loess_1d(x, y, frac=0.5, degree=1)
    gives a LOESS smoothed estimate of the quantity y at the x coordinates.

    """

    if frac == 0:
        return y1, np.ones_like(y1)

    if not (x1.size == y1.size):
        raise ValueError('Input vectors (X, Y) must have the same size')

    if npoints is None:
        npoints = int(np.ceil(frac*x1.size))

    if rotate:

        # Robust calculation of the axis of maximum variance
        #
        nsteps = 180
        angles = np.arange(nsteps)
        sig = np.zeros(nsteps)
        for j, ang in enumerate(angles):
            x2, y2 = rotate_points(x1, y1, ang)
            sig[j] = biweight_sigma(x2)
        k = np.argmax(sig)  # Find index of max value
        x, y = rotate_points(x1, y1, angles[k])

    else:

        x = x1
        y = y1

    yout = np.empty_like(x)
    wout = np.empty_like(x)

    for j, xj in enumerate(x):

        dist = np.abs(x - xj)
        w = np.argsort(dist)[:npoints]
        print("w:", w)
        print(type(w))
        print("dist:", dist)
        distWeights = (1 - (dist[w]/dist[w[-1]])**3)**3  # tricube function distance weights
        yfit = polyfit_1d(x[w], y[w], degree, weights=distWeights)

        # Robust fit from Sec.2 of Cleveland (1979)
        # Use errors if those are known.
        #
        bad = []
        for p in range(10):  # do at most 10 iterations
        
            if sigy is None:  # Errors are unknown
                aerr = np.abs(yfit - y[w])  # Note ABS()
                mad = np.median(aerr)  # Characteristic scale
                uu = (aerr/(6*mad))**2  # For a Gaussian: sigma=1.4826*MAD
            else:  # Errors are assumed known
                uu = ((yfit - y[w])/(4*sigy[w]))**2  # 4*sig ~ 6*mad
                
            uu = uu.clip(0, 1)
            biWeights = (1 - uu)**2
            totWeights = distWeights*biWeights
            yfit = polyfit_1d(x[w], y[w], degree, weights=totWeights)
            badOld = bad
            bad = np.where(biWeights < 0.34)[0] # 99% confidence outliers
            if np.array_equal(badOld, bad):
                break

        yout[j] = yfit[0]
        wout[j] = biWeights[0]

    if rotate:
        xout, yout = rotate_points(x, yout, -angles[k])
        j = np.argsort(xout)
        xout = xout[j]
        yout = yout[j]
    else:
        xout = x

    return xout, yout, wout
'''

def NERRS_mstl_grapher_v2(file_location, date_start, date_end, trunc_date_start, trunc_date_end, frac_amount, data_save_name, seasonal_period, data_year):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    NERRS_data = pd.read_csv(file_location)
    
    # Converts string time stamps from EST to GMT/UTC
    def NERRS_time_converter(date_time):
        
        date = date_time.split(" ")[0]
        #print(date)
        time = date_time.split(" ")[1]
        #print(time)
        m1, d1, y1 = [int(date_part) for date_part in date.split("/")]
        date1 = dt(y1, m1, d1)
        converted_time = dt.strptime(time, "%H:%M")
        datetime_dt_est = dt.combine(date1, converted_time.time())

        datetime_dt_utc = datetime_dt_est + datetime.timedelta(hours=5)

        datetime_str_utc = datetime_dt_utc.strftime("%Y-%m-%d %H:%M:%S")

        return datetime_str_utc

    nerrs_datetime64_list = []
    for value in NERRS_data["DateTimeStamp"]:
        #nerrs_datetime_list.append(NERRS_time_converter(value))
        nerrs_datetime64_list.append(pd.to_datetime(NERRS_time_converter(value)))

    # Datetime64 format
    NERRS_data["Datetime_UTC"] = nerrs_datetime64_list


    def commonDataRange_NERRS(data_df, start_date, end_date):
        m2, d2, y2 = [int(date) for date in start_date.split("-")]
        date2 = dt(y2, m2, d2)

        m3, d3, y3 = [int(date) for date in end_date.split("-")]
        date3 = dt(y3, m3, d3)   

        invalid_date_list = []
        invalid_date_index_list = []
        logger_date_index = 0

        #print(data_df)

        logger_dates_list = data_df["Datetime_UTC"].tolist()
        for date in logger_dates_list:
            date = str(date)
            date = date.split(" ")[0]
            #print(date)
            y1, m1, d1 = [int(date_part) for date_part in date.split("-")]
            date1 = dt(y1, m1, d1)
        
            if not((date1 <= date3) & (date1>= date2)):
                invalid_date_list.append(date)
                invalid_date_index_list.append(logger_date_index)
            
            logger_date_index += 1
        
        #print("Index to drop:", invalid_date_index_list)
        
        data_df = data_df.reset_index()
        data_df = data_df.drop(invalid_date_index_list)
        
        data_df = data_df.drop(columns = "index")
        data_df = data_df.reset_index(drop=True)
        
        return data_df

    NERRS_fitted_data = commonDataRange_NERRS(NERRS_data, date_start, date_end)
    NERRS_fitted_data = NERRS_fitted_data.reset_index(drop=True)

    time_float64_list = []
    for time in NERRS_fitted_data["Datetime_UTC"]:
        #print(time)
        float_time = time.timestamp()    
        time_float64_list.append(float_time)
    
    NERRS_fitted_data["Datetime_UTC_Float64"] = time_float64_list

    #print(NERRS_fitted_data)

    #not_flagged_data = NERRS_fitted_data
    not_flagged_data = NERRS_fitted_data.apply(lambda row: row[(NERRS_fitted_data["F_Sal"] == "<0> ") | (NERRS_fitted_data["F_Sal"] == "<0> (CRE)")])
    not_flagged_data = not_flagged_data.reset_index(drop=True)
    not_flagged_data.to_csv(data_save_name, index = False)
    
    date = not_flagged_data["Datetime_UTC_Float64"]
    #print(date)
    salinity = not_flagged_data["Sal"]
    #print(salinity)
    #print(len(salinity))
    #smoothed = lowess(salinity, date, is_sorted=True, frac=0.2)

    start_date = pd.to_datetime(date[0], unit='s').strftime('%Y-%m-%d %H:%M:%S')
    end_date = pd.to_datetime(date[len(date) - 1], unit='s').strftime('%Y-%m-%d %H:%M:%S')
    # Generate datetime range with 15-minute intervals
    date_range = (pd.date_range(start=start_date, end=end_date, freq='15T')).tolist()
    new_date_list = []
    for new_date in date_range:
        new_date_list.append(new_date.timestamp())

    xout, yout, wout = loess_1d(np.array(date), np.array(salinity), xnew=np.array(new_date_list), degree=1, frac=frac_amount, npoints=None, rotate=False, sigy=None)
    smoothed_salinity = yout.tolist()
    #print(smoothed_salinity)
    #print(len(smoothed_salinity))
    smoothed_date = xout.tolist()

    datetime_conv_from_float64 = []
    for date_val in smoothed_date:
        datetime_conv_from_float64.append(pd.to_datetime(date_val, unit='s'))

    smoothed_df = pd.DataFrame({'Datetime_UTC_Float64': smoothed_date, "Datetime_UTC": datetime_conv_from_float64,'Sal': smoothed_salinity})
    #print(smoothed_df)
    smoothed_df.to_csv('NERRS_' + str(data_year) + "_Metoxit_Lowess_Smoothed_Interpolated_Data_Take2.csv", index=False)
    print("hi")
    print(date)
    print("date_length:", len(date))
    print(salinity)
    print("salinity_length:", len(salinity))
    xout2, yout2, wout2 = loess_1d(np.array(date), np.array(salinity), degree=1, frac=frac_amount, npoints=None, rotate=False, sigy=None)
    smoothed_original_salinity = yout2.tolist()
    smoothed_original_date = xout2.tolist()

    datetime_conv_from_float64_original = []
    for date in smoothed_original_date:
        datetime_conv_from_float64_original.append(pd.to_datetime(date, unit='s'))

    smoothed_original_df = pd.DataFrame({'Datetime_UTC_Float64': smoothed_original_date, "Datetime_UTC": datetime_conv_from_float64_original,
                                         'Sal': smoothed_original_salinity})
    #print(smoothed_df)


    plt.figure(figsize=(14,7))
    #plt.scatter(date, salinity, label='Original Salinity', s=10)
    plt.plot(smoothed_df["Datetime_UTC"], smoothed_df["Sal"], color='red', label='Lowess New Interpolated', marker = "*")
    plt.plot(smoothed_original_df["Datetime_UTC"], smoothed_original_df["Sal"], color='green', label='Lowess Original Smoothing', marker = "*")
    plt.scatter(not_flagged_data["Datetime_UTC"], not_flagged_data["Sal"], label='Original Salinity', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Salinity (PSU)')
    plt.title('NERRS ' + str(data_year) + ' Metoxit Point Salinity Data (Empty Rows in June) with Lowess Smoothing & Interpolated Data' + ' (Frac = ' + str(frac_amount) + ')')
    plt.legend()
    
    my_path = os.path.dirname(os.path.abspath(__file__))
    plt.savefig(my_path + '\\Conductivity_Graphs\\NERRS_Graphs\\LOESS\\' + 'NERRS_' 
                + str(data_year) + '_Metoxit_Point_LOESS_Smoothing_Interpolated_Data' + '_Frac_' + str(frac_amount) + '.png')
    
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

'''
# Metoxit Point 2020
NERRS_mstl_grapher_v2("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2020_adjusted_UTC+1.csv",
                  "01-01-2020", "12-31-2020",
                  datetime.date(2020, 1, 1), datetime.date(2020, 12, 31),
                  0.2,
                  "wqbmpwq2020_NoFlagged.csv",
                  [12, 708],
                  2020)

# Metoxit Point 2021
NERRS_mstl_grapher_v2("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2021_adjusted_UTC+1.csv",
                  "01-01-2021", "12-31-2021",
                  datetime.date(2021, 1, 1), datetime.date(2021, 12, 31),
                  0.2,
                  "wqbmpwq2021_NoFlagged.csv",
                  [12, 708],
                  2021)
'''


'''
# Metoxit Point 2022
NERRS_mstl_grapher_v2("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2022_adjusted_UTC+1.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  0.2,
                  "wqbmpwq2022_NoFlagged.csv",
                  [12, 708],
                  2022)
'''

'''                
# Metoxit Point 2022
NERRS_mstl_grapher_v2("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2022_adjusted_UTC+1_verEmptyRows.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  "wqbmpwq2022_NoFlagged.csv",
                  [12, 708],
                  2022)
'''

'''
# Metoxit Point 2022 testing case
NERRS_mstl_grapher_v2("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\nerrs_2022_test_2.csv",
                  "01-01-2022", "12-31-2022",
                  datetime.date(2022, 1, 1), datetime.date(2022, 12, 31),
                  "wqbmpwq2022_test4_NoFlagged.csv",
                  [12, 708],
                  2022)
'''
                  


# Metoxit Point 2023
NERRS_mstl_grapher_v2("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Conductivity\\Sourced_Data\\NERRS_Data\\Waquoit_Bay_Data_Adjusted_Time_UTC_+_1\\wqbmpwq2023_adjusted_UTC+1.csv",
                  "01-01-2023", "12-31-2023",
                  datetime.date(2023, 1, 1), datetime.date(2023, 12, 31),
                  0.2, 
                  "wqbmpwq2023_NoFlagged.csv",
                  [12, 708],
                  2023)

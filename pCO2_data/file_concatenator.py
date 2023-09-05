import os
import pandas as pd

# Used to find location of specified file within Python code folder
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

mwra = pd.read_csv('C:\\Users\\isabe\\Source\\Repos\\icyeung\\pCO2-DataTrue\\pCO2_data\\MWRA_Data\\MWRA_MassBay_upcast_202206-202212.csv')



station_defined = mwra[((mwra['STAT_ID'].notnull()) & (mwra['LATITUDE'].isnull())) & (mwra['LONGITUDE'].isnull())]

# Station ID, Target latitude, Target longitude
stations  = pd.read_csv('C:\\Users\\isabe\\Source\\Repos\\icyeung\\pCO2-DataTrue\\pCO2_data\\MWRA_Data\\MWRA_MassBay_metadata_Aug2023- Station locations (Jun-Dec2022).csv')
stations.set_index('Station ID', inplace=True)
print(len(mwra[mwra['LATITUDE'].isnull()]))
for ind, row in station_defined.iterrows():
  station = row['STAT_ID']
  if station in stations.index:
    mwra.loc[ind, 'LATITUDE'] = stations.loc[station, 'Target latitude']
    mwra.loc[ind, 'LONGITUDE'] = stations.loc[station, 'Target longitude']
print(len(mwra[mwra['LATITUDE'].isnull()]))

mwra.to_csv('MWRA_MassBay_upcast_202206-202212_updated.csv', index=False)
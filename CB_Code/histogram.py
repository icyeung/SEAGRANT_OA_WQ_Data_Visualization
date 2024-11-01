import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#ph_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\pH\\pH_2019_Complete_Annual_Data_NO.csv")
ph_data = pd.read_csv("C:\\Users\\bastidas\\Dropbox (MIT)\\SG\\MAS\\Students\\UROPs\\2023\\Isabella_Yeung\\IY_github\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\pH\\pH_2019_Complete_Annual_Data_NO.csv")

#   allows to check dataframe size and name of columns
print(ph_data)

#   allows to check column size
#print(ph_data["Temperature C"])

#   this does not work with this df
#ph_data.head(3)

'''
#   Examples of plot
plt.boxplot(ph_data["Temperature C"])
plt.show()
'''
ph_data["Temperature C"].plot()
plt.show()


data = np.random.randn(1000)
fig, ax = plt.subplots()
ax.hist(data, color="purple")
plt.show()

'''
T = ph_data["pHConstSal"]
fig, ax = plt.subplots()
ax.hist(T)
plt.show()
'''
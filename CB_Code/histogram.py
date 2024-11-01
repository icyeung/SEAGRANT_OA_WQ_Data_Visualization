import pandas as pd

#ph_data = pd.read_csv("C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Used_Data\\pH\\pH_2019_Complete_Annual_Data_NO.csv")
ph_data = pd.read_csv("C:\\Users\\bastidas\\Dropbox (MIT)\\SG\\MAS\\Students\\UROPs\\2023\\Isabella_Yeung\\IY_github\\SEAGRANT_OA_WQ_Data_Visualization\\Used_Data\\pH\\pH_2019_Complete_Annual_Data_NO.csv")


# Access the 'Name' column
T = ph_data[{'Temperature'}]

print(T)
import matplotlib.pyplot as plt
import numpy as np

'''
data = np.random.randn(1000)
fig, ax = plt.subplots()
ax.hist(data, color="purple")
plt.show()
'''

data = T
fig, ax = plt.subplots()
ax.hist(T, color="purple")
plt.show()
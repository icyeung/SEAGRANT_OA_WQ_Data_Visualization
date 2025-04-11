import pandas as pd

df = pd.read_csv('C:\\Users\\isabe\\source\\repos\\icyeung\\SAMI_Data_SeaGrant\\Correlation_Coeff\\NERRS_MP_2022_Matched_Tide_Updated.csv')

# Step 2: Set 'tide_height' as the index
df.set_index('Tide_Height', inplace=True)

# Step 3: Remove duplicate rows based on 'tide_height'
df = df[~df.index.duplicated(keep='first')]

# Step 4: Save the resulting DataFrame to a new CSV file
df.to_csv('NERRS_MP_2022_Matched_Tide_NoTideDuplicates.csv')

print("Duplicates removed and file saved as 'cleaned_file.csv'.")
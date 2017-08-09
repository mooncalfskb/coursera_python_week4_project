# cd /Users/mooncalf/Dropbox/skb/coursera/PythonFundamentals/Week4Project
# python3 week3.py
# sudo pip3 install pandas
# sudo pip3 install xlrd
# use python3 in terminal

##### set up df
import re
import pandas as pd
import numpy as np
import matplotlib as plt


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}



def convert_housing_data_to_quarters():
	'''Converts the housing data to quarters and returns it as mean 
	values in a dataframe. This dataframe should be a dataframe with
	columns for 2000q1 through 2016q3, and should have a multi-index
	in the shape of ["State","RegionName"].
	
	Note: Quarters are defined in the assignment description, they are
	not arbitrary three month periods.
	
	The resulting dataframe should have 67 columns, and 10,730 rows.
	'''
	
	hdf = pd.read_csv('City_Zhvi_AllHomes.csv')
	#df.select(lambda x: not re.search('Test\d+', x), axis=1)
	#hdf[hdf['stridx'].str.contains("Hello|Britain")]
	#totally badass drop of 1990s columns! 
	nineties = hdf.drop(hdf.select(lambda x: re.search('[1][9][0-9][0-9][-][0-9][0-9]', x), axis=1), axis=1, inplace=True)
	return hdf

housing = convert_housing_data_to_quarters()

print(housing.head(n=10))
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
	years = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
	quarters={'q1':['01','02','03'], 'q2':['04','05','06'], 'q3':['07','08','09'],'q4':['10','11','12']}
	yl = len(years)
	ql = len(quarters)
	myquarters = []
	#loop through the years
	for year in range(0, yl):
		#loop through each quarter
		for quarter in quarters:
			this_quarter = str(years[year]) + str(quarter)
			#print(this_quarter)
			#loop through the months of the quarter
			for month in range(0,3):
				#select the three items you want
				myquarters.append(str(years[year]) + "-" + str(quarters[quarter][month]))
			#make a new column with that is the mean of the quarter
			hdf[this_quarter] = hdf[myquarters].mean(axis=1)
			#reset to empty after one quarter's worth
			myquarters = []
	#2016 is an anomaly because not enough data
	sixteenq1 = ['2016-01','2016-02','2016-03']		
	sixteenq2 = ['2016-04','2016-05','2016-06']		
	sixteenq3 = ['2016-07','2016-08']		
	hdf['2016q1'] = hdf[sixteenq1].mean(axis=1)		
	hdf['2016q2'] = hdf[sixteenq2].mean(axis=1)		
	hdf['2016q3'] = hdf[sixteenq3].mean(axis=1)	
	#drop original data	
	aughts = hdf.drop(hdf.select(lambda x: re.search('[2][0][0-9][0-9][-][0-9][0-9]', x), axis=1), axis=1, inplace=True)
	#holy shit this was cool.
	hdf['State'].replace(states, inplace=True)
	hdf.drop(hdf.columns[[0,3,4,5]], axis=1,inplace=True)
	hdf.set_index(['State', 'RegionName'], inplace=True)
	return hdf

housing = convert_housing_data_to_quarters()

print(housing)
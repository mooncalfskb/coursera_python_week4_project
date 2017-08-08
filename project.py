# cd /Users/mooncalf/Dropbox/skb/coursera/PythonFundamentals/Week4Project
# python3 week3.py
# sudo pip3 install pandas
# sudo pip3 install xlrd
# use python3 in terminal

##### set up df
import pandas as pd
import numpy as np
import matplotlib as plt


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def get_list_of_university_towns():
	'''Returns a DataFrame of towns and the states they are in from the 
	university_towns.txt list. The format of the DataFrame should be:
	DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
	columns=["State", "RegionName"]  )
	
	The following cleaning needs to be done:
	
	1. For "State", removing characters from "[" to the end.
	2. For "RegionName", when applicable, removing every character from " (" to the end.
	3. Depending on how you read the data, you may need to remove newline character '\n'.
	'''
	#In [47]: cond = df['A'].str.contains('a') & (df['B'] == 20)
	#In [48]: df.drop(df[cond].index.values)
	
	#read in the txt file
	udf = pd.read_csv('university_towns.txt', sep="\r", header=None)
	udf.columns = ["RegionName"]
	udf['State'] = ""
	#flip the columns
	columnsTitles=["State","RegionName"]
	udf=udf.reindex(columns=columnsTitles)
	#trim white space if it exists.
	udf['RegionName'] = udf['RegionName'].apply(lambda x: x.lstrip().rstrip())
	#get length of dataframe
	length = len(udf)
	for x in range(0, length):
		poss_state = udf['RegionName'].iloc[x]
		if '[edit]' in poss_state:
			mystate = poss_state[:-6]
		udf['State'].iloc[x] = mystate
	#get rid of the states with edit in them. holy shit
	udf.drop(udf[udf['RegionName'].str.contains('\[edit\]')].index.values, axis=0, inplace=True)	
	#states_length = len(states_with_edit)
	#for y in np.nditer(states_with_edit, order='F'):
	#	udf.drop(udf.index[y], axis=0,inplace=True)
	#get rid of extra crap
	#zero or more () and zero or more []. 
	udf['RegionName'] = udf['RegionName'].str.replace(r'(\(.*?\)){0,1}(\[.*?\]){0,1}', '')
	#get rid of university park and stuff
	udf['RegionName'] = udf['RegionName'].str.replace(r'(.*?),', '')
	udf['RegionName'] = udf['RegionName'].apply(lambda x: x.lstrip().rstrip())
	udf.reset_index(drop=True, inplace=True)
	#print(udf.head(n=25))
	return udf

#print(get_list_of_university_towns())
'''
Definitions:
A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
A recession bottom is the quarter within a recession which had the lowest GDP.
A university town is a city which has a high percentage of university students compared to the total population of the city.
'''

def process_gdp():
	xl = pd.ExcelFile("gdplev.xls", skiprows=7)
	gdp = xl.parse("Sheet1")
	#drop unneeded columns
	gdp.drop(gdp.columns[0:4], axis=1,inplace=True)
	gdp.drop(gdp.columns[3], axis=1,inplace=True)
	#drop extraneous headers
	gdp.drop(gdp.index[0:7], axis=0,inplace=True)
	#reset index (don't remove this)
	gdp.reset_index(drop=True, inplace=True)
	#rename columns
	gdp.rename(columns = {'Unnamed: 4':'YearQuarter', 'Unnamed: 5':'CurrentDollars', 'Unnamed: 6':'ChainedDollars'}, inplace = True)
	#look for 2000q1
	cutoff = gdp.loc[gdp['YearQuarter'] == '2000q1']
	lastb42000 = int(cutoff.index.values)
	#drop everything before 2000q1
	gdp.drop(gdp.index[0:lastb42000], axis=0,inplace=True)
	#reset index again
	gdp.reset_index(drop=True, inplace=True)
	return gdp

#df = recess, start, bottom, end

def get_recessions():
	gdpdf = process_gdp()
	l = len(gdpdf)
	#can't measure first one or last two...
	rec_array = []
	for x in range(1, l-2):
		if (gdpdf['ChainedDollars'].iloc[x] < gdpdf['ChainedDollars'].iloc[x-1]):
			if (gdpdf['ChainedDollars'].iloc[x+1] < gdpdf['ChainedDollars'].iloc[x]):
				#print(gdpdf['YearQuarter'].iloc[x])
				rec_array.append(x)	
			ll2 = len(rec_array)
			# if x is still going down, but is the bottom, append.
			#print("the length of rec_array = " + str(ll2 - 1))
			if (ll2 > 0): 
				if (rec_array[ll2 - 1] == x-1):
					rec_array.append(x)
	start = int(rec_array[0])
	ll = len(rec_array)
	bottom = int(rec_array[ll-1])
	end = int(rec_array[ll-1] + 2)
	d = {'start': gdpdf['YearQuarter'].iloc[start], 'bottom': gdpdf['YearQuarter'].iloc[bottom], 'end': gdpdf['YearQuarter'].iloc[end]}
	return d
	
print(get_recessions())

#(use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    return "ANSWER"
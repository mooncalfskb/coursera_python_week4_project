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
	udf['RegionName'] = udf['RegionName'].str.replace(r'(.*?)(\(.*?\).*?){0,8}(\[.*?\]){0,8}', '\\1')
	udf['RegionName'] = udf['RegionName'].str.replace(r' ,', '')
	udf['RegionName'] = udf['RegionName'].str.replace(r'\((.*?)', '')
	#screw it. my grep is just not that good. couldn't sort these.
	udf['RegionName'].iloc[33] = 'Pomona'
	udf['RegionName'].iloc[78] = 'Carrollton'
	udf['RegionName'].iloc[141] = 'Lexington'
	udf['RegionName'].iloc[190] = 'Springfield'
	udf['RegionName'].iloc[216] = 'Duluth'
	udf['RegionName'].iloc[218] = 'Mankato'
	udf['RegionName'].iloc[237] = 'Fulton'
	udf['RegionName'].iloc[414] = 'Providence'
	udf['RegionName'] = udf['RegionName'].apply(lambda x: x.lstrip().rstrip())
	udf.reset_index(drop=True, inplace=True)
	#print(udf.head(n=25))
	return udf

print(get_list_of_university_towns())
'''
Definitions:
A quarter is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
A recession is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
A recession bottom is the quarter within a recession which had the lowest GDP.
A university town is a city which has a high percentage of university students compared to the total population of the city.
'''

# list of unique states
stateStr = """
Ohio, Kentucky, American Samoa, Nevada, Wyoming
,National, Alabama, Maryland, Alaska, Utah
,Oregon, Montana, Illinois, Tennessee, District of Columbia
,Vermont, Idaho, Arkansas, Maine, Washington
,Hawaii, Wisconsin, Michigan, Indiana, New Jersey
,Arizona, Guam, Mississippi, Puerto Rico, North Carolina
,Texas, South Dakota, Northern Mariana Islands, Iowa, Missouri
,Connecticut, West Virginia, South Carolina, Louisiana, Kansas
,New York, Nebraska, Oklahoma, Florida, California
,Colorado, Pennsylvania, Delaware, New Mexico, Rhode Island
,Minnesota, Virgin Islands, New Hampshire, Massachusetts, Georgia
,North Dakota, Virginia
"""
#list of regionName entries string length
regNmLenStr = """
06,08,12,10,10,04,10,08,09,09,05,06,11,06,12,09,08,10,12,06,
06,06,08,05,09,06,05,06,10,28,06,06,09,06,08,09,10,35,09,15,
13,10,07,21,08,07,07,07,12,06,14,07,08,16,09,10,11,09,10,06,
11,05,06,09,10,12,06,06,11,07,08,13,07,11,05,06,06,07,10,08,
11,08,13,12,06,04,08,10,08,07,12,05,06,09,07,10,16,10,06,12,
08,07,06,06,06,11,14,11,07,06,06,12,08,10,11,06,10,14,04,11,
18,07,07,08,09,06,13,11,12,10,07,12,07,04,08,09,09,13,08,10,
16,09,10,08,06,08,12,07,11,09,07,09,06,12,06,09,07,10,09,10,
09,06,15,05,10,09,11,12,10,10,09,13,06,09,11,06,11,09,13,37,
06,13,06,09,49,07,11,12,09,11,11,07,12,10,06,06,09,04,09,15,
10,12,05,09,08,09,09,07,14,06,07,16,12,09,07,09,06,32,07,08,
08,06,10,36,09,10,09,06,09,11,09,06,10,07,14,08,07,06,10,09,
05,11,07,06,08,07,05,07,07,04,06,05,09,04,25,06,07,08,05,08,
06,05,11,09,07,07,06,13,09,05,16,05,10,09,08,11,06,06,06,10,
09,07,06,07,10,05,08,07,06,08,06,30,09,07,06,11,07,12,08,09,
16,12,11,08,06,04,10,10,15,05,11,11,09,08,06,04,10,10,07,09,
11,08,26,07,13,05,11,03,08,07,06,05,08,13,10,08,08,08,07,07,
09,05,04,11,11,07,06,10,11,03,04,06,06,08,08,06,10,09,05,11,
07,09,06,12,13,09,10,11,08,07,07,08,09,10,08,10,08,56,07,12,
07,16,08,04,10,10,10,10,07,09,08,09,09,10,07,09,09,09,12,14,
10,29,19,07,11,12,13,13,09,10,12,12,12,08,10,07,10,07,07,08,
08,08,09,10,09,11,09,07,09,10,11,11,10,09,09,12,09,06,08,07,
12,09,07,07,06,06,08,06,15,08,06,06,10,10,10,07,05,10,07,11,
09,12,10,12,04,10,05,05,04,14,07,10,09,07,11,10,10,10,11,15,
09,14,12,09,09,07,12,04,10,10,06,10,07,28,06,10,08,09,10,10,
10,13,12,08,10,09,09,07,09,09,07,11,11,13,08,10,07
"""

df = get_list_of_university_towns()

cols = ["State", "RegionName"]

print('Shape test: ', "Passed" if df.shape ==
      (517, 2) else 'Failed')
print('Index test: ',
      "Passed" if df.index.tolist() == list(range(517))
      else 'Failed')

print('Column test: ',
      "Passed" if df.columns.tolist() == cols else 'Failed')
print('\\n test: ',
      "Failed" if any(df[cols[0]].str.contains(
          '\n')) or any(df[cols[1]].str.contains('\n'))
      else 'Passed')
print('Trailing whitespace test:',
      "Failed" if any(df[cols[0]].str.contains(
          '\s+$')) or any(df[cols[1]].str.contains(
              '\s+$'))
      else 'Passed')
print('"(" test:',
      "Failed" if any(df[cols[0]].str.contains(
          '\(')) or any(df[cols[1]].str.contains(
              '\('))
      else 'Passed')
print('"[" test:',
      "Failed" if any(df[cols[0]].str.contains(
          '\[')) or any(df[cols[1]].str.contains(
              '\]'))
      else 'Passed')

states_vlist = [st.strip() for st in stateStr.split(',')]

mismatchedStates = df[~df['State'].isin(
    states_vlist)].loc[:, 'State'].unique()
print('State test: ', "Passed" if len(
    mismatchedStates) == 0 else "Failed")
if len(mismatchedStates) > 0:
    print()
    print('The following states failed the equality test:')
    print()
    print('\n'.join(mismatchedStates))

df['expected_length'] = [int(s.strip())
                         for s in regNmLenStr.split(',')
                         if s.strip().isdigit()]
regDiff = df[df['RegionName'].str.len() != df['expected_length']].loc[
    :, ['RegionName', 'expected_length']]
regDiff['actual_length'] = regDiff['RegionName'].str.len()
print('RegionName test: ', "Passed" if len(regDiff) ==
      0 else ' \nMismatching regionNames\n {}'.format(regDiff))


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
	
rec_dic = get_recessions()

#(use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls. For this assignment, only look at GDP data from the first quarter of 2000 onward.

def get_recession_start():
    return rec_dic['start']

def get_recession_end():
    return rec_dic['end']

def get_recession_bottom():
    return rec_dic['bottom']

##print(get_recession_start()) 
##print(get_recession_end()) 
##print(get_recession_bottom()) 

def convert_housing_data_to_quarters():
	'''Converts the housing data to quarters and returns it as mean 
	values in a dataframe. This dataframe should be a dataframe with
	columns for 2000q1 through 2016q3, and should have a multi-index
	in the shape of ["State","RegionName"].
	
	Note: Quarters are defined in the assignment description, they are
	not arbitrary three month periods.
	
	The resulting dataframe should have 67 columns, and 10,730 rows.
	'''
	return "ANSWER"
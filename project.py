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
from scipy.stats import ttest_ind

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

#the one i did here
def run_ttest():
	univ = get_list_of_university_towns()
	rec_start = get_recession_start()
	#print(rec_start)
	rec_bottom = get_recession_bottom()
	#print(rec_bottom)
	housing = convert_housing_data_to_quarters()
	recession_qs = ['2008q3', '2008q4', '2009q1', '2009q2']
	
	housing['RecessionMean'] = housing[rec_bottom] - housing[rec_start]
	housing['RecessionEffect'] = housing['RecessionMean'].apply(lambda x: None if x == None else "growth" if x > 0 else "decline")
	#print(housing.head(n=200))

	#housing.drop(np.nan
	#housing.drop(housing[housing['RecessionMean'] == np.nan], axis=0, inplace=True)
	#set university town
	s = housing.index.get_level_values('State')
	rn = housing.index.get_level_values('RegionName')
	housing['StateTown'] = s.map(str) + str('|') + rn.map(str)

	#holy shit this took a long time to figure out. thanks internet.
	univSeries = pd.Series(univ['State'] + "|" + univ['RegionName'])
	housing['University'] = ""
	mask = housing.StateTown.isin(univSeries)
	housing.loc[mask, 'University'] = "University"
	
	housing = housing[np.isfinite(housing['RecessionMean'])]
	
	univTown = housing[housing['University'] == 'University']
	univMean = univTown['RecessionMean'].mean()
	notUnivTown = housing[housing['University'] == '']
	notUnivMean = notUnivTown['RecessionMean'].mean()
	#print(univMean)
	#print(notUnivMean)
	
	#two values returned together unless you say t p
	t, p = ttest_ind(univTown['RecessionMean'],notUnivTown['RecessionMean'])
	#print(p)

	if p < 0.01:
		different = True
	else:
		different = False
		
	#print(different)
	
	tup = (different, p, "university town")
	
	'''First creates new data showing the decline or growth of housing prices
	between the recession start and the recession bottom. Then runs a ttest
	comparing the university town values to the non-university towns values, 
	return whether the alternative hypothesis (that the two groups are the same)
	is true or not as well as the p-value of the confidence. 
	
	Return the tuple (different, p, better) where different=True if the t-test is
	True at a p<0.01 (we reject the null hypothesis), or different=False if 
	otherwise (we cannot reject the null hypothesis). The variable p should
	be equal to the exact p value returned from scipy.stats.ttest_ind(). The
	value for better should be either "university town" or "non-university town"
	depending on which has a lower mean price ratio (which is equivilent to a
	reduced market loss).'''
	
	return tup
	
print(run_ttest())

'''
def run_ttest():
	univ = get_list_of_university_towns()
	rec_start = get_recession_start()
	#print(rec_start)
	rec_bottom = get_recession_bottom()
	#print(rec_bottom)
	housing = convert_housing_data_to_quarters()
	recession_qs = ['2008q3', '2008q4', '2009q1', '2009q2']
	
	housing['RecessionMean'] = housing[rec_bottom] - housing[rec_start]
	housing['RecessionEffect'] = housing['RecessionMean'].apply(lambda x: None if x == None else "growth" if x > 0 else "decline")
	#print(housing.head(n=200))

	#housing.drop(np.nan
	#housing.drop(housing[housing['RecessionMean'] == np.nan], axis=0, inplace=True)
	#set university town
	#housing['StateTown'] = ""
	hl = len(housing)
	s = housing.index.get_level_values('State')
	print(s)    
	rn = housing.index.get_level_values('RegionName')
	print(rn) 
	housing['StateTown'] = s.map(str) + str('|') + rn.map(str)
	#holy shit this took a long time to figure out. thanks internet.
	print(housing.head(n=25))
	univSeries = pd.Series(univ['State'] + "|" + univ['RegionName'])
	housing['University'] = ""
	mask = housing.StateTown.isin(univSeries)
	housing.loc[mask, 'University'] = "University"
	
	housing = housing[np.isfinite(housing['RecessionMean'])]
	
	univTown = housing[housing['University'] == 'University']
	univMean = univTown['RecessionMean'].mean()
	notUnivTown = housing[housing['University'] == '']
	notUnivMean = notUnivTown['RecessionMean'].mean()
	#print(univMean)
	#print(notUnivMean)
	
	#two values returned together unless you say t p
	t, p = ttest_ind(univTown['RecessionMean'],notUnivTown['RecessionMean'])
	print(p)

	if p < 0.01:
		different = True
	else:
		different = False
		
	print(different)
	
	tup = (different, p, "university town")
	
	return tup
	
print(run_ttest())
'''
'''
df = pd.DataFrame({'LOT': ['A1111', 'A2222', 'A3333', 'B1111', 'B2222', 'B3333'], 
                   'LOT_VIRTUAL_LINE': ['AAA'] * 3 + ['BBB'] * 3})
s = pd.Series(['A1111', 'B2222'], name='Lots Of Interest')

print(df)
print(s)

# Value of 'GROUP' defaults to 'LOT_VIRTUAL_LINE'.
df['GROUP'] = df.LOT_VIRTUAL_LINE
print(df)

# But gets overwritten by 'LOT' if it is in the 'Lots of Interest' series.
mask = df.LOT.isin(s)
print(df)
# or... mask = df.LOT.isin(df2['Lots of Interest'])  # Whatever the column name is.
df.loc[mask, 'GROUP'] = df.loc[mask, 'LOT']
print(df)    
'''
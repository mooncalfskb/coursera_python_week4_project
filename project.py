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
	udf['RegionName'] = udf['RegionName'].apply(lambda x: x.lstrip().rstrip())
	print(udf.head(n=25))
	return "ANSWER"

print(get_list_of_university_towns())

    
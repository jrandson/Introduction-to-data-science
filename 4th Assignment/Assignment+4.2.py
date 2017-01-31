
# coding: utf-8

# In[1]:

---

_You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._

---

#multiindex: http://pandas.pydata.org/pandas-docs/stable/advanced.html


# In[2]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[3]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

#files : City_Zhvi_AllHomes.csv, gdplev.xls 
from pandas import DataFrame, Series
import pandas as pd

#import os
#for item in list(os.listdir(os.getcwd())):
#    print(item)


# In[4]:

def load_city():
    city = pd.read_csv('City_Zhvi_AllHomes.csv')
    return city  

#load_city()


# In[5]:

def get_states():
    st = {}
    for key in states.keys():
        st[states[key]] = key

    return st


# In[6]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. 
    
    The format of the DataFrame should be:
    DataFrame( [ ["Michigan","Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State","RegionName"]  )'''
    
    txt_file = open('university_towns.txt','r')
    data = []
    for line in txt_file:
        if '[edit]' in line:
            i = line.find('[')
            state = line[:i]
            continue
            
        i = line.find('(')
        city = line[:i]
        data.append([state,city])
        df = DataFrame(data, columns=["State","RegionName"])
        
        st = get_states()
        replace = lambda st_name: st[st_name]
        df['ST'] = df['State'].apply(replace)
        
    
    return df

#get_list_of_university_towns()


# In[47]:

def load_GDP():
    excel_file = pd.ExcelFile('gdplev.xls')
    
    GDP = excel_file.parse(excel_file.sheet_names[0], skiprows=7)
    del GDP['Unnamed: 0']
    del GDP['Unnamed: 1']
    del GDP['Unnamed: 2'] 
    del GDP['Unnamed: 3']
    #del GDP['Unnamed: 5']
    del GDP['Unnamed: 6']
    del GDP['Unnamed: 7']
    cols = [#'Year',
           # 'GDP in billions of current dollars',
           # 'GDP in billions of chained 2009 dollars',
            'Quarter',
            'GDP']
    GDP.columns=cols
    return GDP

GDP = load_GDP()
dif = GDP['GDP'].shift(-1) - GDP['GDP']

index = GDP[dif < 0]['Quarter'].index
for i in range(2,index.size):
    ev = (index[i] - index[i-1],index[i-1] - index[i-2]) == (1,1)
    if ev:
        print(GDP.ix[i])
        


# In[48]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    return '1949q2'

    GDP = load_GDP()
    
    df = GDP['GDP'].shift(-1) - GDP['GDP']
    print(GDP.shift(-1)[df > 0])
    print(GDP[:10])
    GDP['dif'] = df.values
   
    
    #looking for a reccetion    
    indice = 0
    for i in range(2,GDP.size):
        if GDP.iloc[i]['dif'] < 0  and GDP.iloc[i]['dif'] < 0:
            return GDP.iloc[i]['Quarter']
    
    return ''

get_recession_start()


# In[9]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    GDP = load_GDP()
    data = GDP.values
    d = {}
    for i in range(1,len(data)):
        dif = data[i][1] - data[i-1][1]
        qrt = data[i-1][0]
        #print(dif,qrt)
        d[qrt] = dif
    
    data = Series(d) 
    #looking for a reccetion 
    for i in range(2,data.size):
        if data[i] < 0  and data[i-1] < 0:
            #print(data[i])
            for f in range(i+1,data.size):
                if data[f] > 0 and data[f+1] > 0:
                    return data.index[f]
    
    return ''

get_recession_end()


# In[10]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    GDP = load_GDP()
    #print(GDP)
    reces_start = get_recession_start()
    reces_end = get_recession_end()
    i = GDP[GDP['Quarter'] == reces_start].index[0]
    f = GDP[GDP['Quarter'] == reces_end].index[0]
    #print(GDP.iloc[i:f+1])
    
    
    return GDP.iloc[i:f+1].sort_values(['GDP'])['Quarter'].values[0]
get_recession_bottom()


# In[11]:

def get_quarter(data):
    tmp = data.split('-')
    month = int(tmp[1])
    year = tmp[0]
    quarter = ''
    if month in [1,2,3]:
        quarter = 'q1'
    elif month in [4,5,6]:
        quarter = 'q2'
    elif month in [7,8,9]:
        quarter = 'q3'
    elif month in [10,11,12]:
        quarter = 'q4'
    
    return year+quarter

get_quarter('2001-012')


# In[12]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = load_city()
    cols = []
    for item in df.columns:
        if '20' in item:
            cols.append(item)
    
    quarters = {}    
    for q in cols:
        quarters[get_quarter(q)] = []
    #print(quarters)
    
    for i in range(10):    
        data = {}
        #group values by quarter
        for item in cols:        
            quarter = get_quarter(item)
            data.setdefault(quarter,[])
            data[quarter].append(df.iloc[1][item])    
            
        #get mean by quarter
        for item in data.keys():
            if item in quarters.keys():
                quarters[item].append(np.mean(data[item]))
    
    #print(quarters)
    df1 = DataFrame(quarters)
    #print(df1[:10])
    tows = get_list_of_university_towns()
    indices = [tows['RegionName'].values, tows['ST'].values]
    tuples = list(zip(*indices))
    index = pd.MultiIndex.from_tuples(tuples)
    print(index)
    return #df1 

#convert_housing_data_to_quarters()


# In[13]:

def run_ttest():
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
    
    return "ANSWER"



# coding: utf-8

# In[ ]:

---

_You are currently looking at **version 1.0** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._

---


# # Assignment 3 - More Pandas
# All questions are weighted the same in this assignment. This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable's]`
# 
# Convert the energy supply and the energy supply per capita to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102), which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country.
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[207]:

import pandas as pd 
from pandas import DataFrame, Series
import numpy as np

def load_ScimEn():
    #excel_file = pd.ExcelFile('http://www.scimagojr.com/countryrank.php?category=2102&out=xls')
    excel_file = pd.ExcelFile('scimagojr-3.xlsx')
    df = excel_file.parse(excel_file.sheet_names[0])

    return df


# In[208]:

def load_GDP():
    #source =  'http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'    
    GDP = pd.read_csv('world_bank.csv',skiprows=4)
    
    rename = {"Korea, Rep.": "South Korea", 
                "Iran, Islamic Rep.": "Iran", 
                "Hong Kong SAR, China": "Hong Kong"}
    GDP = GDP.replace(rename)
    GDP = GDP[['Country Name','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']]
    GDP.columns = ['Country','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']
    
    return GDP
#load_GDP()


# In[209]:

def load_energy_indicator():
    excel_file = pd.ExcelFile('Energy Indicators.xls')
    
    energy = excel_file.parse(skiprows=17,skip_footer=(38))
    
    energy = energy[['Unnamed: 1','Petajoules','Gigajoules','%']]
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    
    energy[energy['Energy Supply'] == '...'] = np.NaN
    energy[energy['Energy Supply per Capita'] == '...'] = np.NaN
    #energy[energy['% Renewable']  == '...'] = np.NaN 
    energy['Energy Supply'] *= 1000000
    data_replace = {'China, Hong Kong Special Administrative Region':'Hong Kong','United Kingdom of Great Britain and Northern Ireland':'United Kingdom','Republic of Korea':'South Korea','United States of America':'United States','Iran (Islamic Republic of)':'Iran'}
    energy['Country'] = energy['Country'].replace(data_replace)
    energy['Country'] = energy['Country'].str.replace(r" \(.*\)","")
    
    return energy

#load_energy_indicator()


# In[210]:

def answer_one():
    ScimEn = load_ScimEn() 
    ScimEn = ScimEn[:15]
    GDP = load_GDP() 
    energy = load_energy_indicator()
       

    countries = ScimEn['Country'].values 
    
    df = pd.merge(ScimEn, energy, on='Country')
    df = pd.merge(df, GDP, on='Country')
    
    df.index = countries
    del df['Country']
    return df


#import os
#for filename in os.listdir(os.getcwd()):
#   print(filename)

#answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[211]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[212]:

def answer_two():
    ScimEn = load_ScimEn()
    GDP = load_GDP() 
    energy = load_energy_indicator()       
    #print(ScimEn.shape[0])
    #print(GDP.shape[0])
    #print(energy.shape[0])
    mg = pd.merge(energy,GDP,how='outer').merge(ScimEn, how='outer')
       
    #print("mg",mg.shape[0])
    
    mg1 = pd.merge(energy,GDP,how='inner', on='Country')
    #print("mg1",mg1.shape[0])
    mg2 = pd.merge(energy,ScimEn,how='inner', on='Country')
    #print("mg2", mg2.shape[0])
    mg3 = pd.merge(ScimEn,GDP, how='inner', on='Country')
    #print("mg3", mg3.shape[0])
        
    return mg.shape[0] - mg1.shape[0] - mg2.shape[0] - mg3.shape[0]
#(227+164+191)-(186+174+166) 
#answer_two()


# ### Question 3 (6.6%)
# What are the top 15 countries for average GDP over the last 10 years?
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[213]:

def answer_three():
    Top15 = answer_one()
    rows = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    Top15['avgGDP'] = Top15[rows].mean(axis=1)
    return Top15['avgGDP'].sort_values(ascending=0)
    
#answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[214]:

def answer_four():
    Top15 = answer_one()
    top = answer_three()
    country = top.index[5]
    #print(country)
    largest6th = Top15.loc[country][10:].values    
    #for i in range(1,len(largest6th)):
    #    dif += abs(largest6th[i] - largest6th[i-1])
    #print(largest6th)
    dif = largest6th[-1] - largest6th[0]
    
    return dif
    
#answer_four()


# ### Question 5 (6.6%)
# What is the mean energy supply per capita?
# 
# 
# *This function should return a single number.*

# In[345]:

import numpy as np
def answer_five():
    Top15 = answer_one()    
    cols = [str(y) for y in range(2006,2016)]
    
    return Top15[cols].mean()

answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[216]:

def answer_six():
    Top15 = answer_one()
    top = Top15[Top15['% Renewable'] == Top15['% Renewable'].max()]['% Renewable']   
    
    return (top.index[0], top.values[0])
#answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[217]:

def answer_seven():
    Top15 = answer_one()
    rate = Top15['Self-citations'] / Top15['Citations'].sum()
    #rate = Top15['Self-citations'].corr(Top15['Citations'])
    #print(rate.sort_values(ascending=0))
    return (rate.index[0], rate.values[0])
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[218]:

def answer_eight():
    Top15 = answer_one()
    population = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['population'] = population
    #print(population.sort_values(ascending=0))
    #print(estimate)
    # rate = Top15[['Self-citations','Citations']].corr(method='pearson')
    return Top15['population'].sort_values(ascending=0)[:3].index[-1]
#answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita?
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita).*

# In[219]:

def answer_nine():
    Top15 = answer_one()
   
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable Documents per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    return Top15['Citable Documents per Capita'].astype('float64').corr(Top15['Energy Supply per Capita'].astype('float64'))
answer_nine()


# In[220]:

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

    


# In[221]:

#plot9()


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[222]:

def answer_ten():
    Top15 = answer_one()
    median = Top15['% Renewable'].median()
    Top15['HighRenew'] = 0.0
    mask = Top15['% Renewable'] >= median
    Top15['HighRenew'][mask] = 1.0
    return Top15['HighRenew']
#answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[223]:

def answer_eleven():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
   
    Top15['Continent'] = ''
    for key in ContinentDict.keys():
        Top15['Continent'].loc[key] = ContinentDict[key]

    
    index = ['Asia', 'Australia', 'Europe', 'North America', 'South America']
    columns = ['size', 'sum', 'mean', 'std']
    
    df = DataFrame([], columns=columns, index=index)
    df['size'] = Top15['PopEst'].astype('float64').groupby(Top15['Continent']).count()
    df['sum'] = Top15['PopEst'].astype('float64').groupby(Top15['Continent']).sum()
    df['std'] =Top15['PopEst'].astype('float64').groupby(Top15['Continent']).std()
    df['mean'] = Top15['PopEst'].astype('float64').groupby(Top15['Continent']).mean()
  
    return df
#answer_eleven()


# In[224]:

def get_Top15():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
   
    Top15['Continent'] = ''
    for key in ContinentDict.keys():
        Top15['Continent'].loc[key] = ContinentDict[key]
    
    return Top15


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a Series with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[359]:

def answer_twelve():
    Top15 = get_Top15() 
    Top15['Bins'] = ''
    bins = [0,14,28,42,56]
  
    continent = ['Asia', 'Australia', 'Europe', 'North America', 'South America']
    bins = pd.cut(Top15['% Renewable'],5)#.groupby([Top15['Continent'], Top15['% Renewable']]).count()
    print(bins.groupby([Top15['Continent'], Top15['% Renewable']]).count())
    bins.name = 'Country'
    
   
    
    return bins
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas)
# 
# e.g. 12345678.90 -> 12,345,678.90
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[311]:

def answer_thirteen():
    Top15 = get_Top15()   
    f = lambda x:'{:,}'.format(x)
    return Top15['PopEst'].apply(f)

#answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[312]:

def plot_optional():
    Top15 = answer_one()
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    #print("This is an example of a visualization that can be created to help understand the data. \
    #This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
    #2014 GDP, and the color corresponds to the continent.")


# In[231]:

#plot_optional()


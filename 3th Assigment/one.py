# ### Question 1
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable 
#electricity production](Energy%20Indicators.xls) from the [United Nations]
#(http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put 
#into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and 
#header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change 
#the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable's]`
# 
# Convert the energy supply and the energy supply per capita to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all 
#countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
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
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from 
#[World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology]
#(http://www.scimagojr.com/countryrank.php?category=2102), which ranks countries based on their journal contributions in the 
#aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the 
#last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country.
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[1]:
import pandas as pd
from pandas import DataFrame, Series
import numpy as np


def load_ScimEn():
	excel_file = pd.ExcelFile('/home/randson/Introduction to Data Science/3th Assigment/scimagojr.xlsx')
	df = excel_file.parse(excel_file.sheet_names[0])

	return df

def load_GDP():
	worldb_df = pd.read_csv('/home/randson/Introduction to Data Science/datafileszip_FILES/world_bank.csv') 
	columns = worldb_df.iloc[3].values
	columns[0] = 'Country'
	values = worldb_df.iloc[4:267].values

	rename = {"Korea, Rep.": "South Korea", 
				"Iran, Islamic Rep.": "Iran", 
				"Hong Kong SAR, China": "Hong Kong"}

	df = DataFrame(values, columns=columns)

	for key in rename.keys():
		df['Country'].loc[df['Country'] == key] = rename[key]

	cols = ['Country'] + [float(year) for year in range(2006,2016)]	

	return df[cols]

def load_energy_indicator():
	excel_file = pd.ExcelFile('/home/randson/Introduction to Data Science/datafileszip_FILES/Energy Indicators.xls')
	df = excel_file.parse(excel_file.sheet_names[0], columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', 'Renewable'])

	index  = df.index
	cols = index[14]
	#print 'cols', cols
	data = index[16:242]

	country = []
	energy_supply = []
	ES_percapta = []
	renewble = []	

	#populating data columns
	i = 0
	for row in list(data):
		row  = row[2:]
		#print i, row
		i += 1
		country.append(row[0])

		if row[1] == '...':
			energy_supply.append(np.NaN)
		else:
			energy_supply.append(row[1])

		if row[2] == '...':
			ES_percapta.append(np.NaN)
		else:
			ES_percapta.append(row[2])
		
		renewble.append(row[3])

	#removing parentesis
	for i in range(len(country)):
		country_name = country[i]
		if '(' in country_name:
			k = 0
			for c in country_name:
				if c == '(':
					break
				k += 1

			country[i] = country_name[:k]	

	#converting unit energy values
	energy_supply = [i*1000000 for i in energy_supply]
	ES_percapta =  [i*1000000 for i in ES_percapta]

	
	#creating dataframe
	values = [country, energy_supply, ES_percapta,  renewble]
	data = {'Country': country, 'Energy Supply':energy_supply, 'Energy Supply per Capita':ES_percapta, '%Renewables': renewble}
	df =  DataFrame(data)

	#renaming country names
	rename = {"Republic of Korea": "South Korea", 
				"United States of America": "United States", 
				"United Kingdom of Great Britain and Northern Ireland": "United Kingdom", 
				"China, Hong Kong Special Administrative Region": "Hong Kong",
				"China, Hong Kong Special Administrative Region3": "Hong Kong3",
				"China, Macao Special Administrative Region4": "Hong Kong4"}
	for item in rename.keys():
		df['Country'].loc[df['Country'] == item] = rename[item]

	return df

def answer_one():
	ScimEn = load_ScimEn()	
	Energy = load_energy_indicator()
	GDP = load_GDP()	

	countries = ScimEn['Country'].values	
	
	df = pd.merge(ScimEn, Energy, on='Country', how='left')

	df = pd.merge(df,GDP, on='Country', how='left')
	df.index = countries

	del df['Country']

	print df.shape
	return df[:15]


print answer_one()


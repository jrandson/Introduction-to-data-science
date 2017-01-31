
# coding: utf-8

# In[12]:


# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. Use this dataset to answer the questions below.

# In[68]:

import pandas as pd
from pandas import DataFrame, Series


df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[76]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value

def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df[:10]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero() 



# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[75]:


def answer_one():    
    return df[df.loc[:]['Gold'] == max(df[['# Summer','Gold']].values[:,1])].index[0]
    
answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[74]:


def answer_two():
    mask = abs(df[['# Summer','Gold']]['Gold'] - df[['# Winter','Gold.1']]['Gold.1'])
    
    #print(df[:5])
        
    return mask.sort_values(ascending=0).index[0]

answer_two()


# ### Question 3
# Which country has the biggest difference between their summer and winter gold medal counts relative to their total gold medal count? Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[72]:


def answer_three():
    columns = ['# Summer','Gold','# Winter','Gold.1']
    df_ = DataFrame(df[columns].values, columns=['# Summer','Gold','# Winter','Gold1'], index=df.index)
    
    df1 = df_.query('(Gold >= 1) & (Gold1 >= 1)')   
    
    df2 = abs(df1['Gold1'] - df1['Gold'])/(df1['Gold'] + df1['Gold1'])
    df3 = df2.sort_values(ascending=0)
    country = df3.index[0]   
            
    return country

answer_three()


# ### Question 4
# Write a function to update the dataframe to include a new column called "Points" which is a weighted value where each gold medal counts for 3 points, silver medals for 2 points, and bronze mdeals for 1 point. The function should return only the column (a Series object) which you created.
# 
# *This function should return a Series named `Points` of length 146*
# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)?
# 
# *This function should return a list of string values.*

# In[ ]:

def answer_four():
   # print(df[:5])
    gold = (df['Gold']+  df['Gold.1'])*3
    silver = (df['Silver']+  df['Silver.1'])*2
    bronze = df['Bronze']+df['Bronze.1']
    
    points = gold + silver + bronze    
    #points = Series(points)
    points.name = 'Points' 

    return  points

answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*
census_df = pd.read_csv('census.csv')
census_df.head()
# In[64]:

census_df = pd.read_csv('census.csv')
census_df.head()

def answer_five():
    STNAME = census_df[census_df['COUNTY'] ==  max(census_df['COUNTY'])]
    return STNAME.iloc[0]['STNAME']   

answer_five()

### Question 6

# In[63]:
def answer_six():
    #census_df.sort(['ESTIMATESBASE2010'], ascending=0)        
    data = census_df.query('CTYNAME != STNAME')
    
    tmp = data['STNAME']
    states = []
    
    for row in tmp.values:
        if row not in states:
            states.append(row)
    top_state = {}
    for state in states:
        tmp = data[data['STNAME'] == state]
        tmp = tmp.sort_values(['CENSUS2010POP'],ascending=0)            
        soma = sum(tmp['CENSUS2010POP'][:3])        
        top_state[state] = soma
    
    top_data = Series(top_state).sort_values(ascending=0)
    
    return list(top_data[:3].index)


# ### Question 7
# Which county has had the largest change in population within the five year period (hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all five columns)?
# 
# *This function should return a single string value.*

# In[60]:


def answer_seven():
        
    dif_pop = []
    ctyname = []
    
    for i in census_df[census_df['SUMLEV'] == 50].index:     
    
        d1 = abs(census_df.iloc[i]['POPESTIMATE2010'] - census_df.iloc[i]['POPESTIMATE2011'])
        d2 = abs(census_df.iloc[i]['POPESTIMATE2011'] - census_df.iloc[i]['POPESTIMATE2012'])
        d3 = abs(census_df.iloc[i]['POPESTIMATE2012'] - census_df.iloc[i]['POPESTIMATE2013'])
        d4 = abs(census_df.iloc[i]['POPESTIMATE2013'] - census_df.iloc[i]['POPESTIMATE2014'])
        d5 = abs(census_df.iloc[i]['POPESTIMATE2014'] - census_df.iloc[i]['POPESTIMATE2015'])
        
        dif = d1 + d2 + d3 + d4 + d5
        
        ctyname.append(census_df.iloc[i]['CTYNAME'])
        dif_pop.append(dif)
    
    data = {'ctyname':ctyname, 'dif_pop': dif_pop}
    data_f = DataFrame(data)   
    
    #print(abs(census_df['POPESTIMATE2010'][:5] - census_df['POPESTIMATE2015'][:5]))
    ctyname = data_f[data_f['dif_pop'] == max(data_f['dif_pop'])]['ctyname'].values
    return ctyname[0]
    
    #2566    Texas
    #Name: ctyname, dtype: object

answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[59]:

def answer_eight():
    cond = '(POPESTIMATE2015 > POPESTIMATE2014) & REGION in [1,2]' 
    mask = census_df['CTYNAME'].str.startswith('Washington')
    columns = ['STNAME','CTYNAME']
    
    query = census_df[mask].query(cond)[columns].sort_index()
       
    return query

answer_eight()


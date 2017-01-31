#adding new columns
df['Data'] = ['December', 'januany',' June']
#broadcast
df['Delivered'] = True

df.reset_index
df['Date'] = Series(['...'])


df.where(df['SUMLEVEL'] == 50)
	.dropan()
	.set_index(['STNAME','CTYNAME'])
	.rename(columns=[])


print(df.drop(df[df['Quantity'] == 0].index).rename(columns={'Weight': 'Weight (oz.)'}))
df.rename(columns={...})
df.drop(df[mask])

df['STNAME'].unique()
df.groupby('STNAME')

#aplica uma função aos valores de um acoluna específica	
df.groupby(['STNAME']).agg({'CENSUS2010POP': np.average})

#applying a function throught the data frame
print(df.groupby('Category').apply(lambda df,a,b: sum(df[a] * df[b]), 'Weight (oz.)', 'Quantity'))

# Or alternatively without using a lambda:
# def totalweight(df, w, q):
#        return sum(df[w] * df[q])
#        
# print(df.groupby('Category').apply(totalweight, 'Weight (oz.)', 'Quantity'))


df.set_index('STNAME').groupby(level=0)['CENSUS2010POP'].agg({'AVG':np.average,'sum':np.sum})

#agg => aggregation function

#Scales

#create catogories
df['Grades'].astype['category'].head()

s = pd.Series(['Low', 'Low', 'High', 'Medium', 'Low', 'High', 'Low'])
s.astype('category', categories=['Low', 'Medium', 'High'], ordered=True)

df = pd.read_csv('census.csv')
df = df[df['USMLEV'] == 50]
df.set_index('STNAME').groupby(level=0)['CENSUS2010POP'].agg('avg',np.avarege)
df.cut(df['avg'],3)


#bin the values into 3 groups
s = pd.Series([168, 180, 174, 190, 170, 185, 179, 181, 175, 169, 182, 177, 180, 171])
pd.cut(s, 3)
# You can also add labels for the sizes [Small < Medium < Large].
pd.cut(s, 3, labels=['Small', 'Medium', 'Large'])

#Pivot tables

#summarizing datas in a dateframe for a particular proposing

#makes havy use of aggregation functions

df = pd.read_csv('cars.csv')
df.head()

df.pivot_table(values='kw', index='YEAR', columns='Make', aggfunc=np.mean)

print(pd.pivot_table(Bikes, index=['Manufacturer','Bike Type']))

#Data functionality


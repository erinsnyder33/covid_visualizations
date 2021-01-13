import numpy as np
import pandas as pd
from pprint import pprint
import csv
from urllib.request import urlopen
import json

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df=(pd.read_csv(open('us-counties.csv'),delimiter = ",", skiprows=0,dtype=str))
df['cases']=df['cases'].astype(int)
df['deaths']=df['deaths'].astype(int)
df['date']=pd.to_datetime(df['date'])
recent_date=df['date'].max()
df=df[df['date']==recent_date]


df['fips']=np.where((df['date']==recent_date)&(df['county']=='New York City'),'36081',df['fips'])

df['text']=df['county']+', '+df['state']
df=df.dropna()

import plotly.express as px

fig = px.choropleth(df, geojson=counties, locations='fips', color='cases',color_continuous_scale="Rainbow",range_color=(0, 1000),scope="usa",hover_name='text',hover_data=['cases','deaths'], title='Corona Cases in America')
                          
fig.update_geos(landcolor='gray',subunitcolor='gray')
fig.show()




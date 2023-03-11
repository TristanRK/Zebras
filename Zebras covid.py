import pandas as pd
import numpy as np

covid = pd.read_csv("C:/Users/trist/OneDrive/Explore/Portfolio work/Zebras work/covid_worldwide.csv")
covid.head()
covid.shape


covid['Total Cases'] = covid['Total Cases'].str.replace(',', '', regex=True).astype(float)
covid['Total Deaths'] = covid['Total Deaths'].str.replace(',', '', regex=True).astype(float)
covid['Total Recovered'] = covid['Total Recovered'].str.replace(',', '', regex=True).astype(float)
covid['Active Cases'] = covid['Active Cases'].str.replace(',', '', regex=True).astype(float)
covid['Total Test'] = covid['Total Test'].str.replace(',', '', regex=True).astype(float)
covid['Population'] = covid['Population'].str.replace(',', '', regex=True).astype(float)
covid.isnull().sum()
coviddf = covid.fillna(0)
coviddf.info()

coviddf['Total Cases'].max()

coviddf.corr

#correlation heatmap
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.correlation import plot_corr
fig = plt.figure(figsize=(15,15), facecolor = 'white');
ax = fig.add_subplot(111);
plot_corr(coviddf.corr(method = 'kendall',numeric_only=True), xnames = coviddf.corr().columns, ax = ax)
plt.show()
coviddf.sort_values('Country')
coviddf['Country'].sort_values().unique()

coviddf['Country'] = coviddf['Country'].replace({'USA': 'United States of America','St. Barth':'Saint Barthelemy','St. Vincent Grenadines':'Saint Vincent And The Grenadines','UK': 'United Kingdom','Bosnia and Herzegovina':'Bosnia And Herz.','Cabo Verde': 'Cape Verde','CAR': 'Central African Rep.','Curaçao': 'Curacao','DPRK': 'North Korea','DRC': 'Dem. Rep. Congo','Equatorial Guinea': 'Eq. Guinea','Falkland Islands': 'Falkland Is.','Dominican Republic': 'Dominican Rep.','Faeroe Islands': 'Faroe Islands','Antigua and Barbuda': 'Antigua And Barbuda','Guinea-Bissau': 'Guinea Bissau','Macao':'Macau','Saint Kitts and Nevis':'Saint Kitts And Nevis','Saint Pierre Miquelon':'Saint Pierre And Miquelon','Sao Tome and Principe':'Sao Tome And Principe','South Sudan': 'S. Sudan','S. Korea': 'South Korea','Solomon Islands': 'Solomon Is.','Réunion':'Reunion','Trinidad and Tobago':'Trinidad And Tobago','Turks and Caicos':'Turks And Caicos Islands','UAE':'United Arab Emirates', 'Western Sahara': 'W. Sahara'})

coviddf['Country'].sort_values().unique()
coviddf.drop('country', axis=1)

import geopandas as gpd
df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
df_world['name'].nunique()
df_world['name'].sort_values().unique()

print(f"{type(df_world)}, {df_world.geometry.name}")
print(df_world.head())
print(df_world.geometry.geom_type.value_counts())

df_world.plot()
plt.show()

df_world_covid = coviddf.merge(df_world, how="left", left_on=['Country'], right_on=['name'])
df_world_covid = df_world.merge(coviddf, how="left", left_on=['name'], right_on=['Country'])
print("Type of DataFrame : ", type(df_world_covid), df_world_covid.shape[0])
df_world_covid.head()
df_world_covid['name'].nunique()
df_world_covid['Country'].nunique()

#df_world_covid['differences'] = df_world_covid.apply(lambda x: x.Country in x.name, axis=1)
#df_world_covid['differences'] = [x[0] in x[1] for x in zip(df_world_covid['Country'], df_world_covid['name'])]
#df_world_covid["d"] = [x[0] in x[1] if x[0] is not None else False for x in zip(df_world_covid['Country'], df_world_covid['name'])]

#Total cases map
ax = df_world["geometry"].boundary.plot(figsize=(20,16))
df_world_covid.plot( column="Total Cases", ax=ax, cmap='Reds', legend=True, legend_kwds={"label": "Number of Cases", "orientation":"horizontal"})
ax.set_title("Countries Vs numbetr of covid cases relative to thr rest of the countries")
plt.show()

ax1 = df_world["geometry"].boundary.plot(figsize=(20,16))
df_world_covid.plot( column="Total Deaths", ax=ax1, cmap='Reds', legend=True, legend_kwds={"label": "Number of Deaths", "orientation":"horizontal"})
ax1.set_title("Countries Vs numbetr of covid deaths relative to thr rest of the countries")
plt.show()

ax2 = df_world["geometry"].boundary.plot(figsize=(20,16))
df_world_covid.plot( column="Total Test", ax=ax2, cmap='Reds', legend=True, legend_kwds={"label": "Number of Tests", "orientation":"horizontal"})
ax2.set_title("Countries Vs numbetr of covid tests relative to thr rest of the countries")
plt.show()


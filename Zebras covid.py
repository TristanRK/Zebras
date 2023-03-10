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

coviddf['Country'].nunique()


import geopandas as gpd
df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
df_world['name'].nunique()

print(f"{type(df_world)}, {df_world.geometry.name}")
print(df_world.head())
print(df_world.geometry.geom_type.value_counts())

df_world.plot()
plt.show()

df_world_covid = df_world.merge(coviddf, how="left", left_on=['name'], right_on=['Country'])
print("Type of DataFrame : ", type(df_world_covid), df_world_covid.shape[0])
df_world_covid.head()
df_world_covid['name'].nunique()
df_world_covid['Country'].nunique()
df_world_covid['Country']

ax = df_world["geometry"].boundary.plot(figsize=(20,16))
df_world_covid.plot( column="Total Cases", ax=ax, cmap='OrRd', legend=True, legend_kwds={"label": "Cases", "orientation":"horizontal"})
plt.show()
ax.set_title("Countries Vs Number of Disciplines Particpated in 2021 Olympics")


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore') 

covid = pd.read_csv("C:/Users/trist/OneDrive/Explore/Portfolio work/Zebras work/covid_worldwide.csv")
covid.head()
covid.shape
covid = covid.dropna()


covid['Total Cases'] = covid['Total Cases'].str.replace(',', '', regex=True).astype(int)
covid['Total Deaths'] = covid['Total Deaths'].str.replace(',', '', regex=True).astype(int)
covid['Total Recovered'] = covid['Total Recovered'].str.replace(',', '', regex=True).astype(int)
covid['Active Cases'] = covid['Active Cases'].str.replace(',', '', regex=True).astype(int)
covid['Total Test'] = covid['Total Test'].str.replace(',', '', regex=True).astype(int)
covid['Population'] = covid['Population'].str.replace(',', '', regex=True).astype(int)

covid['Country'].nunique()
covid.isnull().sum()
covid.info()
covid['Total Cases'].max()
covid.sort_values('Total Cases', ascending=False)

#correlation heatmap
from statsmodels.graphics.correlation import plot_corr
fig = plt.figure(figsize=(15,15), facecolor = 'white');
ax = fig.add_subplot(111);
plot_corr(covid.corr(method = 'kendall',numeric_only=True), xnames = covid.corr().columns, ax = ax)
plt.show()

#Unique rows
covid.sort_values('Country')
covid['Country'].sort_values().unique()


coviddf = covid
coviddf['Country'] = coviddf['Country'].replace({'USA': 'United States of America','St. Barth':'Saint Barthelemy','St. Vincent Grenadines':'Saint Vincent And The Grenadines','UK': 'United Kingdom','Bosnia and Herzegovina':'Bosnia And Herz.','Cabo Verde': 'Cape Verde','CAR': 'Central African Rep.','Curaçao': 'Curacao','DPRK': 'North Korea','DRC': 'Dem. Rep. Congo','Equatorial Guinea': 'Eq. Guinea','Falkland Islands': 'Falkland Is.','Dominican Republic': 'Dominican Rep.','Faeroe Islands': 'Faroe Islands','Antigua and Barbuda': 'Antigua And Barbuda','Guinea-Bissau': 'Guinea Bissau','Macao':'Macau','Saint Kitts and Nevis':'Saint Kitts And Nevis','Saint Pierre Miquelon':'Saint Pierre And Miquelon','Sao Tome and Principe':'Sao Tome And Principe','South Sudan': 'S. Sudan','S. Korea': 'South Korea','Solomon Islands': 'Solomon Is.','Réunion':'Reunion','Trinidad and Tobago':'Trinidad And Tobago','Turks and Caicos':'Turks And Caicos Islands','UAE':'United Arab Emirates', 'Western Sahara': 'W. Sahara'})

coviddf['Country'].sort_values().unique()

import geopandas as gpd
df_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
df_world['name'].nunique()
df_world['name'].sort_values().unique()

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



#Total cases map
ax = df_world["geometry"].boundary.plot(figsize=(20,16))
df_world_covid.plot( column="Total Cases", ax=ax, cmap='Reds', legend=True, legend_kwds={"label": "Number of Cases", "orientation":"horizontal"})
ax.set_title("Countries Vs numbetr of covid cases relative to thr rest of the countries")
plt.show()

#Total Deaths map
ax1 = df_world["geometry"].boundary.plot(figsize=(20,16))
df_world_covid.plot( column="Total Deaths", ax=ax1, cmap='Reds', legend=True, legend_kwds={"label": "Number of Deaths", "orientation":"horizontal"})
ax1.set_title("Countries Vs numbetr of covid deaths relative to thr rest of the countries")
plt.show()

#Total Tests map
ax2 = df_world["geometry"].boundary.plot(figsize=(20,16))
df_world_covid.plot( column="Total Test", ax=ax2, cmap='Reds',  legend=True, legend_kwds={"label": "Number of Tests", "orientation":"horizontal"})
ax2.set_title("Countries Vs numbetr of covid tests relative to thr rest of the countries")
plt.show()

def create_features(df):
    df['case_per_capita'] = np.log1p(df['Total Cases']/df['Population'])
    df['case_fatality_rate'] = np.log1p(df['Total Deaths'] / df['Total Cases'])
    df['deaths_per_capita'] = np.log1p(df['Total Deaths']/df['Population'])
    df['active_cases_per_capita'] = np.log1p(df['Active Cases']/df['Population'])
    df['recovery_rate'] = np.log1p(df['Total Recovered']/df['Total Cases'])
    df['tests_per_capita'] = np.log1p(df['Total Test']/df['Population'])


    
    return df
df = create_features(coviddf)

df_worldcovid = df_world.merge(df, how="left", left_on=['name'], right_on=['Country'])

#Total cases map
ax3 = df_world["geometry"].boundary.plot(figsize=(20,16))
df_worldcovid.plot( column="case_per_capita", ax=ax3, cmap='Reds', legend=True, legend_kwds={"label": "Number of Cases per population size", "orientation":"horizontal"})
ax3.set_title("Countries Vs numbetr of covid cases relative to thr rest of the countries")
plt.show()

ax4 = df_world["geometry"].boundary.plot(figsize=(20,16))
df_worldcovid.plot( column="case_fatality_rate", ax=ax4, cmap='Reds', legend=True, legend_kwds={"label": "Deaths per cases", "orientation":"horizontal"})
ax4.set_title("Countries Vs numbetr of covid cases relative to thr rest of the countries")
plt.show()

ax5 = df_world["geometry"].boundary.plot(figsize=(20,16))
df_worldcovid.plot( column="tests_per_capita", ax=ax5, cmap='Reds', legend=True, legend_kwds={"label": "tests per capita", "orientation":"horizontal"})
ax5.set_title("Countries Vs numbetr of covid cases relative to thr rest of the countries")
plt.show()
import Base
import pandas as pd
import numpy as np
import plotly.express as px

df=pd.read_csv("athlete_events.csv")
df_region=pd.read_csv("noc_regions.csv")

# calling result from base data
d=Base.preprocess(df,df_region)

# using base data to get medal counts
def medal_tally(d):
    medal_tally = d.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally=medal_tally.groupby("Region").sum().sort_values("Gold",ascending=False)[["Gold","Silver","Bronze"]].reset_index()
    medal_tally["Total"] = medal_tally["Gold"] + medal_tally["Silver"] + medal_tally["Bronze"]
    return medal_tally

def years_countries_list(d):
    years = d["Year"].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    countries = np.unique(d["Region"].dropna().values).tolist()
    countries.sort()
    countries.insert(0, "Overall")

    return years,countries

def fetch_medal_tally(d,years,countries):
    medal_d=d.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag=0
    if years=="Overall" and countries=="Overall":
        temp_d=medal_d
    if years!="Overall" and countries!="Overall":
        temp_d=medal_d[(medal_d["Region"]==countries) & (medal_d["Year"]==years)]
    if years!="Overall" and countries=="Overall":
        temp_d=medal_d[medal_d["Year"]==years]
    if years=="Overall" and countries!="Overall":
        flag=1
        temp_d=medal_d[medal_d["Region"]==countries]
    if flag==1:
        x=temp_d.groupby("Year").sum()[["Gold","Silver","Bronze"]].sort_values("Year").reset_index()
    else:
        x=temp_d.groupby("Region").sum()[["Gold","Silver","Bronze"]].sort_values("Gold",ascending=False).reset_index()
    x["Total"]=x["Gold"]+x["Silver"]+x["Bronze"]
    return x

def data_over_time(d,col):
    nations_over_time = d.drop_duplicates(["Year", col])["Year"].value_counts().reset_index().sort_values("index")
    nations_over_time.rename(columns={"index": "Edition", "Year": col}, inplace=True)
    return nations_over_time

def yearwise_medal_tally(d,coun):
    temp_df = d.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"], inplace=True)
    new_df = temp_df[temp_df["Region"] == coun]
    final_df = new_df.groupby("Year").count()["Medal"].reset_index()
    return final_df

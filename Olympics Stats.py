import numpy as np
import pandas as pd
import streamlit as st
import Base,Usage
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("athlete_events.csv")
df_region=pd.read_csv("noc_regions.csv")
d=Base.preprocess(df,df_region)

st.sidebar.title("Olympic Analysis")
st.sidebar.image("C:/Users/hp/OneDrive/Desktop/Olympics.png")

user_menu=st.sidebar.radio("Select an option",("Medal Tally","Overall Analysis","Country-wise Tally"))

if user_menu=="Medal Tally":
    st.sidebar.header("Medal Tally")
    years,countries=Usage.years_countries_list(d)

    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_countries = st.sidebar.selectbox("Select Country",countries)

    medal_tally=Usage.fetch_medal_tally(d,selected_year,selected_countries)
    if selected_year=="Overall" and selected_countries=="Overall":
        st.title("Overall Tally")
    if selected_year!="Overall" and selected_countries=="Overall":
        st.title("Global Tally in " + str(selected_year))
    if selected_year=="Overall" and selected_countries != "Overall":
        st.title("Overall Tally of "+ str(selected_countries))
    if selected_year != "Overall" and selected_countries != "Overall":
        st.title(str(selected_year) +" Tally of "+ str(selected_countries))
    st.table(medal_tally)

if user_menu=="Overall Analysis":
    st.title("Overall Analysis")
    Editions=d["Year"].unique().shape[0]-1
    Cities = d["City"].unique().shape[0]
    Sports = d["Sport"].unique().shape[0]
    Events = d["Event"].unique().shape[0]
    Athletes=d["Name"].unique().shape[0]
    Nations =d["Region"].unique().shape[0]

    st.title("Historical Stats")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(Editions)
    with col2:
        st.header("Cities")
        st.title(Cities)
    with col3:
        st.header("Sports")
        st.title(Sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Event")
        st.title(Events)
    with col2:
        st.header("Athletes")
        st.title(Athletes)
    with col3:
        st.header("Nations")
        st.title(Nations)

    nations_over_time=Usage.data_over_time(d,'Region')
    fig = px.line(nations_over_time, x="Edition", y="Region")
    st.title("Nations Tally Over The Years")
    st.plotly_chart(fig)

    events_over_time = Usage.data_over_time(d, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events Tally Over The Years")
    st.plotly_chart(fig)

    athletes_over_time = Usage.data_over_time(d, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    st.title("Athletes Tally Over The Years")
    st.plotly_chart(fig)

if user_menu=="Country-wise Tally":
    st.sidebar.title("Country-wise Analysis")
    country_list=d["Region"].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select a country',country_list)

    country_df=Usage.yearwise_medal_tally(d,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country+" Medal Tally Over The Years")
    st.plotly_chart(fig)


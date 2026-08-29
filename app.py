import os
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Bird Species Observation Dashboard",
    layout="wide",
    page_icon="🦅",
)


# Load data from SQL database
@st.cache_data
def get_data():
  if os.path.exists("bird_conservation.db"):
    conn = sqlite3.connect("bird_conservation.db")
    df = pd.read_sql("SELECT * FROM Fact_Bird_Observations", conn)
    conn.close()
  else:
    df = pd.read_csv("Cleaned_Combined_Bird_Data.csv")
  return df


df = get_data()

# App Title
st.title("🦅 Bird Species Observation & Ecosystem Diversity Analytics")
st.markdown(
    "Interactive Biodiversity & Habitat Analysis across 11 National Park"
    " Service Administrative Units"
)

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
unit_list = sorted(df["Admin_Unit_Code"].dropna().unique())
habitat_list = sorted(df["Habitat_Source"].dropna().unique())

units = st.sidebar.multiselect(
    "Select Administrative Unit", options=unit_list, default=unit_list[:5]
)
habitats = st.sidebar.multiselect(
    "Select Habitat Type", options=habitat_list, default=habitat_list
)
watchlist_only = st.sidebar.checkbox(
    "Show Only PIF Watchlist Species (At Risk)"
)

# Filter Data
filtered_df = df.copy()
if units:
  filtered_df = filtered_df[filtered_df["Admin_Unit_Code"].isin(units)]
if habitats:
  filtered_df = filtered_df[filtered_df["Habitat_Source"].isin(habitats)]
if watchlist_only:
  filtered_df = filtered_df[filtered_df["PIF_Watchlist_Status"] == True]

# Top KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Sightings", f"{len(filtered_df):,}")
kpi2.metric(
    "Unique Species", f"{filtered_df['Scientific_Name'].nunique():,}"
)
watchlist_count = filtered_df["PIF_Watchlist_Status"].sum()
kpi3.metric("Watchlist (At Risk) Sightings", f"{watchlist_count:,}")
kpi4.metric(
    "Vocal Detections",
    f"{(filtered_df['ID_Method'].isin(['Singing', 'Calling'])).sum():,}",
)

st.markdown("---")

# Visual Charts
col1, col2 = st.columns([6, 4])
with col1:
  st.subheader("Top 10 Most Observed Species")
  top_sp = filtered_df["Common_Name"].value_counts().head(10).reset_index()
  top_sp.columns = ["Species", "Sightings"]
  fig1 = px.bar(
      top_sp,
      x="Sightings",
      y="Species",
      orientation="h",
      color="Sightings",
      color_continuous_scale="Greens",
  )
  fig1.update_layout(
      yaxis={"categoryorder": "total ascending"},
      height=350,
      margin=dict(l=0, r=0, t=30, b=0),
  )
  st.plotly_chart(fig1, use_container_width=True)

with col2:
  st.subheader("Observations by Habitat")
  hab_count = filtered_df["Habitat_Source"].value_counts().reset_index()
  hab_count.columns = ["Habitat", "Count"]
  fig2 = px.pie(
      hab_count,
      values="Count",
      names="Habitat",
      hole=0.45,
      color_discrete_sequence=["#059669", "#0284c7"],
  )
  fig2.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
  st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
  st.subheader("Annual Observation Trends")
  year_trend = (
      filtered_df.groupby("Year").size().reset_index(name="Observations")
  )
  fig3 = px.line(
      year_trend,
      x="Year",
      y="Observations",
      markers=True,
      color_discrete_sequence=["#10b981"],
  )
  fig3.update_layout(height=320, margin=dict(l=0, r=0, t=30, b=0))
  st.plotly_chart(fig3, use_container_width=True)

with col4:
  st.subheader("Temperature vs Observation Activity")
  fig4 = px.histogram(
      filtered_df,
      x="Temperature",
      nbins=15,
      color="Habitat_Source",
      color_discrete_sequence=["#064e3b", "#38bdf8"],
  )
  fig4.update_layout(height=320, margin=dict(l=0, r=0, t=30, b=0))
  st.plotly_chart(fig4, use_container_width=True)

with st.expander("📋 View Cleaned Data Records"):
  st.dataframe(filtered_df.head(100), use_container_width=True)
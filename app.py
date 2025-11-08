import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App title
st.title("CO₂ Emissions in Africa")
st.write("Exploratoryy analysis of CO₂ emissions across African countries and sectors.")



#Loading the dataset
st.cache_data
def load_data():
    df = pd.read_csv("co2_Emission_Africa.csv")
    return df

df = load_data()

#Sidebar filters 
st.sidebar.header("Filter Data")
countries = df["Country"].unique()
years = sorted(df["Year"].unique())

selected_country = st.sidebar.selectbox("Select a country:", countries)
selected_year = st.sidebar.selectbox("Select a year:", years)

# Filtered data  
df_country = df[df["Country"] == selected_country]
df_year = df_country[df_country["Year"] == selected_year]

# --- Display summary ---
st.subheader(f"CO₂ Emission Summary for {selected_country} ({selected_year})")
if not df_year.empty:
    st.dataframe(df_year)

    # Identify sector columns
    sector_keywords = ['energy', 'transport', 'industrial', 'industry', 'agri', 'agriculture', 'waste']
    sector_cols = [c for c in df.columns if any(k in c.lower() for k in sector_keywords)]

    # Plot sectoral emissions
    st.write("### Sectoral Emissions Breakdown")
    sector_data = df_year[sector_cols].T
    sector_data.columns = ['Emissions (Mt)']

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=sector_data.index, y='Emissions (Mt)', data=sector_data, palette="Blues_d", ax=ax)
    plt.xticks(rotation=45)
    plt.title(f"Sectoral CO₂ Emissions - {selected_country} ({selected_year})")
    st.pyplot(fig)

    # Trend analysis over time
    st.write("### Emission Trend Over Time")
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.lineplot(x="Year", y="Total CO2 Emission excluding LUCF (Mt)", data=df_country, marker="o", ax=ax2)
    plt.title(f"CO₂ Emission Trend - {selected_country}")
    st.pyplot(fig2)
else:
    st.warning("No data available for this selection.")

# --- Regional comparison ---
st.subheader("Regional Comparison")
regions = df.groupby("Sub-Region")["Total CO2 Emission excluding LUCF (Mt)"].mean().sort_values(ascending=False)
st.bar_chart(regions)

st.caption("Data Source: African CO₂ Emissions Dataset | Created by Kelyian Sankei, Strathmore University (2025)")

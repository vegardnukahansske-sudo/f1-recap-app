import streamlit as st
import fastf1
import fastf1.plotting
import pandas as pd
import matplotlib.pyplot as plt

import os

cache_dir = '/tmp/f1_cache'
os.makedirs(cache_dir, exist_ok=True)

fastf1.Cache.enable_cache(cache_dir)
fastf1.plotting.setup_mpl()

st.set_page_config(page_title="F1 Recap", layout="wide")

st.title("🏁 F1 Race Recap Dashboard")

year = st.number_input("Year", value=2024)
race = st.text_input("Race (e.g. Belgium)")

if st.button("Load Race"):

    session = fastf1.get_session(year, race, 'R')
    session.load()

    st.success(f"{year} {race} loaded")

    res = session.results.copy()

    # 1. Let the user choose the year and race
    year_choice = st.selectbox("Select Year", [2020, 2021, 2022, 2023, 2024, 2025])
    race_choice = st.selectbox("Select Race", ["Bahrain", "Saudi Arabia", "Australia", "Miami", "Monaco", "Silverstone", "Abu Dhabi"])

    # 2. Update the session line to use your choices
    session = fastf1.get_session(year_choice, race_choice, 'R')


    # Use the 'race_choice' variable instead of a fixed name
    session = fastf1.get_session(2015, race_choice, 'R')

   # 1. UI Selection for Year and Race
year_choice = st.selectbox("Select Year", [2025, 2026])
race_choice = st.selectbox("Select Race", ["Bahrain", "Saudi Arabia", "Australia", "Miami", "Monaco", "Silverstone", "Abu Dhabi"])

# 2. Cached Function to Handle Data Retrieval
@st.cache_data
def load_lap_data(year, race):
    # Downloads data once and stores it to prevent RateLimitExceededError
    session = fastf1.get_session(year, race, 'R')
    session.load(laps=True, telemetry=True, weather=False)
    lap = session.laps.pick_fastest()
    return lap.get_pos_data()

# 3. Coordinate Processing (Ensured flush-left alignment)
pos = load_lap_data(year_choice, race_choice)

# 4. Matplotlib Visualization (Ensured flush-left alignment)
fig, ax = plt.subplots()
ax.plot(pos['X'], pos['Y'])
ax.axis('off')

st.pyplot(fig)


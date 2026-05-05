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

\

    # 1. Let the user choose the year and race
    year_choice = st.selectbox("Select Year", [2025, 2026])
    race_choice = st.selectbox("Select Race", ["Bahrain", "Saudi Arabia", "Australia", "Miami", "Monaco", "Silverstone", "Abu Dhabi"])

    # 2. Update the session line to use your choices
    session = fastf1.get_session(year_choice, race_choice, 'R')


    # Use the 'race_choice' variable instead of a fixed name
    session = fastf1.get_session(2026, race_choice, 'R')

    session.load()
    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()
    # 1. Let the user choose the year and race
    year_choice = st.selectbox("Select Year", [2025, 2026])
    race_choice = st.selectbox("Select Race", ["Bahrain", "Saudi Arabia", "Australia", "Miami", "Monaco", "Silverstone", "Abu Dhabi"])

    # 2. Use a cached function to load the data (stops the Rate Limit error)
    @st.cache_data
    def load_lap_data(year, race):
    session = fastf1.get_session(year, race, 'R')
    session.load(laps=True, telemetry=True, weather=False)
    lap = session.laps.pick_fastest()
    return lap.get_pos_data()

    # 3. Get the coordinates using the choices from the dropdowns
    pos = load_lap_data(year_choice, race_choice)

    fig, ax = plt.subplots() # Line 54 - Ensure no extra spaces here
    ax.plot(pos['X'], pos['Y'])
    ax.axis('off')

    st.pyplot(fig)


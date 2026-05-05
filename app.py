import streamlit as st
import fastf1
import fastf1.plotting
import pandas as pd
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('f1_cache')
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

    def safe_int(x):
        try:
            return int(x)
        except:
            return None

    res["Position"] = res["ClassifiedPosition"].apply(safe_int)
    res = res.dropna(subset=["Position"]).sort_values("Position")

    res["Grid"] = res["GridPosition"].apply(lambda x: x if x > 0 else len(res))
    res["Diff"] = res["Grid"] - res["Position"]

    st.dataframe(res[["Position","Abbreviation","TeamName","Grid","Diff","Status"]])

    st.subheader("Track Map")

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()

    fig, ax = plt.subplots()
    ax.plot(pos['X'], pos['Y'])
    ax.axis('off')

    st.pyplot(fig)

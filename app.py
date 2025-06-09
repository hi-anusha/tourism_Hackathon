import streamlit as st
from streamlit_option_menu import option_menu
from pages import Cultural_AirLens, Tourism_Insight_Studio, Tourism_Trends, Heritage_sites_map
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import re
import os
import pydeck as pdk
import matplotlib.pyplot as plt

st.set_page_config(page_title="India Cultural Tourism Intelligence", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Tourism Trends","Heritage Sites","Rain & Tourism Tracker","Pollution Lens"],
    icons=["bar-chart", "building","cloud","cloud-haze"],
    menu_icon="cast",
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f9fafc"},
        "icon": {"color": "#0F6AB4", "font-size": "20px"},
        "nav-link": {"font-size": "18px", "margin":"0px", "padding": "10px 20px"},
        "nav-link-selected": {"background-color": "#0F6AB4", "color": "white"},
    },
)


if selected == "Pollution Lens":
    Cultural_AirLens.render()
elif selected == "Rain & Tourism Tracker":
    Tourism_Insight_Studio.render()
elif selected == "Tourism Trends":
    Tourism_Trends.render()
elif selected == "Heritage Sites":
    Heritage_sites_map.render()
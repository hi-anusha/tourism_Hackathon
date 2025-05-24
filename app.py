import streamlit as st
from streamlit_option_menu import option_menu
from pages import Cultural_AirLens, Tourism_Insight_Studio,museum

st.set_page_config(page_title="India Cultural Tourism Intelligence", layout="wide")

st.markdown("""
    <style>
    #MainMenu, footer {visibility: hidden;}
    .css-18ni7ap.e8zbici2 {padding-top: 1rem;}
    </style>
""", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["🏞️ Cultural AirLens", "📊 Tourism Insight Studio" ,"🏛️ Museum Explorer"],
    icons=["cloud", "bar-chart", "building"],
    menu_icon="cast",
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f9fafc"},
        "icon": {"color": "#0F6AB4", "font-size": "20px"},
        "nav-link": {"font-size": "18px", "margin":"0px", "padding": "10px 20px"},
        "nav-link-selected": {"background-color": "#0F6AB4", "color": "white"},
    },
)

if selected == "🏞️ Cultural AirLens":
    Cultural_AirLens.render()
elif selected == "📊 Tourism Insight Studio":
    Tourism_Insight_Studio.render()
elif selected == "🏛️ Museum Explorer":
    museum.render()

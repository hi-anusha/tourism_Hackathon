import streamlit as st
import streamlit as st
import pandas as pd
import re
import os
import pydeck as pdk
import matplotlib.pyplot as plt

def render():
    @st.cache_data
    def load_data(path):
        return pd.read_csv(path, encoding='latin1')

    BASE_DIR = os.path.dirname(__file__)


    DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data/Cultural_Heritage_Datasets"))   
    df_heritage = load_data(os.path.join(DATA_DIR, "combined_heritage_with_coords.csv"))
    st.title("🗺️ Interactive Heritage Site Explorer")
    st.markdown(
        """
        **Interactive Heritage Explorer:**  
        Navigate an interactive 3D map of UNESCO and nationally 
        recognized heritage sites. Filter by city to:
        - See site locations clustered by type  
        - View age distribution and usage patterns  
        - Identify the oldest monuments

        **Data Source:**  
        - combined_heritage_with_coords.csv (Cultural Heritage sites from data.gov.in)
        
        **How to Use:**  
        1. Pick a city to highlight its sites in red.  
        2. Hover to see site names.  
        3. Scroll to the analysis section for age and use breakdowns.
        """
    )

    # Parse age helper
    def parse_age(age):
        if pd.isnull(age):
            return None
        if isinstance(age, (int, float)):
            return age
        age_str = str(age).lower()
        if "more than" in age_str or "above" in age_str:
            nums = re.findall(r'\d+', age_str)
            return int(nums[0]) if nums else None
        elif "century" in age_str:
            nums = re.findall(r'\d+', age_str)
            if "pre" in age_str or "17th" in age_str:
                return 400
            return 2025 - (int(nums[0]) * 100)
        elif '-' in age_str:
            nums = re.findall(r'\d+', age_str)
            if len(nums) == 2:
                return (int(nums[0]) + int(nums[1])) / 2
        nums = re.findall(r'\d+', age_str)
        return int(nums[0]) if nums else None

    df_heritage["Parsed Age"] = df_heritage["Age of heritage (in Years)"].apply(parse_age)
    df_heritage = df_heritage.dropna(subset=["Latitude", "Longitude"])

    cities = sorted(df_heritage["City Name"].dropna().unique())
    selected_city = st.selectbox("Or choose a city manually", cities)

    highlighted_data = df_heritage[df_heritage["City Name"] == selected_city]
    other_data = df_heritage[df_heritage["City Name"] != selected_city]

    # Icon data for selected
    icon_data = highlighted_data[["Longitude", "Latitude", "Name of heritage"]].copy()
    icon_data["icon_data"] = icon_data.apply(lambda row: {
        "url": "https://img.icons8.com/color/48/marker--v1.png",
        "width": 48, "height": 48, "anchorY": 48
    }, axis=1)

    st.subheader(f"📍 Highlight: {selected_city}")

    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=highlighted_data["Latitude"].mean() if not highlighted_data.empty else 20.59,
            longitude=highlighted_data["Longitude"].mean() if not highlighted_data.empty else 78.96,
            zoom=6, pitch=30,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=other_data,
                get_position="[Longitude, Latitude]",
                get_color="[0, 100, 200, 120]",
                get_radius=400,
            ),
            pdk.Layer(
                "IconLayer",
                data=icon_data,
                get_icon="icon_data",
                get_size=4,
                size_scale=10,
                get_position='[Longitude, Latitude]',
                pickable=True
            )
        ],
        tooltip={"html": "<b>{Name of heritage}</b>", "style": {"color": "white"}}
    ))

    if not highlighted_data.empty:
        st.header(f"🏙️ Cultural Insights for **{selected_city}**")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Number of Heritage Sites")
            st.metric(label="Total Heritage Sites", value=len(highlighted_data))

            st.subheader("🏛️ Nature of Heritage")
            nature_counts = highlighted_data["Nature of heritage"].value_counts()
            fig, ax = plt.subplots()
            ax.pie(nature_counts.values, labels=nature_counts.index, autopct='%1.1f%%')
            st.pyplot(fig)

        with col2:
            st.subheader("📈 Average Heritage Age")
            avg_age = highlighted_data["Parsed Age"].mean()
            st.metric(label="Average Age (Years)", value=f"{avg_age:.0f}" if avg_age else "N/A")

            st.subheader("🔍 Heritage Use")
            use_counts = highlighted_data["Heritage use"].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(use_counts.values, labels=use_counts.index, autopct='%1.1f%%')
            st.pyplot(fig2)

        st.subheader("🏆 Top 10 Oldest Heritage Sites")
        oldest_sites = highlighted_data[["Name of heritage", "Parsed Age"]].dropna()\
                            .sort_values(by="Parsed Age", ascending=False).head(10)
        st.dataframe(oldest_sites)

        st.subheader("📄 Full Data (Filtered)")
        st.dataframe(highlighted_data.reset_index(drop=True))
    else:
        st.info("Select a city with heritage data to view analysis.")

if __name__ == "__main__":
    render()



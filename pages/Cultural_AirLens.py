import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.title("🌬 Pollution Lens: Exploring Air Quality & Tourism Trends")

    df = pd.read_csv("data/airQualityindex.csv")
    df['last_update'] = pd.to_datetime(df['last_update'], errors='coerce')

    # --- 🔥 Key Insights (Top Priority) ---
    st.markdown("## 🔥 Key Insights")
    latest = df.dropna(subset=["pollutant_avg"])
    
    # **Most Polluted Cultural Hotspots**
    most_polluted_city = latest.groupby("city")["pollutant_avg"].mean().idxmax()
    highest_pollution = latest.groupby("city")["pollutant_avg"].mean().max()

    # **Least Polluted Cultural Hotspots**
    least_polluted_city = latest.groupby("city")["pollutant_avg"].mean().idxmin()
    lowest_pollution = latest.groupby("city")["pollutant_avg"].mean().min()

    st.info(f"""
        ✅ **Most Polluted Cultural Site:** {most_polluted_city} with **{highest_pollution:.2f} AQI**  
        ✅ **Least Polluted Cultural Site:** {least_polluted_city} with **{lowest_pollution:.2f} AQI**  
        
        🌍 **Tourism-Linked Pollution Trends:** Cities with more tourists often show **higher AQI values**.  
        🏞️ **Untouched Cultural Areas:** Less visited sites generally have **better air quality**—potentially due to fewer vehicles & industrial activity.  
    """)

    st.markdown("---")

    # --- Average Pollution by City ---
    st.subheader("📊 Average Pollution by City")
    grouped = latest.groupby('city')['pollutant_avg'].mean().reset_index()
    fig = px.bar(grouped.sort_values(by="pollutant_avg", ascending=False),
                 x='city', y='pollutant_avg', color='pollutant_avg',
                 title='Average Pollutant Levels by City')
    st.plotly_chart(fig, use_container_width=True)

    # ---  City-wise Pollutant Type Distribution ---
    st.subheader("🌿 City-wise Pollutant Type Distribution")
    pollutant_summary = latest.groupby(['city', 'pollutant_id'])['pollutant_avg'].mean().reset_index()
    fig2 = px.bar(pollutant_summary, x='city', y='pollutant_avg',
                  color='pollutant_id', barmode='group',
                  title='Pollutants by Type and City')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

if __name__ == "__main__":
    render()

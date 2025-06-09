import streamlit as st
import pandas as pd
import plotly.express as px
import os

def render():
    @st.cache_data
    def load_data(path):
        return pd.read_csv(path, encoding='latin1')

    BASE_DIR = os.path.dirname(__file__)
    DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

    # Load datasets
    df_dance = load_data(os.path.join(DATA_DIR, "India_Statewise_Cultural_Dance.csv"))
    df_festival = load_data(os.path.join(DATA_DIR, "Statewise_Festival.csv"))
    df_tourism1 = load_data(os.path.join(DATA_DIR, "India-Tourism-Statistics.csv"))
    df_tourism3 = load_data(os.path.join(DATA_DIR, "Quarter_data.csv"))
    df_tourism4 = load_data(os.path.join(DATA_DIR, "Age_data.csv"))
    df_fee = load_data(os.path.join(DATA_DIR, "revenue.csv"))
    df_country = load_data(os.path.join(DATA_DIR, "Countries_data.csv"))

    st.title("📊 Cultural Hotspots & Tourism Dynamics")

    st.markdown(
        """
        Understand how cultural richness drives tourism in India.  
        Explore patterns in **seasonality**, **age group preferences**, **economic impact**, and **global reach**.  
        Identify **underexplored regions** and potential for sustainable growth.
        """
    )

    # 1. FTAs Over Time
    st.subheader("📈 Foreign Tourist Arrivals (FTAs) Over Time")
    fig1 = px.line(df_tourism1, x="Year", y="FTAs in India (in Million)", markers=True,
                   title="Rising Trend in Inbound Tourism (1981–2020)")
    st.plotly_chart(fig1, use_container_width=True)
    st.info("Insight: India witnessed a steady rise in foreign tourist arrivals until 2019, indicating growing global interest in its cultural and historical attractions.")

    # 2. Seasonal Trends
    st.subheader("🕒 Seasonal Patterns in Tourism")
    fig_quarter = px.line(
        df_tourism3,
        x="Year",
        y=[
            "% distribution by quarter - 1st Quarter - (Jan-Mar)",
            "% distribution by quarter - 2nd Quarter - (Apr-June)",
            "% distribution by quarter - 3rd Quarter - (July-Sep)",
            "% distribution by quarter - 4th Quarter - (Oct-Dec)"
        ],
        markers=True,
        title="Tourist Flow by Season"
    )
    st.plotly_chart(fig_quarter, use_container_width=True)
    st.info("Insight: Peak footfall occurs in Oct–Dec and Jan–Mar, suggesting strong winter preferences. The Apr–Jun (summer) quarter sees the lowest traffic — offering a strategic window to promote indoor or offbeat cultural experiences.")

    # 3. Age Distribution
    st.subheader("👥 Age Group Preferences")
    age_cols = [col for col in df_tourism4.columns if "Age-Group" in col]
    fig_age = px.area(df_tourism4, x="Year", y=age_cols, title="Tourist Arrivals by Age Group")
    st.plotly_chart(fig_age, use_container_width=True)
    st.info("Insight: Most foreign tourists visiting India are between 35–54 years old. This age group is a great target for promoting cultural tours and heritage experiences.")

    # 4. Foreign Exchange Earnings
    st.subheader("💰 Economic Contribution of Tourism")
    fig_fee_rs = px.line(df_fee, x="Year", y="FEE in Rs. terms - Rs. Crore",
                         title="Tourism Revenue (₹ Crores)", markers=True)
    st.plotly_chart(fig_fee_rs, use_container_width=True)
    st.info("Insight: As more tourists visited India, the money earned from tourism also increased. This shows that investing in cultural heritage sites can help boost the country’s income even more.")

    # 5. Top Source Countries
    st.subheader("🌍 Top Contributing Countries (2019)")
    df_country["Year"] = df_country["Year"].astype(str).str.strip()
    top_year = df_country[df_country["Year"] == "2019"].drop(columns=["Year"], errors="ignore")
    if not top_year.empty:
        top_countries = pd.DataFrame({
            "Country": top_year.columns,
            "Arrivals": top_year.iloc[0].values.astype(int)
        }).sort_values("Arrivals", ascending=False).head(10)
        fig_countries = px.bar(top_countries, x="Country", y="Arrivals", text_auto=True,
                               title="Top 10 Tourist Source Countries")
        st.plotly_chart(fig_countries, use_container_width=True)
        st.info("Insight: Tourists majorly arrive from neighboring and Western nations — revealing scope to market India's cultural diversity in emerging countries.")
    else:
        st.error("No data found for the year 2019 in Countries_data.csv.")


if __name__ == "__main__":
    render()

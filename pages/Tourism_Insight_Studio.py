import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.title("🌧 Rain & Tourism Tracker")
    st.caption("Discover trends, anomalies, and correlations in India's tourism and climate.")

    # Load data
    df1 = pd.read_csv("data/India-Tourism-Statistics-2021-Table-5.2.1.csv")
    df1.columns = df1.columns.str.strip()
    df1 = df1.dropna(subset=["Year", "Number of Visitors - Total"])
    df1["Year"] = pd.to_numeric(df1["Year"], errors="coerce")
    df1["Number of Visitors - Total"] = pd.to_numeric(df1["Number of Visitors - Total"], errors="coerce")

    df2 = pd.read_csv("data/rainfall_area-wt_sd_1901-2015.csv", encoding="ISO-8859-1")
    df2.columns = df2.columns.str.strip()

    # User Inputs
    subdivision_selected = st.selectbox("🌍 Select a Region (Subdivision)", sorted(df2["SUBDIVISION"].unique()))
    year_selected = st.selectbox("📆 Select a Year", sorted(df2["YEAR"].unique()))

    # Pre-filter data
    filtered_df = df2[(df2["SUBDIVISION"] == subdivision_selected) & (df2["YEAR"] == year_selected)]
    rainfall_data = df2[df2["SUBDIVISION"] == subdivision_selected][["YEAR", "ANNUAL"]]
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    seasons = ["Jan-Feb", "Mar-May", "Jun-Sep", "Oct-Dec"]

    mean_rainfall = rainfall_data["ANNUAL"].mean()
    std_rainfall = rainfall_data["ANNUAL"].std()
    anomalies = rainfall_data[(rainfall_data["ANNUAL"] > mean_rainfall + 2*std_rainfall) |
                              (rainfall_data["ANNUAL"] < mean_rainfall - 2*std_rainfall)]
    top5_wet = rainfall_data.nlargest(5, "ANNUAL")
    top5_dry = rainfall_data.nsmallest(5, "ANNUAL")

    # 🔍 Top-Level Highlighted Insights
    st.markdown("## 🔍 Key Insights", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.success(f"💧 Average Annual Rainfall in {subdivision_selected}: **{mean_rainfall:.2f} mm**")
        st.warning(f"🌧️ Top Wet Year: **{top5_wet.iloc[0]['YEAR']}** with **{top5_wet.iloc[0]['ANNUAL']} mm**")
        st.info(f"🌵 Driest Year: **{top5_dry.iloc[0]['YEAR']}** with **{top5_dry.iloc[0]['ANNUAL']} mm**")

    with col2:
        if not anomalies.empty:
            st.error(f"⚠️ {len(anomalies)} Rainfall Anomalies Detected")
            st.dataframe(anomalies.rename(columns={"ANNUAL": "Rainfall (mm)"}))
        else:
            st.success("✅ No major rainfall anomalies detected.")

    st.info(f"""
    🌍 **Tourism Suggestion for {subdivision_selected}**:
    - This region experiences a rainfall average of **{mean_rainfall:.1f} mm** annually.
    - Consider promoting tourism during **drier months** or designing **monsoon-specific experiences** like:
        - River trails
        - Cultural monsoon festivals
        - Wildlife spotting
    """)

    st.markdown("---")

    # 📈 Domestic Tourism
    st.subheader("📈 Domestic Tourism Trends (2021)")
    fig_domestic = px.line(df1, x="Year", y="Number of Visitors - Total", title="Domestic Visitor Trends Over Years")
    st.plotly_chart(fig_domestic, use_container_width=True)

    # 🌧️ Rainfall Charts
    if not filtered_df.empty:
        st.metric("Annual Rainfall", f"{filtered_df['ANNUAL'].values[0]} mm")

        st.subheader("📅 Monthly Rainfall Pattern")
        monthly_df = filtered_df.melt(id_vars=["SUBDIVISION", "YEAR"], value_vars=months,
                                      var_name="Month", value_name="Rainfall")
        fig_monthly = px.line(monthly_df, x="Month", y="Rainfall", title="Monthly Rainfall")
        st.plotly_chart(fig_monthly, use_container_width=True)

        st.subheader("☀️ Seasonal Rainfall Distribution")
        seasonal_df = filtered_df.melt(id_vars=["SUBDIVISION", "YEAR"], value_vars=seasons,
                                       var_name="Season", value_name="Rainfall")
        fig_seasonal = px.bar(seasonal_df, x="Season", y="Rainfall", title="Seasonal Rainfall")
        st.plotly_chart(fig_seasonal, use_container_width=True)

        st.subheader("📉 Annual Rainfall Trend")
        fig_annual = px.line(df2[df2["SUBDIVISION"] == subdivision_selected], x="YEAR", y="ANNUAL",
                             title=f"Annual Rainfall in {subdivision_selected}")
        st.plotly_chart(fig_annual, use_container_width=True)

    # Show Top 5 Wettest/Driest Years
    st.subheader("🗓️ Wettest & Driest Years")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**🌧️ Top 5 Wettest Years**")
        st.dataframe(top5_wet.rename(columns={"ANNUAL": "Rainfall (mm)"}))
    with col4:
        st.markdown("**🌵 Top 5 Driest Years**")
        st.dataframe(top5_dry.rename(columns={"ANNUAL": "Rainfall (mm)"}))

    st.markdown("---")
    st.caption("📌 Data Sources: Ministry of Tourism & IMD (1901–2015)")

if __name__ == "__main__":
    render()

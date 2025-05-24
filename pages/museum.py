import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.title("🏛️ Karnataka Museum Explorer")
    st.caption("Unlocking insights into government museums across Karnataka")

    # Load data
    df = pd.read_csv("data/List_Of_Museums.csv", encoding="utf-8")
    df.columns = df.columns.str.strip()

    # Standardize column names
    df.rename(columns={
        "District": "District",
        "Museum Name": "Museum_Name",
        "Fee": "Fee",
        "Museum incharge head": "Incharge",
        "Contact Numbers": "Contact",
        "Email.Id": "Email"
    }, inplace=True)

    # --- 🚀 Key Insights (Top Priority) ---
    st.markdown("## 🔥 Key Insights")
    total_museums = len(df)
    unique_districts = df["District"].nunique()
    avg_fee = df["Fee"].mean()

    st.info(f"""
        ✅ **Total Museums:** {total_museums}  
        ✅ **Unique Districts Covered:** {unique_districts}  
        ✅ **Average Entry Fee:** ₹{avg_fee:.2f}  
        
        🔍 **Incharge Role Distribution:** {df["Incharge"].value_counts().to_dict()}  
        {"🔴 Some museums lack proper contact details." if df['Contact'].isna().sum() > 0 else "🟢 All museums provide contact information."}
    """)

    st.markdown("---")

    # --- 📊 Overview Metrics ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Museums", total_museums)
    col2.metric("Unique Districts", unique_districts)
    col3.metric("Average Entry Fee", f"₹{avg_fee:.2f}")

    # --- 💰 Entry Fee Distribution ---
    st.markdown("## 💰 Entry Fee Distribution")
    fig_fee = px.histogram(df, x="Fee", nbins=10, color_discrete_sequence=['#0F6AB4'])
    st.plotly_chart(fig_fee, use_container_width=True)

    # --- 🔍 District Selection ---
    selected_city = st.selectbox("🔍 Select a District for Insights", sorted(df["District"].unique()))
    city_data = df[df["District"] == selected_city]

    st.markdown(f"## 🗺️ Museums in {selected_city}")
    st.dataframe(city_data[["Museum_Name", "Fee", "Incharge", "Contact", "Email"]], use_container_width=True)

    # --- 👥 Museum Incharge Distribution ---
    st.markdown("## 👥 Museum Incharge Role Distribution")
    role_counts = df["Incharge"].value_counts().reset_index()
    role_counts.columns = ["Role", "Count"]
    fig_roles = px.pie(role_counts, names="Role", values="Count", title="Incharge Roles")
    st.plotly_chart(fig_roles, use_container_width=True)

    # --- ☎️ Contact Info Availability ---
    st.markdown("## ☎️ Contact Info Availability")
    df["Has_Contact"] = df["Contact"].notna()
    contact_counts = df["Has_Contact"].value_counts().rename({True: "Has Contact", False: "Missing Contact"})
    fig_contact = px.bar(
        x=contact_counts.index,
        y=contact_counts.values,
        labels={"x": "Contact Info", "y": "Number of Museums"},
        color=contact_counts.index,
        color_discrete_sequence=['#2E8B57', '#DC143C']
    )
    st.plotly_chart(fig_contact, use_container_width=True)

    st.markdown("---")

if __name__ == "__main__":
    render()

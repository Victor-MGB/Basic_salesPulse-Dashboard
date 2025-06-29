import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ---------- Page Config ----------
st.set_page_config(page_title=" Professional Sales Dashboard", layout="wide")

# ---------- Sample Data ----------
np.random.seed(42)
df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=100),
    "Sales": np.random.randint(500, 2000, size=100),
    "Region": np.random.choice(['North', 'South', 'East', 'West'], size=100),
    "Product": np.random.choice(['Product A', 'Product B', 'Product C'], size=100)
})

# ---------- Sidebar Navigation ----------
with st.sidebar:
    # st.image("https://cdn-icons-png.flaticon.com/512/1170/1170678.png", width=100)
    st.title(" SalesPulse Dashboard")
    selected_page = st.radio("Go to page:", [" Visual Dashboard", " Basic Table View"])

    st.markdown("---")
    st.subheader(" Filters")

    # Region/Product Filters
    regions = st.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
    products = st.multiselect("Product", df["Product"].unique(), default=df["Product"].unique())

    # Date Filter
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    start_date, end_date = st.date_input("Date Range", [min_date, max_date])

# ---------- Data Filtering ----------
filtered_data = df[
    (df["Region"].isin(regions)) &
    (df["Product"].isin(products)) &
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date))
]

# ---------- Shared KPI Metrics ----------
def show_kpis(data):
    total_sales = data["Sales"].sum()
    avg_sales = data["Sales"].mean()
    transactions = len(data)

    st.markdown("###  Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric(" Total Sales", f"${total_sales:,.0f}")
    col2.metric(" Average Sale", f"${avg_sales:,.0f}")
    col3.metric(" Transactions", transactions)

# ---------- Visual Dashboard ----------
if selected_page == " Visual Dashboard":
    st.title(" Advanced Sales Visual Dashboard")
    show_kpis(filtered_data)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" Sales Over Time")
        line_fig = px.line(filtered_data, x="Date", y="Sales", markers=True, title="Daily Sales")
        line_fig.update_layout(margin=dict(t=30, b=10), height=400)
        st.plotly_chart(line_fig, use_container_width=True)

    with col2:
        st.subheader(" Sales by Region")
        bar_fig = px.bar(filtered_data, x="Region", y="Sales", color="Region", title="Sales Distribution by Region")
        bar_fig.update_layout(margin=dict(t=30, b=10), height=400)
        st.plotly_chart(bar_fig, use_container_width=True)

    st.subheader(" Sales by Product")
    pie_fig = px.pie(filtered_data, names="Product", values="Sales", hole=0.4, title="Product Contribution")
    pie_fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(pie_fig, use_container_width=True)

# ---------- Basic Table View ----------
elif selected_page == " Basic Table View":
    st.title(" Sales Data Table")
    show_kpis(filtered_data)
    st.markdown("---")

    # Table
    st.subheader(" Filtered Sales Records")
    st.dataframe(filtered_data, use_container_width=True)

    # Download Button
    @st.cache_data
    def convert_df_to_csv(data):
        return data.to_csv(index=False).encode("utf-8")

    csv_data = convert_df_to_csv(filtered_data)
    st.download_button(
        label="⬇️ Download as CSV",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv"
    )

    st.markdown(" Data includes filters applied above.")

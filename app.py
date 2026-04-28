import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

st.title("E-commerce Dashboard")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("ecommerce.csv")

df = load_data()

# -------- NAVBAR -------- #
selected = option_menu(
    menu_title=None,
    options=["Home", "Product Analysis", "City Insights", "Comparison", "Data Explorer"],
    icons=["house","box","geo","bar-chart","table"],
    orientation="horizontal"
)

# -------- HOME -------- #
if selected == "Home":
    st.subheader("Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", df["Row ID"].nunique())
    col2.metric("Total Sales", round(df["Sales"].sum(),2))
    col3.metric("Total Profit", round(df["Profit"].sum(),2))
    col4.metric("Total Quantity", df["Quantity"].sum())

    st.dataframe(df.head())

# -------- PRODUCT ANALYSIS -------- #
elif selected == "Product Analysis":
    st.subheader("Product Analysis")

    product = st.selectbox("Select Product", df["Product Name"])

    pdata = df[df["Product Name"] == product]

    col1, col2, col3 = st.columns(3)

    col1.metric("Sales", round(pdata["Sales"].sum(),2))
    col2.metric("Profit", round(pdata["Profit"].sum(),2))
    col3.metric("Quantity", pdata["Quantity"].sum())

    fig = px.bar(
        pdata,
        x="City",
        y="Sales",
        color="City",
        title="Sales by City"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------- CITY INSIGHTS -------- #
elif selected == "City Insights":
    st.subheader("City Insights")

    # Top 5 cities only
    city_sales = (
        df.groupby("City")["Sales"]
        .sum()
        .reset_index()
        .sort_values(by="Sales", ascending=False)
        .head(5)   #  sirf top 5
    )

    fig = px.pie(
        city_sales,
        names="City",
        values="Sales",
        title="Top 5 Cities by Sales",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)
# -------- COMPARISON -------- #
elif selected == "Comparison":
    st.subheader("Product Comparison")

    products = st.multiselect(
        "Select Products",
        df["Product Name"].unique(),
        default=df["Product Name"].unique()[:5]
    )

    compare = df[df["Product Name"].isin(products)]

    fig = px.scatter(
        compare,
        x="Sales",
        y="Profit",
        size="Quantity",
        color="Category",
        hover_name="Product Name",
        title="Sales vs Profit"
    )

    st.plotly_chart(fig, use_container_width=True)

# -------- DATA EXPLORER -------- #
elif selected == "Data Explorer":
    st.subheader("Full Dataset")
    st.dataframe(df)
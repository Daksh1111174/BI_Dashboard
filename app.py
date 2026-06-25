import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Intelligence Dashboard")

st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("sample_sales_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

# ---------------- Sidebar Filters ---------------- #

st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category))
]

# ---------------- KPI Cards ---------------- #

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
orders = filtered_df.shape[0]
customers = filtered_df["Customer"].nunique()

c1,c2,c3,c4 = st.columns(4)

c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Orders", orders)
c4.metric("Customers", customers)

st.divider()

# ---------------- Sales Trend ---------------- #

sales_trend = (
    filtered_df
    .groupby("Date")["Sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    sales_trend,
    x="Date",
    y="Sales",
    markers=True,
    title="Sales Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Two Charts ---------------- #

left,right = st.columns(2)

with left:

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=.4,
        title="Sales by Category"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Regional Sales"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- Monthly Analysis ---------------- #

filtered_df["Month"] = filtered_df["Date"].dt.strftime("%b")

monthly = (
    filtered_df.groupby("Month")[["Sales","Profit"]]
    .sum()
    .reset_index()
)

fig = px.bar(
    monthly,
    x="Month",
    y=["Sales","Profit"],
    barmode="group",
    title="Monthly Sales & Profit"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------- Top Customers ---------------- #

top_customer = (
    filtered_df.groupby("Customer")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_customer,
    x="Customer",
    y="Sales",
    color="Sales",
    title="Top Customers"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------- Data Table ---------------- #

st.subheader("Sales Data")

st.dataframe(filtered_df,use_container_width=True)

# ---------------- Download ---------------- #

csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "Filtered_Data.csv",
    "text/csv"
)

# ---------------- Business Insights ---------------- #

st.subheader("Business Insights")

best_region = region_sales.sort_values("Sales",ascending=False).iloc[0]["Region"]
best_category = category_sales.sort_values("Sales",ascending=False).iloc[0]["Category"]
best_customer = top_customer.iloc[0]["Customer"]

st.success(f"""
✅ Highest Sales Region : **{best_region}**

✅ Best Performing Category : **{best_category}**

✅ Top Customer : **{best_customer}**

✅ Profit Margin : **{(total_profit/total_sales)*100:.2f}%**
""")

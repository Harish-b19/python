import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.data_filter import apply_filters
from utils.charts import (
    bar_chart,
    horizontal_bar_chart,
    histogram,
    scatter_chart
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Executive Portfolio Overview",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# PAGE TITLE
# =========================================================

st.title("🏦 Executive Portfolio Overview")

st.markdown(
    """
    **High-level overview of the Home Credit loan portfolio,
    customer characteristics, credit exposure, and repayment risk.**
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data("data/application_train.csv")

except FileNotFoundError:

    st.error("❌ application_train.csv not found.")
    st.stop()


# =========================================================
# COMMON FILTERS
# =========================================================

filtered_df = apply_filters(df)


# =========================================================
# CHECK FILTER RESULT
# =========================================================

if filtered_df.empty:

    st.warning("⚠️ No applications match the selected filters.")
    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_customers = filtered_df["SK_ID_CURR"].nunique()

total_applications = len(filtered_df)

default_customers = filtered_df.loc[
    filtered_df["TARGET"] == 1,
    "SK_ID_CURR"
].nunique()

non_default_customers = filtered_df.loc[
    filtered_df["TARGET"] == 0,
    "SK_ID_CURR"
].nunique()

default_rate = (
    filtered_df["TARGET"].mean() * 100
)

total_credit_amount = (
    filtered_df["AMT_CREDIT"].sum()
)

average_credit_amount = (
    filtered_df["AMT_CREDIT"].mean()
)

average_customer_income = (
    filtered_df["AMT_INCOME_TOTAL"].mean()
)

average_annuity = (
    filtered_df["AMT_ANNUITY"].mean()
)

average_goods_price = (
    filtered_df["AMT_GOODS_PRICE"].mean()
)

median_income = (
    filtered_df["AMT_INCOME_TOTAL"].median()
)

median_credit_amount = (
    filtered_df["AMT_CREDIT"].median()
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Portfolio KPIs")


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "📋 Total Applications",
        f"{total_applications:,}"
    )

with col3:
    st.metric(
        "🔴 Default Customers",
        f"{default_customers:,}"
    )

with col4:
    st.metric(
        "🟢 Non-Default Customers",
        f"{non_default_customers:,}"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "⚠️ Default Rate",
        f"{default_rate:.2f}%"
    )

with col6:
    st.metric(
        "💰 Total Credit Amount",
        f"{total_credit_amount:,.0f}"
    )

with col7:
    st.metric(
        "💳 Average Credit",
        f"{average_credit_amount:,.0f}"
    )

with col8:
    st.metric(
        "💵 Average Income",
        f"{average_customer_income:,.0f}"
    )


col9, col10, col11, col12 = st.columns(4)

with col9:
    st.metric(
        "📆 Average Annuity",
        f"{average_annuity:,.0f}"
    )

with col10:
    st.metric(
        "🏷️ Average Goods Price",
        f"{average_goods_price:,.0f}"
    )

with col11:
    st.metric(
        "📌 Median Income",
        f"{median_income:,.0f}"
    )

with col12:
    st.metric(
        "📌 Median Credit",
        f"{median_credit_amount:,.0f}"
    )


st.divider()


# =========================================================
# DEFAULT VS NON-DEFAULT
# =========================================================

st.subheader("🎯 Portfolio Risk Overview")

default_summary = (
    filtered_df["TARGET"]
    .map({
        0: "Non-Default",
        1: "Default"
    })
    .value_counts()
    .reset_index()
)

default_summary.columns = [
    "Risk Status",
    "Applications"
]


col1, col2 = st.columns(2)


with col1:

    fig_default = px.bar(
        default_summary,
        x="Risk Status",
        y="Applications",
        title="Default vs Non-Default",
        text="Applications"
    )

    st.plotly_chart(
        fig_default,
        use_container_width=True
    )


# =========================================================
# DEFAULT PERCENTAGE - DONUT
# =========================================================

with col2:

    fig_donut = px.pie(
        default_summary,
        names="Risk Status",
        values="Applications",
        title="Default Percentage",
        hole=0.55
    )

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )


# =========================================================
# APPLICATIONS BY CONTRACT TYPE
# =========================================================

st.subheader("🏦 Loan Portfolio Composition")

col1, col2 = st.columns(2)


with col1:

    fig_contract = bar_chart(
        filtered_df,
        "NAME_CONTRACT_TYPE",
        None,
        "Applications by Contract Type"
    )

    st.plotly_chart(
        fig_contract,
        use_container_width=True
    )


# =========================================================
# CREDIT AMOUNT DISTRIBUTION
# =========================================================

with col2:

    fig_credit = histogram(
        filtered_df,
        "AMT_CREDIT",
        "Credit Amount Distribution"
    )

    st.plotly_chart(
        fig_credit,
        use_container_width=True
    )


# =========================================================
# INCOME DISTRIBUTION
# =========================================================

st.subheader("💰 Customer Financial Profile")

col1, col2 = st.columns(2)


with col1:

    fig_income = histogram(
        filtered_df,
        "AMT_INCOME_TOTAL",
        "Income Distribution"
    )

    st.plotly_chart(
        fig_income,
        use_container_width=True
    )


# =========================================================
# CREDIT BY INCOME TYPE - TREEMAP
# =========================================================

with col2:

    income_type_credit = (
        filtered_df
        .groupby("NAME_INCOME_TYPE")["AMT_CREDIT"]
        .sum()
        .reset_index()
    )

    fig_treemap = px.treemap(
        income_type_credit,
        path=["NAME_INCOME_TYPE"],
        values="AMT_CREDIT",
        title="Credit Exposure by Income Type"
    )

    st.plotly_chart(
        fig_treemap,
        use_container_width=True
    )


# =========================================================
# DEFAULT RATE BY INCOME TYPE
# =========================================================

st.subheader("⚠️ Risk by Customer Segment")

col1, col2 = st.columns(2)


with col1:

    fig_income_risk = horizontal_bar_chart(
        filtered_df,
        "NAME_INCOME_TYPE",
        "TARGET",
        "Default Rate by Income Type",
        aggfunc="mean"
    )

    # Convert proportion to percentage
    fig_income_risk.update_xaxes(
        tickformat=".1%"
    )

    st.plotly_chart(
        fig_income_risk,
        use_container_width=True
    )


# =========================================================
# INCOME VS CREDIT
# =========================================================

with col2:

    fig_income_credit = scatter_chart(
        filtered_df,
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "TARGET",
        "Income vs Credit"
    )

    st.plotly_chart(
        fig_income_credit,
        use_container_width=True
    )


st.divider()


# =========================================================
# REQUIRED INSIGHTS
# =========================================================

st.subheader("💡 Portfolio Insights")


# Largest customer segment

largest_segment = (
    filtered_df["NAME_INCOME_TYPE"]
    .value_counts()
    .idxmax()
)

largest_segment_count = (
    filtered_df["NAME_INCOME_TYPE"]
    .value_counts()
    .max()
)


# Highest-risk income segment

income_risk = (
    filtered_df
    .groupby("NAME_INCOME_TYPE")["TARGET"]
    .mean()
    .sort_values(ascending=False)
)

highest_risk_segment = income_risk.index[0]

highest_risk_rate = (
    income_risk.iloc[0] * 100
)


# =========================================================
# DISPLAY INSIGHTS
# =========================================================

insight_col1, insight_col2 = st.columns(2)


with insight_col1:

    st.info(
        f"""
        **🎯 Overall Default Rate**

        The current portfolio default rate is
        **{default_rate:.2f}%**.

        This represents the percentage of applications
        with payment difficulties.
        """
    )

    st.info(
        f"""
        **💰 Total Credit Exposure**

        The portfolio has total credit exposure of
        **{total_credit_amount:,.0f}**.

        Average credit amount is
        **{average_credit_amount:,.0f}**.
        """
    )


with insight_col2:

    st.info(
        f"""
        **👥 Largest Customer Segment**

        **{largest_segment}** is the largest income
        segment with **{largest_segment_count:,} applications**.
        """
    )

    st.warning(
        f"""
        **⚠️ Highest-Risk Income Segment**

        **{highest_risk_segment}** has the highest
        observed default rate at **{highest_risk_rate:.2f}%**.
        """
    )


# =========================================================
# TYPICAL CUSTOMER PROFILE
# =========================================================

st.subheader("👤 Typical Customer Profile")

st.markdown(
    f"""
    - **Median Income:** {median_income:,.0f}
    - **Median Credit Amount:** {median_credit_amount:,.0f}
    - **Average Annuity:** {average_annuity:,.0f}
    - **Average Goods Price:** {average_goods_price:,.0f}
    """
)


# =========================================================
# MANAGEMENT RECOMMENDATIONS
# =========================================================

st.subheader("📌 Management Recommendations")
st.markdown(
    f"""
    **1. 🎯 Strengthen Risk Assessment**

    Give additional attention to high-risk customer segments,
    particularly **{highest_risk_segment}**, when evaluating
    loan applications.

    **2. 💰 Monitor Credit Exposure**

    Closely monitor large credit exposures and compare requested
    credit amounts against customer income and affordability.

    **3. 📊 Segment-Based Lending Strategy**

    Use customer income and demographic segments to develop
    differentiated lending policies, pricing, and risk controls.

    **4. 🔍 Continuous Portfolio Monitoring**

    Track the default rate and credit exposure regularly to
    identify emerging changes in portfolio risk.
    """
)


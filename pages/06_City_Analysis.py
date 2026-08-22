import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.features import create_income_features
from utils.kpi import (
    calculate_income_metrics,
    calculate_home_metrics
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Income Analysis",
    page_icon="💰",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("💰 Income Analysis")

st.markdown(
    """
    Analyze customer income distribution and its
    relationship with lending and default risk.
    """
)


# ==================================================
# LOAD DATA
# ==================================================

try:

    df = load_data(
        "data/application_train.csv"
    )

except FileNotFoundError:

    st.error(
        "❌ application_train.csv not found."
    )

    st.stop()


# ==================================================
# FEATURE ENGINEERING
# ==================================================

df = create_income_features(df)


# ==================================================
# KPI CALCULATIONS
# ==================================================

income_metrics = calculate_income_metrics(df)

home_metrics = calculate_home_metrics(df)


# ==================================================
# KPI CARDS
# ==================================================

st.subheader("📊 Income KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "💰 Average Income",
        f"{income_metrics['average_income']:,.0f}"
    )

with col2:

    st.metric(
        "📊 Median Income",
        f"{income_metrics['median_income']:,.0f}"
    )

with col3:

    st.metric(
        "💵 Maximum Income",
        f"{income_metrics['maximum_income']:,.0f}"
    )

with col4:

    st.metric(
        "👨‍👩‍👧 Income / Family Member",
        f"{income_metrics['average_income_per_family']:,.0f}"
    )

with col5:

    st.metric(
        "🏆 Largest Income Group",
        income_metrics["largest_income_group"]
    )


st.divider()


# ==================================================
# INCOME HISTOGRAM
# ==================================================

st.subheader("📊 Income Distribution")

fig_income = px.histogram(
    df,
    x="AMT_INCOME_TOTAL",
    nbins=50,
    title="Income Distribution"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# ==================================================
# INCOME GROUP DISTRIBUTION
# ==================================================

st.subheader("📂 Income Group Distribution")

income_group_data = (
    df["INCOME_GROUP"]
    .value_counts()
    .reindex([
        "Very Low",
        "Low",
        "Middle",
        "High",
        "Very High"
    ])
    .reset_index()
)

income_group_data.columns = [
    "Income Group",
    "Applications"
]

fig_income_group = px.bar(
    income_group_data,
    x="Income Group",
    y="Applications",
    text="Applications",
    title="Applications by Income Group"
)

st.plotly_chart(
    fig_income_group,
    use_container_width=True
)


# ==================================================
# INCOME BY EDUCATION
# ==================================================

st.subheader("🎓 Income by Education")

fig_education = px.box(
    df,
    x="NAME_EDUCATION_TYPE",
    y="AMT_INCOME_TOTAL",
    title="Income Distribution by Education",
    points=False
)

fig_education.update_layout(
    xaxis_title="Education",
    yaxis_title="Income"
)

st.plotly_chart(
    fig_education,
    use_container_width=True
)


# ==================================================
# INCOME BY OCCUPATION
# ==================================================

st.subheader("💼 Income by Occupation")

occupation_income = (
    df.groupby(
        "OCCUPATION_TYPE",
        dropna=False
    )["AMT_INCOME_TOTAL"]
    .mean()
    .sort_values(ascending=True)
    .reset_index()
)

occupation_income["OCCUPATION_TYPE"] = (
    occupation_income["OCCUPATION_TYPE"]
    .fillna("Unknown")
)

fig_occupation = px.bar(
    occupation_income,
    x="AMT_INCOME_TOTAL",
    y="OCCUPATION_TYPE",
    orientation="h",
    text="AMT_INCOME_TOTAL",
    title="Average Income by Occupation"
)

fig_occupation.update_traces(
    texttemplate="%{text:,.0f}"
)

st.plotly_chart(
    fig_occupation,
    use_container_width=True
)


# ==================================================
# INCOME BY INCOME TYPE
# ==================================================

st.subheader("🏢 Income by Income Type")

fig_income_type = px.box(
    df,
    x="NAME_INCOME_TYPE",
    y="AMT_INCOME_TOTAL",
    title="Income Distribution by Income Type",
    points=False
)

fig_income_type.update_layout(
    xaxis_title="Income Type",
    yaxis_title="Income"
)

st.plotly_chart(
    fig_income_type,
    use_container_width=True
)


# ==================================================
# INCOME VS CREDIT
# ==================================================

st.subheader("💰 Income vs Credit")

fig_income_credit = px.scatter(
    df,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="TARGET",
    opacity=0.5,
    title="Income vs Credit Amount",
    labels={
        "AMT_INCOME_TOTAL": "Income",
        "AMT_CREDIT": "Credit Amount",
        "TARGET": "Default"
    }
)

st.plotly_chart(
    fig_income_credit,
    use_container_width=True
)


# ==================================================
# INCOME GROUP VS DEFAULT RATE
# ==================================================

st.subheader("⚠️ Income Group vs Default Rate")

default_by_income = (
    df.groupby(
        "INCOME_GROUP",
        observed=True
    )["TARGET"]
    .mean()
    .mul(100)
    .reindex([
        "Very Low",
        "Low",
        "Middle",
        "High",
        "Very High"
    ])
    .reset_index()
)

default_by_income.columns = [
    "Income Group",
    "Default Rate"
]

fig_default_income = px.bar(
    default_by_income,
    x="Income Group",
    y="Default Rate",
    text="Default Rate",
    title="Default Rate by Income Group"
)

fig_default_income.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(
    fig_default_income,
    use_container_width=True
)


# ==================================================
# INCOME SEGMENT SUMMARY
# ==================================================

st.subheader("📋 Income Segment Summary")

income_summary = (
    df.groupby(
        "INCOME_GROUP",
        observed=True
    )
    .agg(
        Applications=("SK_ID_CURR", "count"),
        Average_Income=("AMT_INCOME_TOTAL", "mean"),
        Average_Credit=("AMT_CREDIT", "mean"),
        Average_Annuity=("AMT_ANNUITY", "mean"),
        Default_Rate=("TARGET", "mean")
    )
    .reset_index()
)

income_summary["Default_Rate"] = (
    income_summary["Default_Rate"] * 100
)

income_summary["Credit_to_Income"] = (
    income_summary["Average_Credit"]
    / income_summary["Average_Income"]
)

st.dataframe(
    income_summary,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# RECOMMENDATIONS
# ==================================================

st.subheader("💡 Income Analysis Recommendations")

st.markdown(
    """
    **Key areas to evaluate:**

    - 💰 Which income groups receive the highest credit amounts?
    - ⚠️ Which income groups have the highest observed default rate?
    - 💳 Which income groups have the highest credit-to-income burden?
    - 👨‍👩‍👧 Which income groups have lower income per family member?
    - 🏢 Which occupations have the highest average income?
    - 🎓 How does education level relate to income distribution?

    **Important:** A higher observed default rate does not
    automatically mean that income alone causes default.
    Other factors such as age, employment, loan size and
    credit history should also be considered.
    """
)
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Loan Application Analysis",
    page_icon="📋",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📋 Loan Application Analysis")

st.markdown(
    """
    Analyse customer loan applications using
    **application_train.csv**.
    """
)


# =========================================================
# LOAD APPLICATION DATA
# =========================================================

try:

    df = load_data(
        "data/application_train.csv"
    )

except FileNotFoundError:

    st.error(
        "❌ application_train.csv not found in the data folder."
    )

    st.stop()


# =========================================================
# DATASET INFORMATION
# =========================================================

st.success(
    f"✅ Application dataset loaded successfully: "
    f"{len(df):,} rows × {len(df.columns)} columns"
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [
    "SK_ID_CURR",
    "NAME_CONTRACT_TYPE",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "TARGET"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        "❌ Required columns are missing:"
    )

    st.write(missing_columns)

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_applications = len(df)

payment_difficulties = (
    df["TARGET"] == 1
).sum()

no_payment_difficulties = (
    df["TARGET"] == 0
).sum()

default_rate = (
    payment_difficulties
    / total_applications
    * 100
)

total_credit = (
    df["AMT_CREDIT"]
    .sum()
)

average_credit = (
    df["AMT_CREDIT"]
    .mean()
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Loan Application KPIs")


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📋 Total Applications",
        f"{total_applications:,}"
    )

with col2:

    st.metric(
        "✅ No Payment Difficulties",
        f"{no_payment_difficulties:,}"
    )

with col3:

    st.metric(
        "⚠️ Payment Difficulties",
        f"{payment_difficulties:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "📉 Default Rate",
        f"{default_rate:.2f}%"
    )

with col5:

    st.metric(
        "💰 Total Credit",
        f"{total_credit:,.0f}"
    )

with col6:

    st.metric(
        "💳 Average Credit",
        f"{average_credit:,.0f}"
    )


st.divider()


# =========================================================
# CONTRACT TYPE DISTRIBUTION
# =========================================================

st.subheader("💳 Contract Type Distribution")


contract_data = (
    df["NAME_CONTRACT_TYPE"]
    .value_counts()
    .reset_index()
)

contract_data.columns = [
    "CONTRACT_TYPE",
    "COUNT"
]


fig = px.bar(
    contract_data,
    x="CONTRACT_TYPE",
    y="COUNT",
    title="Loan Contract Type Distribution",
    labels={
        "CONTRACT_TYPE": "Contract Type",
        "COUNT": "Applications"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# PAYMENT DIFFICULTIES BY CONTRACT TYPE
# =========================================================

st.subheader(
    "⚠️ Payment Difficulties by Contract Type"
)


contract_risk = (
    df.groupby(
        "NAME_CONTRACT_TYPE"
    )["TARGET"]
    .sum()
    .reset_index()
)

contract_risk.columns = [
    "CONTRACT_TYPE",
    "PAYMENT_DIFFICULTIES"
]


fig = px.bar(
    contract_risk,
    x="CONTRACT_TYPE",
    y="PAYMENT_DIFFICULTIES",
    title="Payment Difficulties by Contract Type",
    labels={
        "CONTRACT_TYPE": "Contract Type",
        "PAYMENT_DIFFICULTIES": "Payment Difficulties"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT AMOUNT DISTRIBUTION
# =========================================================

st.subheader("💰 Credit Amount Distribution")


fig = px.histogram(
    df,
    x="AMT_CREDIT",
    nbins=50,
    title="Loan Credit Amount Distribution",
    labels={
        "AMT_CREDIT": "Credit Amount"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# ANNUITY DISTRIBUTION
# =========================================================

st.subheader("💵 Annuity Distribution")


fig = px.histogram(
    df,
    x="AMT_ANNUITY",
    nbins=50,
    title="Loan Annuity Distribution",
    labels={
        "AMT_ANNUITY": "Annuity Amount"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# INCOME VS CREDIT
# =========================================================

st.subheader("💰 Income vs Credit Amount")


scatter_df = df[
    [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "TARGET"
    ]
].dropna()


# Limit points for faster display

if len(scatter_df) > 100000:

    scatter_df = scatter_df.sample(
        100000,
        random_state=42
    )


scatter_df["RISK_STATUS"] = (
    scatter_df["TARGET"]
    .map({
        0: "No Payment Difficulties",
        1: "Payment Difficulties"
    })
)


fig = px.scatter(
    scatter_df,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="RISK_STATUS",
    title="Income vs Credit Amount",
    labels={
        "AMT_INCOME_TOTAL": "Total Income",
        "AMT_CREDIT": "Credit Amount",
        "RISK_STATUS": "Risk Status"
    },
    opacity=0.6
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# AVERAGE CREDIT BY RISK
# =========================================================

st.subheader("📊 Average Credit by Risk Status")


risk_credit = (
    df.groupby("TARGET")["AMT_CREDIT"]
    .mean()
    .reset_index()
)

risk_credit["RISK_STATUS"] = (
    risk_credit["TARGET"]
    .map({
        0: "No Payment Difficulties",
        1: "Payment Difficulties"
    })
)


fig = px.bar(
    risk_credit,
    x="RISK_STATUS",
    y="AMT_CREDIT",
    title="Average Credit by Risk Status",
    labels={
        "RISK_STATUS": "Risk Status",
        "AMT_CREDIT": "Average Credit"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CUSTOMER-LEVEL FEATURES
# =========================================================

st.divider()

st.subheader(
    "👤 Customer-Level Application Features"
)


customer_features = (
    df.groupby("SK_ID_CURR")
    .agg(
        APPLICATION_COUNT=(
            "SK_ID_CURR",
            "count"
        ),

        TOTAL_CREDIT=(
            "AMT_CREDIT",
            "sum"
        ),

        AVERAGE_CREDIT=(
            "AMT_CREDIT",
            "mean"
        ),

        MAXIMUM_CREDIT=(
            "AMT_CREDIT",
            "max"
        ),

        AVERAGE_ANNUITY=(
            "AMT_ANNUITY",
            "mean"
        ),

        PAYMENT_DIFFICULTIES=(
            "TARGET",
            "sum"
        )
    )
    .reset_index()
)


customer_features["DEFAULT_RATE"] = (
    customer_features["PAYMENT_DIFFICULTIES"]
    /
    customer_features["APPLICATION_COUNT"]
    * 100
)


# =========================================================
# CUSTOMER FEATURE INFORMATION
# =========================================================

st.success(
    f"✅ Customer-level features created for "
    f"{len(customer_features):,} customers."
)


# =========================================================
# CUSTOMER FEATURE TABLE
# =========================================================

st.dataframe(
    customer_features.head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CUSTOMER-LEVEL SUMMARY
# =========================================================

st.subheader(
    "📈 Customer-Level Summary"
)


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👥 Customers",
        f"{len(customer_features):,}"
    )

with col2:

    st.metric(
        "📋 Avg Applications",
        f"{customer_features['APPLICATION_COUNT'].mean():.2f}"
    )

with col3:

    st.metric(
        "💰 Avg Customer Credit",
        f"{customer_features['AVERAGE_CREDIT'].mean():,.0f}"
    )

with col4:

    st.metric(
        "⚠️ Customers with Difficulties",
        f"{(customer_features['PAYMENT_DIFFICULTIES'] > 0).sum():,}"
    )


# =========================================================
# CUSTOMER FEATURE SUMMARY
# =========================================================

st.subheader(
    "📋 Customer Application Summary"
)


summary_columns = [
    "SK_ID_CURR",
    "APPLICATION_COUNT",
    "TOTAL_CREDIT",
    "AVERAGE_CREDIT",
    "MAXIMUM_CREDIT",
    "AVERAGE_ANNUITY",
    "PAYMENT_DIFFICULTIES",
    "DEFAULT_RATE"
]


st.dataframe(
    customer_features[
        summary_columns
    ].head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DATA PREVIEW
# =========================================================

st.divider()

st.subheader("📄 Application Data Preview")

st.dataframe(
    df.head(100),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# INTERPRETATION
# =========================================================

st.divider()

st.subheader(
    "💡 Loan Application Interpretation"
)

st.markdown(
    """
    ### What to investigate

    - **Total Applications** → total loan applications.
    - **Payment Difficulties** → applications where TARGET = 1.
    - **Default Rate** → percentage of applications with
      payment difficulties.
    - **Contract Type** → distribution of loan contract types.
    - **Credit Amount** → loan credit exposure.
    - **Income vs Credit** → relationship between income
      and credit amount.
    - **Customer-Level Features** → aggregated application,
      credit, annuity and risk information for each customer.

    These are descriptive observations and should not
    automatically be interpreted as causal relationships.
    """
)
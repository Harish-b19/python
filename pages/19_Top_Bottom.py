import streamlit as st
import plotly.express as px

from utils.data_loader import load_data

from utils.features import (
    create_risk_segmentation_features
)

from utils.kpi import (
    calculate_risk_segmentation_metrics
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Risk Segmentation",
    page_icon="⚠️",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title(
    "⚠️ Customer Risk Segmentation Using EDA Rules"
)

st.markdown(
    """
    Create descriptive customer segments using
    rule-based EDA indicators.

    **These segments are not predictions and are not
    generated using a machine-learning model.**
    """
)


# =========================================================
# LOAD APPLICATION DATA
# =========================================================

try:

    application_df = load_data(
        "data/application_train.csv"
    )

except FileNotFoundError:

    st.error(
        "❌ application_train.csv not found "
        "in the data folder."
    )

    st.stop()


# =========================================================
# LOAD BUREAU DATA
# =========================================================

try:

    bureau_df = load_data(
        "data/bureau.csv"
    )

except FileNotFoundError:

    st.error(
        "❌ bureau.csv not found in the data folder."
    )

    st.stop()


# =========================================================
# DATASET INFORMATION
# =========================================================

st.success(
    f"✅ Application data: "
    f"{len(application_df):,} rows"
)

st.success(
    f"✅ Bureau data: "
    f"{len(bureau_df):,} rows"
)


# =========================================================
# CREATE RISK FEATURES
# =========================================================

with st.spinner(
    "Creating rule-based customer risk segments..."
):

    try:

        df = create_risk_segmentation_features(
            application_df,
            bureau_df
        )

    except Exception as e:

        st.error(
            f"❌ Error creating risk segments: {e}"
        )

        st.stop()


# =========================================================
# CALCULATE KPIs
# =========================================================

try:

    metrics = (
        calculate_risk_segmentation_metrics(df)
    )

except Exception as e:

    st.error(
        f"❌ Error calculating risk KPIs: {e}"
    )

    st.stop()


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Risk Segmentation KPIs")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🟢 Low-Risk Customers",
        f"{metrics['low_risk_customers']:,}"
    )


with col2:

    st.metric(
        "🟡 Moderate-Risk Customers",
        f"{metrics['moderate_risk_customers']:,}"
    )


with col3:

    st.metric(
        "🟠 Elevated-Risk Customers",
        f"{metrics['elevated_risk_customers']:,}"
    )


with col4:

    st.metric(
        "🔴 High-Risk Customers",
        f"{metrics['high_risk_customers']:,}"
    )


st.metric(
    "💰 Credit Exposure in High-Risk Segment",
    f"{metrics['high_risk_exposure']:,.0f}"
)


st.divider()


# =========================================================
# CUSTOMER COUNT BY RISK SEGMENT
# =========================================================

st.subheader(
    "👥 Customer Count by Risk Segment"
)


segment_count = (
    df["OBSERVED_RISK_SEGMENT"]
    .value_counts()
    .reindex(
        [
            "Low Observed Risk",
            "Moderate Observed Risk",
            "Elevated Observed Risk",
            "High Observed Risk"
        ],
        fill_value=0
    )
    .reset_index()
)

segment_count.columns = [
    "RISK_SEGMENT",
    "CUSTOMER_COUNT"
]


fig = px.bar(
    segment_count,
    x="RISK_SEGMENT",
    y="CUSTOMER_COUNT",
    title="Customer Count by Risk Segment",
    labels={
        "RISK_SEGMENT": "Risk Segment",
        "CUSTOMER_COUNT": "Customers"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# PORTFOLIO EXPOSURE BY SEGMENT
# =========================================================

st.subheader(
    "💰 Portfolio Exposure by Segment"
)


exposure_data = (
    df.groupby(
        "OBSERVED_RISK_SEGMENT"
    )["AMT_CREDIT"]
    .sum()
    .reindex(
        [
            "Low Observed Risk",
            "Moderate Observed Risk",
            "Elevated Observed Risk",
            "High Observed Risk"
        ]
    )
    .reset_index()
)


fig = px.pie(
    exposure_data,
    names="OBSERVED_RISK_SEGMENT",
    values="AMT_CREDIT",
    hole=0.45,
    title="Portfolio Credit Exposure by Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# AVERAGE INCOME BY SEGMENT
# =========================================================

st.subheader(
    "💰 Average Income by Segment"
)


income_data = (
    df.groupby(
        "OBSERVED_RISK_SEGMENT"
    )["AMT_INCOME_TOTAL"]
    .mean()
    .reindex(
        [
            "Low Observed Risk",
            "Moderate Observed Risk",
            "Elevated Observed Risk",
            "High Observed Risk"
        ]
    )
    .reset_index()
)


fig = px.bar(
    income_data,
    x="OBSERVED_RISK_SEGMENT",
    y="AMT_INCOME_TOTAL",
    title="Average Income by Risk Segment",
    labels={
        "OBSERVED_RISK_SEGMENT":
            "Risk Segment",
        "AMT_INCOME_TOTAL":
            "Average Income"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# AVERAGE CREDIT BY SEGMENT
# =========================================================

st.subheader(
    "💳 Average Credit by Segment"
)


credit_data = (
    df.groupby(
        "OBSERVED_RISK_SEGMENT"
    )["AMT_CREDIT"]
    .mean()
    .reindex(
        [
            "Low Observed Risk",
            "Moderate Observed Risk",
            "Elevated Observed Risk",
            "High Observed Risk"
        ]
    )
    .reset_index()
)


fig = px.bar(
    credit_data,
    x="OBSERVED_RISK_SEGMENT",
    y="AMT_CREDIT",
    title="Average Credit by Risk Segment",
    labels={
        "OBSERVED_RISK_SEGMENT":
            "Risk Segment",
        "AMT_CREDIT":
            "Average Credit"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT-TO-INCOME BY SEGMENT
# =========================================================

st.subheader(
    "📊 Credit-to-Income by Segment"
)


fig = px.box(
    df,
    x="OBSERVED_RISK_SEGMENT",
    y="CREDIT_TO_INCOME",
    category_orders={
        "OBSERVED_RISK_SEGMENT": [
            "Low Observed Risk",
            "Moderate Observed Risk",
            "Elevated Observed Risk",
            "High Observed Risk"
        ]
    },
    title="Credit-to-Income Ratio by Risk Segment",
    labels={
        "OBSERVED_RISK_SEGMENT":
            "Risk Segment",
        "CREDIT_TO_INCOME":
            "Credit-to-Income Ratio"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# BUREAU DEBT BY SEGMENT
# =========================================================

st.subheader(
    "🏦 Bureau Debt by Segment"
)


bureau_debt_data = (
    df.groupby(
        "OBSERVED_RISK_SEGMENT"
    )["TOTAL_BUREAU_DEBT"]
    .mean()
    .reindex(
        [
            "Low Observed Risk",
            "Moderate Observed Risk",
            "Elevated Observed Risk",
            "High Observed Risk"
        ]
    )
    .reset_index()
)


fig = px.bar(
    bureau_debt_data,
    x="OBSERVED_RISK_SEGMENT",
    y="TOTAL_BUREAU_DEBT",
    title="Average Bureau Debt by Risk Segment",
    labels={
        "OBSERVED_RISK_SEGMENT":
            "Risk Segment",
        "TOTAL_BUREAU_DEBT":
            "Average Bureau Debt"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# OBSERVED RISK RULES
# =========================================================

st.divider()

st.subheader(
    "📋 EDA Risk Segmentation Rules"
)


st.markdown(
    """
    ### Rule Documentation

    Each customer receives one point for every observed
    condition below:

    **1. High Credit Burden**

    Credit-to-Income Ratio >= **5**

    **2. High Annuity Burden**

    Annuity-to-Income Ratio >= **40%**

    **3. High Bureau Debt**

    Total Bureau Debt >= **2 × Annual Income**

    **4. Bureau Overdue**

    Total Bureau Overdue Amount > **0**

    **5. Short Employment**

    Employment duration < **2 years**

    ### Segment Classification

    | Score | Descriptive Segment |
    |---:|---|
    | 0 | Low Observed Risk |
    | 1 | Moderate Observed Risk |
    | 2–3 | Elevated Observed Risk |
    | 4–5 | High Observed Risk |

    **Important:** These segments are descriptive EDA
    groupings. They are not credit-risk predictions,
    probabilities, or machine-learning classifications.
    """
)


# =========================================================
# SEGMENT DATA
# =========================================================

st.subheader(
    "📋 Customer Risk Segment Data"
)


display_columns = [
    "SK_ID_CURR",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "EMPLOYMENT_YEARS",
    "TOTAL_BUREAU_DEBT",
    "TOTAL_BUREAU_OVERDUE",
    "CREDIT_TO_INCOME",
    "ANNUITY_TO_INCOME",
    "OBSERVED_RISK_SCORE",
    "OBSERVED_RISK_SEGMENT"
]


available_columns = [
    col
    for col in display_columns
    if col in df.columns
]


st.dataframe(
    df[available_columns].head(1000),
    use_container_width=True,
    hide_index=True
)
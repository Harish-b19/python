import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.features import create_risk_segmentation_features
from utils.kpi import calculate_risk_segmentation_metrics


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Risk Segmentation",
    page_icon="⚠️",
    layout="wide"
)


# =========================================================
# PAGE TITLE
# =========================================================

st.title("⚠️ Customer Risk Segmentation")

st.markdown(
    """
    Create descriptive customer segments using
    **EDA-driven business rules**.

    > These are **Observed Risk Segments**, not predictions.
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
        "❌ application_train.csv not found in data folder."
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
        "❌ bureau.csv not found in data folder."
    )

    st.stop()


# =========================================================
# DATA LOADED
# =========================================================

st.success(
    f"✅ Application dataset: "
    f"{len(application_df):,} rows"
)

st.success(
    f"✅ Bureau dataset: "
    f"{len(bureau_df):,} rows"
)


# =========================================================
# CREATE FEATURES
# =========================================================

with st.spinner(
    "Creating customer risk segments..."
):

    try:

        df = create_risk_segmentation_features(
            application_df,
            bureau_df
        )

    except Exception as e:

        st.error(
            f"❌ Feature creation error: {e}"
        )

        st.stop()


# =========================================================
# CALCULATE KPIs
# =========================================================

try:

    metrics = calculate_risk_segmentation_metrics(
        df
    )

except Exception as e:

    st.error(
        f"❌ KPI calculation error: {e}"
    )

    st.stop()


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Executive Risk KPIs")


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
# FILTER
# =========================================================

st.sidebar.header("🔎 Filters")

segments = [
    "All",
    "Low Observed Risk",
    "Moderate Observed Risk",
    "Elevated Observed Risk",
    "High Observed Risk"
]

selected_segment = st.sidebar.selectbox(
    "Risk Segment",
    segments
)


if selected_segment != "All":

    filtered_df = df[
        df["OBSERVED_RISK_SEGMENT"]
        == selected_segment
    ].copy()

else:

    filtered_df = df.copy()


st.sidebar.write(
    f"Customers: {len(filtered_df):,}"
)


# =========================================================
# CUSTOMER COUNT BY RISK SEGMENT
# =========================================================

st.subheader(
    "👥 Customer Count by Risk Segment"
)


segment_order = [
    "Low Observed Risk",
    "Moderate Observed Risk",
    "Elevated Observed Risk",
    "High Observed Risk"
]


segment_count = (
    filtered_df[
        "OBSERVED_RISK_SEGMENT"
    ]
    .value_counts()
    .reindex(
        segment_order,
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
    title="Customer Count by Risk Segment"
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


exposure = (
    filtered_df
    .groupby(
        "OBSERVED_RISK_SEGMENT"
    )["AMT_CREDIT"]
    .sum()
    .reindex(
        segment_order,
        fill_value=0
    )
    .reset_index()
)


fig = px.pie(
    exposure,
    names="OBSERVED_RISK_SEGMENT",
    values="AMT_CREDIT",
    hole=0.45,
    title="Credit Exposure by Risk Segment"
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


income = (
    filtered_df
    .groupby(
        "OBSERVED_RISK_SEGMENT"
    )["AMT_INCOME_TOTAL"]
    .mean()
    .reindex(
        segment_order
    )
    .reset_index()
)


fig = px.bar(
    income,
    x="OBSERVED_RISK_SEGMENT",
    y="AMT_INCOME_TOTAL",
    title="Average Income by Risk Segment"
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


credit = (
    filtered_df
    .groupby(
        "OBSERVED_RISK_SEGMENT"
    )["AMT_CREDIT"]
    .mean()
    .reindex(
        segment_order
    )
    .reset_index()
)


fig = px.bar(
    credit,
    x="OBSERVED_RISK_SEGMENT",
    y="AMT_CREDIT",
    title="Average Credit by Risk Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT-TO-INCOME BOX PLOT
# =========================================================

st.subheader(
    "📊 Credit-to-Income by Segment"
)


fig = px.box(
    filtered_df,
    x="OBSERVED_RISK_SEGMENT",
    y="CREDIT_TO_INCOME",
    category_orders={
        "OBSERVED_RISK_SEGMENT":
            segment_order
    },
    title="Credit-to-Income Ratio by Segment"
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


bureau_debt = (
    filtered_df
    .groupby(
        "OBSERVED_RISK_SEGMENT"
    )["TOTAL_BUREAU_DEBT"]
    .mean()
    .reindex(
        segment_order
    )
    .reset_index()
)


fig = px.bar(
    bureau_debt,
    x="OBSERVED_RISK_SEGMENT",
    y="TOTAL_BUREAU_DEBT",
    title="Average Bureau Debt by Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# HIGH-BURDEN CUSTOMERS
# =========================================================

st.subheader(
    "⚠️ High-Burden Customers"
)


burden_count = (
    filtered_df[
        "HIGH_CREDIT_BURDEN"
    ]
    .sum()
)


st.metric(
    "Customers with High Credit Burden",
    f"{burden_count:,}"
)


# =========================================================
# RISK SCORE DISTRIBUTION
# =========================================================

st.subheader(
    "📊 Observed Risk Score Distribution"
)


score_data = (
    filtered_df[
        "OBSERVED_RISK_SCORE"
    ]
    .value_counts()
    .sort_index()
    .reset_index()
)


score_data.columns = [
    "RISK_SCORE",
    "CUSTOMER_COUNT"
]


fig = px.bar(
    score_data,
    x="RISK_SCORE",
    y="CUSTOMER_COUNT",
    title="Observed Risk Score Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# RULE DOCUMENTATION
# =========================================================

st.divider()

st.subheader(
    "📋 EDA Risk Segmentation Rules"
)

st.markdown(
    """
    Each customer receives **1 point** for every condition
    that is observed:

    **1. High Credit Burden**

    `Credit-to-Income >= 5`

    **2. High Annuity Burden**

    `Annuity-to-Income >= 40%`

    **3. High Bureau Debt**

    `Total Bureau Debt >= 2 × Annual Income`

    **4. Bureau Overdue**

    `Total Bureau Overdue > 0`

    **5. Short Employment**

    `Employment < 2 years`

    ### Segment Mapping

    | Score | Segment |
    |---:|---|
    | 0 | Low Observed Risk |
    | 1 | Moderate Observed Risk |
    | 2–3 | Elevated Observed Risk |
    | 4–5 | High Observed Risk |

    **Important:** These segments describe observed characteristics
    in the dataset. They are **not default predictions**.
    """
)


# =========================================================
# CUSTOMER TABLE
# =========================================================

st.divider()

st.subheader(
    "👤 Customer Risk Details"
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
    if col in filtered_df.columns
]


st.dataframe(
    filtered_df[
        available_columns
    ].head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DOWNLOAD
# =========================================================

csv_data = filtered_df[
    available_columns
].to_csv(
    index=False
)


st.download_button(
    label="⬇️ Download Risk Segment Data",
    data=csv_data,
    file_name="customer_risk_segments.csv",
    mime="text/csv"
)
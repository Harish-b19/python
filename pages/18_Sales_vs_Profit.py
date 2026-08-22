import streamlit as st
import plotly.express as px

from utils.data_loader import load_data


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bureau Balance Analysis",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📊 Bureau Balance Analysis")

st.markdown(
    """
    Analyse historical monthly bureau account status
    using **bureau_balance.csv**.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data(
        "data/bureau_balance.csv"
    )

except FileNotFoundError:

    st.error(
        "❌ bureau_balance.csv not found in the data folder."
    )

    st.stop()


# =========================================================
# DATASET INFORMATION
# =========================================================

st.success(
    f"✅ Bureau balance dataset loaded successfully: "
    f"{len(df):,} rows × {len(df.columns)} columns"
)


# =========================================================
# REQUIRED COLUMNS
# =========================================================

required_columns = [
    "SK_ID_BUREAU",
    "MONTHS_BALANCE",
    "STATUS"
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
# STATUS CLEANING
# =========================================================

df["STATUS"] = df["STATUS"].astype(str)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_records = len(df)

unique_bureau_accounts = (
    df["SK_ID_BUREAU"]
    .nunique()
)

most_common_status = (
    df["STATUS"]
    .mode()
    .iloc[0]
)

delinquency_records = (
    df["STATUS"]
    .isin(["1", "2", "3", "4", "5"])
    .sum()
)

closed_records = (
    df["STATUS"]
    .eq("C")
    .sum()
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Bureau Balance KPIs")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📋 Monthly Records",
        f"{total_records:,}"
    )


with col2:

    st.metric(
        "🏦 Bureau Accounts",
        f"{unique_bureau_accounts:,}"
    )


with col3:

    st.metric(
        "📊 Most Common Status",
        most_common_status
    )


col4, col5 = st.columns(2)


with col4:

    st.metric(
        "⚠️ Delinquency Records",
        f"{delinquency_records:,}"
    )


with col5:

    st.metric(
        "🔴 Closed Records",
        f"{closed_records:,}"
    )


st.divider()


# =========================================================
# STATUS DISTRIBUTION
# =========================================================

st.subheader("📊 Status Distribution")


status_data = (
    df["STATUS"]
    .value_counts()
    .reset_index()
)

status_data.columns = [
    "STATUS",
    "COUNT"
]


fig = px.bar(
    status_data,
    x="STATUS",
    y="COUNT",
    title="Bureau Account Status Distribution"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# STATUS PERCENTAGE
# =========================================================

st.subheader("🍩 Status Percentage")


fig = px.pie(
    status_data,
    names="STATUS",
    values="COUNT",
    hole=0.45,
    title="Bureau Status Percentage"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# ACCOUNT STATUS BY MONTH
# =========================================================

st.subheader("📅 Account Status by Month")


monthly_status = (
    df.groupby(
        [
            "MONTHS_BALANCE",
            "STATUS"
        ]
    )
    .size()
    .reset_index(
        name="COUNT"
    )
)


monthly_status = monthly_status.sort_values(
    "MONTHS_BALANCE"
)


fig = px.bar(
    monthly_status,
    x="MONTHS_BALANCE",
    y="COUNT",
    color="STATUS",
    title="Account Status by Month"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# MONTHLY DELINQUENCY TREND
# =========================================================

st.subheader(
    "⚠️ Monthly Delinquency Trend"
)


df["DELINQUENCY_FLAG"] = (
    df["STATUS"]
    .isin(["1", "2", "3", "4", "5"])
    .astype(int)
)


monthly_delinquency = (
    df.groupby(
        "MONTHS_BALANCE"
    )["DELINQUENCY_FLAG"]
    .sum()
    .reset_index()
)


monthly_delinquency.columns = [
    "MONTHS_BALANCE",
    "DELINQUENCY_COUNT"
]


monthly_delinquency = (
    monthly_delinquency
    .sort_values("MONTHS_BALANCE")
)


fig = px.line(
    monthly_delinquency,
    x="MONTHS_BALANCE",
    y="DELINQUENCY_COUNT",
    markers=True,
    title="Monthly Delinquency Trend"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# STATUS HEATMAP
# =========================================================

st.subheader("🔥 Status Heatmap")


heatmap_data = (
    df.groupby(
        [
            "STATUS",
            "MONTHS_BALANCE"
        ]
    )
    .size()
    .reset_index(
        name="COUNT"
    )
)


heatmap_data = heatmap_data.pivot(
    index="STATUS",
    columns="MONTHS_BALANCE",
    values="COUNT"
).fillna(0)


fig = px.imshow(
    heatmap_data,
    aspect="auto",
    title="Bureau Status Heatmap",
    labels={
        "x": "Months Balance",
        "y": "Status",
        "color": "Records"
    }
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# ACCOUNT-LEVEL FEATURES
# =========================================================

st.divider()

st.subheader(
    "🏦 Bureau Account-Level Features"
)


account_features = (
    df.groupby(
        "SK_ID_BUREAU",
        sort=False
    )
    .agg(
        MONTHS_REPORTED=(
            "MONTHS_BALANCE",
            "count"
        ),

        MONTHS_WITH_DELINQUENCY=(
            "DELINQUENCY_FLAG",
            "sum"
        ),

        CLOSED_MONTH_COUNT=(
            "STATUS",
            lambda x: (
                x == "C"
            ).sum()
        ),

        ACTIVE_MONTH_COUNT=(
            "STATUS",
            lambda x: (
                x == "0"
            ).sum()
        )
    )
    .reset_index()
)


# =========================================================
# FEATURE TABLE
# =========================================================

st.success(
    f"✅ Account-level features created for "
    f"{len(account_features):,} bureau accounts."
)


st.dataframe(
    account_features.head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DATA PREVIEW
# =========================================================

st.divider()

st.subheader("📋 Bureau Balance Data Preview")


st.dataframe(
    df.head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# INTERPRETATION
# =========================================================

st.divider()

st.subheader(
    "💡 Bureau Balance Interpretation"
)


st.markdown(
    """
    ### What to investigate

    - **Status 0** represents an active account status.

    - **Statuses 1–5** indicate progressively higher
      delinquency levels.

    - **Status C** represents a closed account.

    - **Months with Delinquency** shows how frequently
      delinquency was observed for a bureau account.

    - **Closed Month Count** shows the number of monthly
      records marked as closed.

    - **Active Month Count** shows the number of monthly
      records with status 0.

    These are descriptive observations based on the
    bureau balance history.
    """
)
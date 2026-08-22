import streamlit as st
import pandas as pd
import plotly.express as px


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
    Analyse historical monthly bureau account status using
    **bureau_balance.csv**.
    """
)


# =========================================================
# LOAD BUREAU BALANCE
# =========================================================

@st.cache_data
def load_bureau_balance():

    return pd.read_csv(
        "data/bureau_balance.csv"
    )


try:

    df = load_bureau_balance()

except FileNotFoundError:

    st.error(
        "❌ bureau_balance.csv not found in data folder."
    )
    st.stop()

except Exception as e:

    st.error(
        f"❌ Error loading bureau_balance.csv: {e}"
    )
    st.stop()


st.success(
    f"✅ Bureau Balance dataset loaded: "
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
        f"❌ Missing columns: {missing_columns}"
    )

    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

df["MONTHS_BALANCE"] = pd.to_numeric(
    df["MONTHS_BALANCE"],
    errors="coerce"
)

df["STATUS"] = df["STATUS"].astype(str)


# =========================================================
# STATUS DEFINITIONS
# =========================================================

# 1–5 = delinquency
delinquency_statuses = [
    "1",
    "2",
    "3",
    "4",
    "5"
]

# 0–5 = active/reported monthly status
active_statuses = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5"
]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_monthly_records = len(df)

unique_bureau_accounts = (
    df["SK_ID_BUREAU"].nunique()
)

most_common_status = (
    df["STATUS"]
    .mode()
    .iloc[0]
)

delinquency_records = (
    df["STATUS"]
    .isin(delinquency_statuses)
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
        "📋 Total Bureau Monthly Records",
        f"{total_monthly_records:,}"
    )

with col2:

    st.metric(
        "🏦 Unique Bureau Accounts",
        f"{unique_bureau_accounts:,}"
    )

with col3:

    st.metric(
        "📌 Most Common Status",
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

status_distribution = (
    df["STATUS"]
    .value_counts()
    .reset_index()
)

status_distribution.columns = [
    "STATUS",
    "COUNT"
]

fig = px.bar(
    status_distribution,
    x="STATUS",
    y="COUNT",
    title="Bureau Balance Status Distribution",
    labels={
        "STATUS": "Status",
        "COUNT": "Number of Records"
    }
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
    status_distribution,
    names="STATUS",
    values="COUNT",
    hole=0.45,
    title="Bureau Balance Status Percentage"
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
    title="Account Status by Month",
    labels={
        "MONTHS_BALANCE": "Months Balance",
        "COUNT": "Number of Records",
        "STATUS": "Status"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# MONTHLY DELINQUENCY TREND
# =========================================================

st.subheader("⚠️ Monthly Delinquency Trend")

monthly_delinquency = (
    df[
        df["STATUS"].isin(
            delinquency_statuses
        )
    ]
    .groupby(
        "MONTHS_BALANCE"
    )
    .size()
    .reset_index(
        name="DELINQUENCY_RECORDS"
    )
)

monthly_delinquency = (
    monthly_delinquency
    .sort_values(
        "MONTHS_BALANCE"
    )
)

fig = px.line(
    monthly_delinquency,
    x="MONTHS_BALANCE",
    y="DELINQUENCY_RECORDS",
    markers=True,
    title="Monthly Delinquency Trend",
    labels={
        "MONTHS_BALANCE": "Months Balance",
        "DELINQUENCY_RECORDS": "Delinquency Records"
    }
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

heatmap_pivot = (
    heatmap_data
    .pivot(
        index="STATUS",
        columns="MONTHS_BALANCE",
        values="COUNT"
    )
    .fillna(0)
)

fig = px.imshow(
    heatmap_pivot,
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
# CUSTOMER-LEVEL FEATURE ENGINEERING
# =========================================================

st.divider()

st.subheader(
    "👤 Customer-Level Bureau Balance Features"
)

st.info(
    "Creating account-level monthly features..."
)


# =========================================================
# CREATE FLAGS
# =========================================================

df["DELINQUENCY_FLAG"] = (
    df["STATUS"]
    .isin(delinquency_statuses)
    .astype("int8")
)

df["CLOSED_FLAG"] = (
    df["STATUS"]
    .eq("C")
    .astype("int8")
)

df["ACTIVE_FLAG"] = (
    df["STATUS"]
    .isin(active_statuses)
    .astype("int8")
)

df["DELINQUENCY_LEVEL"] = pd.to_numeric(
    df["STATUS"],
    errors="coerce"
)


# =========================================================
# ACCOUNT-LEVEL AGGREGATION
# =========================================================

account_features = (
    df.groupby(
        "SK_ID_BUREAU",
        sort=False
    )
    .agg(
        MONTHS_WITH_DELINQUENCY=(
            "DELINQUENCY_FLAG",
            "sum"
        ),

        MAX_DELINQUENCY_LEVEL=(
            "DELINQUENCY_LEVEL",
            "max"
        ),

        CLOSED_MONTHS=(
            "CLOSED_FLAG",
            "sum"
        ),

        ACTIVE_MONTHS=(
            "ACTIVE_FLAG",
            "sum"
        )
    )
    .reset_index()
)


st.success(
    f"✅ Account-level features created for "
    f"{len(account_features):,} bureau accounts."
)


# =========================================================
# LOAD CUSTOMER MAPPING
# =========================================================

st.info(
    "Mapping bureau accounts to customers using bureau.csv..."
)


@st.cache_data
def load_bureau_mapping():

    return pd.read_csv(
        "data/bureau.csv",
        usecols=[
            "SK_ID_CURR",
            "SK_ID_BUREAU"
        ]
    )


try:

    bureau_mapping = load_bureau_mapping()

except FileNotFoundError:

    st.error(
        "❌ bureau.csv not found."
    )
    st.stop()

except Exception as e:

    st.error(
        f"❌ Error loading bureau.csv: {e}"
    )
    st.stop()


# =========================================================
# MAP ACCOUNT → CUSTOMER
# =========================================================

account_customer = account_features.merge(
    bureau_mapping,
    on="SK_ID_BUREAU",
    how="left"
)


# =========================================================
# CUSTOMER-LEVEL AGGREGATION
# =========================================================

customer_features = (
    account_customer
    .dropna(
        subset=["SK_ID_CURR"]
    )
    .groupby(
        "SK_ID_CURR",
        sort=False
    )
    .agg(
        MONTHS_WITH_DELINQUENCY=(
            "MONTHS_WITH_DELINQUENCY",
            "sum"
        ),

        MAX_DELINQUENCY_LEVEL=(
            "MAX_DELINQUENCY_LEVEL",
            "max"
        ),

        CLOSED_MONTHS=(
            "CLOSED_MONTHS",
            "sum"
        ),

        ACTIVE_MONTHS=(
            "ACTIVE_MONTHS",
            "sum"
        )
    )
    .reset_index()
)


# =========================================================
# CUSTOMER FEATURE RESULT
# =========================================================

st.success(
    f"✅ Customer-level features created for "
    f"{len(customer_features):,} customers."
)


# =========================================================
# CUSTOMER TABLE
# =========================================================

st.subheader(
    "📋 Customer Bureau Balance Summary"
)

st.dataframe(
    customer_features.head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CUSTOMER FEATURE KPIs
# =========================================================

st.subheader(
    "📈 Customer Feature Summary"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Customers",
        f"{len(customer_features):,}"
    )

with col2:

    st.metric(
        "Avg Delinquency Months",
        f"{customer_features['MONTHS_WITH_DELINQUENCY'].mean():.2f}"
    )

with col3:

    max_delinquency = (
        customer_features[
            "MAX_DELINQUENCY_LEVEL"
        ].max()
    )

    st.metric(
        "Max Delinquency Level",
        (
            f"{max_delinquency:.0f}"
            if pd.notna(max_delinquency)
            else "N/A"
        )
    )

with col4:

    st.metric(
        "Max Closed Months",
        f"{customer_features['CLOSED_MONTHS'].max():,.0f}"
    )


# =========================================================
# DELINQUENCY DISTRIBUTION
# =========================================================

st.subheader(
    "⚠️ Months with Delinquency"
)

fig = px.histogram(
    customer_features,
    x="MONTHS_WITH_DELINQUENCY",
    nbins=30,
    title="Customer Months with Delinquency",
    labels={
        "MONTHS_WITH_DELINQUENCY":
            "Months with Delinquency"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
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
    ### Customer-Level Features

    - **Months with Delinquency** → number of monthly bureau
      records with status 1–5.

    - **Maximum Delinquency Level** → highest observed
      delinquency level for the customer.

    - **Number of Closed Months** → number of monthly records
      with status C.

    - **Number of Active Months** → number of monthly records
      with status 0–5.

    ### Important

    These are descriptive historical observations.
    They should not automatically be interpreted as
    causal relationships.
    """
)
import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bureau Credit History Analysis",
    page_icon="📜",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📜 Bureau Credit History Analysis")

st.markdown(
    """
    Analyse loans previously reported by other financial
    institutions using the **bureau.csv** dataset.
    """
)


# =========================================================
# LOAD BUREAU DATA
# =========================================================

try:

    df = pd.read_csv(
        "data/bureau.csv"
    )

except FileNotFoundError:

    st.error(
        "❌ bureau.csv not found in the data folder."
    )

    st.stop()


st.success(
    f"✅ Bureau dataset loaded successfully: "
    f"{len(df):,} rows × {len(df.columns)} columns"
)


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "SK_ID_CURR",
    "SK_ID_BUREAU",
    "CREDIT_ACTIVE",
    "CREDIT_CURRENCY",
    "CREDIT_TYPE",
    "AMT_CREDIT_SUM",
    "AMT_CREDIT_SUM_DEBT",
    "AMT_CREDIT_SUM_OVERDUE",
    "DAYS_CREDIT",
    "DAYS_CREDIT_ENDDATE"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"❌ Missing columns: {missing_columns}"
    )

    st.stop()


# =========================================================
# KPI CALCULATIONS
# =========================================================

bureau_accounts = len(df)

customers_with_bureau_history = (
    df["SK_ID_CURR"]
    .nunique()
)

active_credits = (
    df["CREDIT_ACTIVE"]
    .eq("Active")
    .sum()
)

closed_credits = (
    df["CREDIT_ACTIVE"]
    .eq("Closed")
    .sum()
)

total_bureau_debt = (
    df["AMT_CREDIT_SUM_DEBT"]
    .sum()
)

total_overdue_amount = (
    df["AMT_CREDIT_SUM_OVERDUE"]
    .sum()
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Bureau Credit KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📋 Bureau Accounts",
        f"{bureau_accounts:,}"
    )

with col2:
    st.metric(
        "👥 Customers with Bureau History",
        f"{customers_with_bureau_history:,}"
    )

with col3:
    st.metric(
        "🟢 Active Credits",
        f"{active_credits:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "⚪ Closed Credits",
        f"{closed_credits:,}"
    )

with col5:
    st.metric(
        "💰 Total Bureau Debt",
        f"{total_bureau_debt:,.0f}"
    )

with col6:
    st.metric(
        "⚠️ Total Overdue Amount",
        f"{total_overdue_amount:,.0f}"
    )


st.divider()


# =========================================================
# ACTIVE VS CLOSED LOANS
# =========================================================

st.subheader("🟢 Active vs Closed Loans")

active_closed = (
    df["CREDIT_ACTIVE"]
    .value_counts()
    .reset_index()
)

active_closed.columns = [
    "CREDIT_ACTIVE",
    "COUNT"
]

fig = px.bar(
    active_closed,
    x="CREDIT_ACTIVE",
    y="COUNT",
    title="Active vs Closed Bureau Loans",
    labels={
        "CREDIT_ACTIVE": "Credit Status",
        "COUNT": "Number of Accounts"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT TYPE DISTRIBUTION
# =========================================================

st.subheader("📊 Credit Type Distribution")

credit_type = (
    df["CREDIT_TYPE"]
    .value_counts()
    .reset_index()
)

credit_type.columns = [
    "CREDIT_TYPE",
    "COUNT"
]

credit_type = credit_type.sort_values(
    "COUNT",
    ascending=True
)

fig = px.bar(
    credit_type,
    x="COUNT",
    y="CREDIT_TYPE",
    orientation="h",
    title="Bureau Credit Type Distribution",
    labels={
        "CREDIT_TYPE": "Credit Type",
        "COUNT": "Number of Accounts"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# BUREAU CREDIT AMOUNT DISTRIBUTION
# =========================================================

st.subheader("💰 Bureau Credit Amount Distribution")

credit_amount = df[
    "AMT_CREDIT_SUM"
].dropna()

fig = px.histogram(
    credit_amount,
    x="AMT_CREDIT_SUM",
    nbins=50,
    title="Bureau Credit Amount Distribution",
    labels={
        "AMT_CREDIT_SUM": "Credit Amount"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# BUREAU DEBT DISTRIBUTION
# =========================================================

st.subheader("💳 Bureau Debt Distribution")

debt_amount = df[
    "AMT_CREDIT_SUM_DEBT"
].dropna()

fig = px.histogram(
    debt_amount,
    x="AMT_CREDIT_SUM_DEBT",
    nbins=50,
    title="Bureau Debt Distribution",
    labels={
        "AMT_CREDIT_SUM_DEBT": "Bureau Debt"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# OVERDUE AMOUNT DISTRIBUTION
# =========================================================

st.subheader("⚠️ Overdue Amount Distribution")

overdue_amount = df[
    "AMT_CREDIT_SUM_OVERDUE"
].dropna()

fig = px.histogram(
    overdue_amount,
    x="AMT_CREDIT_SUM_OVERDUE",
    nbins=50,
    title="Overdue Amount Distribution",
    labels={
        "AMT_CREDIT_SUM_OVERDUE": "Overdue Amount"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT TYPE VS TOTAL DEBT
# =========================================================

st.subheader("💳 Credit Type vs Total Debt")

credit_type_debt = (
    df.groupby(
        "CREDIT_TYPE",
        dropna=False
    )["AMT_CREDIT_SUM_DEBT"]
    .sum()
    .reset_index()
)

credit_type_debt = credit_type_debt.sort_values(
    "AMT_CREDIT_SUM_DEBT",
    ascending=False
)

fig = px.bar(
    credit_type_debt,
    x="CREDIT_TYPE",
    y="AMT_CREDIT_SUM_DEBT",
    title="Total Bureau Debt by Credit Type",
    labels={
        "CREDIT_TYPE": "Credit Type",
        "AMT_CREDIT_SUM_DEBT": "Total Bureau Debt"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CUSTOMER-LEVEL BUREAU FEATURES
# =========================================================

st.divider()

st.subheader("👤 Customer-Level Bureau Features")

st.info(
    "Creating customer-level aggregates from the bureau history..."
)


# ---------------------------------------------------------
# Create helper columns
# ---------------------------------------------------------

df["ACTIVE_FLAG"] = (
    df["CREDIT_ACTIVE"]
    .eq("Active")
    .astype("int8")
)

df["CLOSED_FLAG"] = (
    df["CREDIT_ACTIVE"]
    .eq("Closed")
    .astype("int8")
)


# ---------------------------------------------------------
# Customer-level aggregation
# ---------------------------------------------------------

customer_features = (
    df.groupby(
        "SK_ID_CURR",
        sort=False
    )
    .agg(
        BUREAU_ACCOUNT_COUNT=(
            "SK_ID_BUREAU",
            "count"
        ),

        ACTIVE_ACCOUNT_COUNT=(
            "ACTIVE_FLAG",
            "sum"
        ),

        CLOSED_ACCOUNT_COUNT=(
            "CLOSED_FLAG",
            "sum"
        ),

        TOTAL_BUREAU_CREDIT=(
            "AMT_CREDIT_SUM",
            "sum"
        ),

        TOTAL_BUREAU_DEBT=(
            "AMT_CREDIT_SUM_DEBT",
            "sum"
        ),

        AVERAGE_BUREAU_CREDIT=(
            "AMT_CREDIT_SUM",
            "mean"
        ),

        MAX_OVERDUE_AMOUNT=(
            "AMT_CREDIT_SUM_OVERDUE",
            "max"
        )
    )
    .reset_index()
)


# ---------------------------------------------------------
# Success message
# ---------------------------------------------------------

st.success(
    f"✅ Customer-level features created for "
    f"{len(customer_features):,} customers."
)


# =========================================================
# CUSTOMER-LEVEL SUMMARY
# =========================================================

st.subheader("📋 Customer Bureau Feature Summary")

st.markdown(
    """
    Each row represents one customer and summarizes their
    previously reported bureau credit history.
    """
)


summary_columns = [
    "SK_ID_CURR",
    "BUREAU_ACCOUNT_COUNT",
    "ACTIVE_ACCOUNT_COUNT",
    "CLOSED_ACCOUNT_COUNT",
    "TOTAL_BUREAU_CREDIT",
    "TOTAL_BUREAU_DEBT",
    "AVERAGE_BUREAU_CREDIT",
    "MAX_OVERDUE_AMOUNT"
]


st.dataframe(
    customer_features[summary_columns].head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CUSTOMER-LEVEL KPIs
# =========================================================

st.subheader("👥 Customer Bureau Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Customers",
        f"{len(customer_features):,}"
    )

with col2:

    st.metric(
        "Avg Bureau Accounts",
        f"{customer_features['BUREAU_ACCOUNT_COUNT'].mean():.2f}"
    )

with col3:

    st.metric(
        "Avg Bureau Credit",
        f"{customer_features['AVERAGE_BUREAU_CREDIT'].mean():,.0f}"
    )

with col4:

    st.metric(
        "Maximum Overdue",
        f"{customer_features['MAX_OVERDUE_AMOUNT'].max():,.0f}"
    )


# =========================================================
# CUSTOMER BUREAU CREDIT DISTRIBUTION
# =========================================================

st.subheader("👥 Customer Total Bureau Credit")

fig = px.histogram(
    customer_features,
    x="TOTAL_BUREAU_CREDIT",
    nbins=50,
    title="Customer-Level Total Bureau Credit Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CUSTOMER BUREAU DEBT DISTRIBUTION
# =========================================================

st.subheader("💳 Customer Total Bureau Debt")

fig = px.histogram(
    customer_features,
    x="TOTAL_BUREAU_DEBT",
    nbins=50,
    title="Customer-Level Total Bureau Debt Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# INTERPRETATION
# =========================================================

st.divider()

st.subheader("💡 Bureau Credit History Interpretation")

st.markdown(
    """
    ### What to investigate

    - **Bureau Accounts** → number of previously reported credit
      accounts for a customer.

    - **Active Accounts** → currently active reported accounts.

    - **Closed Accounts** → previously reported accounts that
      are closed.

    - **Total Bureau Credit** → total credit amount reported
      across bureau accounts.

    - **Total Bureau Debt** → aggregate reported outstanding debt.

    - **Average Bureau Credit** → average credit amount per
      bureau account.

    - **Maximum Overdue Amount** → highest overdue amount
      reported for the customer.

    These are **descriptive observations**. They should not
    automatically be interpreted as causal relationships.
    """
)
import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.kpi import calculate_bureau_metrics
from utils.features import create_bureau_features


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bureau Credit Analysis",
    page_icon="📜",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📜 Bureau Credit Analysis")

st.markdown(
    """
    Analyse customers' historical credit information
    reported by other financial institutions using
    **bureau.csv**.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data(
        "data/bureau.csv"
    )

    st.success(
        f"✅ Bureau dataset loaded successfully: "
        f"{len(df):,} rows × {len(df.columns)} columns"
    )

except Exception as e:

    st.error(
        f"❌ Error loading bureau.csv: {e}"
    )

    st.stop()


# =========================================================
# DATA PREVIEW
# =========================================================

st.subheader("📋 Bureau Data Preview")

st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

st.subheader("📊 Bureau Credit KPIs")

with st.spinner("Calculating Bureau KPIs..."):

    try:

        metrics = calculate_bureau_metrics(df)

    except Exception as e:

        st.error(
            f"❌ Error calculating Bureau KPIs: {e}"
        )

        st.stop()


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📋 Bureau Accounts",
        f"{metrics['bureau_accounts']:,}"
    )

with col2:

    st.metric(
        "👥 Customers with Bureau History",
        f"{metrics['customers_with_bureau_history']:,}"
    )

with col3:

    st.metric(
        "🟢 Active Credits",
        f"{metrics['active_credits']:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "⚪ Closed Credits",
        f"{metrics['closed_credits']:,}"
    )

with col5:

    st.metric(
        "💰 Total Bureau Debt",
        f"{metrics['total_bureau_debt']:,.0f}"
    )

with col6:

    st.metric(
        "⚠️ Total Overdue Amount",
        f"{metrics['total_overdue_amount']:,.0f}"
    )


st.divider()


# =========================================================
# ACTIVE VS CLOSED
# =========================================================

st.subheader("🟢 Active vs Closed Loans")

status_data = (
    df["CREDIT_ACTIVE"]
    .value_counts()
    .reset_index()
)

status_data.columns = [
    "CREDIT_ACTIVE",
    "COUNT"
]

fig = px.bar(
    status_data,
    x="CREDIT_ACTIVE",
    y="COUNT",
    title="Active vs Closed Bureau Loans"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT TYPE
# =========================================================

st.subheader("📊 Credit Type Distribution")

credit_type_data = (
    df["CREDIT_TYPE"]
    .value_counts()
    .reset_index()
)

credit_type_data.columns = [
    "CREDIT_TYPE",
    "COUNT"
]

credit_type_data = credit_type_data.sort_values(
    "COUNT",
    ascending=True
)

fig = px.bar(
    credit_type_data,
    x="COUNT",
    y="CREDIT_TYPE",
    orientation="h",
    title="Bureau Credit Type Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT AMOUNT
# =========================================================

st.subheader("💰 Bureau Credit Amount Distribution")

credit_amount = df[
    "AMT_CREDIT_SUM"
].dropna()

fig = px.histogram(
    x=credit_amount,
    nbins=50,
    title="Bureau Credit Amount Distribution",
    labels={
        "x": "Bureau Credit Amount"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# BUREAU DEBT
# =========================================================

st.subheader("💳 Bureau Debt Distribution")

debt_amount = df[
    "AMT_CREDIT_SUM_DEBT"
].dropna()

fig = px.histogram(
    x=debt_amount,
    nbins=50,
    title="Bureau Debt Distribution",
    labels={
        "x": "Bureau Debt"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# OVERDUE
# =========================================================

st.subheader("⚠️ Overdue Amount Distribution")

overdue_amount = df[
    "AMT_CREDIT_SUM_OVERDUE"
].dropna()

fig = px.histogram(
    x=overdue_amount,
    nbins=50,
    title="Overdue Amount Distribution",
    labels={
        "x": "Overdue Amount"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# CREDIT TYPE VS DEBT
# =========================================================

st.subheader("💳 Credit Type vs Total Debt")

credit_debt = (
    df.groupby(
        "CREDIT_TYPE",
        dropna=False
    )["AMT_CREDIT_SUM_DEBT"]
    .sum()
    .reset_index()
)

credit_debt = credit_debt.sort_values(
    "AMT_CREDIT_SUM_DEBT",
    ascending=False
)

fig = px.bar(
    credit_debt,
    x="CREDIT_TYPE",
    y="AMT_CREDIT_SUM_DEBT",
    title="Total Bureau Debt by Credit Type"
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
    "👤 Customer-Level Bureau Features"
)

st.info(
    "Creating customer-level aggregates from "
    "1.7 million bureau records. This may take some time..."
)


with st.spinner(
    "Creating customer-level bureau features..."
):

    try:

        customer_features = create_bureau_features(df)

    except Exception as e:

        st.error(
            f"❌ Error creating customer-level features: {e}"
        )

        st.stop()


# =========================================================
# CUSTOMER FEATURE RESULT
# =========================================================

st.success(
    f"✅ Customer-level features created successfully: "
    f"{len(customer_features):,} customers"
)


st.dataframe(
    customer_features.head(1000),
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CUSTOMER FEATURE SUMMARY
# =========================================================

st.subheader(
    "📋 Customer Bureau Feature Summary"
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

available_columns = [
    col
    for col in summary_columns
    if col in customer_features.columns
]

st.dataframe(
    customer_features[
        available_columns
    ].head(1000),
    use_container_width=True,
    hide_index=True
)
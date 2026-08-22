import streamlit as st

from utils.data_loader import load_data

from utils.kpi import calculate_loan_application_metrics

from utils.charts import (
    bar_chart,
    histogram,
    scatter_chart,
    line_chart
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Current Loan Application Analysis",
    page_icon="💳",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("💳 Current Loan Application Analysis")

st.markdown(
    """
    Analyze the structure and characteristics of
    current Home Credit loan applications.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data(
        "data/application_train.csv"
    )

except FileNotFoundError:

    st.error(
        "❌ application_train.csv not found."
    )

    st.stop()


# =========================================================
# CALCULATE KPI METRICS
# =========================================================

metrics = calculate_loan_application_metrics(df)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Loan Application KPIs")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "📋 Total Applications",
        f"{metrics['total_applications']:,}"
    )

with col2:

    st.metric(
        "💰 Average Credit",
        f"{metrics['average_credit']:,.0f}"
    )

with col3:

    st.metric(
        "📊 Median Credit",
        f"{metrics['median_credit']:,.0f}"
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "💳 Average Annuity",
        f"{metrics['average_annuity']:,.0f}"
    )

with col5:

    st.metric(
        "🛒 Average Goods Price",
        f"{metrics['average_goods_price']:,.0f}"
    )

with col6:

    st.metric(
        "🏦 Most Common Contract",
        metrics["most_common_contract_type"]
    )


st.divider()


# =========================================================
# APPLICATIONS BY CONTRACT TYPE
# =========================================================

st.subheader("🏦 Applications by Contract Type")

st.plotly_chart(
    bar_chart(
        df,
        "NAME_CONTRACT_TYPE",
        "SK_ID_CURR",
        "Applications by Contract Type",
        aggfunc="count"
    ),
    use_container_width=True
)


# =========================================================
# CREDIT AMOUNT DISTRIBUTION
# =========================================================

st.subheader("💰 Credit Amount Distribution")

st.plotly_chart(
    histogram(
        df,
        "AMT_CREDIT",
        "Credit Amount Distribution"
    ),
    use_container_width=True
)


# =========================================================
# ANNUITY DISTRIBUTION
# =========================================================

st.subheader("💳 Annuity Distribution")

st.plotly_chart(
    histogram(
        df,
        "AMT_ANNUITY",
        "Annuity Distribution"
    ),
    use_container_width=True
)


# =========================================================
# GOODS PRICE DISTRIBUTION
# =========================================================

st.subheader("🛒 Goods Price Distribution")

st.plotly_chart(
    histogram(
        df,
        "AMT_GOODS_PRICE",
        "Goods Price Distribution"
    ),
    use_container_width=True
)


# =========================================================
# CREDIT VS GOODS PRICE
# =========================================================

st.subheader("💰 Credit vs Goods Price")

st.plotly_chart(
    scatter_chart(
        df,
        "AMT_CREDIT",
        "AMT_GOODS_PRICE",
        "TARGET",
        "Credit vs Goods Price"
    ),
    use_container_width=True
)


# =========================================================
# CREDIT VS ANNUITY
# =========================================================

st.subheader("💳 Credit vs Annuity")

st.plotly_chart(
    scatter_chart(
        df,
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "TARGET",
        "Credit vs Annuity"
    ),
    use_container_width=True
)


# =========================================================
# APPLICATIONS BY WEEKDAY
# =========================================================

st.subheader("📅 Applications by Weekday")

st.plotly_chart(
    bar_chart(
        df,
        "WEEKDAY_APPR_PROCESS_START",
        "SK_ID_CURR",
        "Applications by Weekday",
        aggfunc="count"
    ),
    use_container_width=True
)


# =========================================================
# APPLICATIONS BY HOUR
# =========================================================

st.subheader("⏰ Applications by Hour")

st.plotly_chart(
    line_chart(
        df,
        "HOUR_APPR_PROCESS_START",
        "SK_ID_CURR",
        "Applications by Hour",
        aggfunc="count"
    ),
    use_container_width=True
)


# =========================================================
# APPLICATION SUMMARY TABLE
# =========================================================

st.subheader("📋 Loan Application Summary")

summary_table = (
    df[
        [
            "NAME_CONTRACT_TYPE",
            "AMT_CREDIT",
            "AMT_ANNUITY",
            "AMT_GOODS_PRICE"
        ]
    ]
    .groupby("NAME_CONTRACT_TYPE")
    .agg(
        Applications=("NAME_CONTRACT_TYPE", "count"),
        Average_Credit=("AMT_CREDIT", "mean"),
        Median_Credit=("AMT_CREDIT", "median"),
        Average_Annuity=("AMT_ANNUITY", "mean"),
        Average_Goods_Price=("AMT_GOODS_PRICE", "mean")
    )
    .reset_index()
)

st.dataframe(
    summary_table,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# RECOMMENDATIONS
# =========================================================

st.subheader("💡 Loan Application Insights")

st.write(
    f"🔹 The most common contract type is "
    f"**{metrics['most_common_contract_type']}**."
)

st.write(
    f"🔹 The average credit amount is "
    f"**{metrics['average_credit']:,.0f}**."
)

st.write(
    f"🔹 The median credit amount is "
    f"**{metrics['median_credit']:,.0f}**."
)

st.write(
    "🔹 Review the credit and goods-price relationship "
    "to understand financing patterns."
)

st.write(
    "🔹 Review weekday and hourly application patterns "
    "to identify peak application periods."
)

st.write(
    "🔹 Investigate unusual credit, annuity and goods-price "
    "values before treating them as genuine customer behaviour."
)
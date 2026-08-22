import streamlit as st

from utils.data_loader import load_data
from utils.features import create_credit_affordability_features
from utils.kpi import calculate_credit_affordability_metrics

from utils.charts import (
    histogram,
    box_plot,
    scatter_chart,
    bar_chart
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Credit Affordability Analysis",
    page_icon="💳",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("💳 Credit Affordability Analysis")

st.markdown(
    """
    Analyse whether customers receive credit amounts
    appropriate for their income and repayment capacity.
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

df = create_credit_affordability_features(df)


# ==================================================
# KPI CALCULATIONS
# ==================================================

metrics = calculate_credit_affordability_metrics(df)


# ==================================================
# KPI CARDS
# ==================================================

st.subheader("📊 Credit Affordability KPIs")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "💳 Average Credit-to-Income",
        f"{metrics['average_credit_to_income_ratio']:.2f}"
    )

with col2:

    st.metric(
        "📊 Median Credit-to-Income",
        f"{metrics['median_credit_to_income_ratio']:.2f}"
    )

with col3:

    st.metric(
        "💰 Average Annuity-to-Income",
        f"{metrics['average_annuity_to_income_ratio']:.2f}"
    )


col4, col5 = st.columns(2)

with col4:

    st.metric(
        "⚠️ High Credit Burden",
        f"{metrics['high_credit_burden']:,}"
    )

with col5:

    st.metric(
        "🚨 High Annuity Burden",
        f"{metrics['high_annuity_burden']:,}"
    )


st.divider()


# ==================================================
# THRESHOLD EXPLANATION
# ==================================================

st.subheader("📌 Burden Thresholds")

st.write(
    f"""
    The high-burden groups are defined using the
    **90th percentile of the observed dataset**.

    - Credit-to-Income threshold:
      **{metrics['credit_burden_threshold']:.2f}**

    - Annuity-to-Income threshold:
      **{metrics['annuity_burden_threshold']:.2f}**

    These thresholds are data-driven for exploratory
    analysis and should not automatically be treated
    as business or regulatory limits.
    """
)


# ==================================================
# CREDIT-TO-INCOME DISTRIBUTION
# ==================================================

st.subheader("📊 Credit-to-Income Distribution")

st.plotly_chart(
    histogram(
        df,
        "CREDIT_TO_INCOME_RATIO",
        "Credit-to-Income Ratio Distribution"
    ),
    use_container_width=True
)


# ==================================================
# ANNUITY-TO-INCOME DISTRIBUTION
# ==================================================

st.subheader("📊 Annuity-to-Income Distribution")

st.plotly_chart(
    histogram(
        df,
        "ANNUITY_TO_INCOME_RATIO",
        "Annuity-to-Income Ratio Distribution"
    ),
    use_container_width=True
)


# ==================================================
# CREDIT-TO-INCOME BY DEFAULT
# ==================================================

st.subheader("⚠️ Credit-to-Income by Default Status")

st.plotly_chart(
    box_plot(
        df,
        "TARGET",
        "CREDIT_TO_INCOME_RATIO",
        "Credit-to-Income Ratio by Default Status"
    ),
    use_container_width=True
)


# ==================================================
# INCOME VS CREDIT
# ==================================================

st.subheader("💰 Income vs Credit")

st.plotly_chart(
    scatter_chart(
        df,
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "TARGET",
        "Income vs Credit Amount"
    ),
    use_container_width=True
)


# ==================================================
# CREDIT BURDEN BY INCOME GROUP
# ==================================================

st.subheader("📊 Credit Burden by Income Group")

if "INCOME_GROUP" not in df.columns:

    import pandas as pd

    df["INCOME_GROUP"] = pd.qcut(
        df["AMT_INCOME_TOTAL"],
        q=5,
        labels=[
            "Very Low",
            "Low",
            "Middle",
            "High",
            "Very High"
        ],
        duplicates="drop"
    )

st.plotly_chart(
    bar_chart(
        df,
        "INCOME_GROUP",
        "CREDIT_TO_INCOME_RATIO",
        "Credit Burden by Income Group",
        aggfunc="mean"
    ),
    use_container_width=True
)


# ==================================================
# ANNUITY BURDEN BY AGE GROUP
# ==================================================

st.subheader("👥 Annuity Burden by Age Group")

if "AGE" not in df.columns:

    df["AGE"] = (
        -df["DAYS_BIRTH"] / 365.25
    )

if "AGE_GROUP" not in df.columns:

    df["AGE_GROUP"] = pd.cut(
        df["AGE"],
        bins=[0, 30, 40, 50, 60, 100],
        labels=[
            "20–30",
            "31–40",
            "41–50",
            "51–60",
            "60+"
        ]
    )

st.plotly_chart(
    bar_chart(
        df,
        "AGE_GROUP",
        "ANNUITY_TO_INCOME_RATIO",
        "Annuity Burden by Age Group",
        aggfunc="mean"
    ),
    use_container_width=True
)


# ==================================================
# AFFORDABILITY SUMMARY
# ==================================================

st.subheader("💡 Affordability Summary")

st.markdown(
    f"""
    - Average Credit-to-Income Ratio:
      **{metrics['average_credit_to_income_ratio']:.2f}**

    - Median Credit-to-Income Ratio:
      **{metrics['median_credit_to_income_ratio']:.2f}**

    - Average Annuity-to-Income Ratio:
      **{metrics['average_annuity_to_income_ratio']:.2f}**

    - Customers in the highest 10% of
      Credit-to-Income burden:
      **{metrics['high_credit_burden']:,}**

    - Customers in the highest 10% of
      Annuity-to-Income burden:
      **{metrics['high_annuity_burden']:,}**
    """
)
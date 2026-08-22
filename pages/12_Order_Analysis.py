import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data

from utils.features import (
    create_customer_features,
    create_income_features,
    create_employment_features,
    create_credit_affordability_features,
    create_risk_factor_features
)

from utils.charts import (
    bar_chart
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Risk Factor Exploration",
    page_icon="⚠️",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("⚠️ Risk Factor Exploration")

st.markdown(
    """
    Explore variables showing meaningful **observed relationships**
    with loan default.

    **Important:** Correlation or association does not prove causation.
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
# REUSE EXISTING FEATURE FUNCTIONS
# =========================================================

# Creates AGE and AGE_GROUP
df = create_customer_features(df)

# Creates INCOME_GROUP
df = create_income_features(df)

# Creates EMPLOYMENT_YEARS and EMPLOYMENT_GROUP
df = create_employment_features(df)

# Creates affordability ratios
df = create_credit_affordability_features(df)

# Creates risk-factor bands
df = create_risk_factor_features(df)


# =========================================================
# AGE GROUP VS DEFAULT RATE
# =========================================================

st.subheader("👥 Age Group vs Default Rate")

st.plotly_chart(
    bar_chart(
        df,
        "AGE_GROUP",
        "TARGET",
        "Default Rate by Age Group",
        aggfunc="mean"
    ),
    use_container_width=True
)


# =========================================================
# CREDIT BAND VS DEFAULT RATE
# =========================================================

st.subheader("💳 Credit Band vs Default Rate")

st.plotly_chart(
    bar_chart(
        df,
        "CREDIT_BAND",
        "TARGET",
        "Default Rate by Credit Band",
        aggfunc="mean"
    ),
    use_container_width=True
)


# =========================================================
# INCOME BAND VS DEFAULT RATE
# =========================================================

st.subheader("💰 Income Band vs Default Rate")

st.plotly_chart(
    bar_chart(
        df,
        "INCOME_BAND",
        "TARGET",
        "Default Rate by Income Band",
        aggfunc="mean"
    ),
    use_container_width=True
)


# =========================================================
# EMPLOYMENT BAND VS DEFAULT RATE
# =========================================================

st.subheader("💼 Employment Band vs Default Rate")

st.plotly_chart(
    bar_chart(
        df,
        "EMPLOYMENT_BAND",
        "TARGET",
        "Default Rate by Employment Band",
        aggfunc="mean"
    ),
    use_container_width=True
)


# =========================================================
# CREDIT-TO-INCOME BAND VS DEFAULT
# =========================================================

st.subheader("📊 Credit-to-Income Band vs Default Rate")

st.plotly_chart(
    bar_chart(
        df,
        "CREDIT_TO_INCOME_BAND",
        "TARGET",
        "Default Rate by Credit-to-Income Band",
        aggfunc="mean"
    ),
    use_container_width=True
)


# =========================================================
# ANNUITY-TO-INCOME BAND VS DEFAULT
# =========================================================

st.subheader("💵 Annuity-to-Income Band vs Default Rate")

st.plotly_chart(
    bar_chart(
        df,
        "ANNUITY_TO_INCOME_BAND",
        "TARGET",
        "Default Rate by Annuity-to-Income Band",
        aggfunc="mean"
    ),
    use_container_width=True
)


# =========================================================
# CORRELATION HEATMAP
# =========================================================

st.subheader("🔥 Correlation Heatmap")

correlation_columns = [
    "TARGET",
    "AGE",
    "AMT_INCOME_TOTAL",
    "AMT_CREDIT",
    "AMT_ANNUITY",
    "AMT_GOODS_PRICE",
    "EMPLOYMENT_YEARS",
    "CNT_CHILDREN",
    "CNT_FAM_MEMBERS",
    "CREDIT_TO_INCOME_RATIO",
    "ANNUITY_TO_INCOME_RATIO"
]

# Keep only columns that actually exist
correlation_columns = [
    col
    for col in correlation_columns
    if col in df.columns
]

correlation_data = df[
    correlation_columns
].corr(numeric_only=True)


fig_heatmap = px.imshow(
    correlation_data,
    text_auto=".2f",
    aspect="auto",
    title="Correlation Between Numerical Risk Factors"
)

fig_heatmap.update_layout(
    xaxis_title="Variables",
    yaxis_title="Variables"
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)


# =========================================================
# OBSERVED RELATIONSHIP
# =========================================================

st.divider()

st.subheader("💡 Interpretation Guidelines")

st.markdown(
    """
    ### How to interpret this analysis

    - A higher default rate in a particular band indicates an
      **observed relationship** between that band and default risk.

    - A lower default rate indicates a lower **observed default
      rate within that group**.

    - Correlation values show the strength and direction of a
      linear relationship between numerical variables.

    - **Correlation does not prove causation.**

    Therefore, avoid statements such as:

    > "Income causes default."

    Instead, report:

    > "The analysis shows an observed relationship between income
    > band and default rate."

    Similarly:

    > "Customers in higher credit-to-income bands show a higher
    > observed default rate."

    This is an EDA finding, not a causal conclusion.
    """
)


# =========================================================
# SUMMARY TABLE
# =========================================================

st.subheader("📋 Risk Factor Summary")

summary_tables = []

risk_columns = [
    ("AGE_GROUP", "Age Group"),
    ("CREDIT_BAND", "Credit Band"),
    ("INCOME_BAND", "Income Band"),
    ("EMPLOYMENT_BAND", "Employment Band"),
    ("CREDIT_TO_INCOME_BAND", "Credit-to-Income Band"),
    ("ANNUITY_TO_INCOME_BAND", "Annuity-to-Income Band")
]

for column, label in risk_columns:

    if column in df.columns:

        temp = (
            df.groupby(
                column,
                observed=True
            )["TARGET"]
            .agg(
                Customers="count",
                Defaults="sum",
                Default_Rate="mean"
            )
            .reset_index()
        )

        temp["Risk Factor"] = label

        temp = temp.rename(
            columns={
                column: "Band"
            }
        )

        temp["Default_Rate"] = (
            temp["Default_Rate"] * 100
        )

        summary_tables.append(temp)


if summary_tables:

    final_summary = pd.concat(
        summary_tables,
        ignore_index=True
    )

    st.dataframe(
        final_summary[
            [
                "Risk Factor",
                "Band",
                "Customers",
                "Defaults",
                "Default_Rate"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
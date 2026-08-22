import streamlit as st
import pandas as pd

from utils.data_loader import load_data

from utils.features import (
    create_customer_features,
    create_income_features,
    create_employment_features
)

from utils.kpi import (
    calculate_default_risk_metrics
)

from utils.charts import (
    bar_chart,
    horizontal_bar_chart,
    pie_chart
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Default Risk EDA",
    page_icon="⚠️",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("⚠️ Default Risk EDA")

st.markdown(
    """
    Detailed exploratory analysis of the **TARGET**
    variable to understand customer repayment risk.

    **No predictive model is used on this page.**
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
# REUSE EXISTING FEATURE FUNCTIONS
# ==================================================

# Creates AGE and AGE_GROUP
df = create_customer_features(df)

# Creates INCOME_GROUP and income-related features
df = create_income_features(df)

# Creates EMPLOYMENT_YEARS and EMPLOYMENT_GROUP
df = create_employment_features(df)


# ==================================================
# KPI CALCULATIONS
# ==================================================

risk = calculate_default_risk_metrics(df)


# ==================================================
# KPI CARDS
# ==================================================

st.subheader("📊 Default Risk KPIs")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "⚠️ Default Customers",
        f"{risk['default_customers']:,}"
    )

with col2:

    st.metric(
        "✅ Non-Default Customers",
        f"{risk['non_default_customers']:,}"
    )

with col3:

    st.metric(
        "📉 Default Rate",
        f"{risk['default_rate']:.2f}%"
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "🔴 Highest Risk Age Group",
        str(risk["highest_risk_age_group"])
    )

with col5:

    st.metric(
        "🟠 Highest Risk Income Group",
        str(risk["highest_risk_income_group"])
    )

with col6:

    st.metric(
        "🟣 Highest Risk Employment Group",
        str(risk["highest_risk_employment_group"])
    )


st.divider()


# ==================================================
# TARGET DISTRIBUTION
# ==================================================

st.subheader("🎯 TARGET Distribution")

target_df = (
    df["TARGET"]
    .value_counts()
    .rename_axis("TARGET")
    .reset_index(name="Customers")
)

target_df["TARGET"] = target_df["TARGET"].map({
    0: "Non-Default",
    1: "Default"
})

st.plotly_chart(
    bar_chart(
        target_df,
        "TARGET",
        "Customers",
        "TARGET Distribution",
        aggfunc="sum"
    ),
    use_container_width=True
)


# ==================================================
# DEFAULT PERCENTAGE
# ==================================================

st.subheader("🍩 Default Percentage")

default_df = pd.DataFrame({
    "Status": [
        "Non-Default",
        "Default"
    ],
    "Customers": [
        risk["non_default_customers"],
        risk["default_customers"]
    ]
})

fig_default = pie_chart(
    default_df,
    "Status",
    "Customers",
    "Default vs Non-Default"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# ==================================================
# DEFAULT BY AGE GROUP
# ==================================================

st.subheader("👥 Default by Age Group")

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


# ==================================================
# DEFAULT BY INCOME GROUP
# ==================================================

st.subheader("💰 Default by Income Group")

st.plotly_chart(
    bar_chart(
        df,
        "INCOME_GROUP",
        "TARGET",
        "Default Rate by Income Group",
        aggfunc="mean"
    ),
    use_container_width=True
)


# ==================================================
# DEFAULT BY EMPLOYMENT GROUP
# ==================================================

st.subheader("💼 Default by Employment Group")

st.plotly_chart(
    bar_chart(
        df,
        "EMPLOYMENT_GROUP",
        "TARGET",
        "Default Rate by Employment Group",
        aggfunc="mean"
    ),
    use_container_width=True
)


# ==================================================
# DEFAULT BY EDUCATION
# ==================================================

st.subheader("🎓 Default by Education")

st.plotly_chart(
    horizontal_bar_chart(
        df,
        "NAME_EDUCATION_TYPE",
        "TARGET",
        "Default Rate by Education",
        aggfunc="mean"
    ),
    use_container_width=True
)


# ==================================================
# DEFAULT BY OCCUPATION
# ==================================================

st.subheader("💼 Default by Occupation")

occupation_df = (
    df.groupby(
        "OCCUPATION_TYPE",
        dropna=False
    )["TARGET"]
    .mean()
    .reset_index()
)

occupation_df = occupation_df.dropna(
    subset=["OCCUPATION_TYPE"]
)

occupation_df["TARGET"] = (
    occupation_df["TARGET"] * 100
)

occupation_df = occupation_df.sort_values(
    "TARGET",
    ascending=False
)

st.plotly_chart(
    bar_chart(
        occupation_df,
        "OCCUPATION_TYPE",
        "TARGET",
        "Default Rate by Occupation",
        aggfunc="sum"
    ),
    use_container_width=True
)


# ==================================================
# DEFAULT BY CONTRACT TYPE
# ==================================================

st.subheader("💳 Default by Contract Type")

contract_df = (
    df.groupby(
        "NAME_CONTRACT_TYPE"
    )["TARGET"]
    .mean()
    .reset_index()
)

contract_df["TARGET"] = (
    contract_df["TARGET"] * 100
)

st.plotly_chart(
    bar_chart(
        contract_df,
        "NAME_CONTRACT_TYPE",
        "TARGET",
        "Default Rate by Contract Type",
        aggfunc="sum"
    ),
    use_container_width=True
)


# ==================================================
# DEFAULT COUNT VS DEFAULT RATE
# ==================================================

st.subheader("📌 Default Count vs Default Rate")

st.markdown(
    """
    **Important distinction:**

    - **Default Count** → number of customers who defaulted.
    - **Default Rate** → percentage of customers in a group who defaulted.

    A large customer group can have many defaults simply because
    it contains many customers. Therefore, **default rate should
    also be considered when comparing risk between groups.**
    """
)


# ==================================================
# SUMMARY
# ==================================================

st.subheader("💡 Default Risk Summary")

st.markdown(
    f"""
    - ⚠️ Default customers: **{risk['default_customers']:,}**
    - ✅ Non-default customers: **{risk['non_default_customers']:,}**
    - 📉 Overall default rate: **{risk['default_rate']:.2f}%**
    - 👥 Highest observed-risk age group:
      **{risk['highest_risk_age_group']}**
    - 💰 Highest observed-risk income group:
      **{risk['highest_risk_income_group']}**
    - 💼 Highest observed-risk employment group:
      **{risk['highest_risk_employment_group']}**
    """
)
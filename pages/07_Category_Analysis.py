import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.features import create_employment_features
from utils.kpi import calculate_employment_metrics


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Employment Analysis",
    page_icon="💼",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("💼 Employment Analysis")

st.markdown(
    """
    Analyze employment stability and its relationship
    with income, credit and default risk.
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
# FEATURE ENGINEERING
# =========================================================

df = create_employment_features(df)


# =========================================================
# KPI CALCULATIONS
# =========================================================

employment_metrics = (
    calculate_employment_metrics(df)
)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Employment KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "📅 Average Employment Years",
        f"{employment_metrics['average_employment_years']:.2f}"
    )

with col2:

    st.metric(
        "📅 Median Employment Years",
        f"{employment_metrics['median_employment_years']:.2f}"
    )

with col3:

    st.metric(
        "💼 Most Common Occupation",
        employment_metrics["most_common_occupation"]
    )

with col4:

    st.metric(
        "🏢 Most Common Organization",
        employment_metrics["most_common_organization"]
    )

with col5:

    st.metric(
        "⚠️ Highest Default Group",
        employment_metrics["highest_default_group"]
    )


st.divider()


# =========================================================
# EMPLOYMENT YEARS DISTRIBUTION
# =========================================================

st.subheader("📊 Employment Years Distribution")

fig_employment = px.histogram(
    df[
        df["EMPLOYMENT_YEARS"].notna()
    ],
    x="EMPLOYMENT_YEARS",
    nbins=40,
    title="Distribution of Employment Years"
)

fig_employment.update_layout(
    xaxis_title="Employment Years",
    yaxis_title="Number of Customers"
)

st.plotly_chart(
    fig_employment,
    use_container_width=True
)


# =========================================================
# EMPLOYMENT GROUP DISTRIBUTION
# =========================================================

st.subheader("📂 Employment Group Distribution")

group_order = [
    "<1 Year",
    "1–3 Years",
    "3–5 Years",
    "5–10 Years",
    "10–20 Years",
    "20+ Years",
    "Unemployed / Special"
]

employment_group_data = (
    df["EMPLOYMENT_GROUP"]
    .value_counts()
    .reindex(
        group_order,
        fill_value=0
    )
    .reset_index()
)

employment_group_data.columns = [
    "Employment Group",
    "Customers"
]

fig_group = px.bar(
    employment_group_data,
    x="Employment Group",
    y="Customers",
    text="Customers",
    title="Customers by Employment Group"
)

st.plotly_chart(
    fig_group,
    use_container_width=True
)


# =========================================================
# DEFAULT RATE BY EMPLOYMENT GROUP
# =========================================================

st.subheader("⚠️ Default Rate by Employment Group")

default_group = (
    employment_metrics["default_by_group"]
    .reindex(group_order)
    .dropna()
    .reset_index()
)

default_group.columns = [
    "Employment Group",
    "Default Rate"
]

fig_default = px.bar(
    default_group,
    x="Employment Group",
    y="Default Rate",
    text="Default Rate",
    title="Default Rate by Employment Group"
)

fig_default.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(
    fig_default,
    use_container_width=True
)


# =========================================================
# OCCUPATION VS DEFAULT RATE
# =========================================================

st.subheader("💼 Occupation vs Default Rate")

occupation_default = (
    df.dropna(
        subset=["OCCUPATION_TYPE"]
    )
    .groupby(
        "OCCUPATION_TYPE"
    )["TARGET"]
    .mean()
    .mul(100)
    .sort_values()
    .reset_index()
)

occupation_default.columns = [
    "Occupation",
    "Default Rate"
]

fig_occupation = px.bar(
    occupation_default,
    x="Default Rate",
    y="Occupation",
    orientation="h",
    text="Default Rate",
    title="Default Rate by Occupation"
)

fig_occupation.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(
    fig_occupation,
    use_container_width=True
)


# =========================================================
# ORGANIZATION TYPE VS DEFAULT
# =========================================================

st.subheader("🏢 Organization Type vs Default")

organization_default = (
    df.groupby(
        "ORGANIZATION_TYPE"
    )["TARGET"]
    .mean()
    .mul(100)
    .sort_values()
    .reset_index()
)

organization_default.columns = [
    "Organization Type",
    "Default Rate"
]

fig_organization = px.bar(
    organization_default,
    x="Default Rate",
    y="Organization Type",
    orientation="h",
    text="Default Rate",
    title="Default Rate by Organization Type"
)

fig_organization.update_traces(
    texttemplate="%{text:.2f}%"
)

st.plotly_chart(
    fig_organization,
    use_container_width=True
)


# =========================================================
# EMPLOYMENT YEARS VS INCOME
# =========================================================

st.subheader("💰 Employment Years vs Income")

fig_income = px.scatter(
    df[
        df["EMPLOYMENT_YEARS"].notna()
    ],
    x="EMPLOYMENT_YEARS",
    y="AMT_INCOME_TOTAL",
    color="TARGET",
    opacity=0.5,
    title="Employment Years vs Income",
    labels={
        "EMPLOYMENT_YEARS":
            "Employment Years",
        "AMT_INCOME_TOTAL":
            "Income",
        "TARGET":
            "Default"
    }
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# =========================================================
# EMPLOYMENT YEARS VS CREDIT
# =========================================================

st.subheader("💳 Employment Years vs Credit")

fig_credit = px.scatter(
    df[
        df["EMPLOYMENT_YEARS"].notna()
    ],
    x="EMPLOYMENT_YEARS",
    y="AMT_CREDIT",
    color="TARGET",
    opacity=0.5,
    title="Employment Years vs Credit Amount",
    labels={
        "EMPLOYMENT_YEARS":
            "Employment Years",
        "AMT_CREDIT":
            "Credit Amount",
        "TARGET":
            "Default"
    }
)

st.plotly_chart(
    fig_credit,
    use_container_width=True
)


# =========================================================
# ABNORMAL DAYS_EMPLOYED
# =========================================================

st.subheader("🔎 DAYS_EMPLOYED Validation")

special_count = (
    df["EMPLOYMENT_SPECIAL"].sum()
)

st.metric(
    "Special DAYS_EMPLOYED Records",
    f"{special_count:,}"
)

if special_count > 0:

    st.warning(
        f"""
        ⚠️ {special_count:,} records contain the special
        DAYS_EMPLOYED value 365243.

        These records were not directly converted into
        employment years. They are classified as
        **Unemployed / Special**.
        """
    )

else:

    st.success(
        "✅ No special DAYS_EMPLOYED values detected."
    )


# =========================================================
# SUMMARY
# =========================================================

st.subheader("💡 Employment Analysis Summary")

st.markdown(
    f"""
    - 📅 Average employment duration:
      **{employment_metrics['average_employment_years']:.2f} years**

    - 📅 Median employment duration:
      **{employment_metrics['median_employment_years']:.2f} years**

    - 💼 Most common occupation:
      **{employment_metrics['most_common_occupation']}**

    - 🏢 Most common organization type:
      **{employment_metrics['most_common_organization']}**

    - ⚠️ Employment group with the highest observed
      default rate:
      **{employment_metrics['highest_default_group']}**

    - 🔎 Special `DAYS_EMPLOYED` records:
      **{special_count:,}**
    """
)


# =========================================================
# PREPROCESSING RECOMMENDATIONS
# =========================================================

st.subheader("🛠️ Preprocessing Recommendations")

st.markdown(
    """
    - Investigate the special `DAYS_EMPLOYED` value before
      using the variable for modeling.
    - Do not automatically treat every extreme employment
      value as an error.
    - Keep genuine long-term employment records.
    - Consider the business meaning of unemployed/special
      records before imputing them.
    - Use employment groups when comparing default behaviour.
    - Validate employment duration against other variables
      such as income and organization type.
    """
)
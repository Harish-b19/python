import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.kpi import calculate_outlier_metrics


st.set_page_config(
    page_title="Outlier & Distribution Analysis",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Outlier & Distribution Analysis")

st.markdown(
    """
    Identify unusual numerical values before deeper analysis.
    Outliers are analyzed using the IQR method and are not
    automatically removed.
    """
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:

    df = load_data("data/application_train.csv")

except FileNotFoundError:

    st.error("❌ application_train.csv not found.")
    st.stop()


# --------------------------------------------------
# CALCULATE OUTLIER METRICS
# --------------------------------------------------

outlier = calculate_outlier_metrics(df)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("📊 Outlier Analysis KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "🔢 Numerical Columns",
        f"{outlier['number_of_numerical_columns']:,}"
    )

with col2:

    st.metric(
        "⚠️ Variables with Outliers",
        f"{outlier['variables_with_outliers']:,}"
    )

with col3:

    st.metric(
        "💰 Maximum Income",
        f"{outlier['maximum_income']:,.0f}"
    )

with col4:

    st.metric(
        "💳 Maximum Credit",
        f"{outlier['maximum_credit']:,.0f}"
    )

with col5:

    st.metric(
        "📅 Maximum Annuity",
        f"{outlier['maximum_annuity']:,.0f}"
    )


st.divider()


# --------------------------------------------------
# INCOME DISTRIBUTION
# --------------------------------------------------

st.subheader("💰 Income Distribution")

fig_income = px.histogram(
    df,
    x="AMT_INCOME_TOTAL",
    nbins=50,
    title="Income Distribution"
)

st.plotly_chart(
    fig_income,
    use_container_width=True
)


# --------------------------------------------------
# INCOME OUTLIERS
# --------------------------------------------------

st.subheader("📦 Income Outliers")

fig_income_box = px.box(
    df,
    y="AMT_INCOME_TOTAL",
    title="Income Outlier Detection"
)

st.plotly_chart(
    fig_income_box,
    use_container_width=True
)


# --------------------------------------------------
# CREDIT OUTLIERS
# --------------------------------------------------

st.subheader("📦 Credit Outliers")

fig_credit_box = px.box(
    df,
    y="AMT_CREDIT",
    title="Credit Amount Outlier Detection"
)

st.plotly_chart(
    fig_credit_box,
    use_container_width=True
)


# --------------------------------------------------
# ANNUITY OUTLIERS
# --------------------------------------------------

st.subheader("📦 Annuity Outliers")

fig_annuity_box = px.box(
    df,
    y="AMT_ANNUITY",
    title="Annuity Outlier Detection"
)

st.plotly_chart(
    fig_annuity_box,
    use_container_width=True
)


# --------------------------------------------------
# INCOME VS CREDIT
# --------------------------------------------------

st.subheader("💰 Income vs Credit")

fig_scatter = px.scatter(
    df,
    x="AMT_INCOME_TOTAL",
    y="AMT_CREDIT",
    color="TARGET" if "TARGET" in df.columns else None,
    title="Income vs Credit Amount"
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# --------------------------------------------------
# OUTLIER TABLE
# --------------------------------------------------

st.subheader("📋 Outlier Analysis Details")

st.dataframe(
    outlier["outlier_table"],
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# OUTLIER TECHNIQUES
# --------------------------------------------------

st.subheader("🛠️ Outlier Handling Techniques")

st.write(
    "🔹 **IQR Method:** Identifies values outside "
    "Q1 − 1.5×IQR and Q3 + 1.5×IQR."
)

st.write(
    "🔹 **Percentile Capping:** Limits extreme values "
    "to selected percentile boundaries."
)

st.write(
    "🔹 **Winsorization:** Replaces extreme observations "
    "with percentile boundary values."
)

st.write(
    "🔹 **Log Transformation:** Useful for highly "
    "right-skewed financial variables."
)

st.write(
    "🔹 **Business-rule Validation:** Checks whether "
    "extreme values are actually realistic."
)


# --------------------------------------------------
# IMPORTANT INTERPRETATION
# --------------------------------------------------

st.subheader("💡 Outlier Interpretation")

st.info(
    """
    An outlier should not automatically be removed.

    Possible explanations include:

    • True extreme customer  
    • Data entry issue  
    • Potential invalid value  
    • Legitimate high-income or high-credit customer

    The appropriate treatment should depend on
    business context and data validation.
    """
)
import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.features import create_customer_features
from utils.kpi import calculate_customer_metrics


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Customer Demographic Analysis",
    page_icon="👥",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("👥 Customer Demographic Analysis")

st.markdown(
    """
    Understand the demographic characteristics of
    Home Credit customers.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data(
        "data/application_train.csv"
    )

    # Create only new demographic features
    df = create_customer_features(df)

except FileNotFoundError:

    st.error(
        "❌ application_train.csv not found."
    )

    st.stop()


# =========================================================
# CALCULATE CUSTOMER KPIs
# =========================================================

metrics = calculate_customer_metrics(df)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Customer Demographic KPIs")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🎂 Average Age",
        f"{metrics['average_age']:.1f} years"
    )

with col2:

    st.metric(
        "📊 Median Age",
        f"{metrics['median_age']:.1f} years"
    )

with col3:

    st.metric(
        "⚥ Most Common Gender",
        metrics["most_common_gender"]
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.metric(
        "🎓 Most Common Education",
        metrics["most_common_education"]
    )

with col5:

    st.metric(
        "💼 Most Common Income Type",
        metrics["most_common_income_type"]
    )

with col6:

    st.metric(
        "👨‍👩‍👧 Most Common Family Status",
        metrics["most_common_family_status"]
    )


st.divider()


# =========================================================
# AGE DISTRIBUTION
# =========================================================

st.subheader("🎂 Age Distribution")

fig_age = px.histogram(
    df,
    x="AGE",
    nbins=30,
    title="Customer Age Distribution",
    labels={
        "AGE": "Age"
    }
)

st.plotly_chart(
    fig_age,
    use_container_width=True
)


# =========================================================
# GENDER DISTRIBUTION
# =========================================================

st.subheader("⚥ Gender Distribution")

gender_data = (
    df["CODE_GENDER"]
    .value_counts()
    .reset_index()
)

gender_data.columns = [
    "Gender",
    "Customers"
]

fig_gender = px.pie(
    gender_data,
    names="Gender",
    values="Customers",
    hole=0.5,
    title="Customer Distribution by Gender"
)

st.plotly_chart(
    fig_gender,
    use_container_width=True
)


# =========================================================
# EDUCATION DISTRIBUTION
# =========================================================

st.subheader("🎓 Education Distribution")

education_data = (
    df["NAME_EDUCATION_TYPE"]
    .value_counts()
    .reset_index()
)

education_data.columns = [
    "Education",
    "Customers"
]

fig_education = px.bar(
    education_data.sort_values(
        "Customers",
        ascending=True
    ),
    x="Customers",
    y="Education",
    orientation="h",
    text="Customers",
    title="Customers by Education Type"
)

st.plotly_chart(
    fig_education,
    use_container_width=True
)


# =========================================================
# FAMILY STATUS
# =========================================================

st.subheader("👨‍👩‍👧 Family Status")

family_data = (
    df["NAME_FAMILY_STATUS"]
    .value_counts()
    .reset_index()
)

family_data.columns = [
    "Family Status",
    "Customers"
]

fig_family = px.bar(
    family_data,
    x="Family Status",
    y="Customers",
    text="Customers",
    title="Customers by Family Status"
)

st.plotly_chart(
    fig_family,
    use_container_width=True
)


# =========================================================
# INCOME TYPE
# =========================================================

st.subheader("💼 Income Type")

income_type_data = (
    df["NAME_INCOME_TYPE"]
    .value_counts()
    .reset_index()
)

income_type_data.columns = [
    "Income Type",
    "Customers"
]

fig_income_type = px.bar(
    income_type_data.sort_values(
        "Customers",
        ascending=True
    ),
    x="Customers",
    y="Income Type",
    orientation="h",
    text="Customers",
    title="Customers by Income Type"
)

st.plotly_chart(
    fig_income_type,
    use_container_width=True
)


# =========================================================
# AGE GROUP BY GENDER
# =========================================================

st.subheader("👥 Age Group by Gender")

age_gender_data = (
    df.groupby(
        ["AGE_GROUP", "CODE_GENDER"],
        observed=True
    )
    .size()
    .reset_index(
        name="Customers"
    )
)

fig_age_gender = px.bar(
    age_gender_data,
    x="AGE_GROUP",
    y="Customers",
    color="CODE_GENDER",
    barmode="group",
    text="Customers",
    title="Age Group Distribution by Gender"
)

st.plotly_chart(
    fig_age_gender,
    use_container_width=True
)


# =========================================================
# AGE VS INCOME
# =========================================================

st.subheader("💰 Age vs Income")

fig_age_income = px.scatter(
    df,
    x="AGE",
    y="AMT_INCOME_TOTAL",
    color="CODE_GENDER",
    opacity=0.5,
    title="Age vs Total Income",
    labels={
        "AGE": "Age",
        "AMT_INCOME_TOTAL": "Total Income",
        "CODE_GENDER": "Gender"
    }
)

st.plotly_chart(
    fig_age_income,
    use_container_width=True
)


# =========================================================
# CUSTOMER PROFILE SUMMARY
# =========================================================

st.subheader("💡 Typical Customer Profile")

st.markdown(
    f"""
    - 🎂 Average customer age: **{metrics['average_age']:.1f} years**
    - 📊 Median customer age: **{metrics['median_age']:.1f} years**
    - ⚥ Most common gender: **{metrics['most_common_gender']}**
    - 🎓 Most common education: **{metrics['most_common_education']}**
    - 💼 Most common income type: **{metrics['most_common_income_type']}**
    - 👨‍👩‍👧 Most common family status: **{metrics['most_common_family_status']}**
    """
)
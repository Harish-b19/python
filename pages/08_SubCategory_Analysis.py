import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.features import (
    create_family_housing_features,
    create_income_features
)
from utils.kpi import calculate_family_housing_metrics


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Family & Housing Analysis",
    page_icon="🏠",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🏠 Family & Housing Analysis")

st.markdown(
    """
    Analyze household characteristics including family size,
    children, housing, property ownership and car ownership.
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

# Existing Page 6 feature function
# This creates Income per Family Member
df = create_income_features(df)

# New Page 8 family/housing features
df = create_family_housing_features(df)


# =========================================================
# CALCULATE KPIs
# =========================================================

metrics = calculate_family_housing_metrics(df)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Family & Housing KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "👨‍👩‍👧 Average Family Size",
        f"{metrics['average_family_size']:.2f}"
    )

with col2:

    st.metric(
        "👶 Average Children",
        f"{metrics['average_children']:.2f}"
    )

with col3:

    st.metric(
        "🏠 Home Ownership",
        f"{metrics['home_ownership_percentage']:.2f}%"
    )

with col4:

    st.metric(
        "🚗 Car Ownership",
        f"{metrics['car_ownership_percentage']:.2f}%"
    )

with col5:

    st.metric(
        "🏡 Common Housing Type",
        metrics["most_common_housing_type"]
    )


st.divider()


# =========================================================
# FAMILY SIZE DISTRIBUTION
# =========================================================

st.subheader("👨‍👩‍👧 Family Size Distribution")

fig_family = px.histogram(
    df,
    x="CNT_FAM_MEMBERS",
    nbins=20,
    title="Distribution of Family Size"
)

st.plotly_chart(
    fig_family,
    use_container_width=True
)


# =========================================================
# CHILDREN DISTRIBUTION
# =========================================================

st.subheader("👶 Children Distribution")

children_data = (
    df["CHILDREN_GROUP"]
    .value_counts()
    .sort_index()
    .reset_index()
)

children_data.columns = [
    "Children Group",
    "Number of Customers"
]

fig_children = px.bar(
    children_data,
    x="Children Group",
    y="Number of Customers",
    text="Number of Customers",
    title="Customers by Number of Children"
)

st.plotly_chart(
    fig_children,
    use_container_width=True
)


# =========================================================
# HOUSING TYPE
# =========================================================

st.subheader("🏠 Housing Type Distribution")

housing_data = (
    df["NAME_HOUSING_TYPE"]
    .value_counts()
    .reset_index()
)

housing_data.columns = [
    "Housing Type",
    "Number of Customers"
]

fig_housing = px.bar(
    housing_data,
    x="Housing Type",
    y="Number of Customers",
    text="Number of Customers",
    title="Customers by Housing Type"
)

st.plotly_chart(
    fig_housing,
    use_container_width=True
)


# =========================================================
# PROPERTY OWNERSHIP
# =========================================================

st.subheader("🏡 Property Ownership")

property_data = (
    df["FLAG_OWN_REALTY"]
    .value_counts()
    .reset_index()
)

property_data.columns = [
    "Property Ownership",
    "Number of Customers"
]

fig_property = px.pie(
    property_data,
    names="Property Ownership",
    values="count"
    if "count" in property_data.columns
    else "Number of Customers",
    hole=0.5,
    title="Property Ownership"
)

st.plotly_chart(
    fig_property,
    use_container_width=True
)


# =========================================================
# CAR OWNERSHIP
# =========================================================

st.subheader("🚗 Car Ownership")

car_data = (
    df["FLAG_OWN_CAR"]
    .value_counts()
    .reset_index()
)

car_data.columns = [
    "Car Ownership",
    "Number of Customers"
]

fig_car = px.pie(
    car_data,
    names="Car Ownership",
    values="Number of Customers",
    hole=0.5,
    title="Car Ownership"
)

st.plotly_chart(
    fig_car,
    use_container_width=True
)


# =========================================================
# FAMILY SIZE VS INCOME
# =========================================================

st.subheader("💰 Family Size vs Income")

fig_family_income = px.box(
    df,
    x="CNT_FAM_MEMBERS",
    y="AMT_INCOME_TOTAL",
    title="Income Distribution by Family Size"
)

st.plotly_chart(
    fig_family_income,
    use_container_width=True
)


# =========================================================
# FAMILY SIZE VS DEFAULT RATE
# =========================================================

st.subheader("⚠️ Family Size vs Default Rate")

if "TARGET" in df.columns:

    default_by_family = (
        df.groupby("FAMILY_SIZE_GROUP", observed=False)["TARGET"]
        .mean()
        .mul(100)
        .reset_index()
    )

    default_by_family.columns = [
        "Family Size",
        "Default Rate"
    ]

    fig_default = px.bar(
        default_by_family,
        x="Family Size",
        y="Default Rate",
        text="Default Rate",
        title="Default Rate by Family Size"
    )

    fig_default.update_traces(
        texttemplate="%{text:.2f}%"
    )

    st.plotly_chart(
        fig_default,
        use_container_width=True
    )


# =========================================================
# INCOME PER FAMILY MEMBER
# =========================================================

st.subheader("💰 Income per Family Member")

if "INCOME_PER_FAMILY_MEMBER" in df.columns:

    st.plotly_chart(
        px.box(
            df,
            x="FAMILY_SIZE_GROUP",
            y="INCOME_PER_FAMILY_MEMBER",
            title="Income per Family Member by Family Size"
        ),
        use_container_width=True
    )


# =========================================================
# FINAL SUMMARY
# =========================================================

st.subheader("💡 Family & Housing Summary")

st.markdown(
    f"""
    - 👨‍👩‍👧 Average family size:
      **{metrics['average_family_size']:.2f}**
    - 👶 Average number of children:
      **{metrics['average_children']:.2f}**
    - 🏠 Home ownership:
      **{metrics['home_ownership_percentage']:.2f}%**
    - 🚗 Car ownership:
      **{metrics['car_ownership_percentage']:.2f}%**
    - 🏡 Most common housing type:
      **{metrics['most_common_housing_type']}**
    """
)
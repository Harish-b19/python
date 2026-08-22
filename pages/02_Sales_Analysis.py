import streamlit as st
import plotly.express as px

from utils.data_loader import load_data
from utils.kpi import calculate_data_quality


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Data Quality Dashboard",
    page_icon="🔍",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🔍 Data Quality Dashboard")

st.markdown(
    """
    Evaluate the completeness, consistency and structure
    of the Home Credit Default Risk dataset.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data("data/application_train.csv")

except FileNotFoundError:

    st.error("❌ application_train.csv not found.")
    st.stop()


# =========================================================
# CALCULATE QUALITY METRICS
# =========================================================

quality = calculate_data_quality(df)


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("📊 Data Quality KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋 Total Rows",
        f"{quality['number_of_rows']:,}"
    )

with col2:
    st.metric(
        "🔢 Total Columns",
        f"{quality['number_of_columns']:,}"
    )

with col3:
    st.metric(
        "🔢 Numerical Columns",
        f"{quality['numerical_count']:,}"
    )

with col4:
    st.metric(
        "🔤 Categorical Columns",
        f"{quality['categorical_count']:,}"
    )


col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "❌ Missing Cells",
        f"{quality['missing_cells']:,}"
    )

with col6:
    st.metric(
        "🔁 Duplicate Rows",
        f"{quality['duplicate_rows']:,}"
    )

with col7:
    st.metric(
        "💾 Memory Usage",
        f"{quality['memory_usage_mb']:.2f} MB"
    )

with col8:
    st.metric(
        "👥 Unique Customers",
        f"{quality['unique_customers']:,}"
    )


# =========================================================
# DATA COMPLETENESS
# =========================================================

st.subheader("📈 Dataset Completeness")

st.progress(
    int(quality["completeness"])
)

st.metric(
    "Data Completeness",
    f"{quality['completeness']:.2f}%"
)

st.divider()


# =========================================================
# COLUMN QUALITY TABLE
# =========================================================

st.subheader("📋 Column-Level Data Quality")

st.dataframe(
    quality["quality_table"],
    use_container_width=True,
    hide_index=True
)


# =========================================================
# DATA TYPE CHART
# =========================================================

st.subheader("🔤 Column Data Types")

dtype_data = (
    df.dtypes
    .astype(str)
    .value_counts()
    .reset_index()
)

dtype_data.columns = [
    "Data Type",
    "Number of Columns"
]

fig_dtype = px.bar(
    dtype_data,
    x="Data Type",
    y="Number of Columns",
    text="Number of Columns",
    title="Columns by Data Type"
)

st.plotly_chart(
    fig_dtype,
    use_container_width=True
)


# =========================================================
# MISSING VS AVAILABLE
# =========================================================

st.subheader("🧩 Missing vs Available Data")

total_cells = (
    quality["number_of_rows"]
    * quality["number_of_columns"]
)

available_cells = (
    total_cells
    - quality["missing_cells"]
)

missing_data = {
    "Status": [
        "Available",
        "Missing"
    ],
    "Cells": [
        available_cells,
        quality["missing_cells"]
    ]
}

fig_missing = px.bar(
    missing_data,
    x="Status",
    y="Cells",
    text="Cells",
    title="Available vs Missing Cells"
)

st.plotly_chart(
    fig_missing,
    use_container_width=True
)


# =========================================================
# TOP MISSING COLUMNS
# =========================================================

st.subheader("🚨 Top Missing Columns")

missing_df = quality["quality_table"][
    [
        "Column Name",
        "Missing Count",
        "Missing %"
    ]
].copy()

missing_df = missing_df[
    missing_df["Missing Count"] > 0
]

missing_df = missing_df.sort_values(
    "Missing %",
    ascending=False
).head(20)


if not missing_df.empty:

    fig_missing_columns = px.bar(
        missing_df.sort_values(
            "Missing %",
            ascending=True
        ),
        x="Missing %",
        y="Column Name",
        orientation="h",
        text="Missing %",
        title="Top 20 Columns by Missing Percentage"
    )

    st.plotly_chart(
        fig_missing_columns,
        use_container_width=True
    )

else:

    st.success(
        "✅ No missing values found."
    )


# =========================================================
# UNIQUE VALUES
# =========================================================

st.subheader("🔢 Unique Values by Column")

unique_df = quality["quality_table"][
    [
        "Column Name",
        "Unique Values"
    ]
].sort_values(
    "Unique Values",
    ascending=False
).head(20)


fig_unique = px.bar(
    unique_df.sort_values(
        "Unique Values",
        ascending=True
    ),
    x="Unique Values",
    y="Column Name",
    orientation="h",
    title="Top 20 Columns by Unique Values"
)

st.plotly_chart(
    fig_unique,
    use_container_width=True
)


# =========================================================
# DUPLICATE ANALYSIS
# =========================================================

st.subheader("🔁 Duplicate Analysis")

if quality["duplicate_rows"] == 0:

    st.success(
        "✅ No completely duplicated rows found."
    )

else:

    st.warning(
        f"⚠️ {quality['duplicate_rows']:,} "
        "duplicate rows found."
    )


# =========================================================
# HIGH MISSINGNESS
# =========================================================

st.subheader("🚨 High Missingness Columns")

high_missing = quality["quality_table"][
    quality["quality_table"]["Missing %"] >= 50
].sort_values(
    "Missing %",
    ascending=False
)


if high_missing.empty:

    st.success(
        "✅ No columns have 50% or more missing values."
    )

else:

    st.warning(
        f"⚠️ {len(high_missing)} columns "
        "have 50% or more missing values."
    )

    st.dataframe(
        high_missing[
            [
                "Column Name",
                "Data Type",
                "Missing Count",
                "Missing %",
                "Unique Values"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# CATEGORICAL FEATURES
# =========================================================

st.subheader("🔤 Categorical Feature Summary")

categorical_df = quality["quality_table"][
    quality["quality_table"]["Column Name"].isin(
        df.select_dtypes(
            exclude="number"
        ).columns
    )
][
    [
        "Column Name",
        "Data Type",
        "Unique Values",
        "Missing %"
    ]
]

st.dataframe(
    categorical_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# PREPROCESSING RECOMMENDATIONS
# =========================================================

st.subheader("🛠️ Preprocessing Recommendations")

if quality["missing_cells"] > 0:

    st.write(
        "🔹 Handle missing values using suitable "
        "imputation or missing-value strategies."
    )

if not high_missing.empty:

    st.write(
        "🔹 Review columns with extremely high "
        "missing percentages before analysis."
    )

if quality["duplicate_rows"] > 0:

    st.write(
        "🔹 Investigate and remove duplicate records."
    )

st.write(
    "🔹 Validate categorical values for inconsistent categories."
)

st.write(
    "🔹 Check numerical columns for incorrect data types."
)

st.write(
    "🔹 Perform outlier analysis before using numerical "
    "features for modeling."
)


# =========================================================
# FINAL SUMMARY
# =========================================================

st.subheader("💡 Quality Summary")

st.markdown(
    f"""
    - 📋 Dataset contains **{quality['number_of_rows']:,} rows**
      and **{quality['number_of_columns']:,} columns**.

    - 🔢 **{quality['numerical_count']:,} numerical** features
      and **{quality['categorical_count']:,} categorical** features.

    - ❌ Total missing cells:
      **{quality['missing_cells']:,}**.

    - 🔁 Duplicate rows:
      **{quality['duplicate_rows']:,}**.

    - 👥 Unique customers:
      **{quality['unique_customers']:,}**.

    - 📈 Overall data completeness:
      **{quality['completeness']:.2f}%**.
    """
)
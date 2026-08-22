import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.kpi import calculate_missing_value_metrics


st.set_page_config(
    page_title="Missing Value Analysis",
    page_icon="❌",
    layout="wide"
)

st.title("❌ Missing Value Analysis")

st.markdown(
    """
    Analyze missing values and identify columns that require
    preprocessing before further analysis or modeling.
    """
)

try:

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------

    df = load_data("data/application_train.csv")

    # --------------------------------------------------
    # CALCULATE MISSING VALUE METRICS
    # --------------------------------------------------

    missing = calculate_missing_value_metrics(df)

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

    st.subheader("📊 Missing Value KPIs")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "❌ Total Missing Values",
            f"{missing['total_missing']:,}"
        )

    with col2:
        st.metric(
            "📉 Missing Percentage",
            f"{missing['missing_percentage']:.2f}%"
        )

    with col3:
        st.metric(
            "📋 Columns with Missing Data",
            f"{missing['columns_with_missing']:,}"
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "⚠️ Columns ≥30% Missing",
            f"{missing['columns_above_30']:,}"
        )

    with col5:
        st.metric(
            "🚨 Columns ≥50% Missing",
            f"{missing['columns_above_50']:,}"
        )

    st.divider()

    # --------------------------------------------------
    # TOP 20 MISSING COLUMNS
    # --------------------------------------------------

    st.subheader("🚨 Top 20 Columns by Missing Percentage")

    top_missing = (
        missing["missing_table"]
        .head(20)
        .sort_values(
            "Missing %",
            ascending=True
        )
    )

    fig = px.bar(
        top_missing,
        x="Missing %",
        y="Column Name",
        orientation="h",
        text="Missing %",
        title="Top 20 Columns by Missing Percentage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # MISSING PERCENTAGE DISTRIBUTION
    # --------------------------------------------------

    st.subheader("📊 Missing Percentage Distribution")

    fig = px.histogram(
        missing["missing_table"],
        x="Missing %",
        nbins=20,
        title="Distribution of Missing Percentage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # MISSINGNESS CATEGORIES
    # --------------------------------------------------

    st.subheader("📂 Missingness Categories")

    fig = px.bar(
        missing["category_summary"],
        x="Missing Category",
        y="Number of Columns",
        text="Number of Columns",
        title="Columns by Missingness Category"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # MISSING VALUES BY DATA TYPE
    # --------------------------------------------------

    st.subheader("🔢 Missing Values by Data Type")

    fig = px.bar(
        missing["missing_by_dtype"],
        x="Data Type",
        y="Missing Values",
        text="Missing Values",
        title="Missing Values: Numerical vs Categorical"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # MISSINGNESS HEATMAP
    # --------------------------------------------------

    st.subheader("🔥 Missingness Heatmap")

    heatmap_columns = (
        missing["missing_table"]
        .head(25)["Column Name"]
        .tolist()
    )

    heatmap_data = (
        df[heatmap_columns]
        .isna()
        .astype(int)
        .head(500)
    )

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.T.values,
            x=list(range(len(heatmap_data))),
            y=heatmap_data.columns,
            colorscale="Blues"
        )
    )

    fig.update_layout(
        title="Missingness Pattern - Top 25 Columns",
        xaxis_title="Sample Rows",
        yaxis_title="Columns"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------
    # COLUMN LEVEL DETAILS
    # --------------------------------------------------

    st.subheader("📋 Column-Level Missing Value Details")

    st.dataframe(
        missing["missing_table"],
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # HIGH MISSINGNESS COLUMNS
    # --------------------------------------------------

    st.subheader("🚨 High Missingness Columns")

    high_missing = missing["missing_table"][
        missing["missing_table"]["Missing %"] >= 50
    ]

    if high_missing.empty:

        st.success(
            "✅ No columns have 50% or more missing values."
        )

    else:

        st.warning(
            f"⚠️ {len(high_missing)} columns have "
            "50% or more missing values."
        )

        st.dataframe(
            high_missing,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------
    # PREPROCESSING RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader("🛠️ Preprocessing Recommendations")

    if missing["total_missing"] == 0:

        st.success(
            "✅ No missing values detected."
        )

    else:

        st.write(
            "🔹 Review columns with high missing percentages."
        )

        st.write(
            "🔹 Consider median imputation for suitable numerical columns."
        )

        st.write(
            "🔹 Consider mode imputation for suitable categorical columns."
        )

        st.write(
            "🔹 Evaluate extremely high-missing columns for removal."
        )

        st.write(
            "🔹 Create missing-value indicators where missingness "
            "itself may contain business information."
        )

    # --------------------------------------------------
    # SUMMARY TABLE
    # --------------------------------------------------

    st.subheader("💡 Missing Value Summary")

    summary_df = {
        "Metric": [
            "Total Missing Values",
            "Overall Missing Percentage",
            "Columns with Missing Data",
            "Columns ≥30% Missing",
            "Columns ≥50% Missing"
        ],
        "Value": [
            f"{missing['total_missing']:,}",
            f"{missing['missing_percentage']:.2f}%",
            f"{missing['columns_with_missing']:,}",
            f"{missing['columns_above_30']:,}",
            f"{missing['columns_above_50']:,}"
        ]
    }

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True
    )


except FileNotFoundError:

    st.error(
        "Dataset file not found. Add "
        "`data/application_train.csv`."
    )

except Exception as e:

    st.error(
        f"An error occurred: {e}"
    )
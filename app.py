import streamlit as st
import pandas as pd

from utils.data_loader import load_data

from utils.features import (
    create_customer_features
)

from utils.kpi import (
    dataset_overview,
    calculate_home_metrics,
    display_metrics
)

from utils.charts import (
    bar_chart,
    scatter_chart
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="🏦 Home Credit Loan Risk Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# HOME PAGE
# ==================================================

st.title("🏦 Home Credit Loan Risk Analysis")

st.markdown(
    """
    Welcome to the comprehensive **🏦 Home Credit Loan Risk Analysis**
    dashboard with **20 detailed analysis pages**.

    Use the sidebar navigation to explore different aspects
    of the Home Credit loan data.

    ### Modules

    - 📖 Data Understanding & Preprocessing
    - ❓ Missing Value & Duplicate Analysis
    - 📊 Outlier Detection & Feature Engineering
    - 📈 Univariate, Bivariate & Multivariate Analysis
    - 👥 Customer Analysis
    - 💳 Loan Analysis
    - 📜 Credit History Analysis
    - 💰 Repayment Analysis
    - ⚠️ Default Risk Analysis
    - 💡 Business Insights & Recommendations
    """
)


# ==================================================
# DASHBOARD OVERVIEW
# ==================================================

with st.expander("📋 Dashboard Overview"):

    st.write(
        """
        **20 Pages Available:**

        01_Executive_Overview.py  
        02_Data_Quality.py  
        03_Missing_Value_Analysis.py  
        04_Outlier_Analysis.py  
        05_Customer_Demographics.py  
        06_Income_Analysis.py  
        07_Employment_Analysis.py  
        08_Family_Housing_Analysis.py  
        09_Loan_Application_Analysis.py  
        10_Credit_Affordability.py  
        11_Default_Risk_EDA.py  
        12_Risk_Factor_Analysis.py  
        13_Bureau_Credit_History.py  
        14_Bureau_Balance_Analysis.py  
        15_Previous_Applications.py  
        16_POS_CASH_Analysis.py  
        17_Installment_Payment_Analysis.py  
        18_Credit_Card_Analysis.py  
        19_Customer_Risk_Segmentation.py  
        20_Executive_Insights_Recommendations.py
        """
    )


# ==================================================
# DATASET INFORMATION
# ==================================================

with st.expander("📊 Dataset and Instructions"):

    st.write(
        """
        **Home Credit Default Risk Dataset**

        🏦 307,511 loan applications

        🔢 122 features covering customer and loan information

        👤 Customer details: Age, gender, education, family and employment

        💰 Financial details: Income, credit amount and annuity

        💳 Loan details: Contract type and credit characteristics

        🎯 Risk Target: TARGET

        0 → No payment difficulties

        1 → Payment difficulties

        💡 Objective: Identify key factors associated with loan repayment risk.
        """
    )


# ==================================================
# RELOAD DATA
# ==================================================

if st.button("🔄 Reload Data"):
    st.rerun()


# ==================================================
# EXECUTIVE SUMMARY
# ==================================================

st.header("Executive Summary")


try:

    # ==================================================
    # LOAD APPLICATION DATA
    # ==================================================

    df = load_data(
        "data/application_train.csv"
    )


    # ==================================================
    # CUSTOMER FEATURES
    # ==================================================

    df = create_customer_features(df)


    # ==================================================
    # INCOME GROUP
    # ==================================================

    if "AMT_INCOME_TOTAL" in df.columns:

        df["INCOME_GROUP"] = pd.qcut(
            df["AMT_INCOME_TOTAL"],
            q=4,
            labels=[
                "Low",
                "Medium",
                "High",
                "Very High"
            ],
            duplicates="drop"
        )


    # ==================================================
    # DATASET OVERVIEW
    # ==================================================

    st.subheader("📊 Dataset Overview")

    metrics = dataset_overview(df)

    display_metrics(metrics)


    # ==================================================
    # KEY SNAPSHOT
    # ==================================================

    st.subheader("📈 Key Snapshot")

    summary = calculate_home_metrics(df)


    # ==================================================
    # FIRST KPI ROW
    # ==================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📋 Total Applications",
            f"{summary['total_applications']:,}"
        )

    with col2:

        st.metric(
            "💰 Total Credit Amount",
            f"{summary['total_credit_amount']:,.0f}"
        )

    with col3:

        st.metric(
            "💳 Average Credit Amount",
            f"{summary['average_credit_amount']:,.0f}"
        )


    # ==================================================
    # SECOND KPI ROW
    # ==================================================

    col4, col5, col6 = st.columns(3)

    with col4:

        st.metric(
            "⚠️ Payment Difficulties",
            f"{summary['payment_difficulties']:,}"
        )

    with col5:

        st.metric(
            "📉 Default Rate",
            f"{summary['default_rate']:.2f}%"
        )

    with col6:

        st.metric(
            "✅ Data Completeness",
            f"{summary['data_completeness']:.2f}%"
        )


    st.divider()


    # ==================================================
    # QUICK INSIGHTS
    # ==================================================

    st.subheader("📊 Quick Insights")


    # ==================================================
    # DEFAULT BY INCOME GROUP
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        if "INCOME_GROUP" in df.columns:

            st.plotly_chart(
                bar_chart(
                    df,
                    "INCOME_GROUP",
                    "TARGET",
                    "Default Count by Income Group",
                    aggfunc="sum"
                ),
                use_container_width=True
            )


    # ==================================================
    # DEFAULT BY CONTRACT TYPE
    # ==================================================

    with col2:

        st.plotly_chart(
            bar_chart(
                df,
                "NAME_CONTRACT_TYPE",
                "TARGET",
                "Default Count by Contract Type",
                aggfunc="sum"
            ),
            use_container_width=True
        )


    # ==================================================
    # DEFAULT BY AGE GROUP
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        if "AGE_GROUP" in df.columns:

            st.plotly_chart(
                bar_chart(
                    df,
                    "AGE_GROUP",
                    "TARGET",
                    "Default Count by Age Group",
                    aggfunc="sum"
                ),
                use_container_width=True
            )


    # ==================================================
    # INCOME VS CREDIT
    # ==================================================

    with col2:

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
    # DATA PREVIEW
    # ==================================================

    st.divider()

    st.subheader("📋 Application Data Preview")

    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# ERROR HANDLING
# ==================================================

except FileNotFoundError:

    st.error(
        "❌ application_train.csv not found "
        "in the data folder."
    )

    st.info(
        "Please add application_train.csv "
        "inside the data folder."
    )


except KeyError as e:

    st.error(
        f"❌ Required column is missing: {e}"
    )

    st.info(
        "Please check the column names "
        "in application_train.csv."
    )


except Exception as e:

    st.error(
        f"❌ An error occurred: {e}"
    )
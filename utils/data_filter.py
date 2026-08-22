import streamlit as st
import pandas as pd


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:

    st.sidebar.header("🎛️ Common Filters")

    #  --------------------------------------------------
    # 1. Loan Type
    # --------------------------------------------------

    loan_types = st.sidebar.multiselect(
        "🏦 Loan Type",
        options=sorted(df["NAME_CONTRACT_TYPE"].dropna().unique()),
        default=sorted(df["NAME_CONTRACT_TYPE"].dropna().unique())
    )

    # --------------------------------------------------
    # 2. Gender
    # --------------------------------------------------

    genders = st.sidebar.multiselect(
        "👤 Gender",
        options=sorted(df["CODE_GENDER"].dropna().unique()),
        default=sorted(df["CODE_GENDER"].dropna().unique())
    )

    # --------------------------------------------------
    # 3. Car Ownership
    # --------------------------------------------------

    car_ownership = st.sidebar.multiselect(
        "🚗 Car Ownership",
        options=sorted(df["FLAG_OWN_CAR"].dropna().unique()),
        default=sorted(df["FLAG_OWN_CAR"].dropna().unique())
    )

    # --------------------------------------------------
    # 4. Property Ownership
    # --------------------------------------------------

    property_ownership = st.sidebar.multiselect(
        "🏠 Property Ownership",
        options=sorted(df["FLAG_OWN_REALTY"].dropna().unique()),
        default=sorted(df["FLAG_OWN_REALTY"].dropna().unique())
    )

    # --------------------------------------------------
    # 5. Income Range
    # --------------------------------------------------

    min_income = float(df["AMT_INCOME_TOTAL"].min())
    max_income = float(df["AMT_INCOME_TOTAL"].max())

    income_range = st.sidebar.slider(
        "💰 Income Range",
        min_value=min_income,
        max_value=max_income,
        value=(min_income, max_income)
    )

    # --------------------------------------------------
    # 6. Credit Amount Range
    # --------------------------------------------------

    min_credit = float(df["AMT_CREDIT"].min())
    max_credit = float(df["AMT_CREDIT"].max())

    credit_range = st.sidebar.slider(
        "💳 Credit Amount",
        min_value=min_credit,
        max_value=max_credit,
        value=(min_credit, max_credit)
    )

    # --------------------------------------------------
    # 7. Risk Status
    # --------------------------------------------------

    risk_status = st.sidebar.multiselect(
        "🎯 Risk Status",
        options=[0, 1],
        default=[0, 1],
        format_func=lambda x: (
            "No Payment Difficulties"
            if x == 0
            else "Payment Difficulties"
        )
    )

    # --------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------

    filtered_df = df[
        df["NAME_CONTRACT_TYPE"].isin(loan_types)
        & df["CODE_GENDER"].isin(genders)
        & df["FLAG_OWN_CAR"].isin(car_ownership)
        & df["FLAG_OWN_REALTY"].isin(property_ownership)
        & df["AMT_INCOME_TOTAL"].between(
            income_range[0],
            income_range[1]
        )
        & df["AMT_CREDIT"].between(
            credit_range[0],
            credit_range[1]
        )
        & df["TARGET"].isin(risk_status)
    ].copy()

    return filtered_df
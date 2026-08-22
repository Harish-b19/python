import pandas as pd
import streamlit as st


# =========================================================
# PAGE 1 – EXECUTIVE OVERVIEW
# =========================================================

def dataset_overview(df):

    financial_features = [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "AMT_GOODS_PRICE"
    ]

    customer_features = [
        "CODE_GENDER",
        "CNT_CHILDREN",
        "CNT_FAM_MEMBERS",
        "NAME_FAMILY_STATUS",
        "NAME_EDUCATION_TYPE",
        "NAME_INCOME_TYPE",
        "NAME_HOUSING_TYPE",
        "DAYS_BIRTH",
        "DAYS_EMPLOYED",
        "OCCUPATION_TYPE"
    ]

    loan_features = [
        "NAME_CONTRACT_TYPE",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "AMT_GOODS_PRICE"
    ]

    overview = {
        "Total Applications": df["SK_ID_CURR"].nunique(),

        "Total Features": df.shape[1],

        "Financial Features": len(
            [
                col
                for col in financial_features
                if col in df.columns
            ]
        ),

        "Customer Features": len(
            [
                col
                for col in customer_features
                if col in df.columns
            ]
        ),

        "Loan Features": len(
            [
                col
                for col in loan_features
                if col in df.columns
            ]
        ),

        "Loan Types": (
            df["NAME_CONTRACT_TYPE"].nunique()
            if "NAME_CONTRACT_TYPE" in df.columns
            else 0
        ),

        "Gender Categories": (
            df["CODE_GENDER"].nunique()
            if "CODE_GENDER" in df.columns
            else 0
        ),

        "Risk Target": (
            "TARGET"
            if "TARGET" in df.columns
            else "Not Available"
        )
    }

    return overview


# =========================================================
# PAGE 1 – HOME CREDIT KPI CALCULATIONS
# =========================================================

def calculate_home_metrics(df):

    total_applications = df["SK_ID_CURR"].nunique()

    total_credit_amount = df["AMT_CREDIT"].sum()

    average_credit_amount = df["AMT_CREDIT"].mean()

    payment_difficulties = (
        (df["TARGET"] == 1).sum()
        if "TARGET" in df.columns
        else 0
    )

    default_rate = (
        df["TARGET"].mean() * 100
        if "TARGET" in df.columns
        else 0
    )

    data_completeness = (
        (1 - df.isna().mean().mean()) * 100
    )

    return {
        "total_applications": total_applications,
        "total_credit_amount": total_credit_amount,
        "average_credit_amount": average_credit_amount,
        "payment_difficulties": payment_difficulties,
        "default_rate": default_rate,
        "data_completeness": data_completeness
    }


# =========================================================
# PAGE 2 – DATA QUALITY CALCULATIONS
# =========================================================

def calculate_data_quality(df):

    number_of_rows = len(df)

    number_of_columns = df.shape[1]

    numerical_count = len(
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_count = len(
        df.select_dtypes(
            exclude="number"
        ).columns
    )

    missing_cells = int(
        df.isna().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    memory_usage_mb = (
        df.memory_usage(
            deep=True
        ).sum()
        / (1024 ** 2)
    )

    unique_customers = (
        df["SK_ID_CURR"].nunique()
        if "SK_ID_CURR" in df.columns
        else 0
    )

    total_cells = (
        number_of_rows * number_of_columns
    )

    completeness = (
        (total_cells - missing_cells)
        / total_cells
        * 100
        if total_cells > 0
        else 0
    )

    # -----------------------------------------------------
    # COLUMN LEVEL QUALITY
    # -----------------------------------------------------

    quality_data = []

    for column in df.columns:

        series = df[column]

        row = {
            "Column Name": column,

            "Data Type": str(
                series.dtype
            ),

            "Missing Count": int(
                series.isna().sum()
            ),

            "Missing %": round(
                series.isna().mean() * 100,
                2
            ),

            "Unique Values": int(
                series.nunique(
                    dropna=True
                )
            )
        }

        # Numerical statistics
        if pd.api.types.is_numeric_dtype(series):

            row["Minimum"] = series.min()

            row["Maximum"] = series.max()

            row["Mean"] = series.mean()

            row["Median"] = series.median()

        else:

            row["Minimum"] = None

            row["Maximum"] = None

            row["Mean"] = None

            row["Median"] = None

        quality_data.append(row)

    quality_table = pd.DataFrame(
        quality_data
    )

    return {
        "number_of_rows": number_of_rows,

        "number_of_columns": number_of_columns,

        "numerical_count": numerical_count,

        "categorical_count": categorical_count,

        "missing_cells": missing_cells,

        "duplicate_rows": duplicate_rows,

        "memory_usage_mb": memory_usage_mb,

        "unique_customers": unique_customers,

        "completeness": completeness,

        "quality_table": quality_table
    }


# =========================================================
# PAGE 3 – MISSING VALUE ANALYSIS
# =========================================================

def calculate_missing_value_metrics(df):

    # -----------------------------------------------------
    # OVERALL MISSING VALUE METRICS
    # -----------------------------------------------------

    total_cells = (
        df.shape[0] * df.shape[1]
    )

    total_missing = int(
        df.isna().sum().sum()
    )

    missing_percentage = (
        total_missing / total_cells * 100
        if total_cells > 0
        else 0
    )

    columns_with_missing = int(
        (df.isna().sum() > 0).sum()
    )

    columns_above_30 = int(
        (df.isna().mean() * 100 >= 30).sum()
    )

    columns_above_50 = int(
        (df.isna().mean() * 100 >= 50).sum()
    )

    # -----------------------------------------------------
    # COLUMN LEVEL MISSING ANALYSIS
    # -----------------------------------------------------

    missing_table = pd.DataFrame({

        "Column Name":
            df.columns,

        "Missing Count":
            df.isna().sum().values,

        "Missing %":
            df.isna().mean().values * 100
    })

    missing_table["Missing %"] = (
        missing_table["Missing %"]
        .round(2)
    )

    missing_table = (
        missing_table
        .sort_values(
            "Missing %",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # -----------------------------------------------------
    # MISSINGNESS CATEGORIES
    # -----------------------------------------------------

    def missing_category(value):

        if value <= 5:
            return "0–5%"

        elif value <= 20:
            return "5–20%"

        elif value <= 40:
            return "20–40%"

        elif value <= 60:
            return "40–60%"

        else:
            return "60%+"

    missing_table["Missing Category"] = (
        missing_table["Missing %"]
        .apply(missing_category)
    )

    # -----------------------------------------------------
    # MISSING VALUES BY DATA TYPE
    # -----------------------------------------------------

    numeric_columns = (
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_columns = (
        df.select_dtypes(
            exclude="number"
        ).columns
    )

    numeric_missing = int(
        df[numeric_columns]
        .isna()
        .sum()
        .sum()
    )

    categorical_missing = int(
        df[categorical_columns]
        .isna()
        .sum()
        .sum()
    )

    missing_by_dtype = pd.DataFrame({

        "Data Type": [
            "Numerical",
            "Categorical"
        ],

        "Missing Values": [
            numeric_missing,
            categorical_missing
        ]
    })

    # -----------------------------------------------------
    # CATEGORY SUMMARY
    # -----------------------------------------------------

    category_summary = (
        missing_table["Missing Category"]
        .value_counts()
        .reindex(
            [
                "0–5%",
                "5–20%",
                "20–40%",
                "40–60%",
                "60%+"
            ],
            fill_value=0
        )
        .reset_index()
    )

    category_summary.columns = [
        "Missing Category",
        "Number of Columns"
    ]

    return {

        "total_missing":
            total_missing,

        "missing_percentage":
            missing_percentage,

        "columns_with_missing":
            columns_with_missing,

        "columns_above_30":
            columns_above_30,

        "columns_above_50":
            columns_above_50,

        "missing_table":
            missing_table,

        "missing_by_dtype":
            missing_by_dtype,

        "category_summary":
            category_summary
    }

# =========================================================
# PAGE 4 – OUTLIER & DISTRIBUTION ANALYSIS
# =========================================================

def calculate_outlier_metrics(df):
    
    numerical_columns = [
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
        "AMT_ANNUITY",
        "AMT_GOODS_PRICE",
        "DAYS_BIRTH",
        "DAYS_EMPLOYED",
        "CNT_CHILDREN",
        "CNT_FAM_MEMBERS"
    ]

    # Keep only columns that exist in dataset
    available_columns = [
        col for col in numerical_columns
        if col in df.columns
    ]

    # Count numerical columns
    number_of_numerical_columns = len(
        df.select_dtypes(include="number").columns
    )

    # Outlier calculation using IQR
    outlier_data = []

    for column in available_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = series[
            (series < lower_bound) |
            (series > upper_bound)
        ]

        outlier_data.append({
            "Column": column,
            "Q1": Q1,
            "Q3": Q3,
            "IQR": IQR,
            "Lower Bound": lower_bound,
            "Upper Bound": upper_bound,
            "Outlier Count": len(outliers),
            "Outlier %": round(
                len(outliers) / len(series) * 100,
                2
            )
        })

    outlier_table = pd.DataFrame(outlier_data)

    variables_with_outliers = int(
        (outlier_table["Outlier Count"] > 0).sum()
    ) if not outlier_table.empty else 0

    # Maximum values
    maximum_income = (
        df["AMT_INCOME_TOTAL"].max()
        if "AMT_INCOME_TOTAL" in df.columns
        else 0
    )

    maximum_credit = (
        df["AMT_CREDIT"].max()
        if "AMT_CREDIT" in df.columns
        else 0
    )

    maximum_annuity = (
        df["AMT_ANNUITY"].max()
        if "AMT_ANNUITY" in df.columns
        else 0
    )

    return {
        "number_of_numerical_columns":
            number_of_numerical_columns,

        "variables_with_outliers":
            variables_with_outliers,

        "maximum_income":
            maximum_income,

        "maximum_credit":
            maximum_credit,

        "maximum_annuity":
            maximum_annuity,

        "outlier_table":
            outlier_table
    }
def display_metrics(metrics):
    
    st.subheader("📋 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📋 Total Applications",
            f"{metrics['Total Applications']:,}"
        )

    with col2:
        st.metric(
            "🔢 Total Features",
            metrics["Total Features"]
        )

    with col3:
        st.metric(
            "💰 Financial Features",
            metrics["Financial Features"]
        )

    with col4:
        st.metric(
            "💳 Loan Features",
            metrics["Loan Features"]
        )

# =========================================================
# PAGE 5 – CUSTOMER DEMOGRAPHIC KPI CALCULATIONS
# =========================================================

def calculate_customer_metrics(df):

    # -----------------------------------------------------
    # AGE
    # -----------------------------------------------------

    average_age = (
        df["AGE"].mean()
        if "AGE" in df.columns
        else 0
    )

    median_age = (
        df["AGE"].median()
        if "AGE" in df.columns
        else 0
    )

    # -----------------------------------------------------
    # MOST COMMON GENDER
    # -----------------------------------------------------

    most_common_gender = (
        df["CODE_GENDER"].mode().iloc[0]
        if "CODE_GENDER" in df.columns
        and not df["CODE_GENDER"].mode().empty
        else "Not Available"
    )

    # -----------------------------------------------------
    # MOST COMMON EDUCATION
    # -----------------------------------------------------

    most_common_education = (
        df["NAME_EDUCATION_TYPE"].mode().iloc[0]
        if "NAME_EDUCATION_TYPE" in df.columns
        and not df["NAME_EDUCATION_TYPE"].mode().empty
        else "Not Available"
    )

    # -----------------------------------------------------
    # MOST COMMON INCOME TYPE
    # -----------------------------------------------------

    most_common_income_type = (
        df["NAME_INCOME_TYPE"].mode().iloc[0]
        if "NAME_INCOME_TYPE" in df.columns
        and not df["NAME_INCOME_TYPE"].mode().empty
        else "Not Available"
    )

    # -----------------------------------------------------
    # MOST COMMON FAMILY STATUS
    # -----------------------------------------------------

    most_common_family_status = (
        df["NAME_FAMILY_STATUS"].mode().iloc[0]
        if "NAME_FAMILY_STATUS" in df.columns
        and not df["NAME_FAMILY_STATUS"].mode().empty
        else "Not Available"
    )

    return {

        "average_age":
            average_age,

        "median_age":
            median_age,

        "most_common_gender":
            most_common_gender,

        "most_common_education":
            most_common_education,

        "most_common_income_type":
            most_common_income_type,

        "most_common_family_status":
            most_common_family_status
    }
def calculate_income_metrics(df):
    
    average_income = (
        df["AMT_INCOME_TOTAL"].mean()
    )

    median_income = (
        df["AMT_INCOME_TOTAL"].median()
    )

    maximum_income = (
        df["AMT_INCOME_TOTAL"].max()
    )

    average_income_per_family = (
        df["INCOME_PER_FAMILY_MEMBER"].mean()
    )

    largest_income_group = (
        df["INCOME_GROUP"]
        .value_counts()
        .idxmax()
    )

    return {
        "average_income": average_income,
        "median_income": median_income,
        "maximum_income": maximum_income,
        "average_income_per_family": average_income_per_family,
        "largest_income_group": largest_income_group
    }
# =========================================================
# EMPLOYMENT KPI CALCULATIONS
# =========================================================

def calculate_employment_metrics(df):

    # -----------------------------------------------------
    # Normal employment records only
    # -----------------------------------------------------

    normal_employment = df[
        df["EMPLOYMENT_YEARS"].notna()
    ]

    # -----------------------------------------------------
    # Average Employment Years
    # -----------------------------------------------------

    average_employment_years = (
        normal_employment["EMPLOYMENT_YEARS"].mean()
    )

    # -----------------------------------------------------
    # Median Employment Years
    # -----------------------------------------------------

    median_employment_years = (
        normal_employment["EMPLOYMENT_YEARS"].median()
    )

    # -----------------------------------------------------
    # Most Common Occupation
    # -----------------------------------------------------

    most_common_occupation = (
        df["OCCUPATION_TYPE"]
        .dropna()
        .mode()
    )

    if not most_common_occupation.empty:
        most_common_occupation = (
            most_common_occupation.iloc[0]
        )
    else:
        most_common_occupation = "Not Available"

    # -----------------------------------------------------
    # Most Common Organization Type
    # -----------------------------------------------------

    most_common_organization = (
        df["ORGANIZATION_TYPE"]
        .dropna()
        .mode()
    )

    if not most_common_organization.empty:
        most_common_organization = (
            most_common_organization.iloc[0]
        )
    else:
        most_common_organization = "Not Available"

    # -----------------------------------------------------
    # Default Rate by Employment Group
    # -----------------------------------------------------

    default_by_group = (
        df.groupby(
            "EMPLOYMENT_GROUP",
            observed=True
        )["TARGET"]
        .mean()
        .mul(100)
    )

    # Highest Default Employment Group
    if not default_by_group.empty:

        highest_default_group = (
            default_by_group.idxmax()
        )

    else:

        highest_default_group = "Not Available"

    return {

        "average_employment_years":
            average_employment_years,

        "median_employment_years":
            median_employment_years,

        "most_common_occupation":
            most_common_occupation,

        "most_common_organization":
            most_common_organization,

        "highest_default_group":
            highest_default_group,

        "default_by_group":
            default_by_group
    }
# =========================================================
# FAMILY & HOUSING KPI CALCULATIONS
# =========================================================

def calculate_family_housing_metrics(df):

    # Average family size
    average_family_size = (
        df["CNT_FAM_MEMBERS"].mean()
        if "CNT_FAM_MEMBERS" in df.columns
        else 0
    )

    # Average number of children
    average_children = (
        df["CNT_CHILDREN"].mean()
        if "CNT_CHILDREN" in df.columns
        else 0
    )

    # Home ownership percentage
    if "FLAG_OWN_REALTY" in df.columns:
        home_ownership_percentage = (
            (df["FLAG_OWN_REALTY"] == "Y").mean() * 100
        )
    else:
        home_ownership_percentage = 0

    # Car ownership percentage
    if "FLAG_OWN_CAR" in df.columns:
        car_ownership_percentage = (
            (df["FLAG_OWN_CAR"] == "Y").mean() * 100
        )
    else:
        car_ownership_percentage = 0

    # Most common housing type
    if "NAME_HOUSING_TYPE" in df.columns:
        most_common_housing_type = (
            df["NAME_HOUSING_TYPE"]
            .mode()
            .iloc[0]
        )
    else:
        most_common_housing_type = "Not Available"

    return {
        "average_family_size": average_family_size,
        "average_children": average_children,
        "home_ownership_percentage":
            home_ownership_percentage,
        "car_ownership_percentage":
            car_ownership_percentage,
        "most_common_housing_type":
            most_common_housing_type
    }

# =========================================================
# CURRENT LOAN APPLICATION METRICS
# =========================================================

def calculate_loan_application_metrics(df):

    total_applications = (
        df["SK_ID_CURR"].nunique()
        if "SK_ID_CURR" in df.columns
        else len(df)
    )

    average_credit = (
        df["AMT_CREDIT"].mean()
        if "AMT_CREDIT" in df.columns
        else 0
    )

    median_credit = (
        df["AMT_CREDIT"].median()
        if "AMT_CREDIT" in df.columns
        else 0
    )

    average_annuity = (
        df["AMT_ANNUITY"].mean()
        if "AMT_ANNUITY" in df.columns
        else 0
    )

    average_goods_price = (
        df["AMT_GOODS_PRICE"].mean()
        if "AMT_GOODS_PRICE" in df.columns
        else 0
    )

    most_common_contract_type = (
        df["NAME_CONTRACT_TYPE"].mode().iloc[0]
        if "NAME_CONTRACT_TYPE" in df.columns
        and not df["NAME_CONTRACT_TYPE"].mode().empty
        else "Not Available"
    )

    return {
        "total_applications": total_applications,
        "average_credit": average_credit,
        "median_credit": median_credit,
        "average_annuity": average_annuity,
        "average_goods_price": average_goods_price,
        "most_common_contract_type": most_common_contract_type
    }
def calculate_credit_affordability_metrics(df):
    
    credit_to_income = df["CREDIT_TO_INCOME_RATIO"].dropna()
    annuity_to_income = df["ANNUITY_TO_INCOME_RATIO"].dropna()

    # -----------------------------------------
    # Dynamic high-burden thresholds
    # -----------------------------------------
    # Using 90th percentile avoids inventing
    # an arbitrary business threshold.
    credit_burden_threshold = credit_to_income.quantile(0.90)
    annuity_burden_threshold = annuity_to_income.quantile(0.90)

    high_credit_burden = int(
        (credit_to_income >= credit_burden_threshold).sum()
    )

    high_annuity_burden = int(
        (annuity_to_income >= annuity_burden_threshold).sum()
    )

    return {
        "average_credit_to_income_ratio":
            credit_to_income.mean(),

        "median_credit_to_income_ratio":
            credit_to_income.median(),

        "average_annuity_to_income_ratio":
            annuity_to_income.mean(),

        "high_credit_burden":
            high_credit_burden,

        "high_annuity_burden":
            high_annuity_burden,

        "credit_burden_threshold":
            credit_burden_threshold,

        "annuity_burden_threshold":
            annuity_burden_threshold
    }

def calculate_default_risk_metrics(df):
    
    # -----------------------------------------
    # Default / Non-default counts
    # -----------------------------------------

    default_customers = int(
        (df["TARGET"] == 1).sum()
    )

    non_default_customers = int(
        (df["TARGET"] == 0).sum()
    )

    total_customers = (
        default_customers +
        non_default_customers
    )

    default_rate = (
        default_customers / total_customers * 100
        if total_customers > 0
        else 0
    )

    # -----------------------------------------
    # Highest Risk Age Group
    # -----------------------------------------

    age_risk = (
        df.groupby("AGE_GROUP", observed=True)["TARGET"]
        .mean()
        .sort_values(ascending=False)
    )

    highest_risk_age_group = (
        age_risk.index[0]
        if not age_risk.empty
        else "Not Available"
    )

    # -----------------------------------------
    # Highest Risk Income Group
    # -----------------------------------------

    income_risk = (
        df.groupby("INCOME_GROUP", observed=True)["TARGET"]
        .mean()
        .sort_values(ascending=False)
    )

    highest_risk_income_group = (
        income_risk.index[0]
        if not income_risk.empty
        else "Not Available"
    )

    # -----------------------------------------
    # Highest Risk Employment Group
    # -----------------------------------------

    employment_risk = (
        df.groupby(
            "EMPLOYMENT_GROUP",
            observed=True
        )["TARGET"]
        .mean()
        .sort_values(ascending=False)
    )

    highest_risk_employment_group = (
        employment_risk.index[0]
        if not employment_risk.empty
        else "Not Available"
    )

    return {
        "default_customers":
            default_customers,

        "non_default_customers":
            non_default_customers,

        "default_rate":
            default_rate,

        "highest_risk_age_group":
            highest_risk_age_group,

        "highest_risk_income_group":
            highest_risk_income_group,

        "highest_risk_employment_group":
            highest_risk_employment_group
    }

# =========================================================
# BUREAU CREDIT HISTORY METRICS
# =========================================================

def calculate_bureau_metrics(df):
    
    return {
        "bureau_accounts": df["SK_ID_BUREAU"].nunique(),

        "customers_with_bureau_history":
            df["SK_ID_CURR"].nunique(),

        "active_credits":
            (df["CREDIT_ACTIVE"] == "Active").sum(),

        "closed_credits":
            (df["CREDIT_ACTIVE"] == "Closed").sum(),

        "total_bureau_debt":
            df["AMT_CREDIT_SUM_DEBT"].sum(),

        "total_overdue_amount":
            df["AMT_CREDIT_SUM_OVERDUE"].sum()
    }



def calculate_previous_application_metrics(df):
    
    previous_applications = len(df)

    approved_applications = (
        df["NAME_CONTRACT_STATUS"]
        .eq("Approved")
        .sum()
    )

    refused_applications = (
        df["NAME_CONTRACT_STATUS"]
        .eq("Refused")
        .sum()
    )

    cancelled_applications = (
        df["NAME_CONTRACT_STATUS"]
        .eq("Canceled")
        .sum()
    )

    approval_rate = (
        approved_applications
        / previous_applications
        * 100
        if previous_applications > 0
        else 0
    )

    rejection_rate = (
        refused_applications
        / previous_applications
        * 100
        if previous_applications > 0
        else 0
    )

    return {
        "previous_applications": previous_applications,
        "approved_applications": approved_applications,
        "refused_applications": refused_applications,
        "cancelled_applications": cancelled_applications,
        "approval_rate": approval_rate,
        "rejection_rate": rejection_rate
    }
def calculate_pos_cash_metrics(df):
    
    pos_cash_records = len(df)

    active_contracts = (
        df["NAME_CONTRACT_STATUS"]
        .eq("Active")
        .sum()
    )

    completed_contracts = (
        df["NAME_CONTRACT_STATUS"]
        .eq("Completed")
        .sum()
    )

    average_installments_remaining = (
        df["CNT_INSTALMENT_FUTURE"]
        .mean()
    )

    customers_with_dpd = (
        df.loc[
            df["SK_DPD"] > 0,
            "SK_ID_CURR"
        ]
        .nunique()
    )

    return {
        "pos_cash_records": pos_cash_records,
        "active_contracts": active_contracts,
        "completed_contracts": completed_contracts,
        "average_installments_remaining":
            average_installments_remaining,
        "customers_with_dpd":
            customers_with_dpd
    }
def calculate_installment_payment_metrics(df):
    
    total_installments = len(df)

    average_installment = (
        df["AMT_INSTALMENT"]
        .mean()
    )

    average_payment = (
        df["AMT_PAYMENT"]
        .mean()
    )

    on_time_count = (
        df["PAYMENT_DELAY"] == 0
    ).sum()

    late_count = (
        df["PAYMENT_DELAY"] > 0
    ).sum()

    underpayment_count = (
        df["PAYMENT_RATIO"] < 1
    ).sum()

    on_time_payment_percentage = (
        on_time_count
        / total_installments
        * 100
        if total_installments > 0
        else 0
    )

    late_payment_percentage = (
        late_count
        / total_installments
        * 100
        if total_installments > 0
        else 0
    )

    underpayment_percentage = (
        underpayment_count
        / total_installments
        * 100
        if total_installments > 0
        else 0
    )

    average_delay_days = (
        df["PAYMENT_DELAY"]
        .mean()
    )

    return {
        "total_installments": total_installments,
        "average_installment": average_installment,
        "average_payment": average_payment,
        "on_time_payment_percentage":
            on_time_payment_percentage,
        "late_payment_percentage":
            late_payment_percentage,
        "underpayment_percentage":
            underpayment_percentage,
        "average_delay_days":
            average_delay_days
    }

def calculate_credit_card_metrics(df):
    
    credit_card_customers = (
        df["SK_ID_CURR"]
        .nunique()
    )

    average_balance = (
        df["AMT_BALANCE"]
        .mean()
    )

    average_credit_limit = (
        df["AMT_CREDIT_LIMIT_ACTUAL"]
        .mean()
    )

    average_utilization = (
        df["CREDIT_UTILIZATION"]
        .mean()
        * 100
    )

    average_monthly_payment = (
        df["AMT_PAYMENT_CURRENT"]
        .mean()
    )

    customers_with_dpd = (
        df.loc[
            df["SK_DPD"] > 0,
            "SK_ID_CURR"
        ]
        .nunique()
    )

    return {
        "credit_card_customers":
            credit_card_customers,

        "average_balance":
            average_balance,

        "average_credit_limit":
            average_credit_limit,

        "average_utilization":
            average_utilization,

        "average_monthly_payment":
            average_monthly_payment,

        "customers_with_dpd":
            customers_with_dpd
    }

def calculate_risk_segmentation_metrics(df):
    
    low_risk = (
        df["OBSERVED_RISK_SEGMENT"]
        .eq("Low Observed Risk")
        .sum()
    )

    moderate_risk = (
        df["OBSERVED_RISK_SEGMENT"]
        .eq("Moderate Observed Risk")
        .sum()
    )

    elevated_risk = (
        df["OBSERVED_RISK_SEGMENT"]
        .eq("Elevated Observed Risk")
        .sum()
    )

    high_risk = (
        df["OBSERVED_RISK_SEGMENT"]
        .eq("High Observed Risk")
        .sum()
    )

    high_risk_exposure = (
        df.loc[
            df["OBSERVED_RISK_SEGMENT"]
            == "High Observed Risk",
            "AMT_CREDIT"
        ]
        .sum()
    )

    return {
        "low_risk_customers": low_risk,
        "moderate_risk_customers": moderate_risk,
        "elevated_risk_customers": elevated_risk,
        "high_risk_customers": high_risk,
        "high_risk_exposure": high_risk_exposure
    }
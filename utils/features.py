import pandas as pd


# =========================================================
# CUSTOMER DEMOGRAPHIC FEATURES
# =========================================================

def create_customer_features(df):

    df = df.copy()

    # -----------------------------------------------------
    # AGE
    # -----------------------------------------------------

    if "DAYS_BIRTH" in df.columns:

        df["AGE"] = (
            -df["DAYS_BIRTH"] / 365.25
        )

    # -----------------------------------------------------
    # AGE GROUP
    # -----------------------------------------------------

    if "AGE" in df.columns:

        df["AGE_GROUP"] = pd.cut(

            df["AGE"],

            bins=[
                20,
                30,
                40,
                50,
                60,
                float("inf")
            ],

            labels=[
                "20–30",
                "31–40",
                "41–50",
                "51–60",
                "60+"
            ],

            include_lowest=True
        )

    return df
import pandas as pd


def create_income_features(df):
    df = df.copy()

    # -----------------------------------------
    # Income Group - Quantile Based
    # -----------------------------------------
    df["INCOME_GROUP"] = pd.qcut(
        df["AMT_INCOME_TOTAL"],
        q=5,
        labels=[
            "Very Low",
            "Low",
            "Middle",
            "High",
            "Very High"
        ],
        duplicates="drop"
    )

    # -----------------------------------------
    # Income per Family Member
    # -----------------------------------------
    df["INCOME_PER_FAMILY_MEMBER"] = (
        df["AMT_INCOME_TOTAL"]
        / df["CNT_FAM_MEMBERS"].replace(0, pd.NA)
    )

    # -----------------------------------------
    # Income per Child
    # -----------------------------------------
    df["INCOME_PER_CHILD"] = (
        df["AMT_INCOME_TOTAL"]
        / df["CNT_CHILDREN"].replace(0, pd.NA)
    )

    # -----------------------------------------
    # Income Percentile
    # -----------------------------------------
    df["INCOME_PERCENTILE"] = (
        df["AMT_INCOME_TOTAL"]
        .rank(pct=True) * 100
    )

    return df

import pandas as pd


# =========================================================
# EMPLOYMENT FEATURE ENGINEERING
# =========================================================

def create_employment_features(df):

    df = df.copy()

    # -----------------------------------------------------
    # Identify special DAYS_EMPLOYED value
    # -----------------------------------------------------

    df["EMPLOYMENT_SPECIAL"] = (
        df["DAYS_EMPLOYED"] == 365243
    )

    # -----------------------------------------------------
    # Employment Years
    # -----------------------------------------------------

    df["EMPLOYMENT_YEARS"] = (
        df["DAYS_EMPLOYED"].where(
            df["DAYS_EMPLOYED"] != 365243
        ).abs() / 365.25
    )

    # -----------------------------------------------------
    # Employment Group
    # -----------------------------------------------------

    def employment_group(years):

        if pd.isna(years):
            return "Unemployed / Special"

        elif years < 1:
            return "<1 Year"

        elif years < 3:
            return "1–3 Years"

        elif years < 5:
            return "3–5 Years"

        elif years < 10:
            return "5–10 Years"

        elif years < 20:
            return "10–20 Years"

        else:
            return "20+ Years"

    df["EMPLOYMENT_GROUP"] = (
        df["EMPLOYMENT_YEARS"]
        .apply(employment_group)
    )

    return df

import pandas as pd


# =========================================================
# FAMILY & HOUSING FEATURES
# =========================================================

def create_family_housing_features(df):

    df = df.copy()

    # Family Size Group
    if "CNT_FAM_MEMBERS" in df.columns:
        df["FAMILY_SIZE_GROUP"] = pd.cut(
            df["CNT_FAM_MEMBERS"],
            bins=[0, 2, 4, 6, 10, float("inf")],
            labels=[
                "1-2 Members",
                "3-4 Members",
                "5-6 Members",
                "7-10 Members",
                "10+ Members"
            ],
            include_lowest=True
        )

    # Children Group
    if "CNT_CHILDREN" in df.columns:
        df["CHILDREN_GROUP"] = pd.cut(
            df["CNT_CHILDREN"],
            bins=[-1, 0, 1, 2, 3, float("inf")],
            labels=[
                "0 Children",
                "1 Child",
                "2 Children",
                "3 Children",
                "4+ Children"
            ]
        )

    return df

def create_credit_affordability_features(df):
    df = df.copy()

    # -----------------------------------------
    # Credit-to-Income Ratio
    # -----------------------------------------
    df["CREDIT_TO_INCOME_RATIO"] = (
        df["AMT_CREDIT"] /
        df["AMT_INCOME_TOTAL"].replace(0, pd.NA)
    )

    # -----------------------------------------
    # Annuity-to-Income Ratio
    # -----------------------------------------
    df["ANNUITY_TO_INCOME_RATIO"] = (
        df["AMT_ANNUITY"] /
        df["AMT_INCOME_TOTAL"].replace(0, pd.NA)
    )

    # -----------------------------------------
    # Goods-to-Income Ratio
    # -----------------------------------------
    df["GOODS_TO_INCOME_RATIO"] = (
        df["AMT_GOODS_PRICE"] /
        df["AMT_INCOME_TOTAL"].replace(0, pd.NA)
    )

    # -----------------------------------------
    # Credit-to-Goods Ratio
    # -----------------------------------------
    df["CREDIT_TO_GOODS_RATIO"] = (
        df["AMT_CREDIT"] /
        df["AMT_GOODS_PRICE"].replace(0, pd.NA)
    )

    # -----------------------------------------
    # Income per Family Member
    # -----------------------------------------
    if "INCOME_PER_FAMILY_MEMBER" not in df.columns:
        df["INCOME_PER_FAMILY_MEMBER"] = (
            df["AMT_INCOME_TOTAL"] /
            df["CNT_FAM_MEMBERS"].replace(0, pd.NA)
        )

    return df

import pandas as pd


# =========================================================
# RISK FACTOR FEATURES
# =========================================================

def create_risk_factor_features(df):

    df = df.copy()

    # -----------------------------------------------------
    # CREDIT BAND
    # Quantile-based to avoid arbitrary business thresholds
    # -----------------------------------------------------

    if "AMT_CREDIT" in df.columns:

        df["CREDIT_BAND"] = pd.qcut(
            df["AMT_CREDIT"],
            q=5,
            labels=[
                "Very Low",
                "Low",
                "Middle",
                "High",
                "Very High"
            ],
            duplicates="drop"
        )

    # -----------------------------------------------------
    # INCOME BAND
    # Reuse INCOME_GROUP if already created
    # -----------------------------------------------------

    if "INCOME_GROUP" in df.columns:

        df["INCOME_BAND"] = df["INCOME_GROUP"]

    elif "AMT_INCOME_TOTAL" in df.columns:

        df["INCOME_BAND"] = pd.qcut(
            df["AMT_INCOME_TOTAL"],
            q=5,
            labels=[
                "Very Low",
                "Low",
                "Middle",
                "High",
                "Very High"
            ],
            duplicates="drop"
        )

    # -----------------------------------------------------
    # EMPLOYMENT BAND
    # Reuse existing employment group
    # -----------------------------------------------------

    if "EMPLOYMENT_GROUP" in df.columns:

        df["EMPLOYMENT_BAND"] = df["EMPLOYMENT_GROUP"]

    # -----------------------------------------------------
    # CREDIT-TO-INCOME BAND
    # Quantile based
    # -----------------------------------------------------

    if "CREDIT_TO_INCOME_RATIO" in df.columns:

        df["CREDIT_TO_INCOME_BAND"] = pd.qcut(
            df["CREDIT_TO_INCOME_RATIO"],
            q=5,
            labels=[
                "Very Low",
                "Low",
                "Middle",
                "High",
                "Very High"
            ],
            duplicates="drop"
        )

    # -----------------------------------------------------
    # ANNUITY-TO-INCOME BAND
    # Quantile based
    # -----------------------------------------------------

    if "ANNUITY_TO_INCOME_RATIO" in df.columns:

        df["ANNUITY_TO_INCOME_BAND"] = pd.qcut(
            df["ANNUITY_TO_INCOME_RATIO"],
            q=5,
            labels=[
                "Very Low",
                "Low",
                "Middle",
                "High",
                "Very High"
            ],
            duplicates="drop"
        )

    return df

# =========================================================
# BUREAU CREDIT HISTORY FEATURES
# =========================================================

import pandas as pd


# =========================================================
# BUREAU CUSTOMER-LEVEL FEATURES
# =========================================================

def create_bureau_features(df):
    
    df = df.copy()

    # -----------------------------------------------------
    # Create flags using vectorized operations
    # -----------------------------------------------------

    df["ACTIVE_FLAG"] = (
        df["CREDIT_ACTIVE"] == "Active"
    ).astype("int8")

    df["CLOSED_FLAG"] = (
        df["CREDIT_ACTIVE"] == "Closed"
    ).astype("int8")


    # -----------------------------------------------------
    # Customer-level aggregation
    # -----------------------------------------------------

    customer_features = (
        df.groupby(
            "SK_ID_CURR",
            sort=False
        )
        .agg(
            BUREAU_ACCOUNT_COUNT=(
                "SK_ID_BUREAU",
                "count"
            ),

            ACTIVE_ACCOUNT_COUNT=(
                "ACTIVE_FLAG",
                "sum"
            ),

            CLOSED_ACCOUNT_COUNT=(
                "CLOSED_FLAG",
                "sum"
            ),

            TOTAL_BUREAU_CREDIT=(
                "AMT_CREDIT_SUM",
                "sum"
            ),

            TOTAL_BUREAU_DEBT=(
                "AMT_CREDIT_SUM_DEBT",
                "sum"
            ),

            AVERAGE_BUREAU_CREDIT=(
                "AMT_CREDIT_SUM",
                "mean"
            ),

            MAX_OVERDUE_AMOUNT=(
                "AMT_CREDIT_SUM_OVERDUE",
                "max"
            )
        )
        .reset_index()
    )

    return customer_features

def create_previous_application_features(df):
    
    df = df.copy()

    # =====================================================
    # APPLICATION STATUS FLAGS
    # =====================================================

    df["APPROVED_FLAG"] = (
        df["NAME_CONTRACT_STATUS"]
        .eq("Approved")
        .astype("int8")
    )

    df["REFUSED_FLAG"] = (
        df["NAME_CONTRACT_STATUS"]
        .eq("Refused")
        .astype("int8")
    )

    # =====================================================
    # CUSTOMER LEVEL FEATURES
    # =====================================================

    customer_features = (
        df.groupby(
            "SK_ID_CURR",
            sort=False
        )
        .agg(

            NUMBER_PREVIOUS_APPLICATIONS=(
                "SK_ID_PREV",
                "nunique"
            ),

            NUMBER_APPROVED=(
                "APPROVED_FLAG",
                "sum"
            ),

            NUMBER_REFUSED=(
                "REFUSED_FLAG",
                "sum"
            ),

            AVERAGE_PREVIOUS_CREDIT=(
                "AMT_CREDIT",
                "mean"
            ),

            MAXIMUM_PREVIOUS_CREDIT=(
                "AMT_CREDIT",
                "max"
            )
        )
        .reset_index()
    )

    # =====================================================
    # APPROVAL RATE
    # =====================================================

    customer_features["APPROVAL_RATE"] = (
        customer_features["NUMBER_APPROVED"]
        /
        customer_features["NUMBER_PREVIOUS_APPLICATIONS"]
        * 100
    )

    return customer_features
def create_pos_cash_features(df):
    
    customer_features = (
        df.groupby("SK_ID_CURR")
        .agg(
            AVERAGE_DPD=(
                "SK_DPD",
                "mean"
            ),

            MAXIMUM_DPD=(
                "SK_DPD",
                "max"
            ),

            TOTAL_DPD_EVENTS=(
                "SK_DPD",
                lambda x: (x > 0).sum()
            ),

            AVERAGE_INSTALLMENTS_REMAINING=(
                "CNT_INSTALMENT_FUTURE",
                "mean"
            ),

            COMPLETED_CONTRACT_COUNT=(
                "NAME_CONTRACT_STATUS",
                lambda x: (x == "Completed").sum()
            )
        )
        .reset_index()
    )

    return customer_features
import numpy as np


def create_installment_payment_features(df):

    df = df.copy()

    # =====================================================
    # PAYMENT DELAY
    # =====================================================

    df["PAYMENT_DELAY"] = (
        df["DAYS_ENTRY_PAYMENT"]
        - df["DAYS_INSTALMENT"]
    )


    # =====================================================
    # PAYMENT DIFFERENCE
    # =====================================================

    df["PAYMENT_DIFFERENCE"] = (
        df["AMT_PAYMENT"]
        - df["AMT_INSTALMENT"]
    )


    # =====================================================
    # PAYMENT RATIO
    # =====================================================

    df["PAYMENT_RATIO"] = np.where(
        df["AMT_INSTALMENT"] > 0,
        df["AMT_PAYMENT"]
        / df["AMT_INSTALMENT"],
        np.nan
    )


    # =====================================================
    # PAYMENT TIMING
    # =====================================================

    df["PAYMENT_TIMING"] = np.select(
        [
            df["PAYMENT_DELAY"] < 0,
            df["PAYMENT_DELAY"] == 0,
            df["PAYMENT_DELAY"] > 0
        ],
        [
            "Early Payment",
            "On-Time Payment",
            "Late Payment"
        ],
        default="Unknown"
    )


    # =====================================================
    # PAYMENT STATUS
    # =====================================================

    df["PAYMENT_STATUS"] = np.select(
        [
            df["PAYMENT_RATIO"] < 1,
            np.isclose(
                df["PAYMENT_RATIO"],
                1,
                equal_nan=False
            ),
            df["PAYMENT_RATIO"] > 1
        ],
        [
            "Underpayment",
            "Full Payment",
            "Overpayment"
        ],
        default="Unknown"
    )


    # =====================================================
    # CUSTOMER-LEVEL FEATURES
    # =====================================================

    customer_features = (
        df.groupby(
            "SK_ID_CURR",
            sort=False
        )
        .agg(
            TOTAL_INSTALLMENTS=(
                "SK_ID_PREV",
                "count"
            ),

            LATE_PAYMENT_COUNT=(
                "PAYMENT_DELAY",
                lambda x: (x > 0).sum()
            ),

            AVERAGE_PAYMENT_DELAY=(
                "PAYMENT_DELAY",
                "mean"
            ),

            MAXIMUM_PAYMENT_DELAY=(
                "PAYMENT_DELAY",
                "max"
            ),

            AVERAGE_PAYMENT_RATIO=(
                "PAYMENT_RATIO",
                "mean"
            ),

            UNDERPAYMENT_COUNT=(
                "PAYMENT_RATIO",
                lambda x: (x < 1).sum()
            )
        )
        .reset_index()
    )


    # =====================================================
    # LATE PAYMENT PERCENTAGE
    # =====================================================

    customer_features["LATE_PAYMENT_PERCENTAGE"] = (
        customer_features["LATE_PAYMENT_COUNT"]
        /
        customer_features["TOTAL_INSTALLMENTS"]
        * 100
    )


    return df, customer_features

def create_credit_card_features(df):
    
    df = df.copy()

    # =====================================================
    # CREDIT UTILIZATION
    # =====================================================

    df["CREDIT_UTILIZATION"] = (
        df["AMT_BALANCE"]
        /
        df["AMT_CREDIT_LIMIT_ACTUAL"]
    )

    # Avoid invalid infinite values
    df["CREDIT_UTILIZATION"] = (
        df["CREDIT_UTILIZATION"]
        .replace([float("inf"), -float("inf")], 0)
        .fillna(0)
    )

    # =====================================================
    # CUSTOMER-LEVEL FEATURES
    # =====================================================

    customer_features = (
        df.groupby(
            "SK_ID_CURR",
            sort=False
        )
        .agg(
            AVERAGE_BALANCE=(
                "AMT_BALANCE",
                "mean"
            ),

            MAXIMUM_BALANCE=(
                "AMT_BALANCE",
                "max"
            ),

            AVERAGE_CREDIT_LIMIT=(
                "AMT_CREDIT_LIMIT_ACTUAL",
                "mean"
            ),

            AVERAGE_UTILIZATION=(
                "CREDIT_UTILIZATION",
                "mean"
            ),

            MAXIMUM_UTILIZATION=(
                "CREDIT_UTILIZATION",
                "max"
            ),

            TOTAL_DRAWINGS=(
                "AMT_DRAWINGS_CURRENT",
                "sum"
            ),

            AVERAGE_PAYMENTS=(
                "AMT_PAYMENT_CURRENT",
                "mean"
            ),

            MAXIMUM_DPD=(
                "SK_DPD",
                "max"
            )
        )
        .reset_index()
    )

    return df, customer_features

def create_risk_segmentation_features(application_df, bureau_df):
    
    app = application_df.copy()
    bureau = bureau_df.copy()

    # =====================================================
    # BUREAU CUSTOMER AGGREGATION
    # =====================================================

    bureau_features = (
        bureau.groupby("SK_ID_CURR")
        .agg(
            TOTAL_BUREAU_DEBT=(
                "AMT_CREDIT_SUM_DEBT",
                "sum"
            ),

            TOTAL_BUREAU_OVERDUE=(
                "AMT_CREDIT_SUM_OVERDUE",
                "sum"
            ),

            BUREAU_ACCOUNT_COUNT=(
                "SK_ID_BUREAU",
                "count"
            )
        )
        .reset_index()
    )

    # =====================================================
    # MERGE APPLICATION + BUREAU
    # =====================================================

    df = app.merge(
        bureau_features,
        on="SK_ID_CURR",
        how="left"
    )

    # Missing bureau history = zero observed bureau exposure

    df["TOTAL_BUREAU_DEBT"] = (
        df["TOTAL_BUREAU_DEBT"]
        .fillna(0)
    )

    df["TOTAL_BUREAU_OVERDUE"] = (
        df["TOTAL_BUREAU_OVERDUE"]
        .fillna(0)
    )

    df["BUREAU_ACCOUNT_COUNT"] = (
        df["BUREAU_ACCOUNT_COUNT"]
        .fillna(0)
    )

    # =====================================================
    # CREDIT-TO-INCOME RATIO
    # =====================================================

    df["CREDIT_TO_INCOME"] = (
        df["AMT_CREDIT"]
        /
        df["AMT_INCOME_TOTAL"]
    )

    df["CREDIT_TO_INCOME"] = (
        df["CREDIT_TO_INCOME"]
        .replace(
            [float("inf"), -float("inf")],
            0
        )
        .fillna(0)
    )

    # =====================================================
    # ANNUITY-TO-INCOME RATIO
    # =====================================================

    df["ANNUITY_TO_INCOME"] = (
        df["AMT_ANNUITY"]
        /
        df["AMT_INCOME_TOTAL"]
    )

    df["ANNUITY_TO_INCOME"] = (
        df["ANNUITY_TO_INCOME"]
        .replace(
            [float("inf"), -float("inf")],
            0
        )
        .fillna(0)
    )

    # =====================================================
    # EMPLOYMENT YEARS
    # =====================================================

    df["EMPLOYMENT_YEARS"] = (
        df["DAYS_EMPLOYED"].abs()
        / 365
    )

    # =====================================================
    # RULE FLAGS
    # =====================================================

    df["HIGH_CREDIT_BURDEN"] = (
        df["CREDIT_TO_INCOME"] >= 5
    )

    df["HIGH_ANNUITY_BURDEN"] = (
        df["ANNUITY_TO_INCOME"] >= 0.40
    )

    df["HIGH_BUREAU_DEBT"] = (
        df["TOTAL_BUREAU_DEBT"]
        >= df["AMT_INCOME_TOTAL"] * 2
    )

    df["BUREAU_OVERDUE"] = (
        df["TOTAL_BUREAU_OVERDUE"] > 0
    )

    df["SHORT_EMPLOYMENT"] = (
        df["EMPLOYMENT_YEARS"] < 2
    )

    # =====================================================
    # DESCRIPTIVE RISK SCORE
    # =====================================================

    df["OBSERVED_RISK_SCORE"] = (
        df["HIGH_CREDIT_BURDEN"].astype(int)
        +
        df["HIGH_ANNUITY_BURDEN"].astype(int)
        +
        df["HIGH_BUREAU_DEBT"].astype(int)
        +
        df["BUREAU_OVERDUE"].astype(int)
        +
        df["SHORT_EMPLOYMENT"].astype(int)
    )

    # =====================================================
    # OBSERVED RISK SEGMENT
    # =====================================================

    df["OBSERVED_RISK_SEGMENT"] = df[
        "OBSERVED_RISK_SCORE"
    ].map(
        {
            0: "Low Observed Risk",
            1: "Moderate Observed Risk",
            2: "Elevated Observed Risk",
            3: "Elevated Observed Risk",
            4: "High Observed Risk",
            5: "High Observed Risk"
        }
    )

    return df
from __future__ import annotations

import inspect
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler


ID_COL = "CustomerID"
TARGET_COL = "Churn"

DROP_COLUMNS = [
    ID_COL,
    TARGET_COL,
    "DaySinceLastOrder", #See Decision 15 for dropping criteria
]

CATEGORICAL_FEATURES = [
    "PreferredLoginDevice",
    "PreferredPaymentMode",
    "Gender",
    "PreferedOrderCat",
    "MaritalStatus",
]

BASE_NUMERIC_FEATURES = [
    "Tenure",
    "CityTier",
    "WarehouseToHome",
    "HourSpendOnApp",
    "NumberOfDeviceRegistered",
    "SatisfactionScore",
    "NumberOfAddress",
    "Complain",
    "OrderAmountHikeFromlastYear",
    "CouponUsed",
    "OrderCount",
    "CashbackAmount",
]

DERIVED_NUMERIC_FEATURES = [
    "valor_cliente_proxy",
    "coupon_per_order",
    "cashback_per_order",
    "complain_x_satisfaction",
]

BINARY_SEGMENT_FEATURES = [
    "is_new_customer",
    "is_loyal_customer",
    "is_low_freq_user",
    "is_high_freq_user",
    "is_high_value",
]

NUMERIC_FEATURES = BASE_NUMERIC_FEATURES + DERIVED_NUMERIC_FEATURES + BINARY_SEGMENT_FEATURES


class SegmentFeatureBuilder(BaseEstimator, TransformerMixin):
    """Binary segment flags fitted on train only.

    Fixed-threshold flags (Tenure cutoffs) encode business rules.
    Statistical-threshold flags (OrderCount, CashbackAmount) learn
    their cutoffs from train to avoid leakage.
    """

    TENURE_NEW = 3     # months: new customer window
    TENURE_LOYAL = 18  # months: established / senior customer

    def fit(self, X: pd.DataFrame, y: Iterable | None = None) -> "SegmentFeatureBuilder":
        self.tenure_median_ = float(X["Tenure"].median())
        self.cashback_median_ = float(X["CashbackAmount"].median())
        # Q25/Q75 instead of Q33/Q67: OrderCount clusters heavily at 1-2-3,
        # so tertiles collapse to the same value and produce overlapping flags.
        order_quantiles = X["OrderCount"].quantile([0.25, 0.75])
        self.order_count_q25_ = float(order_quantiles.iloc[0])
        self.order_count_q75_ = float(order_quantiles.iloc[1])
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = X.copy()
        tenure = X_out["Tenure"].fillna(self.tenure_median_)
        order_count = X_out["OrderCount"].fillna(self.order_count_q25_)
        cashback = X_out["CashbackAmount"].fillna(self.cashback_median_)

        X_out["is_new_customer"] = (tenure <= self.TENURE_NEW).astype(int)
        X_out["is_loyal_customer"] = (tenure >= self.TENURE_LOYAL).astype(int)
        X_out["is_low_freq_user"] = (order_count <= self.order_count_q25_).astype(int)
        X_out["is_high_freq_user"] = (order_count >= self.order_count_q75_).astype(int)
        X_out["is_high_value"] = (cashback >= self.cashback_median_).astype(int)
        return X_out


class BusinessFeatureBuilder(BaseEstimator, TransformerMixin):
    """Create deterministic business features before sklearn preprocessing."""

    def fit(self, X: pd.DataFrame, y: Iterable | None = None) -> "BusinessFeatureBuilder":
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_out = X.copy()
        order_count = X_out["OrderCount"].fillna(0)
        safe_order_count = order_count.clip(lower=1)

        X_out["valor_cliente_proxy"] = X_out["OrderCount"] * X_out["CashbackAmount"]
        X_out["coupon_per_order"] = X_out["CouponUsed"] / safe_order_count
        X_out["cashback_per_order"] = X_out["CashbackAmount"] / safe_order_count
        X_out["complain_x_satisfaction"] = X_out["Complain"] * X_out["SatisfactionScore"]

        return X_out


def _one_hot_encoder() -> OneHotEncoder:
    params = {
        "handle_unknown": "ignore",
    }
    if "sparse_output" in inspect.signature(OneHotEncoder).parameters:
        params["sparse_output"] = False
    else:
        params["sparse"] = False
    return OneHotEncoder(**params)


def build_pipeline() -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", _one_hot_encoder()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return Pipeline(
        steps=[
            ("segment_features", SegmentFeatureBuilder()),
            ("business_features", BusinessFeatureBuilder()),
            ("preprocessor", preprocessor),
        ]
    )


def get_feature_names(fitted_pipeline: Pipeline) -> list[str]:
    preprocessor = fitted_pipeline.named_steps["preprocessor"]
    return list(preprocessor.get_feature_names_out())


def transform_to_dataframe(
    fitted_pipeline: Pipeline,
    X: pd.DataFrame,
    index: pd.Index | None = None,
) -> pd.DataFrame:
    transformed = fitted_pipeline.transform(X)
    feature_names = get_feature_names(fitted_pipeline)
    return pd.DataFrame(
        np.asarray(transformed),
        columns=feature_names,
        index=index if index is not None else X.index,
    )

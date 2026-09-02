"""
Data Preprocessing & Pipeline Module for End-of-1st-Semester Student Dropout Prediction

This module defines dataset loading, explicit column grouping (categorical vs numerical vs excluded),
scikit-learn ColumnTransformer preprocessor construction, and stratified train/test splitting.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

try:
    from src.feature_engineering import create_engineered_features, get_engineered_feature_names
except ImportError:
    from feature_engineering import create_engineered_features, get_engineered_feature_names

# Target Column
TARGET_COLUMN = 'Target'

# Excluded 2nd-Semester Features (Prevent Data Leakage for End-of-1st-Semester System)
EXCLUDED_FEATURES = [
    'Curricular units 2nd sem (credited)',
    'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)',
    'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)',
    'Curricular units 2nd sem (without evaluations)',
]

# Categorical Features (Multi-category encoded integer variables)
CATEGORICAL_FEATURES = [
    'Marital status',
    'Application mode',
    'Application order',
    'Course',
    'Previous qualification',
    'Nacionality',
    "Mother's qualification",
    "Father's qualification",
    "Mother's occupation",
    "Father's occupation",
]

# Numerical Features (Raw Binary + Continuous + 1st Sem Performance + Engineered)
RAW_NUMERICAL_FEATURES = [
    # Binary Indicators (0/1)
    'Daytime/evening attendance',
    'Displaced',
    'Educational special needs',
    'Debtor',
    'Tuition fees up to date',
    'Gender',
    'Scholarship holder',
    'International',
    # Continuous Background & Macroeconomic Features
    'Previous qualification (grade)',
    'Admission grade',
    'Age at enrollment',
    'Unemployment rate',
    'Inflation rate',
    'GDP',
    # 1st-Semester Academic Performance Features
    'Curricular units 1st sem (credited)',
    'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)',
    'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)',
    'Curricular units 1st sem (without evaluations)',
]

ENGINEERED_FEATURES = get_engineered_feature_names()

ALL_NUMERICAL_FEATURES = RAW_NUMERICAL_FEATURES + ENGINEERED_FEATURES

ALL_INPUT_FEATURES = CATEGORICAL_FEATURES + RAW_NUMERICAL_FEATURES


def load_dataset(file_path: str = "data/data.csv") -> pd.DataFrame:
    """
    Loads raw CSV data with semicolon separator and cleans column headers.

    Parameters:
        file_path (str): Path to data.csv.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')
    df.columns = [c.strip().replace('"', '') for c in df.columns]
    return df


def build_preprocessor() -> ColumnTransformer:
    """
    Constructs a scikit-learn ColumnTransformer pipeline.
    
    - Numerical Pipeline: Median Imputation + StandardScaler
    - Categorical Pipeline: Most Frequent Imputation + OneHotEncoder (handle_unknown='ignore')

    Returns:
        ColumnTransformer: Configured preprocessor object.
    """
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipeline, ALL_NUMERICAL_FEATURES),
            ('cat', cat_pipeline, CATEGORICAL_FEATURES)
        ],
        remainder='drop'
    )

    return preprocessor


def build_full_pipeline(classifier) -> Pipeline:
    """
    Constructs the end-to-end sklearn Pipeline:
    Raw Input (30 features) -> Feature Engineering Transformer -> ColumnTransformer Preprocessor -> Classifier
    """
    fe_transformer = FunctionTransformer(create_engineered_features, validate=False)
    preprocessor = build_preprocessor()
    
    pipeline = Pipeline([
        ('feature_engineering', fe_transformer),
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])
    
    return pipeline


def get_train_test_split(
    df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Prepares stratified train/test split (80% train / 20% test) using raw features.

    Parameters:
        df (pd.DataFrame): Raw dataframe.
        test_size (float): Proportion of test data (default 0.2).
        random_state (int): Seed for reproducibility (default 42).

    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataset.")

    y = df[TARGET_COLUMN]
    X = df[ALL_INPUT_FEATURES].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return X_train, X_test, y_train, y_test

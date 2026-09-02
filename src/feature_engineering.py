"""
Feature Engineering Module for Student Dropout Risk Prediction (End-of-1st-Semester System)

This module defines derived features created exclusively from 1st-semester academic performance
and enrollment attributes. No 2nd-semester or target data is used.
"""

import pandas as pd
import numpy as np


def create_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates derived academic performance features for the end-of-1st-semester early warning system.
    
    Engineered Features:
    1. First_Sem_Approval_Rate: Ratio of approved units to evaluated units (approved / evaluations).
       Measures pass rate among units where the student attempted exams/evaluations.
    2. First_Sem_Completion_Rate: Ratio of approved units to total enrolled units (approved / enrolled).
       Measures overall course progress and completion efficiency relative to course load.
    3. First_Sem_Evaluation_Rate: First-semester evaluation participation ratio (evaluations / enrolled).
       Measures the proportion of enrolled curricular units that received an evaluation.

    Safe division is enforced to handle zero denominators without producing Inf or NaN.

    Parameters:
        df (pd.DataFrame): Input dataframe containing raw feature columns.

    Returns:
        pd.DataFrame: Copy of dataframe with added engineered feature columns.
    """
    df_out = df.copy()

    # 1. First_Sem_Approval_Rate = approved / evaluations
    evals = df_out['Curricular units 1st sem (evaluations)']
    approved = df_out['Curricular units 1st sem (approved)']
    df_out['First_Sem_Approval_Rate'] = np.where(evals > 0, approved / evals, 0.0)

    # 2. First_Sem_Completion_Rate = approved / enrolled
    enrolled = df_out['Curricular units 1st sem (enrolled)']
    df_out['First_Sem_Completion_Rate'] = np.where(enrolled > 0, approved / enrolled, 0.0)

    # 3. First_Sem_Evaluation_Rate (First-semester evaluation participation ratio) = evaluations / enrolled
    df_out['First_Sem_Evaluation_Rate'] = np.where(enrolled > 0, evals / enrolled, 0.0)

    return df_out


def get_engineered_feature_names() -> list[str]:
    """Returns the list of engineered feature names."""
    return [
        'First_Sem_Approval_Rate',
        'First_Sem_Completion_Rate',
        'First_Sem_Evaluation_Rate'
    ]

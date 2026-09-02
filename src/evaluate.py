"""
Model Evaluation Module for Student Dropout Early Warning System

This module provides modular functions to evaluate multiclass classification performance,
calculate metrics (Accuracy, Precision, Recall, F1, Macro F1, Weighted F1, Multiclass ROC-AUC),
generate confusion matrix plots, and extract per-class performance metrics.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

CLASS_LABELS = ['Dropout', 'Enrolled', 'Graduate']


def evaluate_model(
    model, X_test, y_test, class_labels: list[str] = CLASS_LABELS
) -> dict:
    """
    Evaluates a trained model pipeline on test data and returns a comprehensive metrics dictionary.

    Parameters:
        model: Trained scikit-learn pipeline or model.
        X_test (pd.DataFrame): Raw test features.
        y_test (pd.Series): True test targets.
        class_labels (list): Target class labels (['Dropout', 'Enrolled', 'Graduate']).

    Returns:
        dict: Complete dictionary of evaluation metrics and per-class performance.
    """
    y_pred = model.predict(X_test)
    
    # Calculate probabilities if available
    y_prob = None
    if hasattr(model, "predict_proba"):
        try:
            y_prob = model.predict_proba(X_test)
        except Exception:
            y_prob = None

    # Overall metrics
    acc = accuracy_score(y_test, y_pred)
    prec_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    prec_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    # Multiclass ROC-AUC (One-vs-Rest)
    roc_auc = np.nan
    if y_prob is not None:
        try:
            # Map target labels to indicator matrix for multiclass roc_auc_score
            roc_auc = roc_auc_score(y_test, y_prob, multi_class='ovr', average='macro')
        except Exception as e:
            roc_auc = np.nan

    # Per-class metrics
    report_dict = classification_report(y_test, y_pred, target_names=class_labels, output_dict=True, zero_division=0)

    dropout_prec = report_dict['Dropout']['precision']
    dropout_rec = report_dict['Dropout']['recall']
    dropout_f1 = report_dict['Dropout']['f1-score']

    enrolled_prec = report_dict['Enrolled']['precision']
    enrolled_rec = report_dict['Enrolled']['recall']
    enrolled_f1 = report_dict['Enrolled']['f1-score']

    graduate_prec = report_dict['Graduate']['precision']
    graduate_rec = report_dict['Graduate']['recall']
    graduate_f1 = report_dict['Graduate']['f1-score']

    metrics = {
        'Accuracy': float(acc),
        'Precision': float(prec_macro),
        'Recall': float(rec_macro),
        'Macro F1': float(f1_macro),
        'Weighted F1': float(f1_weighted),
        'ROC-AUC': float(roc_auc) if not np.isnan(roc_auc) else None,
        # Dropout specific
        'Dropout Precision': float(dropout_prec),
        'Dropout Recall': float(dropout_rec),
        'Dropout F1': float(dropout_f1),
        # Enrolled specific
        'Enrolled Precision': float(enrolled_prec),
        'Enrolled Recall': float(enrolled_rec),
        'Enrolled F1': float(enrolled_f1),
        # Graduate specific
        'Graduate Precision': float(graduate_prec),
        'Graduate Recall': float(graduate_rec),
        'Graduate F1': float(graduate_f1),
        # Raw predictions
        'y_pred': y_pred,
        'y_prob': y_prob
    }

    return metrics


def plot_confusion_matrix(
    y_true, y_pred, model_name: str, class_labels: list[str] = CLASS_LABELS, save_path: str = None
):
    """
    Plots and optionally saves a clean, clearly labeled confusion matrix.

    Parameters:
        y_true: True targets.
        y_pred: Predicted targets.
        model_name (str): Title name for the model.
        class_labels (list): Target class labels.
        save_path (str): Filepath to save plot PNG.
    """
    cm = confusion_matrix(y_true, y_pred, labels=class_labels)
    
    plt.figure(figsize=(7, 6))
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues',
        xticklabels=class_labels, yticklabels=class_labels,
        cbar=True, annot_kws={"size": 13, "weight": "bold"}
    )
    plt.title(f'Confusion Matrix - {model_name}', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.ylabel('Actual Label', fontsize=12, fontweight='bold')
    plt.tight_layout()

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def save_classification_report(
    y_true, y_pred, model_name: str, class_labels: list[str] = CLASS_LABELS, save_path: str = None
) -> str:
    """
    Generates and saves formatted classification report text.
    """
    report_str = classification_report(y_true, y_pred, target_names=class_labels, digits=4, zero_division=0)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(f"Classification Report - {model_name}\n")
            f.write("=" * 60 + "\n\n")
            f.write(report_str)
            
    return report_str

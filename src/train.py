"""
Main Training Pipeline Script for End-of-1st-Semester Student Dropout Early Warning System

This script executes the complete model training, evaluation, comparison, selection,
and saving workflow:
1. Loads dataset and applies feature engineering inside the pipeline.
2. Performs 80/20 stratified train/test split.
3. Constructs scikit-learn pipelines with column preprocessing for multiple models:
   - Logistic Regression (Default & Balanced)
   - Decision Tree (Default & Balanced)
   - Random Forest (Default & Balanced)
   - XGBoost Classifier
4. Evaluates all models on untouched test set using Accuracy, Precision, Recall, F1, Macro F1, Weighted F1, ROC-AUC.
5. Saves model comparisons, classification reports, confusion matrices, and feature importances.
6. Selects the best model based on PRIMARY METRIC: Macro F1.
7. Saves the best complete pipeline to models/best_model.pkl and metadata to models/model_metadata.pkl.
8. Verifies end-to-end reload and sample prediction.
"""

import os
import sys
import datetime
import joblib
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False

from src.preprocessing import (
    load_dataset, get_train_test_split, build_full_pipeline,
    CATEGORICAL_FEATURES, ALL_NUMERICAL_FEATURES, ALL_INPUT_FEATURES, TARGET_COLUMN
)
from src.evaluate import (
    evaluate_model, plot_confusion_matrix, save_classification_report, CLASS_LABELS
)

# Output directories
RESULTS_DIR = "results"
CONFUSION_DIR = os.path.join(RESULTS_DIR, "confusion_matrices")
REPORTS_DIR = os.path.join(RESULTS_DIR, "classification_reports")
IMPORTANCE_DIR = os.path.join(RESULTS_DIR, "feature_importance")
MODELS_DIR = "models"

for directory in [RESULTS_DIR, CONFUSION_DIR, REPORTS_DIR, IMPORTANCE_DIR, MODELS_DIR]:
    os.makedirs(directory, exist_ok=True)


def get_transformed_feature_names(preprocessor) -> list[str]:
    """Retrieves feature names after column transformation (one-hot encoding + scaling)."""
    num_names = list(ALL_NUMERICAL_FEATURES)
    cat_encoder = preprocessor.named_transformers_['cat'].named_steps['onehot']
    cat_names = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    return num_names + cat_names


def main():
    print("=" * 70)
    print("STARTING MODEL TRAINING & EVALUATION PIPELINE")
    print("=" * 70)

    # 1. Load Data
    print("\n[1/8] Loading dataset...")
    raw_df = load_dataset("data/data.csv")
    print(f"Loaded raw dataset shape: {raw_df.shape}")

    # 2. Train / Test Split
    print("\n[2/8] Preparing 80/20 Stratified Train/Test Split...")
    X_train, X_test, y_train, y_test = get_train_test_split(raw_df, test_size=0.2, random_state=42)
    print(f"Training set: {X_train.shape[0]} samples, {X_train.shape[1]} raw input features")
    print(f"Testing set:  {X_test.shape[0]} samples, {X_test.shape[1]} raw input features")

    # Target Label Encoding for XGBoost compatibility
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)

    # 3. Model Definitions
    models_to_train = {
        'Logistic Regression (Default)': LogisticRegression(
            max_iter=1000, random_state=42
        ),
        'Logistic Regression (Balanced)': LogisticRegression(
            max_iter=1000, class_weight='balanced', random_state=42
        ),
        'Decision Tree (Default)': DecisionTreeClassifier(
            max_depth=10, min_samples_split=10, min_samples_leaf=5, random_state=42
        ),
        'Decision Tree (Balanced)': DecisionTreeClassifier(
            max_depth=10, min_samples_split=10, min_samples_leaf=5, class_weight='balanced', random_state=42
        ),
        'Random Forest (Default)': RandomForestClassifier(
            n_estimators=100, max_depth=15, random_state=42
        ),
        'Random Forest (Balanced)': RandomForestClassifier(
            n_estimators=100, max_depth=15, class_weight='balanced', random_state=42
        ),
    }

    if HAS_XGBOOST:
        models_to_train['XGBoost'] = XGBClassifier(
            n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42,
            eval_metric='mlogloss', n_jobs=-1
        )
    else:
        print("[WARNING] XGBoost not installed. Skipping XGBoost model.")

    # 4. Train and Evaluate Each Model
    print(f"\n[3/8] Training and Evaluating {len(models_to_train)} Models...")
    
    comparison_records = []
    dropout_records = []
    trained_pipelines = {}
    evaluation_results = {}

    for name, clf in models_to_train.items():
        print(f"\n   Training {name}...")
        
        pipeline = build_full_pipeline(clf)

        # Train pipeline
        if 'XGBoost' in name:
            pipeline.fit(X_train, y_train_encoded)
            y_pred_enc = pipeline.predict(X_test)
            y_pred = le.inverse_transform(y_pred_enc)
            y_prob = pipeline.predict_proba(X_test)
            metrics = evaluate_model_direct(y_test, y_pred, y_prob, CLASS_LABELS)
        else:
            pipeline.fit(X_train, y_train)
            metrics = evaluate_model(pipeline, X_test, y_test, CLASS_LABELS)
            y_pred = metrics['y_pred']

        trained_pipelines[name] = pipeline
        evaluation_results[name] = metrics

        comparison_records.append({
            'Model': name,
            'Accuracy': metrics['Accuracy'],
            'Precision': metrics['Precision'],
            'Recall': metrics['Recall'],
            'Macro F1': metrics['Macro F1'],
            'Weighted F1': metrics['Weighted F1'],
            'ROC-AUC': metrics['ROC-AUC'] if metrics['ROC-AUC'] is not None else np.nan
        })

        dropout_records.append({
            'Model': name,
            'Dropout Precision': metrics['Dropout Precision'],
            'Dropout Recall': metrics['Dropout Recall'],
            'Dropout F1': metrics['Dropout F1']
        })

        # Save Confusion Matrix plot
        cm_filename = name.lower().replace(' ', '_').replace('(', '').replace(')', '') + "_cm.png"
        cm_path = os.path.join(CONFUSION_DIR, cm_filename)
        plot_confusion_matrix(y_test, y_pred, model_name=name, class_labels=CLASS_LABELS, save_path=cm_path)

        # Save Classification Report text
        rep_filename = name.lower().replace(' ', '_').replace('(', '').replace(')', '') + "_report.txt"
        rep_path = os.path.join(REPORTS_DIR, rep_filename)
        save_classification_report(y_test, y_pred, model_name=name, class_labels=CLASS_LABELS, save_path=rep_path)

        print(f"      Accuracy: {metrics['Accuracy']:.4f} | Macro F1: {metrics['Macro F1']:.4f} | Dropout Recall: {metrics['Dropout Recall']:.4f} | Dropout F1: {metrics['Dropout F1']:.4f}")

    # 5. Build Model Comparison DataFrames & Save
    print("\n[4/8] Generating Model Comparison Tables...")
    df_comparison = pd.DataFrame(comparison_records).sort_values(by='Macro F1', ascending=False).reset_index(drop=True)
    df_dropout = pd.DataFrame(dropout_records).sort_values(by='Dropout F1', ascending=False).reset_index(drop=True)

    comp_csv_path = os.path.join(RESULTS_DIR, "model_comparison.csv")
    df_comparison.to_csv(comp_csv_path, index=False)
    
    dropout_csv_path = os.path.join(RESULTS_DIR, "dropout_comparison.csv")
    df_dropout.to_csv(dropout_csv_path, index=False)

    print(f"\nSaved overall comparison to: {comp_csv_path}")
    print("\n--- MODEL COMPARISON TABLE ---")
    print(df_comparison.to_string(index=False))

    print("\n--- DROPOUT-SPECIFIC PERFORMANCE ---")
    print(df_dropout.to_string(index=False))

    # 6. Extract Feature Importances / Coefficients
    print("\n[5/8] Extracting Feature Importances & Coefficients...")
    for name, pipe in trained_pipelines.items():
        prep = pipe.named_steps['preprocessor']
        clf = pipe.named_steps['classifier']
        tf_names = get_transformed_feature_names(prep)
        safe_name = name.lower().replace(' ', '_').replace('(', '').replace(')', '')

        if hasattr(clf, "feature_importances_"):
            fi_df = pd.DataFrame({
                'Feature': tf_names,
                'Importance': clf.feature_importances_
            }).sort_values(by='Importance', ascending=False).reset_index(drop=True)

            fi_path = os.path.join(IMPORTANCE_DIR, f"{safe_name}_importance.csv")
            fi_df.to_csv(fi_path, index=False)

        elif hasattr(clf, "coef_"):
            coef_dict = {'Feature': tf_names}
            classes = clf.classes_ if hasattr(clf, 'classes_') else ['Class_0', 'Class_1', 'Class_2']
            for i, cls in enumerate(classes):
                coef_dict[f'Coef_{cls}'] = clf.coef_[i]
            
            coef_df = pd.DataFrame(coef_dict)
            coef_path = os.path.join(IMPORTANCE_DIR, f"{safe_name}_coefs.csv")
            coef_df.to_csv(coef_path, index=False)

    # 7. Model Selection based on PRIMARY METRIC: Macro F1
    print("\n[6/8] Selecting Best Model based on PRIMARY METRIC (Macro F1)...")
    best_model_name = df_comparison.iloc[0]['Model']
    best_macro_f1 = df_comparison.iloc[0]['Macro F1']
    best_pipeline = trained_pipelines[best_model_name]
    best_metrics = evaluation_results[best_model_name]

    print(f"SELECTED BEST MODEL: {best_model_name}")
    print(f"   Macro F1:        {best_macro_f1:.4f}")
    print(f"   Accuracy:        {best_metrics['Accuracy']:.4f}")
    print(f"   Dropout Recall:  {best_metrics['Dropout Recall']:.4f}")
    print(f"   Dropout F1:      {best_metrics['Dropout F1']:.4f}")
    print(f"   ROC-AUC:         {best_metrics['ROC-AUC'] if best_metrics['ROC-AUC'] is not None else 'N/A'}")

    # Generate larger, clean confusion matrix for the best model
    best_cm_path = os.path.join(RESULTS_DIR, "best_model_confusion_matrix.png")
    best_y_pred = best_pipeline.predict(X_test)
    if 'XGBoost' in best_model_name:
        best_y_pred = le.inverse_transform(best_y_pred)
    plot_confusion_matrix(y_test, best_y_pred, model_name=f"Best Model ({best_model_name})", class_labels=CLASS_LABELS, save_path=best_cm_path)

    # 8. Save Best Model & Metadata
    print("\n[7/8] Saving Best Model Pipeline and Metadata...")
    model_pkl_path = os.path.join(MODELS_DIR, "best_model.pkl")
    meta_pkl_path = os.path.join(MODELS_DIR, "model_metadata.pkl")

    joblib.dump(best_pipeline, model_pkl_path)
    
    metadata = {
        'model_name': best_model_name,
        'primary_metric': 'Macro F1',
        'primary_metric_value': float(best_macro_f1),
        'metrics': {k: v for k, v in best_metrics.items() if k not in ('y_pred', 'y_prob')},
        'raw_feature_names': ALL_INPUT_FEATURES,
        'transformed_feature_names': get_transformed_feature_names(best_pipeline.named_steps['preprocessor']),
        'target_classes': CLASS_LABELS,
        'label_encoder': le if HAS_XGBOOST else None,
        'training_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    joblib.dump(metadata, meta_pkl_path)

    print(f"Saved best model pipeline to: {model_pkl_path}")
    print(f"Saved model metadata to:       {meta_pkl_path}")

    # 9. Verification & Sample Probability Output
    print("\n[8/8] Verifying Model Reload and Sample Probability Output...")
    loaded_pipeline = joblib.load(model_pkl_path)
    
    sample_student = X_test.iloc[[0]].copy()
    actual_target = y_test.iloc[0]

    probs = loaded_pipeline.predict_proba(sample_student)[0]
    
    if 'XGBoost' in best_model_name:
        classes = list(le.classes_)
    else:
        classes = list(loaded_pipeline.classes_)

    print("\n--- SAMPLE STUDENT PREDICTION TEST ---")
    print(f"Actual Target: {actual_target}")
    print("Predicted Probabilities:")
    prob_sum = 0.0
    for cls, prob in zip(classes, probs):
        print(f"  {cls:10s}: {prob:.4f} ({prob*100:.2f}%)")
        prob_sum += prob

    print(f"Sum of probabilities: {prob_sum:.6f} ~= 1.0")

    print("\n==================================================")
    print("MODEL TRAINING & EVALUATION PIPELINE COMPLETED!")
    print("==================================================")


def evaluate_model_direct(y_test, y_pred, y_prob, class_labels):
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
    acc = accuracy_score(y_test, y_pred)
    prec_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    prec_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    roc_auc = np.nan
    if y_prob is not None:
        try:
            roc_auc = roc_auc_score(y_test, y_prob, multi_class='ovr', average='macro')
        except Exception:
            roc_auc = np.nan

    report_dict = classification_report(y_test, y_pred, target_names=class_labels, output_dict=True, zero_division=0)

    return {
        'Accuracy': float(acc),
        'Precision': float(prec_macro),
        'Recall': float(rec_macro),
        'Macro F1': float(f1_macro),
        'Weighted F1': float(f1_weighted),
        'ROC-AUC': float(roc_auc) if not np.isnan(roc_auc) else None,
        'Dropout Precision': float(report_dict['Dropout']['precision']),
        'Dropout Recall': float(report_dict['Dropout']['recall']),
        'Dropout F1': float(report_dict['Dropout']['f1-score']),
        'y_pred': y_pred,
        'y_prob': y_prob
    }


if __name__ == '__main__':
    main()

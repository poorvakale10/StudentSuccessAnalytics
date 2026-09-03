import os
import pickle
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_recall_fscore_support, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
import shap

COURSE_MAP = {
    33: "Biofuel Production Technologies",
    171: "Animation and Multimedia Design",
    8014: "Social Service (Evening)",
    9003: "Agronomy",
    9070: "Communication Design",
    9085: "Veterinary Nursing",
    9119: "Informatics Engineering",
    9130: "Equiniculture",
    9147: "Management",
    9238: "Social Service (Day)",
    9254: "Tourism",
    9500: "Nursing",
    9556: "Oral Hygiene",
    9670: "Advertising & Marketing",
    9773: "Journalism & Communication",
    9853: "Basic Education",
    9991: "Management (Evening)"
}

FEATURE_COLS = [
    'previous_qualification_grade',
    'admission_grade',
    'first_sem_grade',
    'first_sem_approval_rate',
    'attendance_type',
    'debtor',
    'tuition_up_to_date',
    'scholarship_holder',
    'age_at_enrollment',
    'gender',
    'marital_status',
    'displaced',
    'mother_qualification',
    'father_qualification',
    'application_mode',
    'course',
    'unemployment_rate',
    'gdp'
]

TARGET_MAP = {'Dropout': 0, 'Enrolled': 1, 'Graduate': 2}
TARGET_NAMES = ['Dropout', 'Enrolled', 'Graduate']

def load_and_preprocess(data_path):
    df = pd.read_csv(data_path, sep=';')
    df.columns = [c.strip() for c in df.columns]

    # Feature engineering for approval rate
    enrolled = df['Curricular units 1st sem (enrolled)']
    approved = df['Curricular units 1st sem (approved)']
    df['first_sem_approval_rate'] = np.where(enrolled > 0, approved / enrolled, 0.0)

    # Rename to feature column names
    rename_dict = {
        'Previous qualification (grade)': 'previous_qualification_grade',
        'Admission grade': 'admission_grade',
        'Curricular units 1st sem (grade)': 'first_sem_grade',
        'Daytime/evening attendance': 'attendance_type',
        'Debtor': 'debtor',
        'Tuition fees up to date': 'tuition_up_to_date',
        'Scholarship holder': 'scholarship_holder',
        'Age at enrollment': 'age_at_enrollment',
        'Gender': 'gender',
        'Marital status': 'marital_status',
        'Displaced': 'displaced',
        "Mother's qualification": 'mother_qualification',
        "Father's qualification": 'father_qualification',
        'Application mode': 'application_mode',
        'Course': 'course',
        'Unemployment rate': 'unemployment_rate',
        'GDP': 'gdp'
    }

    df = df.rename(columns=rename_dict)
    
    # Handle missing/extra columns cleanly
    X = df[FEATURE_COLS].copy()
    y = df['Target'].map(TARGET_MAP)

    return df, X, y

def train_and_evaluate(data_path='data/data.csv', artifacts_dir='backend/artifacts'):
    os.makedirs(artifacts_dir, exist_ok=True)

    df_raw, X, y = load_and_preprocess(data_path)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        'Logistic Regression': LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=150, max_depth=12, class_weight='balanced', random_state=42),
        'XGBoost': XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.08, eval_metric='mlogloss', random_state=42),
        'SVM': SVC(probability=True, class_weight='balanced', random_state=42)
    }

    metrics_results = {}
    fitted_models = {}

    best_name = None
    best_macro_f1 = -1.0

    for name, model in models.items():
        if name in ['Logistic Regression', 'SVM']:
            model.fit(X_train_scaled, y_train)
            preds = model.predict(X_test_scaled)
            probs = model.predict_proba(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            probs = model.predict_proba(X_test)

        acc = float(accuracy_score(y_test, preds))
        macro_f1 = float(f1_score(y_test, preds, average='macro'))
        
        prec, rec, f1_cls, _ = precision_recall_fscore_support(y_test, preds, average=None)
        cm = confusion_matrix(y_test, preds).tolist()

        metrics_results[name] = {
            'accuracy': round(acc, 4),
            'macro_f1': round(macro_f1, 4),
            'per_class': {
                TARGET_NAMES[i]: {
                    'precision': round(float(prec[i]), 4),
                    'recall': round(float(rec[i]), 4),
                    'f1': round(float(f1_cls[i]), 4)
                } for i in range(3)
            },
            'confusion_matrix': cm
        }
        fitted_models[name] = model

        if macro_f1 > best_macro_f1:
            best_macro_f1 = macro_f1
            best_name = name

    print(f"Best model based on Macro-F1: {best_name} (Macro F1 = {best_macro_f1:.4f})")

    best_model = fitted_models[best_name]

    # Compute SHAP explainer for best model
    if best_name in ['Random Forest', 'XGBoost']:
        explainer = shap.TreeExplainer(best_model)
    else:
        explainer = shap.Explainer(best_model.predict_proba, X_train.sample(100, random_state=42))

    # Save model artifacts
    artifacts = {
        'best_model_name': best_name,
        'best_model': best_model,
        'scaler': scaler,
        'feature_names': FEATURE_COLS,
        'target_names': TARGET_NAMES,
        'target_map': TARGET_MAP,
        'fitted_models': fitted_models,
        'explainer': explainer,
        'X_background': X_train.sample(min(100, len(X_train)), random_state=42)
    }

    with open(os.path.join(artifacts_dir, 'model_artifacts.pkl'), 'wb') as f:
        pickle.dump(artifacts, f)

    # Save metrics JSON
    metrics_export = {
        'best_model_name': best_name,
        'models': metrics_results,
        'target_classes': TARGET_NAMES,
        'test_set_size': int(len(y_test))
    }
    with open(os.path.join(artifacts_dir, 'model_metrics.json'), 'w') as f:
        json.dump(metrics_export, f, indent=2)

    # Save Dataset Insights for Dashboard
    course_stats = []
    for course_id, group in df_raw.groupby('course'):
        course_name = COURSE_MAP.get(course_id, f"Course {course_id}")
        total = len(group)
        dropout_cnt = (group['Target'] == 'Dropout').sum()
        grad_cnt = (group['Target'] == 'Graduate').sum()
        enrolled_cnt = (group['Target'] == 'Enrolled').sum()
        course_stats.append({
            'course_id': int(course_id),
            'course_name': course_name,
            'total': int(total),
            'dropout_count': int(dropout_cnt),
            'graduate_count': int(grad_cnt),
            'enrolled_count': int(enrolled_cnt),
            'dropout_rate': round(float(dropout_cnt / total), 4),
            'graduate_rate': round(float(grad_cnt / total), 4)
        })
    course_stats.sort(key=lambda x: x['total'], reverse=True)

    financial_stats = {
        'tuition_up_to_date': {
            'paid': {
                'total': int((df_raw['tuition_up_to_date'] == 1).sum()),
                'dropout_rate': round(float((df_raw[df_raw['tuition_up_to_date'] == 1]['Target'] == 'Dropout').mean()), 4)
            },
            'unpaid': {
                'total': int((df_raw['tuition_up_to_date'] == 0).sum()),
                'dropout_rate': round(float((df_raw[df_raw['tuition_up_to_date'] == 0]['Target'] == 'Dropout').mean()), 4)
            }
        },
        'debtor': {
            'yes': {
                'total': int((df_raw['debtor'] == 1).sum()),
                'dropout_rate': round(float((df_raw[df_raw['debtor'] == 1]['Target'] == 'Dropout').mean()), 4)
            },
            'no': {
                'total': int((df_raw['debtor'] == 0).sum()),
                'dropout_rate': round(float((df_raw[df_raw['debtor'] == 0]['Target'] == 'Dropout').mean()), 4)
            }
        },
        'scholarship': {
            'yes': {
                'total': int((df_raw['scholarship_holder'] == 1).sum()),
                'dropout_rate': round(float((df_raw[df_raw['scholarship_holder'] == 1]['Target'] == 'Dropout').mean()), 4)
            },
            'no': {
                'total': int((df_raw['scholarship_holder'] == 0).sum()),
                'dropout_rate': round(float((df_raw[df_raw['scholarship_holder'] == 0]['Target'] == 'Dropout').mean()), 4)
            }
        }
    }

    grade_dist = {}
    for outcome in ['Dropout', 'Enrolled', 'Graduate']:
        sub = df_raw[df_raw['Target'] == outcome]['first_sem_grade']
        grade_dist[outcome] = {
            'mean': round(float(sub.mean()), 2),
            'median': round(float(sub.median()), 2),
            'std': round(float(sub.std()), 2),
            'min': round(float(sub.min()), 2),
            'max': round(float(sub.max()), 2),
            'q25': round(float(sub.quantile(0.25)), 2),
            'q75': round(float(sub.quantile(0.75)), 2)
        }

    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
    else:
        importances = np.abs(best_model.coef_).mean(axis=0)

    feature_importance_list = [
        {'feature': FEATURE_COLS[i], 'importance': round(float(importances[i]), 4)}
        for i in range(len(FEATURE_COLS))
    ]
    feature_importance_list.sort(key=lambda x: x['importance'], reverse=True)

    total_students = len(df_raw)
    dropout_total = int((df_raw['Target'] == 'Dropout').sum())
    graduate_total = int((df_raw['Target'] == 'Graduate').sum())
    enrolled_total = int((df_raw['Target'] == 'Enrolled').sum())

    dataset_insights = {
        'total_students': total_students,
        'overall_rates': {
            'dropout': round(dropout_total / total_students, 4),
            'graduate': round(graduate_total / total_students, 4),
            'enrolled': round(enrolled_total / total_students, 4)
        },
        'counts': {
            'dropout': dropout_total,
            'graduate': graduate_total,
            'enrolled': enrolled_total
        },
        'course_stats': course_stats,
        'financial_stats': financial_stats,
        'grade_dist': grade_dist,
        'feature_importance': feature_importance_list
    }

    with open(os.path.join(artifacts_dir, 'dataset_insights.json'), 'w') as f:
        json.dump(dataset_insights, f, indent=2)

    print("Training and artifact generation completed successfully!")
    return metrics_results, dataset_insights

if __name__ == '__main__':
    train_and_evaluate()

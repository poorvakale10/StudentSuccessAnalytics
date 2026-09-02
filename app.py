"""
Student Success Analytics - Early Warning & Academic Risk Intelligence
=======================================================================
A premium, dark-themed SaaS analytics dashboard for academic risk identification.
Uses Plotly for interactive visualization and Random Forest (Balanced) pipeline for predictions.
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import joblib
import plotly.express as px
import plotly.graph_objects as go

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ------------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIG & COHESIVE DARK SAAS CSS DESIGN SYSTEM
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Success Analytics - Early Warning System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Force a unified, premium Dark SaaS theme across all browser preference settings
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Dark Theme Overrides */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #F8FAFC !important;
        background-color: #0B0F19 !important;
    }

    /* Completely hide sidebar and collapse toggle */
    section[data-testid="stSidebar"],
    div[data-testid="collapsedControl"] {
        display: none !important;
        width: 0 !important;
    }

    /* Full-width container padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1350px;
    }

    /* Brand Headers */
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        line-height: 1.25 !important;
        background: linear-gradient(135deg, #60A5FA 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.025em;
        margin-bottom: 0.2rem;
    }
    .brand-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        font-weight: 500;
        margin-bottom: 1.25rem;
    }

    /* -------------------------------------------------------------------------- */
    /* SLEEK NATIVE STREAMLIT TOP TABS STYLED AS WEBSITE NAVBAR                  */
    /* -------------------------------------------------------------------------- */
    div[data-baseweb="tab-list"] {
        background: rgba(17, 24, 39, 0.6) !important;
        padding: 0.4rem 0.5rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        gap: 0.5rem !important;
        margin-bottom: 1.5rem !important;
    }

    button[data-baseweb="tab"] {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.25rem !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease-in-out !important;
        height: auto !important;
    }

    button[data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #F8FAFC !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
        border-color: #60A5FA !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }

    /* Remove default tab border & underline */
    div[data-baseweb="tab-highlight"],
    div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Glassmorphic Dark Cards */
    .saas-card {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    }
    
    /* KPI Metric Cards */
    .kpi-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        border-color: rgba(96, 165, 250, 0.4);
        transform: translateY(-2px);
    }
    .kpi-val {
        font-size: 1.75rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }
    .kpi-lbl {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.35rem;
    }

    /* Step Workflow Cards */
    .step-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 1.1rem;
        height: 100%;
    }
    .step-badge {
        font-size: 0.8rem;
        font-weight: 800;
        color: #60A5FA;
        background: rgba(37, 99, 235, 0.2);
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        border: 1px solid rgba(96, 165, 250, 0.3);
        margin-bottom: 0.6rem;
    }
    .step-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 0.3rem;
    }
    .step-desc {
        font-size: 0.82rem;
        color: #94A3B8;
        line-height: 1.45;
    }

    /* Section Headings */
    .section-head {
        font-size: 1.2rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 1.25rem;
        margin-bottom: 0.85rem;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Risk Badges */
    .risk-pill-low {
        background: rgba(22, 163, 74, 0.2);
        color: #4ADE80;
        border: 1px solid rgba(74, 222, 128, 0.4);
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.05rem;
        display: inline-block;
    }
    .risk-pill-mod {
        background: rgba(217, 119, 6, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(251, 191, 36, 0.4);
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.05rem;
        display: inline-block;
    }
    .risk-pill-high {
        background: rgba(220, 38, 38, 0.2);
        color: #F87171;
        border: 1px solid rgba(248, 113, 113, 0.4);
        padding: 0.5rem 1.25rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.05rem;
        display: inline-block;
    }

    /* Form submit button */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #4F46E5 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border-radius: 8px !important;
        border: 1px solid #60A5FA !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }

    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 2. DATA & MODEL LOADING (CACHED)
# ------------------------------------------------------------------------------
@st.cache_data
def load_dataset():
    data_path = "data/data.csv"
    if not os.path.exists(data_path):
        st.error(f"Dataset file not found at '{data_path}'. Please verify repository path.")
        return None
    df = pd.read_csv(data_path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip().replace('"', '') for c in df.columns]
    return df


@st.cache_resource
def load_model_artifacts():
    model_path = "models/best_model.pkl"
    meta_path = "models/model_metadata.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(meta_path):
        st.error("Model artifacts not found in 'models/'. Please execute model training script.")
        return None, None
        
    pipeline = joblib.load(model_path)
    metadata = joblib.load(meta_path)
    return pipeline, metadata


@st.cache_data
def load_comparison_results():
    comp_path = "results/model_comparison.csv"
    dropout_path = "results/dropout_comparison.csv"
    
    comp_df = pd.read_csv(comp_path) if os.path.exists(comp_path) else None
    dropout_df = pd.read_csv(dropout_path) if os.path.exists(dropout_path) else None
    return comp_df, dropout_df


# Load cached artifacts
df = load_dataset()
pipeline, metadata = load_model_artifacts()
df_comparison, df_dropout = load_comparison_results()


# ------------------------------------------------------------------------------
# 3. MAPPINGS FOR ENCODED CATEGORICAL VARIABLES
# ------------------------------------------------------------------------------
MARITAL_STATUS_MAP = {
    "Single": 1, "Married": 2, "Widower": 3, 
    "Divorced": 4, "Facto Union": 5, "Legally Separated": 6
}

APPLICATION_MODE_MAP = {
    "1st phase - general contingent": 1,
    "2nd phase - general contingent": 10,
    "3rd phase - general contingent": 15,
    "International student (bachelor)": 17,
    "23 years old or older": 26,
    "Transfer": 27,
    "Change of course": 39,
    "Holders of other higher courses": 7,
    "Technological specialization diploma holders": 42,
    "Change of institution/course": 43,
    "Short cycle diploma holders": 44,
    "Ordinance No. 612/93": 2,
    "Ordinance No. 854/B/99": 16,
    "1st phase - special contingent (Azores)": 5,
    "1st phase - special contingent (Madeira)": 18,
    "Change of institution/course (international)": 51,
    "Short cycle diploma holders (international)": 53,
    "Change of course (international)": 57
}

COURSE_MAP = {
    "Computer Engineering": 9119,
    "Management": 9147,
    "Nursing": 9500,
    "Tourism": 9254,
    "Social Service": 9238,
    "Social Service (evening)": 8014,
    "Communication Design": 9070,
    "Veterinary Nursing": 9085,
    "Advertising and Marketing Management": 9670,
    "Journalistic Journalism": 9773,
    "Basic Education": 9853,
    "Management (evening)": 9991,
    "Agronomy": 9003,
    "Equinculture": 9130,
    "Oral Hygiene": 9556,
    "Animation and Multimedia Design": 171,
    "Biofuel Production Technologies": 33
}

PREV_QUAL_MAP = {
    "Secondary education": 1,
    "Higher education - bachelor's degree": 2,
    "Higher education - degree": 3,
    "Higher education - master's": 4,
    "Higher education - doctorate": 5,
    "Frequency of higher education": 6,
    "12th year of schooling - not completed": 9,
    "11th year of schooling - not completed": 10,
    "Other - 11th year of schooling": 12,
    "10th year of schooling": 14,
    "10th year of schooling - not completed": 15,
    "Basic education 3rd cycle (9th/10th/11th year)": 19,
    "Basic education 2nd cycle (6th/7th/8th year)": 38,
    "Technological specialization course": 39,
    "Higher education - degree (1st cycle)": 40,
    "Professional higher technical course": 42,
    "Higher education - master (2nd cycle)": 43
}

NATIONALITY_MAP = {
    "Portuguese": 1, "Brazilian": 41, "Cape Verdean": 22,
    "Angolan": 21, "Santomean": 26, "Mozambican": 25,
    "Guinean": 24, "Spanish": 6, "Italian": 11,
    "Dutch": 13, "English": 14, "German": 2,
    "Moldavian": 100, "Ukrainian": 103, "Russian": 105,
    "Romanian": 62, "Mexican": 101, "Colombian": 109,
    "Cuban": 108, "Turkish": 32, "Lithuanian": 17
}

QUALIFICATION_MAP = {
    "Secondary Education - 12th Year": 1,
    "Higher Education - Bachelor's Degree": 2,
    "Higher Education - Degree": 3,
    "Higher Education - Master's": 4,
    "Higher Education - Doctorate": 5,
    "Basic Education 3rd Cycle (9th/10th/11th Year)": 19,
    "Basic Education 2nd Cycle (6th/7th/8th Year)": 38,
    "Basic Education 1st Cycle (4th/5th Year)": 37,
    "Unknown": 34,
    "Can't read or write": 35,
    "Can read without 4th year": 36,
    "Technological specialization course": 39,
    "Professional higher technical course": 42
}

OCCUPATION_MAP = {
    "Unskilled Workers": 9,
    "Personal Service, Security & Sellers": 5,
    "Administrative staff": 4,
    "Intermediate Level Technicians": 3,
    "Specialists in Intellectual & Scientific Activities": 2,
    "Executive Directors & Managers": 1,
    "Skilled Workers in Industry & Construction": 7,
    "Installation & Machine Operators": 8,
    "Farmers & Skilled Agricultural Workers": 6,
    "Armed Forces Professions": 10,
    "Student": 0,
    "Other Situation": 90
}


# ------------------------------------------------------------------------------
# 4. TOP WEBSITE BRAND & NAVIGATION TABS
# ------------------------------------------------------------------------------
st.markdown('<div class="brand-title">Student Success Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">Early Warning & Academic Risk Intelligence Platform</div>', unsafe_allow_html=True)

tab_dash, tab_explore, tab_perf, tab_predict = st.tabs([
    "Dashboard",
    "Data Explorer",
    "Model Performance",
    "Student Risk Prediction"
])


# ==============================================================================
# TAB 1: DASHBOARD
# ==============================================================================
with tab_dash:
    st.markdown("""
    <div class="saas-card">
        <div style="font-size: 0.95rem; color: #E2E8F0; line-height: 1.5;">
            Identify students who may need additional academic support using enrollment and first-semester performance data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Row
    st.markdown('<div class="section-head">System Overview</div>', unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown("""<div class="kpi-card"><div class="kpi-val">4,424</div><div class="kpi-lbl">Students Analyzed</div></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown("""<div class="kpi-card"><div class="kpi-val">33</div><div class="kpi-lbl">Model Features</div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown("""<div class="kpi-card"><div class="kpi-val">3</div><div class="kpi-lbl">Outcome Classes</div></div>""", unsafe_allow_html=True)
    with k4:
        acc_str = f"{metadata['metrics']['Accuracy']*100:.2f}%" if metadata and 'metrics' in metadata else "73.90%"
        st.markdown(f"""<div class="kpi-card"><div class="kpi-val">{acc_str}</div><div class="kpi-lbl">Best Model Accuracy</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Student Outcome Distribution Section
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown('<div class="section-head">Student Outcome Distribution</div>', unsafe_allow_html=True)
        if df is not None:
            target_counts = df['Target'].value_counts()
            
            categories = ['Graduate', 'Dropout', 'Enrolled']
            counts = [target_counts.get(c, 0) for c in categories]
            percentages = [(c / len(df)) * 100 for c in counts]
            colors = ['#16A34A', '#DC2626', '#2563EB']

            fig_target = go.Figure()
            fig_target.add_trace(go.Bar(
                y=categories,
                x=counts,
                orientation='h',
                marker=dict(color=colors, cornerradius=4),
                text=[f"  {cnt:,} ({pct:.2f}%)" for cnt, pct in zip(counts, percentages)],
                textposition='outside',
                textfont=dict(color='#F8FAFC', size=12, family='Plus Jakarta Sans'),
                hoverinfo='text',
                hovertext=[f"Status: {cat}<br>Count: {cnt:,}<br>Percentage: {pct:.2f}%" for cat, cnt, pct in zip(categories, counts, percentages)]
            ))

            fig_target.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=130, t=10, b=10),
                height=260,
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)', title=None, tickfont=dict(color='#94A3B8'), range=[0, 2700]),
                yaxis=dict(showgrid=False, tickfont=dict(color='#F8FAFC', size=13, weight=600), autorange="reversed"),
            )
            st.plotly_chart(fig_target, use_container_width=True, config={'displayModeBar': False})

    with col_right:
        st.markdown('<div class="section-head">Model Overview</div>', unsafe_allow_html=True)
        model_name_str = metadata.get('model_name', 'Random Forest (Balanced)') if metadata else 'Random Forest (Balanced)'
        macro_f1_str = f"{metadata['primary_metric_value']:.4f}" if metadata else "0.6898"
        roc_auc_str = f"{metadata['metrics'].get('ROC-AUC', 0.8650):.4f}" if metadata and 'metrics' in metadata else "0.8650"

        st.markdown(f"""
        <div class="saas-card" style="height: 260px; display: flex; flex-direction: column; justify-content: center;">
            <div style="margin-bottom: 0.9rem;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Selected Model</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #F8FAFC;">{model_name_str}</div>
            </div>
            <div style="margin-bottom: 0.9rem;">
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Primary Selection Metric</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #60A5FA;">Macro F1: {macro_f1_str}</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">Multiclass ROC-AUC</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #A855F7;">{roc_auc_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # How the system works
    st.markdown('<div class="section-head">System Workflow</div>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown("""
        <div class="step-card">
            <div class="step-badge">01</div>
            <div class="step-title">Student Data</div>
            <div class="step-desc">Enrollment and first-semester performance information gathered.</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="step-card">
            <div class="step-badge">02</div>
            <div class="step-title">Feature Engineering</div>
            <div class="step-desc">Academic performance ratios are calculated.</div>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="step-card">
            <div class="step-badge">03</div>
            <div class="step-title">ML Risk Assessment</div>
            <div class="step-desc">Random Forest evaluates student outcomes.</div>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div class="step-card">
            <div class="step-badge">04</div>
            <div class="step-title">Early Intervention</div>
            <div class="step-desc">Risk level and support recommendations are generated.</div>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# TAB 2: DATA EXPLORER
# ==============================================================================
with tab_explore:
    if df is not None:
        # Compact Summary Bar
        st.markdown("""
        <div class="saas-card" style="padding: 0.85rem 1.25rem;">
            <div style="display: flex; gap: 2.5rem; flex-wrap: wrap; font-size: 0.9rem; color: #CBD5E1;">
                <div><span style="color: #94A3B8;">Students:</span> <b>4,424</b></div>
                <div><span style="color: #94A3B8;">Raw Features:</span> <b>30</b></div>
                <div><span style="color: #94A3B8;">Engineered Features:</span> <b>3</b></div>
                <div><span style="color: #94A3B8;">Target Classes:</span> <b>3 (Graduate, Dropout, Enrolled)</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info("Data Leakage Safeguard: All six second-semester features (Curricular units 2nd sem...) are displayed in raw exploratory views below for domain context, but are strictly excluded from the prediction model because they represent future information unavailable at the end of the first semester.")

        subtab1, subtab2, subtab3, subtab4 = st.tabs(["Dataset Preview", "Feature Overview", "Target Distribution", "Data Quality"])

        with subtab1:
            st.markdown('<div class="section-head">Dataset Preview</div>', unsafe_allow_html=True)
            st.dataframe(df.head(25), use_container_width=True)
            st.caption(f"Displaying first 25 of {len(df):,} student records.")

        with subtab2:
            st.markdown('<div class="section-head">Feature Categorization (33 Total Input Features)</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("""
                <div class="saas-card">
                    <div style="font-weight: 700; color: #60A5FA; margin-bottom: 0.5rem;">Background & Enrollment Features (18)</div>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; margin: 0; padding-left: 1.2rem; line-height: 1.6;">
                        <li><b>Demographics:</b> Age at enrollment, Gender, Marital status, Nationality, Displaced student, International</li>
                        <li><b>Prior Academic:</b> Previous qualification, Previous qualification grade, Admission grade</li>
                        <li><b>Program & Entry:</b> Course, Application mode, Application order preference, Attendance type</li>
                        <li><b>Family Background:</b> Mother's qualification, Father's qualification, Mother's occupation, Father's occupation, Educational special needs</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="saas-card">
                    <div style="font-weight: 700; color: #60A5FA; margin-bottom: 0.5rem;">Financial & Socioeconomic Features (6)</div>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; margin: 0; padding-left: 1.2rem; line-height: 1.6;">
                        <li>Tuition fees up to date (Binary indicator)</li>
                        <li>Debtor status (Overdue tuition payment indicator)</li>
                        <li>Scholarship holder (Binary grant status)</li>
                        <li>Macroeconomic Indicators: Unemployment rate, Inflation rate, GDP growth rate</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown("""
                <div class="saas-card">
                    <div style="font-weight: 700; color: #60A5FA; margin-bottom: 0.5rem;">First-Semester Academic Features (6)</div>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; margin: 0; padding-left: 1.2rem; line-height: 1.6;">
                        <li>Curricular units 1st sem (credited)</li>
                        <li>Curricular units 1st sem (enrolled)</li>
                        <li>Curricular units 1st sem (evaluations)</li>
                        <li>Curricular units 1st sem (approved)</li>
                        <li>Curricular units 1st sem (grade)</li>
                        <li>Curricular units 1st sem (without evaluations)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="saas-card">
                    <div style="font-weight: 700; color: #A855F7; margin-bottom: 0.5rem;">Engineered Academic Performance Ratios (3)</div>
                    <ul style="font-size: 0.85rem; color: #CBD5E1; margin: 0; padding-left: 1.2rem; line-height: 1.6;">
                        <li><b>First_Sem_Approval_Rate:</b> Approved units / Evaluated units</li>
                        <li><b>First_Sem_Completion_Rate:</b> Approved units / Enrolled units</li>
                        <li><b>First_Sem_Evaluation_Rate:</b> First-semester evaluation participation ratio (Evaluated units / Enrolled units)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        with subtab3:
            st.markdown('<div class="section-head">Interactive Visualizations</div>', unsafe_allow_html=True)
            chart_choice = st.selectbox(
                "Select Interactive Analysis Chart:",
                [
                    "1st Semester Grade Distribution vs Target",
                    "1st Semester Approved Units vs Target",
                    "Tuition Fees Status vs Target",
                    "Scholarship Status vs Target",
                    "Age at Enrollment Distribution"
                ]
            )

            if chart_choice == "1st Semester Grade Distribution vs Target":
                fig_box = px.box(
                    df, x='Target', y='Curricular units 1st sem (grade)', color='Target',
                    color_discrete_map={'Graduate': '#16A34A', 'Dropout': '#DC2626', 'Enrolled': '#2563EB'},
                    title="1st Semester Grade Distribution across Outcomes"
                )
                fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'))
                st.plotly_chart(fig_box, use_container_width=True)

            elif chart_choice == "1st Semester Approved Units vs Target":
                fig_box = px.box(
                    df, x='Target', y='Curricular units 1st sem (approved)', color='Target',
                    color_discrete_map={'Graduate': '#16A34A', 'Dropout': '#DC2626', 'Enrolled': '#2563EB'},
                    title="1st Semester Approved Units across Outcomes"
                )
                fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'))
                st.plotly_chart(fig_box, use_container_width=True)

            elif chart_choice == "Tuition Fees Status vs Target":
                ct = pd.crosstab(df['Tuition fees up to date'], df['Target'], normalize='index') * 100
                fig_bar = px.bar(
                    ct, barmode='stack', color_discrete_map={'Graduate': '#16A34A', 'Dropout': '#DC2626', 'Enrolled': '#2563EB'},
                    title="Outcome Percentage by Tuition Fee Payment Status"
                )
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'),
                                      xaxis=dict(tickvals=[0, 1], ticktext=['Overdue (0)', 'Up to Date (1)']))
                st.plotly_chart(fig_bar, use_container_width=True)

            elif chart_choice == "Scholarship Status vs Target":
                ct = pd.crosstab(df['Scholarship holder'], df['Target'], normalize='index') * 100
                fig_bar = px.bar(
                    ct, barmode='stack', color_discrete_map={'Graduate': '#16A34A', 'Dropout': '#DC2626', 'Enrolled': '#2563EB'},
                    title="Outcome Percentage by Scholarship Holder Status"
                )
                fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'),
                                      xaxis=dict(tickvals=[0, 1], ticktext=['Non-Scholarship (0)', 'Scholarship Holder (1)']))
                st.plotly_chart(fig_bar, use_container_width=True)

            elif chart_choice == "Age at Enrollment Distribution":
                fig_hist = px.histogram(df, x='Age at enrollment', color='Target', marginal='rug',
                                         color_discrete_map={'Graduate': '#16A34A', 'Dropout': '#DC2626', 'Enrolled': '#2563EB'},
                                         title="Distribution of Age at Enrollment by Outcome")
                fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'))
                st.plotly_chart(fig_hist, use_container_width=True)

        with subtab4:
            st.markdown('<div class="section-head">Data Quality & Audit Verification</div>', unsafe_allow_html=True)
            q1, q2, q3, q4 = st.columns(4)
            with q1:
                st.markdown("""<div class="kpi-card"><div class="kpi-val">0</div><div class="kpi-lbl">Missing Values</div></div>""", unsafe_allow_html=True)
            with q2:
                st.markdown("""<div class="kpi-card"><div class="kpi-val">0</div><div class="kpi-lbl">Duplicate Rows</div></div>""", unsafe_allow_html=True)
            with q3:
                st.markdown("""<div class="kpi-card"><div class="kpi-val">80 / 20</div><div class="kpi-lbl">Train / Test Split</div></div>""", unsafe_allow_html=True)
            with q4:
                st.markdown("""<div class="kpi-card"><div class="kpi-val">Enforced</div><div class="kpi-lbl">Leakage Guard</div></div>""", unsafe_allow_html=True)


# ==============================================================================
# TAB 3: MODEL PERFORMANCE
# ==============================================================================
with tab_perf:
    # Selected Model Card
    st.markdown("""
    <div class="saas-card" style="border-left: 4px solid #2563EB;">
        <div style="font-size: 0.78rem; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.05em;">Selected Model</div>
        <div style="font-size: 1.4rem; font-weight: 800; color: #F8FAFC; margin: 0.2rem 0 0.75rem 0;">Random Forest (Balanced)</div>
        <div style="display: flex; gap: 2.5rem; flex-wrap: wrap;">
            <div><span style="font-size: 0.8rem; color: #94A3B8;">Accuracy:</span> <b style="font-size: 1.05rem; color: #F8FAFC;">73.90%</b></div>
            <div><span style="font-size: 0.8rem; color: #94A3B8;">Macro F1:</span> <b style="font-size: 1.05rem; color: #60A5FA;">0.6898</b></div>
            <div><span style="font-size: 0.8rem; color: #94A3B8;">ROC-AUC:</span> <b style="font-size: 1.05rem; color: #A855F7;">0.8650</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model Comparison Table
    if df_comparison is not None:
        st.markdown('<div class="section-head">Model Benchmark Comparison</div>', unsafe_allow_html=True)
        st.dataframe(
            df_comparison.style.highlight_max(subset=['Macro F1', 'Accuracy', 'ROC-AUC'], color='#1E3A8A'),
            use_container_width=True
        )

    # Explanation Box: Why Random Forest (Balanced)?
    st.markdown("""
    <div class="saas-card">
        <div style="font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.35rem;">Why Random Forest (Balanced)?</div>
        <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.5;">
            The balanced Random Forest model was selected using <b>Macro F1</b> because the dataset contains three outcome classes with noticeable class imbalance (Graduate 49.93%, Dropout 32.12%, Enrolled 17.95%). Macro F1 gives equal importance to each class rather than allowing the majority Graduate class to dominate model selection.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dropout-Specific Performance Table
    st.markdown('<div class="section-head">Dropout-Specific Performance</div>', unsafe_allow_html=True)
    
    if df_dropout is not None:
        st.dataframe(
            df_dropout.style.highlight_max(subset=['Dropout Precision', 'Dropout Recall', 'Dropout F1'], color='#4C1D95'),
            use_container_width=True
        )

    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown("""<div class="kpi-card"><div class="kpi-val" style="color:#F8FAFC;">79.84%</div><div class="kpi-lbl">Selected Model Dropout Precision</div></div>""", unsafe_allow_html=True)
    with d2:
        st.markdown("""<div class="kpi-card"><div class="kpi-val" style="color:#F8FAFC;">69.72%</div><div class="kpi-lbl">Selected Model Dropout Recall</div></div>""", unsafe_allow_html=True)
    with d3:
        st.markdown("""<div class="kpi-card"><div class="kpi-val" style="color:#60A5FA;">74.44%</div><div class="kpi-lbl">Selected Model Dropout F1</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Confusion Matrix & Feature Importance
    c_left, c_right = st.columns([1, 1.2])

    with c_left:
        st.markdown('<div class="section-head">Confusion Matrix - Random Forest (Balanced)</div>', unsafe_allow_html=True)
        cm_image_path = "results/best_model_confusion_matrix.png"
        if os.path.exists(cm_image_path):
            st.image(cm_image_path, use_container_width=True)
        else:
            st.info("Confusion matrix image file saved at 'results/best_model_confusion_matrix.png'.")

    with c_right:
        st.markdown('<div class="section-head">Top 15 Feature Importances</div>', unsafe_allow_html=True)
        fi_path = "results/feature_importance/random_forest_balanced_importance.csv"
        if os.path.exists(fi_path):
            fi_df = pd.read_csv(fi_path)
            top_fi = fi_df.head(15).sort_values(by='Importance', ascending=True)

            fig_fi = px.bar(
                top_fi, x='Importance', y='Feature', orientation='h',
                title="Random Forest Feature Importance Scores",
                color='Importance', color_continuous_scale='Viridis'
            )
            fig_fi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                 font=dict(color='#F8FAFC'), coloraxis_showscale=False,
                                 margin=dict(l=0, r=10, t=30, b=10))
            st.plotly_chart(fig_fi, use_container_width=True)

            st.caption("Feature importance indicates which variables were most influential in the trained Random Forest model. It does not imply causation.")


# ==============================================================================
# TAB 4: STUDENT RISK PREDICTION
# ==============================================================================
with tab_predict:
    if pipeline is None:
        st.error("Model pipeline is not loaded. Please ensure 'models/best_model.pkl' exists.")
    else:
        with st.form("student_assessment_form"):
            st.markdown('<div class="section-head">SECTION 1: Student Profile</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                age = st.number_input("Age at enrollment", min_value=17, max_value=70, value=20)
                gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
            with col2:
                marital = st.selectbox("Marital status", options=list(MARITAL_STATUS_MAP.keys()))
                nationality = st.selectbox("Nationality", options=list(NATIONALITY_MAP.keys()))
            with col3:
                displaced = st.selectbox("Displaced student", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", help="Living away from hometown")
                international = st.selectbox("International student", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")

            st.markdown('<div class="section-head">SECTION 2: Academic Background</div>', unsafe_allow_html=True)
            col4, col5, col6 = st.columns(3)
            with col4:
                prev_qual = st.selectbox("Previous qualification", options=list(PREV_QUAL_MAP.keys()))
                prev_grade = st.number_input("Previous qualification grade (0-200)", min_value=0.0, max_value=200.0, value=130.0)
            with col5:
                adm_grade = st.number_input("Admission grade (0-200)", min_value=0.0, max_value=200.0, value=125.0)
                course = st.selectbox("Course", options=list(COURSE_MAP.keys()))
            with col6:
                app_mode = st.selectbox("Application mode", options=list(APPLICATION_MODE_MAP.keys()))
                app_order = st.number_input("Application order (0-9)", min_value=0, max_value=9, value=1)

            st.markdown('<div class="section-head">SECTION 3: Financial & Support Indicators</div>', unsafe_allow_html=True)
            col7, col8, col9 = st.columns(3)
            with col7:
                tuition_up_to_date = st.selectbox("Tuition fees up to date", options=[1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
                debtor = st.selectbox("Debtor status", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes", help="Has overdue financial payments")
                scholarship = st.selectbox("Scholarship holder", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
            with col8:
                special_needs = st.selectbox("Educational special needs", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
                mother_qual = st.selectbox("Mother's qualification", options=list(QUALIFICATION_MAP.keys()))
                father_qual = st.selectbox("Father's qualification", options=list(QUALIFICATION_MAP.keys()))
            with col9:
                day_night = st.selectbox("Attendance type", options=[1, 0], format_func=lambda x: "Daytime" if x == 1 else "Evening")
                mother_occ = st.selectbox("Mother's occupation", options=list(OCCUPATION_MAP.keys()))
                father_occ = st.selectbox("Father's occupation", options=list(OCCUPATION_MAP.keys()))

            # Background macro defaults
            unemp_rate = 10.8
            inf_rate = 1.4
            gdp = 1.74

            st.markdown('<div class="section-head">SECTION 4: First-Semester Performance</div>', unsafe_allow_html=True)
            col10, col11, col12 = st.columns(3)
            with col10:
                sem1_enrolled = st.number_input("Curricular units enrolled", min_value=0, max_value=30, value=6)
                sem1_evals = st.number_input("Curricular units evaluated", min_value=0, max_value=35, value=6)
            with col11:
                sem1_approved = st.number_input("Curricular units approved", min_value=0, max_value=30, value=5)
                sem1_grade = st.number_input("First-semester grade (0-20)", min_value=0.0, max_value=20.0, value=12.5)
            with col12:
                sem1_credited = st.number_input("Curricular units credited", min_value=0, max_value=20, value=0)
                sem1_no_eval = st.number_input("Curricular units without evaluations", min_value=0, max_value=15, value=0)

            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("Assess Student Risk", use_container_width=True)

        if submit_btn:
            input_dict = {
                'Marital status': MARITAL_STATUS_MAP[marital],
                'Application mode': APPLICATION_MODE_MAP[app_mode],
                'Application order': app_order,
                'Course': COURSE_MAP[course],
                'Daytime/evening attendance': day_night,
                'Previous qualification': PREV_QUAL_MAP[prev_qual],
                'Previous qualification (grade)': prev_grade,
                'Nacionality': NATIONALITY_MAP[nationality],
                "Mother's qualification": QUALIFICATION_MAP[mother_qual],
                "Father's qualification": QUALIFICATION_MAP[father_qual],
                "Mother's occupation": OCCUPATION_MAP[mother_occ],
                "Father's occupation": OCCUPATION_MAP[father_occ],
                'Admission grade': adm_grade,
                'Displaced': displaced,
                'Educational special needs': special_needs,
                'Debtor': debtor,
                'Tuition fees up to date': tuition_up_to_date,
                'Gender': gender,
                'Scholarship holder': scholarship,
                'Age at enrollment': age,
                'International': international,
                'Unemployment rate': unemp_rate,
                'Inflation rate': inf_rate,
                'GDP': gdp,
                'Curricular units 1st sem (credited)': sem1_credited,
                'Curricular units 1st sem (enrolled)': sem1_enrolled,
                'Curricular units 1st sem (evaluations)': sem1_evals,
                'Curricular units 1st sem (approved)': sem1_approved,
                'Curricular units 1st sem (grade)': sem1_grade,
                'Curricular units 1st sem (without evaluations)': sem1_no_eval
            }

            raw_input_df = pd.DataFrame([input_dict])

            try:
                prediction = pipeline.predict(raw_input_df)[0]
                probabilities = pipeline.predict_proba(raw_input_df)[0]
                
                target_classes = list(pipeline.classes_)
                prob_dict = dict(zip(target_classes, probabilities))

                dropout_prob = prob_dict.get('Dropout', 0.0) * 100
                enrolled_prob = prob_dict.get('Enrolled', 0.0) * 100
                graduate_prob = prob_dict.get('Graduate', 0.0) * 100

                st.markdown("---")
                st.markdown('<div class="section-head">Risk Assessment Result</div>', unsafe_allow_html=True)

                res_left, res_right = st.columns([1, 1])

                with res_left:
                    st.markdown(f"<div style='font-size:0.9rem; color:#94A3B8; font-weight:600;'>PREDICTED OUTCOME</div><div style='font-size:1.6rem; font-weight:800; color:#F8FAFC;'>{prediction.upper()}</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    if dropout_prob < 30.0:
                        risk_level = "LOW RISK"
                        st.markdown('<div class="risk-pill-low">LOW RISK</div>', unsafe_allow_html=True)
                        st.markdown("<p style='font-size:0.85rem; color:#CBD5E1; margin-top:0.6rem;'>The current first-semester profile indicates a relatively lower estimated probability of dropout.</p>", unsafe_allow_html=True)
                    elif dropout_prob < 60.0:
                        risk_level = "MODERATE RISK"
                        st.markdown('<div class="risk-pill-mod">MODERATE RISK</div>', unsafe_allow_html=True)
                        st.markdown("<p style='font-size:0.85rem; color:#CBD5E1; margin-top:0.6rem;'>The current profile indicates moderate risk. Academic advising check-ins are recommended.</p>", unsafe_allow_html=True)
                    else:
                        risk_level = "HIGH RISK"
                        st.markdown('<div class="risk-pill-high">HIGH RISK</div>', unsafe_allow_html=True)
                        st.markdown("<p style='font-size:0.85rem; color:#CBD5E1; margin-top:0.6rem;'>The current profile indicates elevated dropout probability. Immediate academic intervention recommended.</p>", unsafe_allow_html=True)

                with res_right:
                    # Interactive Plotly Donut Chart for Outcome Probabilities
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=['Graduate', 'Dropout', 'Enrolled'],
                        values=[graduate_prob, dropout_prob, enrolled_prob],
                        hole=.6,
                        marker=dict(colors=['#16A34A', '#DC2626', '#2563EB']),
                        textinfo='percent+label',
                        textposition='inside',
                        hoverinfo='label+percent'
                    )])
                    fig_donut.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=200,
                        annotations=[dict(text=f"Dropout<br><b>{dropout_prob:.1f}%</b>", x=0.5, y=0.5, font_size=14, font_color="#F8FAFC", showarrow=False)]
                    )
                    st.plotly_chart(fig_donut, use_container_width=True)

                st.markdown("---")
                f_left, f_right = st.columns(2)

                with f_left:
                    st.markdown('<div class="section-head">Observed Risk Factors</div>', unsafe_allow_html=True)
                    factors = []
                    if sem1_approved < (sem1_enrolled / 2):
                        factors.append("Low first-semester unit completion: Approved less than 50% of enrolled course load.")
                    if sem1_grade < 10.0:
                        factors.append("Low first-semester academic average (below 10.0 passing threshold).")
                    if tuition_up_to_date == 0:
                        factors.append("Tuition payment status is overdue.")
                    if debtor == 1:
                        factors.append("Student account has an active debtor balance.")
                    if scholarship == 0:
                        factors.append("Non-scholarship holder status.")
                    if age > 25:
                        factors.append("Mature student entry age (>25 years).")

                    if factors:
                        for fac in factors:
                            st.write(f"• {fac}")
                    else:
                        st.write("• No major elevated risk factors detected for this profile.")

                with f_right:
                    st.markdown('<div class="section-head">Recommended Support</div>', unsafe_allow_html=True)
                    if risk_level == "HIGH RISK":
                        st.write("• Schedule priority academic advising session.")
                        st.write("• Assign faculty mentor for progress monitoring.")
                        st.write("• Refer to student bursar / welfare office for financial support options.")
                        st.write("• Enroll in academic tutoring and remediation programs.")
                    elif risk_level == "MODERATE RISK":
                        st.write("• Regular academic progress monitoring.")
                        st.write("• Connect with peer study groups and faculty advisors.")
                        st.write("• Conduct financial advisory review.")
                    else:
                        st.write("• Continue regular academic progress monitoring.")

                st.markdown("<br>", unsafe_allow_html=True)
                st.caption("Predictions are based on historical patterns in the training dataset and should support, not replace, academic advising decisions.")

            except Exception as e:
                st.error(f"Prediction error: {str(e)}")




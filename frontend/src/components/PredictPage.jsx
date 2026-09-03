import React, { useState } from 'react';
import { 
  Calculator, CheckCircle, AlertTriangle, ShieldAlert, ChevronRight, ChevronLeft, Sparkles, RefreshCw, Award, ArrowUpRight, ArrowDownRight, Info, UserCheck, AlertOctagon
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const COURSE_OPTIONS = [
  { id: 9254, name: "Tourism" },
  { id: 9500, name: "Nursing" },
  { id: 9119, name: "Informatics Engineering" },
  { id: 9147, name: "Management" },
  { id: 9070, name: "Communication Design" },
  { id: 9238, name: "Social Service (Day)" },
  { id: 8014, name: "Social Service (Evening)" },
  { id: 9670, name: "Advertising & Marketing" },
  { id: 9773, name: "Journalism & Communication" },
  { id: 171, name: "Animation and Multimedia Design" },
  { id: 9003, name: "Agronomy" },
  { id: 9085, name: "Veterinary Nursing" },
  { id: 9556, name: "Oral Hygiene" },
  { id: 9853, name: "Basic Education" },
  { id: 33, name: "Biofuel Production Technologies" }
];

const PRESETS = {
  highRisk: {
    name: "High Dropout Risk Profile",
    icon: "🔴",
    description: "Overdue tuition, debtor, 20% 1st sem approval, 8.5/20 grade",
    values: {
      previous_qualification_grade: 120.0,
      admission_grade: 115.0,
      first_sem_grade: 8.5,
      first_sem_approval_rate: 0.20,
      attendance_type: 1,
      debtor: 1,
      tuition_up_to_date: 0,
      scholarship_holder: 0,
      age_at_enrollment: 24,
      gender: 1,
      marital_status: 1,
      displaced: 1,
      mother_qualification: 1,
      father_qualification: 1,
      application_mode: 1,
      course: 9254,
      unemployment_rate: 12.4,
      gdp: -1.5
    }
  },
  graduate: {
    name: "High Performing Graduate Profile",
    icon: "🟢",
    description: "Paid tuition, scholarship holder, 100% approval, 15.5/20 grade",
    values: {
      previous_qualification_grade: 150.0,
      admission_grade: 145.0,
      first_sem_grade: 15.5,
      first_sem_approval_rate: 1.0,
      attendance_type: 1,
      debtor: 0,
      tuition_up_to_date: 1,
      scholarship_holder: 1,
      age_at_enrollment: 19,
      gender: 0,
      marital_status: 1,
      displaced: 1,
      mother_qualification: 3,
      father_qualification: 3,
      application_mode: 1,
      course: 9500,
      unemployment_rate: 8.9,
      gdp: 2.1
    }
  },
  borderline: {
    name: "Borderline Enrolled Profile",
    icon: "🟡",
    description: "Paid tuition, no scholarship, 50% approval, 11.0/20 grade",
    values: {
      previous_qualification_grade: 130.0,
      admission_grade: 125.0,
      first_sem_grade: 11.0,
      first_sem_approval_rate: 0.50,
      attendance_type: 1,
      debtor: 0,
      tuition_up_to_date: 1,
      scholarship_holder: 0,
      age_at_enrollment: 21,
      gender: 1,
      marital_status: 1,
      displaced: 0,
      mother_qualification: 1,
      father_qualification: 1,
      application_mode: 1,
      course: 9147,
      unemployment_rate: 10.8,
      gdp: 0.5
    }
  }
};

export default function PredictPage({ showToast }) {
  const [step, setStep] = useState(1);

  const [formData, setFormData] = useState({
    previous_qualification_grade: 130.0,
    admission_grade: 125.0,
    first_sem_grade: 12.0,
    first_sem_approval_rate: 0.80,
    attendance_type: 1,
    debtor: 0,
    tuition_up_to_date: 1,
    scholarship_holder: 0,
    age_at_enrollment: 20,
    gender: 1,
    marital_status: 1,
    displaced: 1,
    mother_qualification: 1,
    father_qualification: 1,
    application_mode: 1,
    course: 9254,
    unemployment_rate: 10.8,
    gdp: 1.74
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (field, val) => {
    setFormData(prev => ({ ...prev, [field]: val }));
  };

  const applyPreset = (key) => {
    const preset = PRESETS[key];
    setFormData(preset.values);
    if (showToast) showToast(`Loaded "${preset.name}" preset!`, 'info');
  };

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      if (!res.ok) throw new Error('Prediction API call failed');
      const data = await res.json();
      setResult(data);
      if (showToast) showToast(`Prediction calculated: ${data.predicted_class} (${data.risk_tier} Risk)`, 'success');
    } catch (err) {
      console.error(err);
      setError(err.message);
      if (showToast) showToast(`Error: ${err.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const stepsInfo = [
    { num: 1, title: 'Academic' },
    { num: 2, title: 'Financial' },
    { num: 3, title: 'Demographic' },
    { num: 4, title: 'Family Background' },
    { num: 5, title: 'Context & Macro' },
  ];

  return (
    <div className="space-y-8 py-6 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto">
      
      {/* Header */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 backdrop-blur-md flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <Calculator className="w-6 h-6 text-indigo-400" />
            <span>Student Risk Predictor & SHAP Explainer</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Input the 18 curated student features to generate instant 3-class retention prediction & SHAP factor breakdown.
          </p>
        </div>

        {/* Quick Presets */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => applyPreset('highRisk')}
            className="px-3 py-1.5 rounded-lg bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <span>🔴 High Risk</span>
          </button>
          <button
            onClick={() => applyPreset('borderline')}
            className="px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <span>🟡 Borderline</span>
          </button>
          <button
            onClick={() => applyPreset('graduate')}
            className="px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold flex items-center gap-1.5 transition-all"
          >
            <span>🟢 Graduate</span>
          </button>
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-8">
        
        {/* Left Column: Form & Stepper */}
        <div className="lg:col-span-7 bg-slate-900/80 p-6 sm:p-8 rounded-2xl border border-slate-800 space-y-6">
          
          {/* Stepper Navigation */}
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            {stepsInfo.map((s) => (
              <button
                key={s.num}
                onClick={() => setStep(s.num)}
                className={`flex items-center gap-1.5 text-xs font-semibold transition-all ${
                  step === s.num
                    ? 'text-indigo-400 scale-105'
                    : step > s.num
                    ? 'text-slate-300'
                    : 'text-slate-400 hover:text-slate-300'
                }`}
              >
                <span className={`w-6 h-6 rounded-full flex items-center justify-center text-[11px] ${
                  step === s.num
                    ? 'bg-indigo-500 text-white font-bold'
                    : step > s.num
                    ? 'bg-indigo-500/20 text-indigo-400'
                    : 'bg-slate-800 text-slate-400'
                }`}>
                  {s.num}
                </span>
                <span className="hidden sm:inline">{s.title}</span>
              </button>
            ))}
          </div>

          {/* Form Content based on Active Step */}
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Step 1: Academic */}
            {step === 1 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">1. Academic Performance (5 Features)</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Previous Qualification Grade (0 - 200)</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="200"
                      value={formData.previous_qualification_grade}
                      onChange={(e) => handleChange('previous_qualification_grade', parseFloat(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Admission Grade (0 - 200)</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="200"
                      value={formData.admission_grade}
                      onChange={(e) => handleChange('admission_grade', parseFloat(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">1st Semester Average Grade (0 - 20)</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="20"
                      value={formData.first_sem_grade}
                      onChange={(e) => handleChange('first_sem_grade', parseFloat(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      1st Sem Approval Rate ({(formData.first_sem_approval_rate * 100).toFixed(0)}%)
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={formData.first_sem_approval_rate}
                      onChange={(e) => handleChange('first_sem_approval_rate', parseFloat(e.target.value))}
                      className="w-full accent-indigo-500 cursor-pointer mt-2"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1.5">Attendance Type</label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => handleChange('attendance_type', 1)}
                      className={`py-2.5 rounded-xl text-xs font-semibold border transition-all ${
                        formData.attendance_type === 1
                          ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}
                    >
                      Daytime Attendance
                    </button>
                    <button
                      type="button"
                      onClick={() => handleChange('attendance_type', 0)}
                      className={`py-2.5 rounded-xl text-xs font-semibold border transition-all ${
                        formData.attendance_type === 0
                          ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500'
                          : 'bg-slate-800 text-slate-400 border-slate-700'
                      }`}
                    >
                      Evening Attendance
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Step 2: Financial */}
            {step === 2 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">2. Financial Indicators (3 Features)</h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 rounded-xl bg-slate-800/60 border border-slate-700/60">
                    <div>
                      <p className="text-sm font-semibold text-white">Tuition Fees Up To Date?</p>
                      <p className="text-xs text-slate-400">Has the student paid all required tuition fees?</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleChange('tuition_up_to_date', formData.tuition_up_to_date === 1 ? 0 : 1)}
                      className={`w-14 h-7 rounded-full transition-colors relative p-1 ${
                        formData.tuition_up_to_date === 1 ? 'bg-emerald-500' : 'bg-slate-700'
                      }`}
                    >
                      <div className={`w-5 h-5 rounded-full bg-white transition-transform ${
                        formData.tuition_up_to_date === 1 ? 'translate-x-7' : 'translate-x-0'
                      }`} />
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4 rounded-xl bg-slate-800/60 border border-slate-700/60">
                    <div>
                      <p className="text-sm font-semibold text-white">Debtor Status</p>
                      <p className="text-xs text-slate-400">Does the student have outstanding debts with the university?</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleChange('debtor', formData.debtor === 1 ? 0 : 1)}
                      className={`w-14 h-7 rounded-full transition-colors relative p-1 ${
                        formData.debtor === 1 ? 'bg-rose-500' : 'bg-slate-700'
                      }`}
                    >
                      <div className={`w-5 h-5 rounded-full bg-white transition-transform ${
                        formData.debtor === 1 ? 'translate-x-7' : 'translate-x-0'
                      }`} />
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4 rounded-xl bg-slate-800/60 border border-slate-700/60">
                    <div>
                      <p className="text-sm font-semibold text-white">Scholarship Holder</p>
                      <p className="text-xs text-slate-400">Is the student receiving a financial scholarship grant?</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => handleChange('scholarship_holder', formData.scholarship_holder === 1 ? 0 : 1)}
                      className={`w-14 h-7 rounded-full transition-colors relative p-1 ${
                        formData.scholarship_holder === 1 ? 'bg-indigo-500' : 'bg-slate-700'
                      }`}
                    >
                      <div className={`w-5 h-5 rounded-full bg-white transition-transform ${
                        formData.scholarship_holder === 1 ? 'translate-x-7' : 'translate-x-0'
                      }`} />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Step 3: Demographic */}
            {step === 3 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">3. Demographic Background (4 Features)</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Age at Enrollment</label>
                    <input
                      type="number"
                      min="15"
                      max="70"
                      value={formData.age_at_enrollment}
                      onChange={(e) => handleChange('age_at_enrollment', parseInt(e.target.value) || 20)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Gender</label>
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        type="button"
                        onClick={() => handleChange('gender', 1)}
                        className={`py-2 rounded-xl text-xs font-semibold border ${
                          formData.gender === 1 ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500' : 'bg-slate-800 text-slate-400 border-slate-700'
                        }`}
                      >
                        Male
                      </button>
                      <button
                        type="button"
                        onClick={() => handleChange('gender', 0)}
                        className={`py-2 rounded-xl text-xs font-semibold border ${
                          formData.gender === 0 ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500' : 'bg-slate-800 text-slate-400 border-slate-700'
                        }`}
                      >
                        Female
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Marital Status</label>
                    <select
                      value={formData.marital_status}
                      onChange={(e) => handleChange('marital_status', parseInt(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none cursor-pointer"
                    >
                      <option value={1}>Single</option>
                      <option value={2}>Married</option>
                      <option value={3}>Widower</option>
                      <option value={4}>Divorced</option>
                      <option value={5}>Facto Union</option>
                      <option value={6}>Legally Separated</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Displaced (Living away from home)</label>
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        type="button"
                        onClick={() => handleChange('displaced', 1)}
                        className={`py-2 rounded-xl text-xs font-semibold border ${
                          formData.displaced === 1 ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500' : 'bg-slate-800 text-slate-400 border-slate-700'
                        }`}
                      >
                        Yes
                      </button>
                      <button
                        type="button"
                        onClick={() => handleChange('displaced', 0)}
                        className={`py-2 rounded-xl text-xs font-semibold border ${
                          formData.displaced === 0 ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500' : 'bg-slate-800 text-slate-400 border-slate-700'
                        }`}
                      >
                        No
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Step 4: Family Background */}
            {step === 4 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">4. Family Background (2 Features)</h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Mother's Qualification Level</label>
                    <select
                      value={formData.mother_qualification}
                      onChange={(e) => handleChange('mother_qualification', parseInt(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none cursor-pointer"
                    >
                      <option value={1}>Secondary Education (12th Year)</option>
                      <option value={2}>Higher Education - Bachelor's Degree</option>
                      <option value={3}>Higher Education - Master's / Doctorate</option>
                      <option value={19}>Basic Education 3rd Cycle (9th Year)</option>
                      <option value={37}>Basic Education 1st Cycle (4th Year)</option>
                      <option value={38}>Unknown / Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Father's Qualification Level</label>
                    <select
                      value={formData.father_qualification}
                      onChange={(e) => handleChange('father_qualification', parseInt(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none cursor-pointer"
                    >
                      <option value={1}>Secondary Education (12th Year)</option>
                      <option value={2}>Higher Education - Bachelor's Degree</option>
                      <option value={3}>Higher Education - Master's / Doctorate</option>
                      <option value={19}>Basic Education 3rd Cycle (9th Year)</option>
                      <option value={37}>Basic Education 1st Cycle (4th Year)</option>
                      <option value={38}>Unknown / Other</option>
                    </select>
                  </div>
                </div>
              </div>
            )}

            {/* Step 5: Context & Macro */}
            {step === 5 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">5. Enrollment Context & Macroeconomic (4 Features)</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Enrolled Academic Course</label>
                    <select
                      value={formData.course}
                      onChange={(e) => handleChange('course', parseInt(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none cursor-pointer"
                    >
                      {COURSE_OPTIONS.map(c => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Application Mode Code</label>
                    <input
                      type="number"
                      value={formData.application_mode}
                      onChange={(e) => handleChange('application_mode', parseInt(e.target.value) || 1)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Unemployment Rate (%)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.unemployment_rate}
                      onChange={(e) => handleChange('unemployment_rate', parseFloat(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">GDP Growth Rate (%)</label>
                    <input
                      type="number"
                      step="0.1"
                      value={formData.gdp}
                      onChange={(e) => handleChange('gdp', parseFloat(e.target.value))}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Stepper Control Buttons */}
            <div className="flex items-center justify-between pt-4 border-t border-slate-800">
              {step > 1 ? (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition-colors"
                >
                  <ChevronLeft className="w-4 h-4" />
                  <span>Previous</span>
                </button>
              ) : <div />}

              {step < 5 ? (
                <button
                  type="button"
                  onClick={() => setStep(step + 1)}
                  className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md shadow-indigo-600/20 transition-all"
                >
                  <span>Next Step</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={loading}
                  className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-bold text-xs shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:scale-[1.02] transition-all disabled:opacity-50"
                >
                  {loading ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Evaluating Risk...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      <span>Run Risk Analysis</span>
                    </>
                  )}
                </button>
              )}
            </div>

          </form>

        </div>

        {/* Right Column: Prediction Results View */}
        <div className="lg:col-span-5 space-y-6">
          
          {!result ? (
            <div className="bg-slate-900/80 p-8 rounded-2xl border border-slate-800 text-center space-y-4 h-full flex flex-col items-center justify-center min-h-[400px]">
              <div className="w-16 h-16 rounded-2xl bg-indigo-500/10 flex items-center justify-center text-indigo-400">
                <Calculator className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-bold text-white">Ready for Risk Evaluation</h3>
              <p className="text-xs text-slate-400 max-w-sm leading-relaxed">
                Complete the 5-step feature form or select a quick profile preset above to generate an immediate student dropout prediction with SHAP explanations.
              </p>
            </div>
          ) : (
            <div className="space-y-6 animate-fadeIn">
              
              {/* Predicted Class Card */}
              <div className={`p-6 rounded-2xl border backdrop-blur-md relative overflow-hidden ${
                result.predicted_class === 'Dropout'
                  ? 'bg-rose-950/40 border-rose-500/40'
                  : result.predicted_class === 'Enrolled'
                  ? 'bg-amber-950/40 border-amber-500/40'
                  : 'bg-emerald-950/40 border-emerald-500/40'
              }`}>
                
                <div className="flex items-center justify-between mb-4">
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Predicted Outcome</span>
                  <span className={`px-3 py-1 rounded-full text-xs font-extrabold flex items-center gap-1.5 ${
                    result.risk_tier === 'High'
                      ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                      : result.risk_tier === 'Medium'
                      ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
                      : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                  }`}>
                    <AlertOctagon className="w-3.5 h-3.5" />
                    <span>{result.risk_tier} Risk Tier</span>
                  </span>
                </div>

                <h2 className={`text-3xl font-extrabold mb-4 ${
                  result.predicted_class === 'Dropout' ? 'text-rose-400' :
                  result.predicted_class === 'Enrolled' ? 'text-amber-400' : 'text-emerald-400'
                }`}>
                  {result.predicted_class}
                </h2>

                {/* Probability Distribution Gauge */}
                <div className="space-y-2 pt-2 border-t border-slate-800/80">
                  <p className="text-xs font-semibold text-slate-300">Model Probability Distribution:</p>
                  <div className="grid grid-cols-3 gap-2">
                    <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800 text-center">
                      <p className="text-[11px] text-slate-400">Dropout</p>
                      <p className="text-sm font-extrabold text-rose-400">{(result.probabilities.Dropout * 100).toFixed(1)}%</p>
                    </div>
                    <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800 text-center">
                      <p className="text-[11px] text-slate-400">Enrolled</p>
                      <p className="text-sm font-extrabold text-amber-400">{(result.probabilities.Enrolled * 100).toFixed(1)}%</p>
                    </div>
                    <div className="bg-slate-900/90 p-2.5 rounded-xl border border-slate-800 text-center">
                      <p className="text-[11px] text-slate-400">Graduate</p>
                      <p className="text-sm font-extrabold text-emerald-400">{(result.probabilities.Graduate * 100).toFixed(1)}%</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* SHAP Factors Explanation Chart */}
              <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-indigo-400" />
                  <span>Top SHAP Contributing Risk Factors</span>
                </h3>

                <div className="space-y-3">
                  {result.top_factors.map((factor, idx) => (
                    <div key={idx} className="p-3 bg-slate-800/60 rounded-xl border border-slate-700/60 space-y-1.5">
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-slate-200">{factor.label}</span>
                        <span className={`font-semibold px-2 py-0.5 rounded-full text-[10px] ${
                          factor.shap_value > 0 ? 'bg-rose-500/10 text-rose-300' : 'bg-emerald-500/10 text-emerald-300'
                        }`}>
                          {factor.effect} ({factor.shap_value > 0 ? '+' : ''}{factor.shap_value})
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 leading-relaxed">{factor.explanation}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Actionable Recommendations */}
              <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <UserCheck className="w-4 h-4 text-emerald-400" />
                  <span>Advisor Next Steps & Interventions</span>
                </h3>

                <ul className="space-y-2">
                  {result.recommendations.map((rec, idx) => (
                    <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-300">
                      <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>

            </div>
          )}

        </div>

      </div>

    </div>
  );
}

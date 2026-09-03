import React, { useState } from 'react';
import { 
  Calculator, CheckCircle, AlertTriangle, ShieldAlert, ChevronRight, ChevronLeft, Sparkles, RefreshCw, Award, ArrowUpRight, ArrowDownRight, Info, UserCheck, AlertOctagon, HeartPulse, Brain, Moon, Clock, Monitor
} from 'lucide-react';

const PRESETS = {
  highRisk: {
    name: "High Dropout Risk Profile",
    icon: "🔴",
    description: "55% 10th, 50% 12th, 4.2 GPA, Overdue tuition, Debtor, 9/10 Stress",
    values: {
      tenth_grade_pct: 55.0,
      twelfth_grade_pct: 50.0,
      current_sem_gpa: 4.2,
      cgpa: 4.5,
      first_sem_approval_rate: 0.20,
      debtor: 1,
      tuition_up_to_date: 0,
      scholarship_holder: 0,
      age_at_enrollment: 24,
      gender: 1,
      marital_status: 1,
      displaced: 1,
      stress_level: 9,
      screen_time_hours: 9.0,
      sleep_hours: 4.5,
      study_hours: 8.0
    }
  },
  graduate: {
    name: "High Performing Graduate Profile",
    icon: "🟢",
    description: "88% 10th, 85% 12th, 8.8 GPA, Paid tuition, Scholarship, 3/10 Stress",
    values: {
      tenth_grade_pct: 88.0,
      twelfth_grade_pct: 85.0,
      current_sem_gpa: 8.8,
      cgpa: 9.1,
      first_sem_approval_rate: 1.0,
      debtor: 0,
      tuition_up_to_date: 1,
      scholarship_holder: 1,
      age_at_enrollment: 19,
      gender: 0,
      marital_status: 1,
      displaced: 1,
      stress_level: 3,
      screen_time_hours: 3.5,
      sleep_hours: 8.0,
      study_hours: 25.0
    }
  },
  borderline: {
    name: "Borderline Enrolled Profile",
    icon: "🟡",
    description: "70% 10th, 65% 12th, 6.2 GPA, Paid tuition, No scholarship, 6/10 Stress",
    values: {
      tenth_grade_pct: 70.0,
      twelfth_grade_pct: 65.0,
      current_sem_gpa: 6.2,
      cgpa: 6.5,
      first_sem_approval_rate: 0.50,
      debtor: 0,
      tuition_up_to_date: 1,
      scholarship_holder: 0,
      age_at_enrollment: 21,
      gender: 1,
      marital_status: 1,
      displaced: 0,
      stress_level: 6,
      screen_time_hours: 5.5,
      sleep_hours: 6.5,
      study_hours: 14.0
    }
  }
};

export default function PredictPage({ showToast }) {
  const [step, setStep] = useState(1);

  const [formData, setFormData] = useState({
    tenth_grade_pct: 75.0,
    twelfth_grade_pct: 72.0,
    current_sem_gpa: 7.5,
    cgpa: 7.8,
    first_sem_approval_rate: 0.80,
    debtor: 0,
    tuition_up_to_date: 1,
    scholarship_holder: 0,
    age_at_enrollment: 20,
    gender: 1,
    marital_status: 1,
    displaced: 1,
    stress_level: 5,
    screen_time_hours: 4.5,
    sleep_hours: 7.0,
    study_hours: 18.0
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Clamped handler to enforce min/max validation
  const handleChange = (field, rawVal, minVal = 0, maxVal = 100) => {
    let val = parseFloat(rawVal);
    if (isNaN(val)) val = minVal;
    if (val < minVal) val = minVal;
    if (val > maxVal) val = maxVal;
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
    { num: 1, title: 'Academic Performance' },
    { num: 2, title: 'Financial Status' },
    { num: 3, title: 'Demographics & Wellbeing' },
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
            Input academic (10th%, 12th%, GPA, CGPA), financial, demographic & mental wellbeing signals to evaluate retention risk.
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
                className={`flex items-center gap-2 text-xs font-semibold transition-all ${
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
                <span>{s.title}</span>
              </button>
            ))}
          </div>

          {/* Form Content based on Active Step */}
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Step 1: Academic Performance */}
            {step === 1 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">1. Academic Marks & GPA Signals</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      10th Grade Marks (0 - 100%)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="100"
                      value={formData.tenth_grade_pct}
                      onChange={(e) => handleChange('tenth_grade_pct', e.target.value, 0, 100)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                      placeholder="e.g. 85.0"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      12th Grade Marks (0 - 100%)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="100"
                      value={formData.twelfth_grade_pct}
                      onChange={(e) => handleChange('twelfth_grade_pct', e.target.value, 0, 100)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                      placeholder="e.g. 80.0"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      Current Semester GPA (0.0 - 10.0)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="10"
                      value={formData.current_sem_gpa}
                      onChange={(e) => handleChange('current_sem_gpa', e.target.value, 0, 10)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                      placeholder="e.g. 7.5"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      Aggregate CGPA Until Now (0.0 - 10.0)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      max="10"
                      value={formData.cgpa}
                      onChange={(e) => handleChange('cgpa', e.target.value, 0, 10)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                      placeholder="e.g. 7.8"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">
                    1st Sem Course Approval Rate ({(formData.first_sem_approval_rate * 100).toFixed(0)}%)
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.05"
                    value={formData.first_sem_approval_rate}
                    onChange={(e) => handleChange('first_sem_approval_rate', e.target.value, 0, 1)}
                    className="w-full accent-indigo-500 cursor-pointer mt-2"
                  />
                </div>
              </div>
            )}

            {/* Step 2: Financial Status */}
            {step === 2 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">2. Financial Status Indicators</h3>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 rounded-xl bg-slate-800/60 border border-slate-700/60">
                    <div>
                      <p className="text-sm font-semibold text-white">Tuition Fees Up To Date?</p>
                      <p className="text-xs text-slate-400">Has the student paid all required tuition fees?</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => setFormData(prev => ({ ...prev, tuition_up_to_date: prev.tuition_up_to_date === 1 ? 0 : 1 }))}
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
                      onClick={() => setFormData(prev => ({ ...prev, debtor: prev.debtor === 1 ? 0 : 1 }))}
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
                      onClick={() => setFormData(prev => ({ ...prev, scholarship_holder: prev.scholarship_holder === 1 ? 0 : 1 }))}
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

            {/* Step 3: Demographics & Mental Wellbeing */}
            {step === 3 && (
              <div className="space-y-5 animate-fadeIn">
                <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-wider">3. Demographics, Mental Health & Lifestyle Signals</h3>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Age at Enrollment (15 - 70)</label>
                    <input
                      type="number"
                      min="15"
                      max="70"
                      value={formData.age_at_enrollment}
                      onChange={(e) => handleChange('age_at_enrollment', e.target.value, 15, 70)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">Gender</label>
                    <div className="grid grid-cols-2 gap-2">
                      <button
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, gender: 1 }))}
                        className={`py-2 rounded-xl text-xs font-semibold border ${
                          formData.gender === 1 ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500' : 'bg-slate-800 text-slate-400 border-slate-700'
                        }`}
                      >
                        Male
                      </button>
                      <button
                        type="button"
                        onClick={() => setFormData(prev => ({ ...prev, gender: 0 }))}
                        className={`py-2 rounded-xl text-xs font-semibold border ${
                          formData.gender === 0 ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500' : 'bg-slate-800 text-slate-400 border-slate-700'
                        }`}
                      >
                        Female
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      Perceived Stress Level (1 - 10)
                    </label>
                    <div className="flex items-center gap-3">
                      <input
                        type="range"
                        min="1"
                        max="10"
                        value={formData.stress_level}
                        onChange={(e) => handleChange('stress_level', e.target.value, 1, 10)}
                        className="w-full accent-rose-500 cursor-pointer"
                      />
                      <span className={`px-2.5 py-1 rounded-lg text-xs font-bold ${
                        formData.stress_level >= 7 ? 'bg-rose-500/20 text-rose-300' :
                        formData.stress_level >= 5 ? 'bg-amber-500/20 text-amber-300' : 'bg-emerald-500/20 text-emerald-300'
                      }`}>
                        {formData.stress_level}/10
                      </span>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      Daily Screen Time (Hours)
                    </label>
                    <input
                      type="number"
                      step="0.5"
                      min="0"
                      max="24"
                      value={formData.screen_time_hours}
                      onChange={(e) => handleChange('screen_time_hours', e.target.value, 0, 24)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      Nightly Sleep (Hours)
                    </label>
                    <input
                      type="number"
                      step="0.5"
                      min="0"
                      max="12"
                      value={formData.sleep_hours}
                      onChange={(e) => handleChange('sleep_hours', e.target.value, 0, 12)}
                      className="w-full bg-slate-800 text-white text-sm px-3.5 py-2.5 rounded-xl border border-slate-700 focus:border-indigo-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-300 mb-1">
                      Weekly Study Hours
                    </label>
                    <input
                      type="number"
                      step="1"
                      min="0"
                      max="100"
                      value={formData.study_hours}
                      onChange={(e) => handleChange('study_hours', e.target.value, 0, 100)}
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

              {step < 3 ? (
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
                Complete the 3-step feature form or select a quick profile preset above to generate an immediate student dropout prediction with SHAP explanations.
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
                  <span>Advisor Next Steps & Wellbeing Interventions</span>
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

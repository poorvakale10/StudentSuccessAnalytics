import React, { useState, useEffect } from 'react';
import { ArrowRight, Brain, Cpu, TrendingUp, Sparkles, CheckCircle2, ShieldCheck, Zap, BarChart2 } from 'lucide-react';

export default function LandingPage({ setActiveTab }) {
  // Animated counters
  const [datasetCount, setDatasetCount] = useState(0);
  const [accuracyVal, setAccuracyVal] = useState(0);
  const [featureCount, setFeatureCount] = useState(0);
  const [retentionVal, setRetentionVal] = useState(0);

  useEffect(() => {
    const duration = 1200;
    const steps = 40;
    const stepTime = duration / steps;
    let currentStep = 0;

    const timer = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;
      setDatasetCount(Math.round(progress * 4424));
      setAccuracyVal(parseFloat((progress * 71.5).toFixed(1)));
      setFeatureCount(Math.round(progress * 18));
      setRetentionVal(parseFloat((progress * 67.9).toFixed(1)));

      if (currentStep >= steps) {
        clearInterval(timer);
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="space-y-16 py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-slate-900 via-slate-900/90 to-slate-950 border border-slate-800/80 p-8 sm:p-12 lg:p-16 shadow-2xl">
        <div className="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-96 h-96 rounded-full bg-pink-500/10 blur-3xl pointer-events-none" />

        <div className="relative z-10 grid lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-7 space-y-6">
            
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5 text-indigo-400 animate-pulse" />
              <span>Next-Gen Academic Risk Intelligence</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight">
              Predict Student Risk <br />
              <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                Before Dropout Happens.
              </span>
            </h1>

            <p className="text-lg text-slate-300 max-w-2xl leading-relaxed">
              DropoutSense leverages machine learning trained on the UCI Higher Education Dataset to accurately forecast student retention outcomes, highlight SHAP-driven risk factors, and empower advisors with targeted intervention strategies.
            </p>

            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={() => setActiveTab('predict')}
                className="flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white font-semibold text-sm shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:scale-[1.02] transition-all"
              >
                <span>Launch Risk Predictor</span>
                <ArrowRight className="w-4 h-4" />
              </button>

              <button
                onClick={() => setActiveTab('dashboard')}
                className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-200 font-semibold text-sm border border-slate-700 hover:border-slate-600 transition-all"
              >
                <BarChart2 className="w-4 h-4 text-indigo-400" />
                <span>Explore Dataset Insights</span>
              </button>
            </div>

          </div>

          {/* Quick Stat Cards Grid */}
          <div className="lg:col-span-5 grid grid-cols-2 gap-4">
            
            <div className="bg-slate-800/60 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-lg hover:border-indigo-500/40 transition-colors group">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-3 group-hover:scale-110 transition-transform">
                <Cpu className="w-5 h-5" />
              </div>
              <p className="text-3xl font-extrabold text-white">{datasetCount.toLocaleString()}</p>
              <p className="text-xs text-slate-400 font-medium mt-1">UCI Student Samples</p>
            </div>

            <div className="bg-slate-800/60 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-lg hover:border-pink-500/40 transition-colors group">
              <div className="w-10 h-10 rounded-xl bg-pink-500/10 flex items-center justify-center text-pink-400 mb-3 group-hover:scale-110 transition-transform">
                <ShieldCheck className="w-5 h-5" />
              </div>
              <p className="text-3xl font-extrabold text-white">{accuracyVal}%</p>
              <p className="text-xs text-slate-400 font-medium mt-1">Best Model Accuracy</p>
            </div>

            <div className="bg-slate-800/60 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-lg hover:border-purple-500/40 transition-colors group">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400 mb-3 group-hover:scale-110 transition-transform">
                <Brain className="w-5 h-5" />
              </div>
              <p className="text-3xl font-extrabold text-white">{featureCount}</p>
              <p className="text-xs text-slate-400 font-medium mt-1">Curated Feature Signals</p>
            </div>

            <div className="bg-slate-800/60 backdrop-blur-md p-6 rounded-2xl border border-slate-700/60 shadow-lg hover:border-emerald-500/40 transition-colors group">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-400 mb-3 group-hover:scale-110 transition-transform">
                <TrendingUp className="w-5 h-5" />
              </div>
              <p className="text-3xl font-extrabold text-white">{retentionVal}%</p>
              <p className="text-xs text-slate-400 font-medium mt-1">Graduation & Enrolled Rate</p>
            </div>

          </div>
        </div>
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid md:grid-cols-3 gap-6">
        
        <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-800 hover:border-slate-700 transition-all space-y-3">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center text-indigo-400">
            <Zap className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Engineered Feature Economy</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Consolidates raw multi-semester curricular breakdowns into 2 high-impact signals: 1st Semester Average Grade & Approval Rate.
          </p>
        </div>

        <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-800 hover:border-slate-700 transition-all space-y-3">
          <div className="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400">
            <Brain className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">SHAP Natural Explanations</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            No black-box predictions. Every student risk assessment breaks down top positive and negative contributing factors in plain English.
          </p>
        </div>

        <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-800 hover:border-slate-700 transition-all space-y-3">
          <div className="w-12 h-12 rounded-xl bg-pink-500/10 flex items-center justify-center text-pink-400">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">Actionable Intervention Playbook</h3>
          <p className="text-sm text-slate-400 leading-relaxed">
            Provides tailored, practical recommendations for academic counselors, financial aid advisors, and retention officers.
          </p>
        </div>

      </div>

    </div>
  );
}

import React, { useState } from 'react';
import Navbar from './components/Navbar';
import LandingPage from './components/LandingPage';
import DashboardPage from './components/DashboardPage';
import PredictPage from './components/PredictPage';
import PerformancePage from './components/PerformancePage';
import Toast from './components/Toast';

export default function App() {
  const [activeTab, setActiveTab] = useState('landing');
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'success') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 4000);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      
      {/* Navbar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Content Area */}
      <main className="flex-1">
        {activeTab === 'landing' && <LandingPage setActiveTab={setActiveTab} />}
        {activeTab === 'dashboard' && <DashboardPage />}
        {activeTab === 'predict' && <PredictPage showToast={showToast} />}
        {activeTab === 'performance' && <PerformancePage />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-8 text-center text-xs text-slate-400 space-y-2 mt-12">
        <p className="font-medium text-slate-300">
          DropoutSense &copy; {new Date().getFullYear()} &mdash; Student Dropout Risk Predictor
        </p>
        <p className="text-[11px] text-slate-400">
          Built with Classical Machine Learning, FastAPI, SHAP Explainability, and React + Tailwind CSS
        </p>
      </footer>

      {/* Toast */}
      <Toast toast={toast} onClose={() => setToast(null)} />

    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { Award, Cpu, AlertTriangle, RefreshCw, Layers, CheckCircle2, ShieldCheck } from 'lucide-react';

export default function PerformancePage() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/model-metrics');
      if (!res.ok) throw new Error('Failed to fetch model metrics');
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20 flex flex-col items-center justify-center space-y-4">
        <div className="w-12 h-12 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin" />
        <p className="text-sm font-medium text-slate-400">Loading model performance metrics...</p>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-rose-400 mx-auto" />
        <h3 className="text-xl font-bold text-white">Failed to Load Metrics</h3>
        <p className="text-sm text-slate-400">{error || "Ensure backend server is running."}</p>
        <button
          onClick={fetchMetrics}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs rounded-lg transition-colors inline-flex items-center gap-2"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  // Model comparison chart data
  const comparisonData = Object.keys(metrics.models).map((name) => ({
    name,
    Accuracy: Math.round(metrics.models[name].accuracy * 1000) / 10,
    'Macro F1': Math.round(metrics.models[name].macro_f1 * 1000) / 10,
  }));

  const bestModelName = metrics.best_model_name;
  const bestMetrics = metrics.models[bestModelName];
  const cm = bestMetrics.confusion_matrix;
  const classes = metrics.target_classes;

  return (
    <div className="space-y-8 py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      
      {/* Header */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 backdrop-blur-md flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <Award className="w-6 h-6 text-indigo-400" />
            <span>Machine Learning Model Benchmark & Performance</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Comparative evaluation across Logistic Regression, Random Forest, XGBoost, and Support Vector Machines (SVM).
          </p>
        </div>

        <div className="px-4 py-2 bg-indigo-500/10 border border-indigo-500/20 rounded-xl flex items-center gap-2.5">
          <ShieldCheck className="w-5 h-5 text-indigo-400" />
          <div>
            <p className="text-[10px] uppercase font-bold text-indigo-300">Winning Classifier</p>
            <p className="text-sm font-extrabold text-white">{bestModelName}</p>
          </div>
        </div>
      </div>

      {/* Main Grid: Comparison Chart + Best Model Stats */}
      <div className="grid lg:grid-cols-12 gap-8">
        
        {/* Model Comparison Bar Chart */}
        <div className="lg:col-span-7 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4">
          <div>
            <h3 className="text-lg font-bold text-white">Algorithm Benchmark (Accuracy vs. Macro-F1 %)</h3>
            <p className="text-xs text-slate-400">Stratified 80/20 Train/Test Split (885 test set evaluations)</p>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={comparisonData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 11 }} tickFormatter={(v) => `${v}%`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                  formatter={(val) => [`${val}%`]}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="Accuracy" fill="#6366f1" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Macro F1" fill="#ec4899" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Per-Class Breakdown Table */}
        <div className="lg:col-span-5 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Winning Model: {bestModelName}</h3>
            <p className="text-xs text-slate-400">Per-Class Precision, Recall, & F1 Scores</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                  <th className="pb-3">Class</th>
                  <th className="pb-3 text-right">Precision</th>
                  <th className="pb-3 text-right">Recall</th>
                  <th className="pb-3 text-right">F1 Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {Object.keys(bestMetrics.per_class).map((cls) => {
                  const item = bestMetrics.per_class[cls];
                  return (
                    <tr key={cls} className="hover:bg-slate-800/40">
                      <td className="py-3 font-bold text-white flex items-center gap-2">
                        <span className={`w-2.5 h-2.5 rounded-full ${
                          cls === 'Dropout' ? 'bg-rose-500' : cls === 'Enrolled' ? 'bg-amber-500' : 'bg-emerald-500'
                        }`} />
                        <span>{cls}</span>
                      </td>
                      <td className="py-3 text-right font-medium text-slate-300">{(item.precision * 100).toFixed(1)}%</td>
                      <td className="py-3 text-right font-medium text-slate-300">{(item.recall * 100).toFixed(1)}%</td>
                      <td className="py-3 text-right font-bold text-indigo-400">{(item.f1 * 100).toFixed(1)}%</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-700/50 flex items-center justify-between text-xs">
            <span className="text-slate-400 font-medium">Overall Accuracy</span>
            <span className="text-white font-extrabold text-sm">{(bestMetrics.accuracy * 100).toFixed(1)}%</span>
          </div>
        </div>

      </div>

      {/* Confusion Matrix Visualization */}
      <div className="bg-slate-900/80 p-6 sm:p-8 rounded-2xl border border-slate-800 space-y-6">
        <div>
          <h3 className="text-lg font-bold text-white">Confusion Matrix Heatmap ({bestModelName})</h3>
          <p className="text-xs text-slate-400">Rows represent Actual Outcomes, Columns represent Predicted Outcomes</p>
        </div>

        <div className="max-w-xl mx-auto space-y-3">
          
          {/* Column Header */}
          <div className="grid grid-cols-4 text-center text-xs font-bold text-slate-400">
            <div></div>
            <div>Pred: Dropout</div>
            <div>Pred: Enrolled</div>
            <div>Pred: Graduate</div>
          </div>

          {/* Matrix Rows */}
          {cm.map((row, rIdx) => (
            <div key={rIdx} className="grid grid-cols-4 items-center gap-2 text-center text-xs">
              <div className="font-bold text-slate-300 text-left pl-2">
                Actual: {classes[rIdx]}
              </div>
              {row.map((count, cIdx) => {
                const isDiagonal = rIdx === cIdx;
                const totalInRow = row.reduce((a, b) => a + b, 0);
                const pct = Math.round((count / totalInRow) * 100);
                return (
                  <div
                    key={cIdx}
                    className={`p-4 rounded-xl border transition-all ${
                      isDiagonal
                        ? 'bg-indigo-600/30 border-indigo-500/50 text-white font-extrabold shadow-lg shadow-indigo-500/10'
                        : 'bg-slate-800/40 border-slate-700/40 text-slate-400 font-medium'
                    }`}
                  >
                    <p className="text-base font-extrabold">{count}</p>
                    <p className="text-[10px] text-slate-400">{pct}%</p>
                  </div>
                );
              })}
            </div>
          ))}

        </div>
      </div>

    </div>
  );
}

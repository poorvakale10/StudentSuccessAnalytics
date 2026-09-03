import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Legend, PieChart, Pie
} from 'recharts';
import { Filter, RefreshCw, AlertTriangle, CheckCircle, GraduationCap, DollarSign, BookOpen, Layers } from 'lucide-react';

export default function DashboardPage() {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters
  const [selectedCourseFilter, setSelectedCourseFilter] = useState('all');

  useEffect(() => {
    fetchInsights();
  }, []);

  const fetchInsights = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/dataset-insights');
      if (!res.ok) throw new Error('Failed to fetch dataset insights');
      const data = await res.json();
      setInsights(data);
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
        <p className="text-sm font-medium text-slate-400">Loading dataset insights & analytics...</p>
      </div>
    );
  }

  if (error || !insights) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-center space-y-4">
        <AlertTriangle className="w-12 h-12 text-rose-400 mx-auto" />
        <h3 className="text-xl font-bold text-white">Failed to Load Dashboard Data</h3>
        <p className="text-sm text-slate-400">{error || "Ensure backend server is running."}</p>
        <button
          onClick={fetchInsights}
          className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs rounded-lg transition-colors inline-flex items-center gap-2"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  // Filter course data if course filter is set
  const filteredCourses = selectedCourseFilter === 'all'
    ? insights.course_stats.slice(0, 10)
    : insights.course_stats.filter(c => c.course_id.toString() === selectedCourseFilter);

  // Outcome distribution pie chart data
  const pieData = [
    { name: 'Graduate', value: insights.counts.graduate, color: '#10b981' },
    { name: 'Dropout', value: insights.counts.dropout, color: '#ef4444' },
    { name: 'Enrolled', value: insights.counts.enrolled, color: '#f59e0b' }
  ];

  // Financial chart data
  const financialChartData = [
    {
      metric: 'Tuition Paid',
      'Paid / Compliant': Math.round(insights.financial_stats.tuition_up_to_date.paid.dropout_rate * 100),
      'Unpaid / Debtor': Math.round(insights.financial_stats.tuition_up_to_date.unpaid.dropout_rate * 100),
    },
    {
      metric: 'Debtor Status',
      'Paid / Compliant': Math.round(insights.financial_stats.debtor.no.dropout_rate * 100),
      'Unpaid / Debtor': Math.round(insights.financial_stats.debtor.yes.dropout_rate * 100),
    },
    {
      metric: 'Scholarship',
      'Paid / Compliant': Math.round(insights.financial_stats.scholarship.yes.dropout_rate * 100),
      'Unpaid / Debtor': Math.round(insights.financial_stats.scholarship.no.dropout_rate * 100),
    }
  ];

  // Grade Distribution Chart Data
  const gradeDistData = [
    { outcome: 'Dropout', avgGrade: insights.grade_dist.Dropout.mean, color: '#ef4444' },
    { outcome: 'Enrolled', avgGrade: insights.grade_dist.Enrolled.mean, color: '#f59e0b' },
    { outcome: 'Graduate', avgGrade: insights.grade_dist.Graduate.mean, color: '#10b981' }
  ];

  return (
    <div className="space-y-8 py-6 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      
      {/* Header & Filter Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <h2 className="text-2xl font-extrabold text-white flex items-center gap-2">
            <Layers className="w-6 h-6 text-indigo-400" />
            <span>Dataset Insights & Analytics Dashboard</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Aggregate student cohort statistical analysis from UCI dataset (4,424 records)
          </p>
        </div>

        {/* Filter Dropdown */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-800/90 px-3.5 py-2 rounded-xl border border-slate-700">
            <Filter className="w-4 h-4 text-indigo-400" />
            <label className="text-xs font-semibold text-slate-300">Course Filter:</label>
            <select
              value={selectedCourseFilter}
              onChange={(e) => setSelectedCourseFilter(e.target.value)}
              className="bg-transparent text-xs text-white font-medium focus:outline-none cursor-pointer"
            >
              <option value="all" className="bg-slate-900 text-white">All Top Courses</option>
              {insights.course_stats.map(c => (
                <option key={c.course_id} value={c.course_id.toString()} className="bg-slate-900 text-white">
                  {c.course_name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">Total Students</span>
            <BookOpen className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-extrabold text-white">{insights.total_students.toLocaleString()}</p>
          <p className="text-[11px] text-slate-400 mt-1">Dataset Population</p>
        </div>

        <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">Graduation Rate</span>
            <GraduationCap className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-extrabold text-emerald-400">
            {(insights.overall_rates.graduate * 100).toFixed(1)}%
          </p>
          <p className="text-[11px] text-slate-400 mt-1">{insights.counts.graduate.toLocaleString()} Students</p>
        </div>

        <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">Overall Dropout Rate</span>
            <AlertTriangle className="w-4 h-4 text-rose-400" />
          </div>
          <p className="text-2xl font-extrabold text-rose-400">
            {(insights.overall_rates.dropout * 100).toFixed(1)}%
          </p>
          <p className="text-[11px] text-slate-400 mt-1">{insights.counts.dropout.toLocaleString()} Students</p>
        </div>

        <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800/80">
          <div className="flex items-center justify-between text-slate-400 mb-2">
            <span className="text-xs font-semibold">Currently Enrolled</span>
            <CheckCircle className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-extrabold text-amber-400">
            {(insights.overall_rates.enrolled * 100).toFixed(1)}%
          </p>
          <p className="text-[11px] text-slate-400 mt-1">{insights.counts.enrolled.toLocaleString()} Students</p>
        </div>

      </div>

      {/* Main Charts Grid 1 */}
      <div className="grid lg:grid-cols-12 gap-6">
        
        {/* Course Dropout Rate Bar Chart */}
        <div className="lg:col-span-8 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4">
          <div>
            <h3 className="text-lg font-bold text-white">Dropout Rate by Academic Course (%)</h3>
            <p className="text-xs text-slate-400">Historical dropout percentage across major university degree tracks</p>
          </div>

          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={filteredCourses}
                layout="vertical"
                margin={{ top: 10, right: 30, left: 100, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" horizontal={false} />
                <XAxis type="number" domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 11 }} tickFormatter={(v) => `${v}%`} />
                <YAxis dataKey="course_name" type="category" width={140} tick={{ fill: '#e2e8f0', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                  formatter={(val, name, props) => [`${(props.payload.dropout_rate * 100).toFixed(1)}%`, 'Dropout Rate']}
                />
                <Bar dataKey={(d) => Math.round(d.dropout_rate * 100)} fill="#ef4444" radius={[0, 4, 4, 0]}>
                  {filteredCourses.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.dropout_rate > 0.4 ? '#ef4444' : entry.dropout_rate > 0.25 ? '#f59e0b' : '#10b981'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cohort Breakdown Pie Chart */}
        <div className="lg:col-span-4 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Student Cohort Outcomes</h3>
            <p className="text-xs text-slate-400">3-Class Target Distribution</p>
          </div>

          <div className="h-56 w-full flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`pie-cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                  formatter={(value) => [`${value} students`, 'Count']}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-800">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-slate-300 font-medium">{item.name}</span>
                </div>
                <span className="text-white font-bold">{item.value} ({((item.value / insights.total_students) * 100).toFixed(1)}%)</span>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Main Charts Grid 2 */}
      <div className="grid lg:grid-cols-12 gap-6">
        
        {/* Financial Factors Comparison */}
        <div className="lg:col-span-6 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-amber-400" />
              <span>Financial Status vs. Dropout Risk (%)</span>
            </h3>
            <p className="text-xs text-slate-400">Dropout rate comparison based on financial indicators</p>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={financialChartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="metric" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 11 }} tickFormatter={(v) => `${v}%`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                  formatter={(val) => [`${val}%`, 'Dropout Rate']}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="Paid / Compliant" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Unpaid / Debtor" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Grade Distribution by Outcome */}
        <div className="lg:col-span-6 bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4">
          <div>
            <h3 className="text-lg font-bold text-white">1st Semester Average Grade by Outcome</h3>
            <p className="text-xs text-slate-400">Mean 1st sem GPA benchmark (0 - 20 point scale)</p>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={gradeDistData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="outcome" tick={{ fill: '#e2e8f0', fontSize: 12, fontWeight: 'bold' }} />
                <YAxis domain={[0, 20]} tick={{ fill: '#94a3b8', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', color: '#fff' }}
                  formatter={(val) => [`${val} / 20`, 'Average Grade']}
                />
                <Bar dataKey="avgGrade" radius={[6, 6, 0, 0]}>
                  {gradeDistData.map((entry, index) => (
                    <Cell key={`grade-cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Feature Importance List */}
      <div className="bg-slate-900/80 p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="text-lg font-bold text-white">Top Curated Feature Importance Ranking (ML Model Signal Weight)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {insights.feature_importance.map((item, idx) => (
            <div key={item.feature} className="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <span className="w-6 h-6 rounded-lg bg-indigo-500/10 text-indigo-400 font-extrabold text-xs flex items-center justify-center">
                  #{idx + 1}
                </span>
                <span className="text-xs font-semibold text-slate-200">{item.feature.replace(/_/g, ' ')}</span>
              </div>
              <span className="text-xs font-bold text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded-full">
                {(item.importance * 100).toFixed(1)}%
              </span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}

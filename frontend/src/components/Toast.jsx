import React from 'react';
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-react';

export default function Toast({ toast, onClose }) {
  if (!toast) return null;

  const { message, type } = toast;

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-bounce-in">
      <div className={`flex items-center gap-3 px-4 py-3 rounded-xl border shadow-2xl backdrop-blur-xl text-xs font-medium ${
        type === 'error'
          ? 'bg-rose-950/90 border-rose-500/50 text-rose-200'
          : type === 'info'
          ? 'bg-indigo-950/90 border-indigo-500/50 text-indigo-200'
          : 'bg-emerald-950/90 border-emerald-500/50 text-emerald-200'
      }`}>
        {type === 'error' ? (
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
        ) : type === 'info' ? (
          <Info className="w-4 h-4 text-indigo-400 shrink-0" />
        ) : (
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
        )}
        <span>{message}</span>
        <button
          onClick={onClose}
          className="ml-2 text-slate-400 hover:text-white transition-colors"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}

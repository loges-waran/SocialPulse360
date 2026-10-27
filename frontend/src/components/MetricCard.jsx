import React from 'react';

export default function MetricCard({ title, value, subtitle, icon: Icon, color = 'cyan', change }) {
  const colorMap = {
    cyan: {
      bg: 'bg-cyan-950/20',
      border: 'border-cyan-800/40',
      text: 'text-cyan-400',
      glow: 'shadow-cyan-500/10'
    },
    emerald: {
      bg: 'bg-emerald-950/20',
      border: 'border-emerald-800/40',
      text: 'text-emerald-400',
      glow: 'shadow-emerald-500/10'
    },
    rose: {
      bg: 'bg-rose-950/20',
      border: 'border-rose-800/40',
      text: 'text-rose-400',
      glow: 'shadow-rose-500/10'
    },
    amber: {
      bg: 'bg-amber-950/20',
      border: 'border-amber-800/40',
      text: 'text-amber-400',
      glow: 'shadow-amber-500/10'
    },
    blue: {
      bg: 'bg-blue-950/20',
      border: 'border-blue-800/40',
      text: 'text-blue-400',
      glow: 'shadow-blue-500/10'
    },
    purple: {
      bg: 'bg-purple-950/20',
      border: 'border-purple-800/40',
      text: 'text-purple-400',
      glow: 'shadow-purple-500/10'
    }
  };

  const c = colorMap[color] || colorMap.cyan;

  return (
    <div className={`p-4 rounded-xl glass-panel border ${c.border} ${c.bg} transition-all hover:scale-[1.02] shadow-lg ${c.glow}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-2 rounded-lg bg-gray-900/60 border border-gray-800 ${c.text}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>
      <div className="mt-2 flex items-baseline justify-between">
        <span className="text-2xl font-extrabold text-white tracking-tight">{value}</span>
        {change && (
          <span className="text-xs font-semibold text-emerald-400 bg-emerald-950/60 border border-emerald-800 px-1.5 py-0.5 rounded">
            {change}
          </span>
        )}
      </div>
      {subtitle && <p className="mt-1 text-xs text-gray-400 truncate">{subtitle}</p>}
    </div>
  );
}

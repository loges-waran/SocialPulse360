import React from 'react';
import { Hash } from 'lucide-react';

export default function HashtagsChart({ hashtags }) {
  if (!hashtags || hashtags.length === 0) {
    return <div className="text-xs text-gray-500 py-8 text-center">No hashtags found in dataset</div>;
  }

  const maxCount = Math.max(...hashtags.map(h => h.value), 1);

  return (
    <div className="space-y-2.5">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-semibold text-gray-200">Trending Hashtags (#)</h4>
        <span className="text-[11px] text-gray-400">{hashtags.length} hashtags detected</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {hashtags.slice(0, 14).map((tag, idx) => {
          const pct = Math.round((tag.value / maxCount) * 100);
          return (
            <div 
              key={idx}
              className="p-2.5 rounded-lg bg-gray-800/40 border border-gray-700/60 hover:border-cyan-500/40 transition-all flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-cyan-300 truncate max-w-[150px]">
                  {tag.key}
                </span>
                <span className="text-xs font-bold text-gray-200 bg-gray-900/80 px-2 py-0.5 rounded border border-gray-700">
                  {tag.value}
                </span>
              </div>
              <div className="w-full bg-gray-900 rounded-full h-1.5 mt-2 overflow-hidden">
                <div 
                  className="bg-gradient-to-r from-cyan-500 to-blue-500 h-1.5 rounded-full" 
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

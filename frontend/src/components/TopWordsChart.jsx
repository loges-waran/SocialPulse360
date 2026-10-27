import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function TopWordsChart({ wordTrends }) {
  const [limit, setLimit] = useState(15);

  if (!wordTrends) return null;

  let data = [];
  if (limit === 10) data = wordTrends.top_10 || [];
  else if (limit === 20) data = wordTrends.top_20 || [];
  else data = wordTrends.top_50 ? wordTrends.top_50.slice(0, limit) : [];

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm font-semibold text-gray-200">MapReduce Word Frequency</h4>
          <p className="text-xs text-gray-400">Tokens filtered through MapReduce pipeline (Stop words removed)</p>
        </div>
        <div className="flex space-x-1 bg-gray-800/80 p-0.5 rounded-lg border border-gray-700">
          {[10, 15, 25, 50].map((count) => (
            <button
              key={count}
              onClick={() => setLimit(count)}
              className={`px-2 py-0.5 text-[11px] font-medium rounded ${
                limit === count
                  ? 'bg-cyan-500 text-white shadow-sm'
                  : 'text-gray-400 hover:text-gray-200'
              }`}
            >
              Top {count}
            </button>
          ))}
        </div>
      </div>

      <div className="w-full h-72">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
            <XAxis type="number" stroke="#6B7280" tick={{ fill: '#9CA3AF', fontSize: 11 }} />
            <YAxis type="category" dataKey="key" stroke="#6B7280" tick={{ fill: '#E5E7EB', fontSize: 11 }} />
            <Tooltip
              cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
              contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.5rem', fontSize: '12px' }}
              formatter={(val) => [val, 'Occurrences']}
            />
            <Bar dataKey="value" fill="#06B6D4" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

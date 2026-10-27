import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function SentimentBarChart({ distribution }) {
  if (!distribution || !distribution.counts) return null;

  const data = [
    { name: 'Positive', count: distribution.counts.positive || 0, color: '#10B981' },
    { name: 'Negative', count: distribution.counts.negative || 0, color: '#F43F5E' },
    { name: 'Neutral', count: distribution.counts.neutral || 0, color: '#F59E0B' },
  ];

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 20, right: 20, left: -20, bottom: 5 }}>
          <XAxis dataKey="name" stroke="#6B7280" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
          <YAxis stroke="#6B7280" tick={{ fill: '#9CA3AF', fontSize: 12 }} />
          <Tooltip 
            cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }}
            contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.5rem', fontSize: '12px' }}
          />
          <Bar dataKey="count" radius={[6, 6, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`bar-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

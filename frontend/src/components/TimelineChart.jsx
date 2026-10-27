import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function TimelineChart({ timeline }) {
  if (!timeline || timeline.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-xs text-gray-500">
        No timestamped trend data available in current dataset
      </div>
    );
  }

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={timeline} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorPos" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10B981" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#F43F5E" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#F43F5E" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorNeu" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#F59E0B" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <XAxis dataKey="date" stroke="#6B7280" tick={{ fill: '#9CA3AF', fontSize: 11 }} />
          <YAxis stroke="#6B7280" tick={{ fill: '#9CA3AF', fontSize: 11 }} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', borderRadius: '0.5rem', fontSize: '12px' }}
          />
          <Legend verticalAlign="top" height={30} />
          <Area type="monotone" dataKey="positive" name="Positive" stroke="#10B981" fillOpacity={1} fill="url(#colorPos)" />
          <Area type="monotone" dataKey="negative" name="Negative" stroke="#F43F5E" fillOpacity={1} fill="url(#colorNeg)" />
          <Area type="monotone" dataKey="neutral" name="Neutral" stroke="#F59E0B" fillOpacity={1} fill="url(#colorNeu)" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

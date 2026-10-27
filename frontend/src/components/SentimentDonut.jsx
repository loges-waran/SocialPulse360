import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = {
  positive: '#10B981', // Emerald
  negative: '#F43F5E', // Rose
  neutral: '#F59E0B',  // Amber
};

export default function SentimentDonut({ distribution }) {
  if (!distribution || !distribution.counts) {
    return <div className="h-64 flex items-center justify-center text-xs text-gray-500">No sentiment data available</div>;
  }

  const data = [
    { name: 'Positive', value: distribution.counts.positive || 0, key: 'positive' },
    { name: 'Negative', value: distribution.counts.negative || 0, key: 'negative' },
    { name: 'Neutral', value: distribution.counts.neutral || 0, key: 'neutral' },
  ].filter(d => d.value > 0);

  const total = distribution.total_records || 1;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const item = payload[0];
      const pct = ((item.value / total) * 100).toFixed(1);
      return (
        <div className="bg-gray-900 border border-gray-700 p-2.5 rounded-lg shadow-xl text-xs">
          <p className="font-semibold text-gray-200">{item.name}</p>
          <p className="text-gray-400 mt-0.5">
            Count: <span className="text-white font-bold">{item.value}</span> ({pct}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-64 relative flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={85}
            paddingAngle={4}
            dataKey="value"
          >
            {data.map((entry) => (
              <Cell key={`cell-${entry.key}`} fill={COLORS[entry.key]} stroke="#111827" strokeWidth={2} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            verticalAlign="bottom" 
            height={36} 
            formatter={(value, entry) => (
              <span className="text-xs text-gray-300 font-medium ml-1">
                {value} ({distribution.percentages[entry.payload.key] || 0}%)
              </span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

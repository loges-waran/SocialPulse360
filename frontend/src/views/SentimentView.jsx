import React from 'react';
import SentimentDonut from '../components/SentimentDonut';
import SentimentBarChart from '../components/SentimentBarChart';
import TimelineChart from '../components/TimelineChart';
import { Smile, Frown, Meh, Sparkles, MessageSquare } from 'lucide-react';

export default function SentimentView({ sentimentData }) {
  if (!sentimentData) {
    return <div className="py-20 text-center text-gray-500">Loading sentiment analytics...</div>;
  }

  const dist = sentimentData.sentiment_distribution || {};
  const counts = dist.counts || {};
  const pcts = dist.percentages || {};
  const keywords = sentimentData.sentiment_keywords || {};

  return (
    <div className="space-y-6 animate-fadeIn pb-12">
      
      {/* Header */}
      <div>
        <h2 className="text-xl font-black text-white">Sentiment Analytics</h2>
        <p className="text-xs text-gray-400">
          Multilingual sentiment classification across English, Tamil-English (Tanglish), and Tamil text
        </p>
      </div>

      {/* Row 1: Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-5 rounded-2xl glass-panel border border-gray-800">
          <h3 className="text-sm font-bold text-white mb-2">Sentiment Distribution</h3>
          <p className="text-xs text-gray-400 mb-4">Relative proportion of positive, negative, and neutral posts</p>
          <SentimentDonut distribution={dist} />
        </div>

        <div className="p-5 rounded-2xl glass-panel border border-gray-800">
          <h3 className="text-sm font-bold text-white mb-2">Absolute Record Counts</h3>
          <p className="text-xs text-gray-400 mb-4">Number of social posts categorized per sentiment</p>
          <SentimentBarChart distribution={dist} />
        </div>
      </div>

      {/* Row 2: Daily Timeline */}
      <div className="p-5 rounded-2xl glass-panel border border-gray-800">
        <h3 className="text-sm font-bold text-white mb-1">Sentiment Timeline Analysis</h3>
        <p className="text-xs text-gray-400 mb-4">
          Tracking shifts in public sentiment over dates (Hadoop MapReduce DailySentiment Job)
        </p>
        <TimelineChart timeline={sentimentData.daily_timeline} />
      </div>

      {/* Row 3: Key Expressions and Drivers */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Positive Drivers */}
        <div className="p-5 rounded-2xl glass-panel border border-emerald-900/40 bg-emerald-950/10">
          <div className="flex items-center space-x-2 text-emerald-400 mb-3">
            <Smile className="w-5 h-5" />
            <h3 className="text-sm font-bold text-white">Top Positive Emotional Triggers</h3>
          </div>
          <p className="text-xs text-gray-400 mb-3">
            Frequent positive terms identified across English & Tanglish posts:
          </p>
          <div className="flex flex-wrap gap-2">
            {(keywords.positive_keywords || []).slice(0, 15).map((item, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-lg text-xs font-medium bg-emerald-950/60 border border-emerald-800/80 text-emerald-300 flex items-center space-x-1"
              >
                <span>{item.word}</span>
                <span className="text-[10px] text-emerald-400/80 font-bold bg-emerald-900/60 px-1 rounded">
                  {item.count}
                </span>
              </span>
            ))}
          </div>
        </div>

        {/* Negative Drivers */}
        <div className="p-5 rounded-2xl glass-panel border border-rose-900/40 bg-rose-950/10">
          <div className="flex items-center space-x-2 text-rose-400 mb-3">
            <Frown className="w-5 h-5" />
            <h3 className="text-sm font-bold text-white">Top Negative Grievances & Complaints</h3>
          </div>
          <p className="text-xs text-gray-400 mb-3">
            Frequent critical terms identified in public discourse:
          </p>
          <div className="flex flex-wrap gap-2">
            {(keywords.negative_keywords || []).slice(0, 15).map((item, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-lg text-xs font-medium bg-rose-950/60 border border-rose-800/80 text-rose-300 flex items-center space-x-1"
              >
                <span>{item.word}</span>
                <span className="text-[10px] text-rose-400/80 font-bold bg-rose-900/60 px-1 rounded">
                  {item.count}
                </span>
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

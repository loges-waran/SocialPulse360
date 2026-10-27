import React from 'react';
import TopWordsChart from '../components/TopWordsChart';
import HashtagsChart from '../components/HashtagsChart';
import { Info, Sparkles, Hash, Layers } from 'lucide-react';

export default function TrendsView({ trendData }) {
  if (!trendData) {
    return <div className="py-20 text-center text-gray-500">Loading trend analytics...</div>;
  }

  const keywords = trendData.sentiment_keywords || {};

  return (
    <div className="space-y-6 animate-fadeIn pb-12">
      {/* Header */}
      <div>
        <h2 className="text-xl font-black text-white">Trend Analytics</h2>
        <p className="text-xs text-gray-400">
          Discourse volume, viral hashtags, and keyword distribution across social media
        </p>
      </div>

      {/* Row 1: Top Words & Hashtags */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="p-5 rounded-2xl glass-panel border border-gray-800">
          <TopWordsChart wordTrends={trendData.word_trends} />
        </div>

        <div className="p-5 rounded-2xl glass-panel border border-gray-800">
          <HashtagsChart hashtags={trendData.top_hashtags} />
        </div>
      </div>

      {/* Row 2: Keyword Comparison Table / Columns */}
      <div className="p-5 rounded-2xl glass-panel border border-gray-800">
        <h3 className="text-sm font-bold text-white mb-1">
          Sentiment-Segmented Keyword Distribution
        </h3>
        <p className="text-xs text-gray-400 mb-4">
          Derived from the MapReduce <code>SentimentWords</code> job (grouped by sentiment label)
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          
          {/* Positive Keywords */}
          <div className="p-4 rounded-xl bg-gray-900/60 border border-emerald-900/50">
            <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-3 flex items-center justify-between">
              <span>Positive Words</span>
              <span className="text-[10px] text-emerald-500 bg-emerald-950 px-2 py-0.5 rounded">High Praise</span>
            </h4>
            <div className="space-y-1.5">
              {(keywords.positive_keywords || []).slice(0, 10).map((item, idx) => (
                <div key={idx} className="flex justify-between items-center text-xs py-1 border-b border-gray-800/60">
                  <span className="text-gray-300 font-medium">{item.word}</span>
                  <span className="text-emerald-400 font-bold">{item.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Negative Keywords */}
          <div className="p-4 rounded-xl bg-gray-900/60 border border-rose-900/50">
            <h4 className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-3 flex items-center justify-between">
              <span>Negative Words</span>
              <span className="text-[10px] text-rose-500 bg-rose-950 px-2 py-0.5 rounded">Grievances</span>
            </h4>
            <div className="space-y-1.5">
              {(keywords.negative_keywords || []).slice(0, 10).map((item, idx) => (
                <div key={idx} className="flex justify-between items-center text-xs py-1 border-b border-gray-800/60">
                  <span className="text-gray-300 font-medium">{item.word}</span>
                  <span className="text-rose-400 font-bold">{item.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Neutral Keywords */}
          <div className="p-4 rounded-xl bg-gray-900/60 border border-amber-900/50">
            <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-3 flex items-center justify-between">
              <span>Neutral / Info Words</span>
              <span className="text-[10px] text-amber-500 bg-amber-950 px-2 py-0.5 rounded">Context</span>
            </h4>
            <div className="space-y-1.5">
              {(keywords.neutral_keywords || []).slice(0, 10).map((item, idx) => (
                <div key={idx} className="flex justify-between items-center text-xs py-1 border-b border-gray-800/60">
                  <span className="text-gray-300 font-medium">{item.word}</span>
                  <span className="text-amber-400 font-bold">{item.count}</span>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>

      {/* Big Data Engineering Note */}
      <div className="p-4 rounded-xl bg-gray-900/80 border border-gray-800 flex items-start space-x-3 text-xs text-gray-400">
        <Info className="w-5 h-5 text-cyan-400 shrink-0 mt-0.5" />
        <div>
          <strong className="text-gray-200">Big Data Analytics Methodology Note:</strong>
          <p className="mt-0.5 leading-relaxed">
            Word count ranking illustrates lexical prevalence across the social corpus. High word frequency alone does not imply semantic importance or causal significance; critical infrastructure topics or low-frequency high-impact events must be interpreted in conjunction with sentiment valence and hashtag context.
          </p>
        </div>
      </div>
    </div>
  );
}

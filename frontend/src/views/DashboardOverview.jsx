import React from 'react';
import { 
  FileText, 
  Smile, 
  Frown, 
  Meh, 
  Cpu, 
  Clock, 
  Database, 
  ArrowRight,
  TrendingUp,
  Download
} from 'lucide-react';
import MetricCard from '../components/MetricCard';
import SentimentDonut from '../components/SentimentDonut';
import TopWordsChart from '../components/TopWordsChart';
import TimelineChart from '../components/TimelineChart';
import SDG9Badge from '../components/SDG9Badge';
import { getExportCsvUrl } from '../api/client';

export default function DashboardOverview({ 
  overview, 
  sentimentData, 
  trendData, 
  onNavigateTab,
  onRunAnalysis,
  isAnalyzing
}) {
  if (!overview) {
    return (
      <div className="py-24 text-center">
        <div className="animate-spin w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full mx-auto mb-3" />
        <p className="text-gray-400 text-sm">Loading analytics pipeline...</p>
      </div>
    );
  }

  const pcts = overview.sentiment_percentages || {};
  const counts = overview.sentiment_counts || {};

  return (
    <div className="space-y-6 animate-fadeIn pb-12">
      
      {/* Top Banner & Dataset Info */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl glass-panel bg-gradient-to-r from-gray-900 via-gray-900/90 to-cyan-950/30 border border-gray-800">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs uppercase tracking-wider font-semibold text-cyan-400">
              Active Dataset Analyzed
            </span>
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-white mt-0.5">
            {overview.dataset_name}
          </h2>
          <p className="text-xs text-gray-400 mt-1">
            Engine: <span className="text-cyan-300 font-semibold">{overview.processing_mode}</span> • Completed in <span className="text-white font-medium">{overview.processing_duration_ms} ms</span>
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <a
            href={getExportCsvUrl()}
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold bg-gray-800/80 hover:bg-gray-700/80 border border-gray-700 text-gray-200 transition-colors shadow-sm"
          >
            <Download className="w-3.5 h-3.5 text-cyan-400" />
            <span>Download CSV</span>
          </a>
          <button
            onClick={() => onNavigateTab('mapreduce')}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg text-xs font-semibold bg-cyan-950/80 hover:bg-cyan-900/80 border border-cyan-700/60 text-cyan-300 transition-colors"
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>MapReduce Telemetry</span>
            <ArrowRight className="w-3 h-3 ml-0.5" />
          </button>
        </div>
      </div>

      {/* KPI Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4">
        <MetricCard
          title="Total Posts"
          value={overview.total_records}
          subtitle="Processed Records"
          icon={FileText}
          color="cyan"
        />
        <MetricCard
          title="Positive"
          value={`${pcts.positive || 0}%`}
          subtitle={`${counts.positive || 0} posts`}
          icon={Smile}
          color="emerald"
        />
        <MetricCard
          title="Negative"
          value={`${pcts.negative || 0}%`}
          subtitle={`${counts.negative || 0} posts`}
          icon={Frown}
          color="rose"
        />
        <MetricCard
          title="Neutral"
          value={`${pcts.neutral || 0}%`}
          subtitle={`${counts.neutral || 0} posts`}
          icon={Meh}
          color="amber"
        />
        <MetricCard
          title="Unique Words"
          value={overview.unique_words}
          subtitle="MapReduce Tokens"
          icon={TrendingUp}
          color="purple"
        />
        <MetricCard
          title="Pipeline Time"
          value={`${overview.processing_duration_ms} ms`}
          subtitle="5 MR Jobs + NLP"
          icon={Clock}
          color="blue"
        />
      </div>

      {/* SDG 9 Alignment Banner */}
      <SDG9Badge />

      {/* Primary Analytics Section: Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Sentiment Distribution Card */}
        <div className="p-5 rounded-2xl glass-panel border border-gray-800 flex flex-col justify-between">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-bold text-white">Sentiment Distribution</h3>
              <p className="text-xs text-gray-400">English, Tanglish & Tamil classification</p>
            </div>
            <button
              onClick={() => onNavigateTab('sentiment')}
              className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold"
            >
              Details →
            </button>
          </div>
          <SentimentDonut distribution={{ counts: counts, percentages: pcts, total_records: overview.total_records }} />
          <div className="grid grid-cols-3 gap-2 pt-3 border-t border-gray-800 text-center">
            <div className="p-2 rounded-lg bg-emerald-950/30 border border-emerald-900/40">
              <span className="text-[10px] text-emerald-400 block font-semibold uppercase">Pos</span>
              <span className="text-sm font-bold text-white">{pcts.positive || 0}%</span>
            </div>
            <div className="p-2 rounded-lg bg-rose-950/30 border border-rose-900/40">
              <span className="text-[10px] text-rose-400 block font-semibold uppercase">Neg</span>
              <span className="text-sm font-bold text-white">{pcts.negative || 0}%</span>
            </div>
            <div className="p-2 rounded-lg bg-amber-950/30 border border-amber-900/40">
              <span className="text-[10px] text-amber-400 block font-semibold uppercase">Neu</span>
              <span className="text-sm font-bold text-white">{pcts.neutral || 0}%</span>
            </div>
          </div>
        </div>

        {/* Word Frequency Chart */}
        <div className="lg:col-span-2 p-5 rounded-2xl glass-panel border border-gray-800">
          <TopWordsChart wordTrends={trendData?.word_trends} />
        </div>
      </div>

      {/* Daily Sentiment Timeline */}
      {sentimentData?.daily_timeline && (
        <div className="p-5 rounded-2xl glass-panel border border-gray-800">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h3 className="text-sm font-bold text-white">Daily Sentiment Timeline</h3>
              <p className="text-xs text-gray-400">Aggregated by MapReduce DailySentiment job</p>
            </div>
            <button
              onClick={() => onNavigateTab('sentiment')}
              className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold"
            >
              Timeline View →
            </button>
          </div>
          <TimelineChart timeline={sentimentData.daily_timeline} />
        </div>
      )}

      {/* Big Data Processing Architecture Card */}
      <div className="p-5 rounded-2xl glass-panel border border-cyan-900/40 bg-gradient-to-br from-gray-950 via-gray-900 to-cyan-950/20">
        <h3 className="text-sm font-bold text-white mb-2 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <span>Big Data MapReduce Architecture Pipeline</span>
        </h3>
        <p className="text-xs text-gray-400 mb-4">
          Strict separation of Input Splitting → Streaming Mapper → Shuffle & Key Sorting → Reducer Aggregation
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-5 gap-2 text-center text-xs">
          <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800">
            <span className="text-cyan-400 font-bold block mb-1">1. Ingestion</span>
            <span className="text-gray-300 text-[11px]">CSV / JSON validation, null & duplicate checks</span>
          </div>
          <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800">
            <span className="text-blue-400 font-bold block mb-1">2. NLP Cleansing</span>
            <span className="text-gray-300 text-[11px]">Emoji, URL, Tanglish tokenization & valence</span>
          </div>
          <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800">
            <span className="text-purple-400 font-bold block mb-1">3. Map Phase</span>
            <span className="text-gray-300 text-[11px]">5 Mappers emit (key, value) pairs</span>
          </div>
          <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800">
            <span className="text-amber-400 font-bold block mb-1">4. Sort & Shuffle</span>
            <span className="text-gray-300 text-[11px]">Partitioning & alphabetical grouping by key</span>
          </div>
          <div className="p-3 rounded-xl bg-gray-900/80 border border-gray-800">
            <span className="text-emerald-400 font-bold block mb-1">5. Reduce Phase</span>
            <span className="text-gray-300 text-[11px]">Aggregates counts into verified output files</span>
          </div>
        </div>
      </div>
    </div>
  );
}

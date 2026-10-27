import React from 'react';
import { 
  Activity, 
  BarChart3, 
  PieChart, 
  TrendingUp, 
  Database, 
  Cpu, 
  Upload, 
  Play, 
  RefreshCw,
  Layers,
  Sparkles
} from 'lucide-react';

export default function Navbar({ 
  activeTab, 
  setActiveTab, 
  datasets, 
  selectedDatasetId, 
  onSelectDataset, 
  onRunAnalysis, 
  onOpenUpload,
  isAnalyzing,
  processingMode
}) {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-gray-800/80 bg-gray-900/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Branding */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Activity className="w-6 h-6 text-white animate-pulse" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-300 bg-clip-text text-transparent">
                  SocialPulse 360
                </span>
                <span className="text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full bg-cyan-950/80 text-cyan-400 border border-cyan-800/60">
                  BDA Platform
                </span>
              </div>
              <p className="text-xs text-gray-400 hidden sm:block">
                Social Media Sentiment & Trend Analytics (Tamil-English & Hadoop)
              </p>
            </div>
          </div>

          {/* Dataset Selector & Action Controls */}
          <div className="flex items-center space-x-3">
            {/* Dataset Select */}
            <div className="hidden md:flex items-center space-x-2 bg-gray-800/60 border border-gray-700/60 rounded-lg px-2.5 py-1.5 text-xs text-gray-300">
              <Database className="w-3.5 h-3.5 text-cyan-400" />
              <select
                value={selectedDatasetId || ''}
                onChange={(e) => onSelectDataset(e.target.value)}
                className="bg-transparent border-none text-xs text-gray-200 focus:outline-none cursor-pointer"
                disabled={isAnalyzing}
              >
                {datasets.map((d) => (
                  <option key={d.id} value={d.id} className="bg-gray-900 text-gray-200">
                    {d.name} ({d.total_rows} rows)
                  </option>
                ))}
              </select>
            </div>

            {/* Run Analysis Button */}
            <button
              onClick={onRunAnalysis}
              disabled={isAnalyzing}
              className={`flex items-center space-x-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold shadow-md transition-all ${
                isAnalyzing 
                  ? 'bg-cyan-900/50 text-cyan-300 cursor-not-allowed border border-cyan-700/50' 
                  : 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white shadow-cyan-500/25 active:scale-95'
              }`}
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>MapReducing...</span>
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>Run Pipeline</span>
                </>
              )}
            </button>

            {/* Upload Dataset Button */}
            <button
              onClick={onOpenUpload}
              className="flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-medium bg-gray-800 hover:bg-gray-700/80 border border-gray-700 text-gray-200 transition-colors"
            >
              <Upload className="w-3.5 h-3.5 text-blue-400" />
              <span className="hidden sm:inline">Upload</span>
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 sm:space-x-2 border-t border-gray-800/80 pt-1 pb-2 overflow-x-auto">
          {[
            { id: 'overview', label: 'Overview', icon: BarChart3 },
            { id: 'sentiment', label: 'Sentiment Analytics', icon: PieChart },
            { id: 'trends', label: 'Trend Analytics', icon: TrendingUp },
            { id: 'explorer', label: 'Dataset Explorer', icon: Database },
            { id: 'mapreduce', label: 'MapReduce Monitor', icon: Cpu },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/50 border border-transparent'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-cyan-400' : 'text-gray-500'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
}

import React, { useState, useEffect } from 'react';
import { Search, Download, Filter, ChevronLeft, ChevronRight, CheckCircle2, AlertCircle, HelpCircle } from 'lucide-react';
import { fetchRecords, getExportCsvUrl } from '../api/client';

export default function ExplorerView() {
  const [records, setRecords] = useState([]);
  const [totalRecords, setTotalRecords] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [sentimentFilter, setSentimentFilter] = useState('all');
  const [languageFilter, setLanguageFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await fetchRecords({
        page: currentPage,
        pageSize,
        sentiment: sentimentFilter,
        language: languageFilter,
        search: searchTerm,
      });
      setRecords(data.records || []);
      setTotalRecords(data.total_records || 0);
      setTotalPages(data.total_pages || 1);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [currentPage, pageSize, sentimentFilter, languageFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadData();
  };

  const getSentimentBadge = (sentiment) => {
    const s = String(sentiment).toLowerCase();
    if (s === 'positive') {
      return (
        <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800 flex items-center space-x-1 w-max">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
          <span>Positive</span>
        </span>
      );
    }
    if (s === 'negative') {
      return (
        <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-rose-950 text-rose-400 border border-rose-800 flex items-center space-x-1 w-max">
          <span className="w-1.5 h-1.5 rounded-full bg-rose-400" />
          <span>Negative</span>
        </span>
      );
    }
    return (
      <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-amber-950 text-amber-400 border border-amber-800 flex items-center space-x-1 w-max">
        <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />
        <span>Neutral</span>
      </span>
    );
  };

  return (
    <div className="space-y-6 animate-fadeIn pb-12">
      
      {/* Header and Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-black text-white">Dataset Explorer</h2>
          <p className="text-xs text-gray-400">
            Inspect raw social posts alongside cleaned representations, predicted sentiments, and confidence scores
          </p>
        </div>

        <a
          href={getExportCsvUrl()}
          target="_blank"
          rel="noreferrer"
          className="flex items-center space-x-2 px-4 py-2 rounded-lg text-xs font-bold bg-cyan-600 hover:bg-cyan-500 text-white shadow-md shadow-cyan-600/20 transition-all self-start md:self-auto"
        >
          <Download className="w-4 h-4" />
          <span>Export All to CSV</span>
        </a>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-xl glass-panel border border-gray-800 flex flex-col md:flex-row gap-3 items-center justify-between">
        
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search keywords, #tags, or authors..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-1.5 rounded-lg bg-gray-900 border border-gray-700 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500"
          />
        </form>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          {/* Sentiment Filter */}
          <div className="flex items-center space-x-1 bg-gray-900 border border-gray-700 rounded-lg p-1 text-xs">
            <span className="text-gray-400 text-[11px] px-1.5">Sentiment:</span>
            {['all', 'positive', 'negative', 'neutral'].map((s) => (
              <button
                key={s}
                onClick={() => { setSentimentFilter(s); setCurrentPage(1); }}
                className={`px-2 py-0.5 rounded capitalize ${
                  sentimentFilter === s
                    ? 'bg-cyan-600 text-white font-semibold'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {s}
              </button>
            ))}
          </div>

          {/* Language Filter */}
          <div className="flex items-center space-x-1 bg-gray-900 border border-gray-700 rounded-lg p-1 text-xs">
            <span className="text-gray-400 text-[11px] px-1.5">Lang:</span>
            {['all', 'english', 'tanglish', 'tamil'].map((l) => (
              <button
                key={l}
                onClick={() => { setLanguageFilter(l); setCurrentPage(1); }}
                className={`px-2 py-0.5 rounded capitalize ${
                  languageFilter === l
                    ? 'bg-blue-600 text-white font-semibold'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {l}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="rounded-xl glass-panel border border-gray-800 overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-gray-300">
            <thead className="bg-gray-900/90 text-gray-400 uppercase tracking-wider text-[10px] border-b border-gray-800">
              <tr>
                <th className="py-3 px-4 w-12 text-center">ID</th>
                <th className="py-3 px-4 min-w-[280px]">Original Text</th>
                <th className="py-3 px-4 min-w-[220px]">Cleaned Text</th>
                <th className="py-3 px-3 w-28">Sentiment</th>
                <th className="py-3 px-3 w-24">Score & Conf</th>
                <th className="py-3 px-3 w-20">Lang</th>
                <th className="py-3 px-3 w-28">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/60">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-gray-500">
                    <div className="animate-spin w-5 h-5 border-2 border-cyan-500 border-t-transparent rounded-full mx-auto mb-2" />
                    Fetching records...
                  </td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-gray-500">
                    No matching records found for the applied filters.
                  </td>
                </tr>
              ) : (
                records.map((r, idx) => (
                  <tr key={idx} className="hover:bg-gray-800/30 transition-colors">
                    <td className="py-3 px-4 text-center text-gray-500 font-mono text-[11px]">
                      {r.id || idx + 1}
                    </td>
                    <td className="py-3 px-4 text-gray-100 font-medium leading-relaxed">
                      {r.original_text}
                    </td>
                    <td className="py-3 px-4 text-gray-400 text-[11px] leading-relaxed font-mono">
                      {r.cleaned_text}
                    </td>
                    <td className="py-3 px-3">
                      {getSentimentBadge(r.sentiment)}
                    </td>
                    <td className="py-3 px-3">
                      <div className="font-mono text-[11px] font-bold text-gray-200">
                        {r.sentiment_score !== undefined ? Number(r.sentiment_score).toFixed(2) : '-'}
                      </div>
                      <div className="text-[10px] text-gray-400">
                        {r.sentiment_confidence ? `${Math.round(r.sentiment_confidence * 100)}% conf` : ''}
                      </div>
                    </td>
                    <td className="py-3 px-3">
                      <span className="text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded bg-gray-800 text-cyan-300 border border-gray-700">
                        {r.language || 'en'}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-[11px] text-gray-400 whitespace-nowrap">
                      {r.formatted_date || r.timestamp || '-'}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-3 bg-gray-900/60 border-t border-gray-800 flex items-center justify-between text-xs text-gray-400">
          <div>
            Showing <span className="text-white font-medium">{records.length}</span> of <span className="text-white font-medium">{totalRecords}</span> records
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage <= 1 || loading}
              className="p-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-2">
              Page <span className="text-white font-bold">{currentPage}</span> of <span className="text-white font-bold">{totalPages}</span>
            </span>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage >= totalPages || loading}
              className="p-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardOverview from './views/DashboardOverview';
import SentimentView from './views/SentimentView';
import TrendsView from './views/TrendsView';
import ExplorerView from './views/ExplorerView';
import MapReduceView from './views/MapReduceView';
import DataUploadModal from './components/DataUploadModal';
import { 
  fetchDatasets, 
  fetchOverview, 
  fetchSentimentAnalytics, 
  fetchTrends, 
  runAnalysis 
} from './api/client';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [datasets, setDatasets] = useState([]);
  const [selectedDatasetId, setSelectedDatasetId] = useState('');
  const [overview, setOverview] = useState(null);
  const [sentimentData, setSentimentData] = useState(null);
  const [trendData, setTrendData] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [errorNotice, setErrorNotice] = useState(null);
  const [successNotice, setSuccessNotice] = useState(null);

  // Load datasets and initial analytics
  const loadInitialData = async () => {
    try {
      const dsRes = await fetchDatasets();
      setDatasets(dsRes.datasets || []);
      if (dsRes.datasets && dsRes.datasets.length > 0) {
        setSelectedDatasetId(dsRes.datasets[0].id);
      }
      await refreshAllAnalytics();
    } catch (err) {
      console.error("Initialization error:", err);
      setErrorNotice("Could not connect to backend API. Please make sure the backend server is running on port 8000.");
    }
  };

  const refreshAllAnalytics = async () => {
    try {
      const [ov, sent, tr] = await Promise.all([
        fetchOverview(),
        fetchSentimentAnalytics(),
        fetchTrends()
      ]);
      setOverview(ov);
      setSentimentData(sent);
      setTrendData(tr);
    } catch (err) {
      console.error("Error refreshing analytics:", err);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const handleSelectDataset = async (datasetId) => {
    setSelectedDatasetId(datasetId);
    await handleExecuteAnalysis(datasetId);
  };

  const handleExecuteAnalysis = async (targetId = null) => {
    const idToRun = targetId || selectedDatasetId;
    if (!idToRun) return;

    setIsAnalyzing(true);
    setErrorNotice(null);
    setSuccessNotice(null);
    try {
      await runAnalysis(idToRun, 'local');
      await refreshAllAnalytics();
      setSuccessNotice("MapReduce pipeline executed successfully!");
      setTimeout(() => setSuccessNotice(null), 3500);
    } catch (err) {
      setErrorNotice(err.message || "Pipeline execution failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleUploadSuccess = async (newDatasetId) => {
    const dsRes = await fetchDatasets();
    setDatasets(dsRes.datasets || []);
    setSelectedDatasetId(newDatasetId);
    await handleExecuteAnalysis(newDatasetId);
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-gray-100 flex flex-col font-['Inter',sans-serif]">
      
      {/* Navigation Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        datasets={datasets}
        selectedDatasetId={selectedDatasetId}
        onSelectDataset={handleSelectDataset}
        onRunAnalysis={() => handleExecuteAnalysis()}
        onOpenUpload={() => setIsUploadOpen(true)}
        isAnalyzing={isAnalyzing}
        processingMode={overview?.processing_mode}
      />

      {/* Global Toast Notifications */}
      <div className="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 mt-4">
        {errorNotice && (
          <div className="p-3.5 rounded-xl bg-rose-950/70 border border-rose-800 text-rose-200 text-xs flex items-center justify-between shadow-lg animate-fadeIn">
            <span>{errorNotice}</span>
            <button onClick={() => setErrorNotice(null)} className="text-rose-400 hover:text-white font-bold ml-2">✕</button>
          </div>
        )}
        {successNotice && (
          <div className="p-3.5 rounded-xl bg-emerald-950/70 border border-emerald-800 text-emerald-200 text-xs flex items-center justify-between shadow-lg animate-fadeIn">
            <span>{successNotice}</span>
            <button onClick={() => setSuccessNotice(null)} className="text-emerald-400 hover:text-white font-bold ml-2">✕</button>
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {activeTab === 'overview' && (
          <DashboardOverview
            overview={overview}
            sentimentData={sentimentData}
            trendData={trendData}
            onNavigateTab={setActiveTab}
            onRunAnalysis={() => handleExecuteAnalysis()}
            isAnalyzing={isAnalyzing}
          />
        )}

        {activeTab === 'sentiment' && (
          <SentimentView sentimentData={sentimentData} />
        )}

        {activeTab === 'trends' && (
          <TrendsView trendData={trendData} />
        )}

        {activeTab === 'explorer' && (
          <ExplorerView />
        )}

        {activeTab === 'mapreduce' && (
          <MapReduceView />
        )}
      </main>

      {/* Upload Modal */}
      <DataUploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onUploadSuccess={handleUploadSuccess}
      />

      {/* Footer */}
      <footer className="border-t border-gray-800/80 bg-gray-950/60 py-6 text-center text-xs text-gray-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>SocialPulse 360 • Big Data Analytics Engineering Project (SDG 9)</span>
          <span className="font-mono text-[11px] text-gray-400">Apache Hadoop • MapReduce • Python • FastAPI • React</span>
        </div>
      </footer>

    </div>
  );
}

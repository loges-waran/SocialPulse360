import React, { useState, useEffect } from 'react';
import { Cpu, Terminal, CheckCircle2, Clock, FileCode, Layers, RefreshCw, Eye } from 'lucide-react';
import { fetchMapReduceJobs, fetchMapReduceSource } from '../api/client';

export default function MapReduceView() {
  const [jobsData, setJobsData] = useState(null);
  const [selectedJobKey, setSelectedJobKey] = useState('wordcount');
  const [codeData, setCodeData] = useState(null);
  const [activeCodeTab, setActiveCodeTab] = useState('mapper'); // 'mapper' | 'reducer' | 'output'
  const [loading, setLoading] = useState(true);

  const loadJobs = async () => {
    setLoading(true);
    try {
      const data = await fetchMapReduceJobs();
      setJobsData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadCode = async (jobKey) => {
    try {
      const data = await fetchMapReduceSource(jobKey);
      setCodeData(data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadJobs();
  }, []);

  useEffect(() => {
    if (selectedJobKey) {
      loadCode(selectedJobKey);
    }
  }, [selectedJobKey]);

  if (loading && !jobsData) {
    return <div className="py-20 text-center text-gray-400">Loading MapReduce telemetry...</div>;
  }

  const selectedJob = (jobsData?.jobs || []).find(j => j.job_key === selectedJobKey) || jobsData?.jobs?.[0];

  return (
    <div className="space-y-6 animate-fadeIn pb-12">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs uppercase font-bold text-cyan-400 tracking-wider">Hadoop & HDFS Simulation</span>
            <span className="px-2 py-0.5 rounded bg-cyan-950 border border-cyan-800 text-[10px] text-cyan-300 font-semibold">
              {jobsData?.processing_mode || 'Local MapReduce'}
            </span>
          </div>
          <h2 className="text-xl font-black text-white mt-1">MapReduce Jobs Telemetry & Code Inspector</h2>
          <p className="text-xs text-gray-400">
            Real execution telemetry across all 5 Big Data stages with verifiable outputs
          </p>
        </div>

        <button
          onClick={loadJobs}
          className="flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-gray-800 hover:bg-gray-700 text-gray-200 border border-gray-700 self-start md:self-auto"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Telemetry</span>
        </button>
      </div>

      {/* Jobs Overview Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {(jobsData?.jobs || []).map((job) => {
          const isSelected = job.job_key === selectedJobKey;
          return (
            <div
              key={job.job_key}
              onClick={() => setSelectedJobKey(job.job_key)}
              className={`p-3.5 rounded-xl cursor-pointer transition-all border ${
                isSelected
                  ? 'bg-cyan-950/40 border-cyan-500/80 shadow-lg shadow-cyan-500/10'
                  : 'glass-panel border-gray-800 hover:border-gray-700'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-white truncate">{job.job_name}</span>
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
              </div>
              <div className="text-[11px] text-gray-400 space-y-1 font-mono">
                <div>Map In: <span className="text-cyan-300 font-bold">{job.metrics.map_input_records}</span></div>
                <div>Pairs: <span className="text-blue-300 font-bold">{job.metrics.map_output_records}</span></div>
                <div>Reduce Out: <span className="text-emerald-300 font-bold">{job.metrics.reduce_output_records}</span></div>
              </div>
              <div className="mt-2 pt-2 border-t border-gray-800 flex items-center justify-between text-[10px] text-gray-400">
                <span>{job.duration_ms} ms</span>
                <span className="text-cyan-400 flex items-center space-x-0.5">
                  <Eye className="w-3 h-3" />
                  <span>Inspect</span>
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Detail Inspector Section */}
      {selectedJob && (
        <div className="rounded-2xl glass-panel border border-gray-800 overflow-hidden shadow-2xl">
          
          {/* Header Bar */}
          <div className="p-4 bg-gray-900/90 border-b border-gray-800 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-extrabold text-white">{selectedJob.job_name} Job</h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-950 text-emerald-400 border border-emerald-800">
                  {selectedJob.status}
                </span>
              </div>
              <p className="text-xs text-gray-400 mt-0.5">
                Saved File: <code className="text-cyan-300 font-mono">{selectedJob.output_file}</code> • Runtime: <strong>{selectedJob.duration_ms} ms</strong>
              </p>
            </div>

            {/* View Tabs */}
            <div className="flex space-x-1 bg-gray-800/90 p-1 rounded-lg border border-gray-700 text-xs">
              <button
                onClick={() => setActiveCodeTab('output')}
                className={`px-3 py-1 rounded-md font-semibold transition-all ${
                  activeCodeTab === 'output'
                    ? 'bg-cyan-600 text-white shadow-sm'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Output Preview
              </button>
              <button
                onClick={() => setActiveCodeTab('mapper')}
                className={`px-3 py-1 rounded-md font-semibold transition-all ${
                  activeCodeTab === 'mapper'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Mapper Script (.py)
              </button>
              <button
                onClick={() => setActiveCodeTab('reducer')}
                className={`px-3 py-1 rounded-md font-semibold transition-all ${
                  activeCodeTab === 'reducer'
                    ? 'bg-indigo-600 text-white shadow-sm'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Reducer Script (.py)
              </button>
            </div>
          </div>

          {/* Telemetry Metrics Strip */}
          <div className="grid grid-cols-2 sm:grid-cols-5 divide-x divide-gray-800 bg-gray-950/60 p-3 text-center text-xs">
            <div>
              <span className="text-[10px] text-gray-400 block uppercase">1. Map Input Records</span>
              <span className="text-sm font-bold text-white font-mono">{selectedJob.metrics.map_input_records}</span>
            </div>
            <div>
              <span className="text-[10px] text-gray-400 block uppercase">2. Map Emitted Pairs</span>
              <span className="text-sm font-bold text-cyan-400 font-mono">{selectedJob.metrics.map_output_records}</span>
            </div>
            <div>
              <span className="text-[10px] text-gray-400 block uppercase">3. Shuffle Distinct Keys</span>
              <span className="text-sm font-bold text-amber-400 font-mono">{selectedJob.metrics.shuffle_keys_count}</span>
            </div>
            <div>
              <span className="text-[10px] text-gray-400 block uppercase">4. Reduce Input Pairs</span>
              <span className="text-sm font-bold text-blue-400 font-mono">{selectedJob.metrics.reduce_input_records}</span>
            </div>
            <div>
              <span className="text-[10px] text-gray-400 block uppercase">5. Reduce Aggregated Records</span>
              <span className="text-sm font-bold text-emerald-400 font-mono">{selectedJob.metrics.reduce_output_records}</span>
            </div>
          </div>

          {/* Terminal / Code Content Container */}
          <div className="p-4 bg-[#080C14] text-gray-200 font-mono text-xs overflow-x-auto min-h-[300px] max-h-[420px]">
            {activeCodeTab === 'output' && (
              <div>
                <div className="text-[11px] text-gray-500 mb-2 border-b border-gray-800/80 pb-1 flex items-center justify-between">
                  <span># Streaming key-value output (Showing first 25 sorted pairs)</span>
                  <span className="text-cyan-400 font-bold">{selectedJob.total_results} total pairs</span>
                </div>
                <pre className="text-emerald-400 whitespace-pre font-mono text-xs leading-5">
                  {selectedJob.sample_output && selectedJob.sample_output.length > 0
                    ? selectedJob.sample_output.join('\n')
                    : 'No output records'}
                </pre>
              </div>
            )}

            {activeCodeTab === 'mapper' && (
              <div>
                <div className="text-[11px] text-gray-500 mb-2 border-b border-gray-800/80 pb-1 flex items-center justify-between">
                  <span># Script: hadoop/mapper/{codeData?.mapper_file || 'mapper.py'}</span>
                  <span className="text-blue-400 font-bold">Standard STDIN / STDOUT</span>
                </div>
                <pre className="text-blue-300 whitespace-pre font-mono text-xs leading-5">
                  {codeData?.mapper_code || 'Loading mapper code...'}
                </pre>
              </div>
            )}

            {activeCodeTab === 'reducer' && (
              <div>
                <div className="text-[11px] text-gray-500 mb-2 border-b border-gray-800/80 pb-1 flex items-center justify-between">
                  <span># Script: hadoop/reducer/{codeData?.reducer_file || 'reducer.py'}</span>
                  <span className="text-indigo-400 font-bold">Hadoop Streaming Reducer</span>
                </div>
                <pre className="text-indigo-300 whitespace-pre font-mono text-xs leading-5">
                  {codeData?.reducer_code || 'Loading reducer code...'}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Hadoop Execution Guide Note */}
      <div className="p-5 rounded-2xl glass-panel border border-gray-800">
        <h4 className="text-sm font-bold text-white mb-2 flex items-center space-x-2">
          <Terminal className="w-4 h-4 text-cyan-400" />
          <span>Executing on Real Hadoop Clusters (Hadoop Streaming Command)</span>
        </h4>
        <p className="text-xs text-gray-400 mb-3">
          To run on an actual Apache Hadoop cluster with HDFS, invoke using the pre-configured Hadoop Streaming command:
        </p>
        <pre className="p-3.5 rounded-xl bg-black/60 border border-gray-800 text-cyan-300 font-mono text-xs overflow-x-auto leading-relaxed">
{`hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \\
  -files hadoop/mapper/${selectedJobKey}_mapper.py,hadoop/reducer/${selectedJobKey}_reducer.py \\
  -mapper "python3 ${selectedJobKey}_mapper.py" \\
  -reducer "python3 ${selectedJobKey}_reducer.py" \\
  -input /socialpulse/input \\
  -output /socialpulse/output/${selectedJobKey}`}
        </pre>
      </div>

    </div>
  );
}

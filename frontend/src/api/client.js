/**
 * API client for SocialPulse 360 backend.
 */

const API_BASE = import.meta.env.VITE_API_BASE || '';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error('Backend health check failed');
  return res.json();
}

export async function fetchDatasets() {
  const res = await fetch(`${API_BASE}/api/datasets`);
  if (!res.ok) throw new Error('Failed to fetch datasets');
  return res.json();
}

export async function uploadDataset(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/api/datasets/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Failed to upload dataset');
  }
  return res.json();
}

export async function runAnalysis(datasetId, processingMode = 'local') {
  const res = await fetch(`${API_BASE}/api/analysis/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ dataset_id: datasetId, processing_mode: processingMode }),
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Analysis execution failed');
  }
  return res.json();
}

export async function fetchOverview() {
  const res = await fetch(`${API_BASE}/api/analytics/overview`);
  if (!res.ok) throw new Error('Failed to fetch overview analytics');
  return res.json();
}

export async function fetchSentimentAnalytics() {
  const res = await fetch(`${API_BASE}/api/analytics/sentiment`);
  if (!res.ok) throw new Error('Failed to fetch sentiment analytics');
  return res.json();
}

export async function fetchTrends() {
  const res = await fetch(`${API_BASE}/api/analytics/trends`);
  if (!res.ok) throw new Error('Failed to fetch trend analytics');
  return res.json();
}

export async function fetchWordFrequency(limit = 50) {
  const res = await fetch(`${API_BASE}/api/analytics/word-frequency?limit=${limit}`);
  if (!res.ok) throw new Error('Failed to fetch word frequency');
  return res.json();
}

export async function fetchRecords({ page = 1, pageSize = 10, sentiment = 'all', language = 'all', search = '' }) {
  const params = new URLSearchParams({
    page: String(page),
    page_size: String(pageSize),
    sentiment,
    language,
    search: search || '',
  });
  const res = await fetch(`${API_BASE}/api/analytics/records?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch records');
  return res.json();
}

export async function fetchMapReduceJobs() {
  const res = await fetch(`${API_BASE}/api/mapreduce/jobs`);
  if (!res.ok) throw new Error('Failed to fetch MapReduce jobs');
  return res.json();
}

export async function fetchMapReduceSource(jobKey) {
  const res = await fetch(`${API_BASE}/api/mapreduce/source/${jobKey}`);
  if (!res.ok) throw new Error(`Failed to fetch source for ${jobKey}`);
  return res.json();
}

export function getExportCsvUrl() {
  return `${API_BASE}/api/export/csv`;
}

import React, { useState } from 'react';
import { X, UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { uploadDataset } from '../api/client';

export default function DataUploadModal({ isOpen, onClose, onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      const ext = selected.name.split('.').pop().toLowerCase();
      if (!['csv', 'json'].includes(ext)) {
        setError('Only .csv and .json files are supported.');
        setFile(null);
        return;
      }
      setError(null);
      setSuccess(null);
      setFile(selected);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setError(null);
    try {
      const res = await uploadDataset(file);
      setSuccess(`Dataset "${file.name}" uploaded successfully!`);
      setTimeout(() => {
        onUploadSuccess(res.dataset.id);
        onClose();
      }, 1200);
    } catch (err) {
      setError(err.message || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-md rounded-2xl glass-panel bg-gray-900 border border-gray-700/80 p-6 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-3 mb-4">
          <div className="p-2.5 rounded-xl bg-cyan-950 border border-cyan-800 text-cyan-400">
            <UploadCloud className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white">Upload Social Media Dataset</h3>
            <p className="text-xs text-gray-400">Support for CSV or JSON files (English & Tanglish)</p>
          </div>
        </div>

        {/* Drag & Drop Area */}
        <div className="mt-4 border-2 border-dashed border-gray-700 hover:border-cyan-500/60 rounded-xl p-6 text-center cursor-pointer transition-colors bg-gray-800/30">
          <input
            type="file"
            accept=".csv,.json"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center">
            <FileText className="w-10 h-10 text-cyan-400 mb-2 opacity-80" />
            <span className="text-sm font-semibold text-gray-200">
              {file ? file.name : 'Click to select CSV or JSON file'}
            </span>
            <span className="text-xs text-gray-400 mt-1">
              {file ? `${(file.size / 1024).toFixed(1)} KB` : 'Maximum file size 50 MB'}
            </span>
          </label>
        </div>

        {/* Feedback Messages */}
        {error && (
          <div className="mt-3 p-3 rounded-lg bg-rose-950/50 border border-rose-800 text-rose-300 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="mt-3 p-3 rounded-lg bg-emerald-950/50 border border-emerald-800 text-emerald-300 text-xs flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{success}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-6 flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleUpload}
            disabled={!file || isUploading}
            className={`px-5 py-2 text-xs font-bold rounded-lg flex items-center space-x-2 transition-all ${
              !file || isUploading
                ? 'bg-gray-800 text-gray-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white hover:from-cyan-400 hover:to-blue-500 shadow-md shadow-cyan-500/20'
            }`}
          >
            {isUploading && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
            <span>{isUploading ? 'Validating...' : 'Upload & Register'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}

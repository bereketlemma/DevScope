import { useState, useEffect } from 'react';
import { useRepos, useAnomalies } from '../hooks/useMetrics';
import AnomalyTimeline from '../components/charts/AnomalyTimeline';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { ShieldAlert, ChevronDown } from 'lucide-react';

export default function Anomalies() {
  const { data: repos, isLoading: reposLoading } = useRepos();
  const [selectedRepo, setSelectedRepo] = useState('');
  const [severity, setSeverity] = useState<string | undefined>();

  // Auto-select first repo when repos load
  useEffect(() => {
    if (repos && repos.length > 0 && !selectedRepo) {
      setSelectedRepo(repos[0].repo_id);
    }
  }, [repos, selectedRepo]);

  const { data: anomalies, isLoading } = useAnomalies(selectedRepo, 30, severity);

  if (reposLoading) return <LoadingSpinner />;

  return (
    <div className="animate-fade-in">
      {/* Page Header */}
      <div className="page-header">
        <div className="flex items-center gap-3 mb-1">
          <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-red-500/10 ring-1 ring-red-500/20">
            <ShieldAlert className="w-5 h-5 text-red-400" />
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">Anomaly Feed</h1>
            <p className="section-subtitle mt-0">
              Productivity regressions flagged by AI anomaly detection
            </p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="glass-card p-4 mb-6">
        <div className="flex flex-col sm:flex-row flex-wrap items-stretch sm:items-center gap-3">
          <div className="relative">
            <select
              value={selectedRepo}
              onChange={(e) => setSelectedRepo(e.target.value)}
              className="input-field appearance-none pr-8 w-full sm:min-w-[200px]"
            >
              <option value="">Select repository...</option>
              {repos?.map((r) => (
                <option key={r.repo_id} value={r.repo_id}>
                  {r.repo_id}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-500 pointer-events-none" />
          </div>

          <div className="relative">
            <select
              value={severity ?? ''}
              onChange={(e) => setSeverity(e.target.value || undefined)}
              className="input-field appearance-none pr-8 w-full sm:min-w-[160px]"
            >
              <option value="">All severities</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
            </select>
            <ChevronDown className="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-500 pointer-events-none" />
          </div>

          {selectedRepo && anomalies && (
            <div className="ml-auto">
              <span className="text-xs text-gray-500">
                <span className="text-white font-semibold">{anomalies.length}</span> anomalies found
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Results */}
      <div>
        {!selectedRepo && (
          <div className="glass-card p-12 text-center">
            <div className="w-14 h-14 rounded-2xl bg-surface-800 ring-1 ring-white/[0.06] flex items-center justify-center mx-auto mb-4">
              <ShieldAlert className="w-7 h-7 text-gray-600" />
            </div>
            <p className="text-sm font-medium text-gray-300">Select a repository</p>
            <p className="text-xs text-gray-500 mt-1">Choose a repo above to view detected anomalies.</p>
          </div>
        )}
        {selectedRepo && isLoading && <LoadingSpinner />}
        {selectedRepo && !isLoading && <AnomalyTimeline anomalies={anomalies ?? []} />}
      </div>
    </div>
  );
}

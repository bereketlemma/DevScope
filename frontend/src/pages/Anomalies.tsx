import { useState } from 'react';
import { useRepos, useAnomalies } from '../hooks/useMetrics';
import AnomalyTimeline from '../components/charts/AnomalyTimeline';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function Anomalies() {
  const { data: repos, isLoading: reposLoading } = useRepos();
  const [selectedRepo, setSelectedRepo] = useState('');
  const [severity, setSeverity] = useState<string | undefined>();

  const { data: anomalies, isLoading } = useAnomalies(selectedRepo, 30, severity);

  if (reposLoading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Anomaly Feed</h1>
      <p className="mt-1 text-sm text-gray-500">
        Productivity regressions flagged by Vertex AI anomaly detection.
      </p>

      {/* Filters */}
      <div className="mt-4 flex gap-3">
        <select
          value={selectedRepo}
          onChange={(e) => setSelectedRepo(e.target.value)}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm dark:bg-gray-800 dark:border-gray-600"
        >
          <option value="">Select a repository</option>
          {repos?.map((r) => (
            <option key={r.repo_id} value={r.repo_id}>
              {r.repo_id}
            </option>
          ))}
        </select>

        <select
          value={severity ?? ''}
          onChange={(e) => setSeverity(e.target.value || undefined)}
          className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm dark:bg-gray-800 dark:border-gray-600"
        >
          <option value="">All severities</option>
          <option value="CRITICAL">Critical</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
        </select>
      </div>

      {/* Results */}
      <div className="mt-6">
        {!selectedRepo && (
          <p className="text-sm text-gray-400 py-8 text-center">
            Select a repository to view anomalies.
          </p>
        )}
        {selectedRepo && isLoading && <LoadingSpinner />}
        {selectedRepo && !isLoading && <AnomalyTimeline anomalies={anomalies ?? []} />}
      </div>
    </div>
  );
}

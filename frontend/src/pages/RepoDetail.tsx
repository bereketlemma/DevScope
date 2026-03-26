import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { usePRLatency, useCodeChurn, useReviewCycles, useHealthScore, useAnomalies } from '../hooks/useMetrics';
import PRLatencyChart from '../components/charts/PRLatencyChart';
import CodeChurnChart from '../components/charts/CodeChurnChart';
import ReviewCycleChart from '../components/charts/ReviewCycleChart';
import HealthScoreGauge from '../components/charts/HealthScoreGauge';
import AnomalyTimeline from '../components/charts/AnomalyTimeline';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { ArrowLeft, AlertTriangle, BarChart3, RefreshCw } from 'lucide-react';
import clsx from 'clsx';

const TIME_RANGES = [
  { label: '7d', days: 7 },
  { label: '30d', days: 30 },
  { label: '60d', days: 60 },
  { label: '90d', days: 90 },
] as const;

export default function RepoDetail() {
  const { repoId } = useParams<{ repoId: string }>();
  const decoded = decodeURIComponent(repoId ?? '');
  const [days, setDays] = useState(30);

  const latency = usePRLatency(decoded, days);
  const churn = useCodeChurn(decoded, days);
  const reviews = useReviewCycles(decoded, days);
  const health = useHealthScore(decoded, days);
  const anomalies = useAnomalies(decoded, days);

  const isLoading = latency.isLoading || churn.isLoading || reviews.isLoading || health.isLoading;
  const isFetching = latency.isFetching || churn.isFetching || reviews.isFetching || health.isFetching;
  const dataUpdatedAt = Math.max(
    latency.dataUpdatedAt ?? 0,
    churn.dataUpdatedAt ?? 0,
    reviews.dataUpdatedAt ?? 0,
    health.dataUpdatedAt ?? 0,
  );

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="animate-fade-in">
      {/* Page Header */}
      <div className="page-header">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-xs font-medium text-gray-500 hover:text-brand-400 transition-colors mb-4"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to Dashboard
        </Link>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center justify-center w-10 h-10 rounded-lg bg-brand-gradient shadow-glow flex-shrink-0">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <div className="min-w-0">
              <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight truncate">{decoded}</h1>
              <div className="flex items-center gap-2 mt-0.5">
                <p className="text-sm text-gray-400">Engineering health metrics</p>
                {dataUpdatedAt > 0 && (
                  <span className="text-[10px] text-gray-600">
                    · Updated {new Date(dataUpdatedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Time range selector */}
          <div className="flex items-center gap-2">
            <div className="flex items-center rounded-lg bg-surface-900 border border-white/[0.06] p-0.5">
              {TIME_RANGES.map((r) => (
                <button
                  key={r.days}
                  onClick={() => setDays(r.days)}
                  className={clsx(
                    'px-3 py-1.5 rounded-md text-xs font-medium transition-all',
                    days === r.days
                      ? 'bg-brand-600/20 text-brand-400 shadow-sm'
                      : 'text-gray-500 hover:text-gray-300'
                  )}
                >
                  {r.label}
                </button>
              ))}
            </div>
            <button
              onClick={() => {
                latency.refetch();
                churn.refetch();
                reviews.refetch();
                health.refetch();
                anomalies.refetch();
              }}
              aria-label="Refresh data"
              className="p-2 rounded-lg text-gray-500 hover:text-gray-300 hover:bg-white/[0.04] transition-colors"
            >
              <RefreshCw className={clsx('w-4 h-4', isFetching && 'animate-spin')} />
            </button>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid gap-4 sm:gap-5 grid-cols-1 lg:grid-cols-2">
        {health.error ? (
          <div className="glass-card p-6 text-center">
            <p className="text-sm text-red-400">Failed to load health score</p>
            <button onClick={() => health.refetch()} className="mt-2 text-xs text-brand-400 hover:underline">Retry</button>
          </div>
        ) : health.data ? <HealthScoreGauge data={health.data} /> : null}

        {latency.error ? (
          <div className="glass-card p-6 text-center">
            <p className="text-sm text-red-400">Failed to load PR latency</p>
            <button onClick={() => latency.refetch()} className="mt-2 text-xs text-brand-400 hover:underline">Retry</button>
          </div>
        ) : latency.data ? <PRLatencyChart data={latency.data} /> : null}

        {churn.error ? (
          <div className="glass-card p-6 text-center">
            <p className="text-sm text-red-400">Failed to load code churn</p>
            <button onClick={() => churn.refetch()} className="mt-2 text-xs text-brand-400 hover:underline">Retry</button>
          </div>
        ) : churn.data ? <CodeChurnChart data={churn.data} /> : null}

        {reviews.error ? (
          <div className="glass-card p-6 text-center">
            <p className="text-sm text-red-400">Failed to load review cycles</p>
            <button onClick={() => reviews.refetch()} className="mt-2 text-xs text-brand-400 hover:underline">Retry</button>
          </div>
        ) : reviews.data ? <ReviewCycleChart data={reviews.data} /> : null}
      </div>

      {/* Anomalies Section */}
      <div className="mt-10">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-5 h-5 text-amber-400" />
          <h2 className="section-title">Anomalies Detected</h2>
          {anomalies.data && anomalies.data.length > 0 && (
            <span className="badge-critical ml-1">{anomalies.data.length}</span>
          )}
        </div>
        <AnomalyTimeline anomalies={anomalies.data ?? []} />
      </div>
    </div>
  );
}

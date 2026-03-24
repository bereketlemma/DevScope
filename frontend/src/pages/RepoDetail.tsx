import { useParams } from 'react-router-dom';
import { usePRLatency, useCodeChurn, useReviewCycles, useHealthScore, useAnomalies } from '../hooks/useMetrics';
import PRLatencyChart from '../components/charts/PRLatencyChart';
import CodeChurnChart from '../components/charts/CodeChurnChart';
import ReviewCycleChart from '../components/charts/ReviewCycleChart';
import HealthScoreGauge from '../components/charts/HealthScoreGauge';
import AnomalyTimeline from '../components/charts/AnomalyTimeline';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function RepoDetail() {
  const { repoId } = useParams<{ repoId: string }>();
  const decoded = decodeURIComponent(repoId ?? '');

  const latency = usePRLatency(decoded);
  const churn = useCodeChurn(decoded);
  const reviews = useReviewCycles(decoded);
  const health = useHealthScore(decoded);
  const anomalies = useAnomalies(decoded);

  const isLoading = latency.isLoading || churn.isLoading || reviews.isLoading || health.isLoading;

  if (isLoading) return <LoadingSpinner />;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{decoded}</h1>
      <p className="mt-1 text-sm text-gray-500">Engineering health metrics — last 30 days</p>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {health.data && <HealthScoreGauge data={health.data} />}
        {latency.data && <PRLatencyChart data={latency.data} />}
        {churn.data && <CodeChurnChart data={churn.data} />}
        {reviews.data && <ReviewCycleChart data={reviews.data} />}
      </div>

      <div className="mt-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
          Anomalies Detected
        </h2>
        <AnomalyTimeline anomalies={anomalies.data ?? []} />
      </div>
    </div>
  );
}

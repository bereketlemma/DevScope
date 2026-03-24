import type { Anomaly } from '../../types/api';

interface Props {
  anomalies: Anomaly[];
}

const severityStyles = {
  CRITICAL: 'bg-red-100 text-red-800 border-red-300 dark:bg-red-900/30 dark:text-red-300',
  HIGH: 'bg-orange-100 text-orange-800 border-orange-300 dark:bg-orange-900/30 dark:text-orange-300',
  MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-300 dark:bg-yellow-900/30 dark:text-yellow-300',
};

export default function AnomalyTimeline({ anomalies }: Props) {
  if (anomalies.length === 0) {
    return (
      <div className="rounded-lg bg-white dark:bg-gray-800 p-6 text-center text-sm text-gray-400">
        No anomalies detected. Everything looks healthy.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {anomalies.map((a, i) => (
        <div
          key={`${a.metric_date}-${a.metric_name}-${i}`}
          className={`rounded-lg border p-4 ${severityStyles[a.severity]}`}
        >
          <div className="flex items-center justify-between">
            <div>
              <span className="text-xs font-semibold uppercase">{a.severity}</span>
              <span className="ml-2 text-xs opacity-70">{a.anomaly_type.replace(/_/g, ' ')}</span>
            </div>
            <span className="text-xs opacity-60">{a.metric_date}</span>
          </div>
          <p className="mt-1 text-sm">
            <strong>{a.metric_name.replace(/_/g, ' ')}</strong>:{' '}
            {a.metric_value.toFixed(1)} (expected ~{a.expected_value.toFixed(1)})
          </p>
          <p className="mt-0.5 text-xs opacity-60">
            Confidence: {(a.confidence * 100).toFixed(0)}%
            {a.z_score != null && ` · z-score: ${a.z_score}`}
          </p>
        </div>
      ))}
    </div>
  );
}

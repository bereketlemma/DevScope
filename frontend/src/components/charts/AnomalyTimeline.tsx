import { AlertTriangle, AlertCircle, Info } from 'lucide-react';
import clsx from 'clsx';
import type { Anomaly } from '../../types/api';
import { formatDate } from '../../utils/formatters';

interface Props {
  anomalies: Anomaly[];
}

const severityConfig = {
  CRITICAL: {
    bg: 'bg-red-500/[0.08]',
    border: 'border-red-500/20',
    icon: AlertTriangle,
    iconColor: 'text-red-400',
    badge: 'badge-critical',
  },
  HIGH: {
    bg: 'bg-orange-500/[0.08]',
    border: 'border-orange-500/20',
    icon: AlertCircle,
    iconColor: 'text-orange-400',
    badge: 'badge-high',
  },
  MEDIUM: {
    bg: 'bg-yellow-500/[0.08]',
    border: 'border-yellow-500/20',
    icon: Info,
    iconColor: 'text-yellow-400',
    badge: 'badge-medium',
  },
};

export default function AnomalyTimeline({ anomalies }: Props) {
  if (anomalies.length === 0) {
    return (
      <div className="glass-card p-10 text-center">
        <div className="w-12 h-12 rounded-full bg-emerald-500/10 ring-1 ring-emerald-500/20 flex items-center justify-center mx-auto mb-3">
          <svg className="w-6 h-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p className="text-sm font-medium text-gray-300">No anomalies detected</p>
        <p className="text-xs text-gray-500 mt-1">Everything looks healthy. Keep it up!</p>
      </div>
    );
  }

  const sorted = [...anomalies].sort(
    (a, b) => new Date(b.metric_date).getTime() - new Date(a.metric_date).getTime()
  );

  return (
    <div className="space-y-3">
      {sorted.map((a, i) => {
        const cfg = severityConfig[a.severity];
        const Icon = cfg.icon;
        return (
          <div
            key={`${a.metric_date}-${a.metric_name}-${i}`}
            className={clsx(
              'rounded-xl border p-4 transition-all duration-200 hover:scale-[1.01]',
              cfg.bg,
              cfg.border
            )}
          >
            <div className="flex items-start gap-3">
              <div className="mt-0.5">
                <Icon className={clsx('w-4 h-4', cfg.iconColor)} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className={cfg.badge}>{a.severity}</span>
                    <span className="text-xs text-gray-500">
                      {a.anomaly_type.replace(/_/g, ' ')}
                    </span>
                  </div>
                  <span className="text-xs text-gray-500 tabular-nums font-mono">{formatDate(a.metric_date)}</span>
                </div>
                <p className="mt-2 text-sm text-gray-200">
                  <span className="font-semibold text-white">
                    {a.metric_name.replace(/_/g, ' ')}
                  </span>{' '}
                  — actual: <span className="font-mono text-white">{a.metric_value.toFixed(1)}</span>,
                  expected: <span className="font-mono text-gray-400">~{a.expected_value.toFixed(1)}</span>
                </p>
                <div className="mt-1.5 flex items-center gap-3 text-xs text-gray-500">
                  <span>Confidence: <span className="text-gray-300 font-medium">{(a.confidence * 100).toFixed(0)}%</span></span>
                  {a.z_score != null && (
                    <span>z-score: <span className="text-gray-300 font-mono">{a.z_score}</span></span>
                  )}
                </div>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}

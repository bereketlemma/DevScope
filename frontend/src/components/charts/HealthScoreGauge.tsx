import type { HealthScore } from '../../types/api';

interface Props {
  data: HealthScore;
}

function scoreColor(score: number): string {
  if (score >= 80) return '#22c55e';
  if (score >= 60) return '#eab308';
  if (score >= 40) return '#f97316';
  return '#ef4444';
}

export default function HealthScoreGauge({ data }: Props) {
  const { health_score, breakdown } = data;
  const color = scoreColor(health_score);

  // SVG arc for gauge (180 degrees)
  const radius = 70;
  const circumference = Math.PI * radius;
  const progress = (health_score / 100) * circumference;

  return (
    <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Health Score
      </h3>
      <div className="flex items-center gap-6">
        {/* Gauge */}
        <svg width="160" height="100" viewBox="0 0 160 100">
          {/* Background arc */}
          <path
            d="M 10 90 A 70 70 0 0 1 150 90"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="10"
            strokeLinecap="round"
          />
          {/* Progress arc */}
          <path
            d="M 10 90 A 70 70 0 0 1 150 90"
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeLinecap="round"
            strokeDasharray={`${progress} ${circumference}`}
          />
          {/* Score text */}
          <text x="80" y="80" textAnchor="middle" fontSize="28" fontWeight="bold" fill={color}>
            {Math.round(health_score)}
          </text>
          <text x="80" y="96" textAnchor="middle" fontSize="10" fill="#9ca3af">
            / 100
          </text>
        </svg>

        {/* Breakdown */}
        <div className="flex-1 space-y-2 text-xs">
          {Object.entries(breakdown).map(([key, value]) => (
            <div key={key} className="flex justify-between">
              <span className="text-gray-500 dark:text-gray-400">
                {key.replace(/_/g, ' ')}
              </span>
              <span className="font-medium text-gray-700 dark:text-gray-200">
                {Math.round(value)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

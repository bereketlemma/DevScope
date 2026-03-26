import { Heart } from 'lucide-react';
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

function scoreLabel(score: number): string {
  if (score >= 80) return 'Excellent';
  if (score >= 60) return 'Good';
  if (score >= 40) return 'Fair';
  return 'Needs Attention';
}

export default function HealthScoreGauge({ data }: Props) {
  const { health_score, breakdown } = data;
  const color = scoreColor(health_score);
  const label = scoreLabel(health_score);

  // SVG arc for gauge (180 degrees)
  const radius = 70;
  const circumference = Math.PI * radius;
  const progress = (health_score / 100) * circumference;

  return (
    <div className="glass-card p-5 animate-fade-in">
      <div className="flex items-center gap-2 mb-4">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-500/10 ring-1 ring-emerald-500/20">
          <Heart className="w-4 h-4 text-emerald-400" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-white">Health Score</h3>
          <p className="text-[11px] text-gray-500">Overall engineering health</p>
        </div>
      </div>
      <div className="flex flex-col sm:flex-row items-center gap-6">
        {/* Gauge */}
        <div className="relative flex-shrink-0">
          <svg viewBox="0 0 160 100" className="w-40 h-[100px] sm:w-[160px] sm:h-[100px]" aria-label={`Health score: ${Math.round(health_score)} out of 100, ${label}`}>
            {/* Background arc */}
            <path
              d="M 10 90 A 70 70 0 0 1 150 90"
              fill="none"
              stroke="#1e293b"
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
              className="transition-all duration-1000 ease-out"
            />
            {/* Score text */}
            <text x="80" y="75" textAnchor="middle" fontSize="30" fontWeight="bold" fill={color}>
              {Math.round(health_score)}
            </text>
            <text x="80" y="94" textAnchor="middle" fontSize="10" fill="#64748b">
              {label}
            </text>
          </svg>
        </div>

        {/* Breakdown */}
        <div className="flex-1 space-y-3">
          {Object.entries(breakdown).map(([key, value]) => (
            <div key={key}>
              <div className="flex justify-between mb-1">
                <span className="text-xs text-gray-400 capitalize">
                  {key.replace(/_/g, ' ')}
                </span>
                <span className="text-xs font-semibold text-gray-200">
                  {Math.round(value)}
                </span>
              </div>
              <div className="h-1.5 w-full rounded-full bg-surface-800">
                <div
                  className="h-1.5 rounded-full transition-all duration-700 ease-out"
                  style={{
                    width: `${Math.min(value, 100)}%`,
                    backgroundColor: scoreColor(value),
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

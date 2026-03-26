import type { LucideIcon } from 'lucide-react';
import clsx from 'clsx';

interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  trend?: { value: number; label: string };
  color?: 'green' | 'yellow' | 'red' | 'blue';
  icon?: LucideIcon;
}

const colorConfig = {
  green: {
    accent: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
    ring: 'ring-emerald-500/20',
    bar: 'bg-emerald-500',
  },
  yellow: {
    accent: 'text-amber-400',
    bg: 'bg-amber-500/10',
    ring: 'ring-amber-500/20',
    bar: 'bg-amber-500',
  },
  red: {
    accent: 'text-red-400',
    bg: 'bg-red-500/10',
    ring: 'ring-red-500/20',
    bar: 'bg-red-500',
  },
  blue: {
    accent: 'text-brand-400',
    bg: 'bg-brand-500/10',
    ring: 'ring-brand-500/20',
    bar: 'bg-brand-500',
  },
};

export default function MetricCard({ label, value, subtitle, trend, color = 'blue', icon: Icon }: MetricCardProps) {
  const cfg = colorConfig[color];

  return (
    <div className="glass-card p-5 animate-fade-in relative overflow-hidden group">
      {/* Subtle top accent bar */}
      <div className={clsx('absolute top-0 left-0 right-0 h-[2px]', cfg.bar, 'opacity-60')} />

      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">{label}</p>
          <p className="mt-2 text-3xl font-bold text-white tabular-nums">{value}</p>
          {subtitle && <p className="mt-1.5 text-xs text-gray-500">{subtitle}</p>}
          {trend && (
            <div className="mt-2 flex items-center gap-1.5">
              <span
                className={clsx(
                  'text-xs font-semibold',
                  trend.value >= 0 ? 'text-emerald-400' : 'text-red-400'
                )}
              >
                {trend.value >= 0 ? '+' : ''}{trend.value}%
              </span>
              <span className="text-xs text-gray-600">{trend.label}</span>
            </div>
          )}
        </div>
        {Icon && (
          <div className={clsx('flex items-center justify-center w-10 h-10 rounded-lg', cfg.bg, 'ring-1', cfg.ring)}>
            <Icon className={clsx('w-5 h-5', cfg.accent)} />
          </div>
        )}
      </div>
    </div>
  );
}

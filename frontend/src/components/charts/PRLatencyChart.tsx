import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import { Clock } from 'lucide-react';
import type { PRLatencyPoint } from '../../types/api';
import { formatDate } from '../../utils/formatters';

interface Props {
  data: PRLatencyPoint[];
}

export default function PRLatencyChart({ data }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-card p-8 text-center">
        <Clock className="w-6 h-6 text-blue-400/40 mx-auto mb-2" />
        <p className="text-sm text-gray-500">No PR latency data available</p>
      </div>
    );
  }

  return (
    <div className="glass-card p-5 animate-fade-in">
      <div className="flex items-center gap-2 mb-4">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-blue-500/10 ring-1 ring-blue-500/20">
          <Clock className="w-4 h-4 text-blue-400" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-white">PR Merge Latency</h3>
          <p className="text-[11px] text-gray-500">Median & p95 time to merge (hours)</p>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="medianGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#6366f1" stopOpacity={0.2} />
              <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="p95Grad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ef4444" stopOpacity={0.1} />
              <stop offset="100%" stopColor="#ef4444" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey="created_date" tickFormatter={formatDate} tick={{ fontSize: 11, fill: '#64748b' }} axisLine={{ stroke: '#1e293b' }} tickLine={false} />
          <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} unit="h" />
          <Tooltip
            labelFormatter={formatDate}
            formatter={(value: number) => [`${value.toFixed(1)}h`, undefined]}
            contentStyle={{
              backgroundColor: '#1a1f2e',
              border: '1px solid rgba(255,255,255,0.06)',
              borderRadius: '8px',
              fontSize: '12px',
              color: '#e2e8f0',
              boxShadow: '0 10px 30px rgba(0,0,0,0.4)',
            }}
          />
          <Legend wrapperStyle={{ fontSize: '11px', color: '#94a3b8' }} />
          <Area
            type="monotone"
            dataKey="median_hours_to_merge"
            name="Median"
            stroke="#6366f1"
            fill="url(#medianGrad)"
            strokeWidth={2}
          />
          <Area
            type="monotone"
            dataKey="p95_hours_to_merge"
            name="p95"
            stroke="#ef4444"
            fill="url(#p95Grad)"
            strokeWidth={1.5}
            strokeDasharray="4 4"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

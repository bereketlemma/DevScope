import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import { RotateCcw } from 'lucide-react';
import type { ReviewCyclePoint } from '../../types/api';

interface Props {
  data: ReviewCyclePoint[];
}

export default function ReviewCycleChart({ data }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-card p-8 text-center">
        <RotateCcw className="w-6 h-6 text-purple-400/40 mx-auto mb-2" />
        <p className="text-sm text-gray-500">No review cycle data available</p>
      </div>
    );
  }

  return (
    <div className="glass-card p-5 animate-fade-in">
      <div className="flex items-center gap-2 mb-4">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-purple-500/10 ring-1 ring-purple-500/20">
          <RotateCcw className="w-4 h-4 text-purple-400" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-white">Review Cycles</h3>
          <p className="text-[11px] text-gray-500">Rounds vs. time to first review</p>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="hours_to_first_review"
            name="Hours to First Review"
            tick={{ fontSize: 11, fill: '#64748b' }}
            axisLine={{ stroke: '#1e293b' }}
            tickLine={false}
            label={{ value: 'Hours to First Review', position: 'bottom', fontSize: 11, fill: '#475569' }}
          />
          <YAxis
            dataKey="review_rounds"
            name="Review Rounds"
            tick={{ fontSize: 11, fill: '#64748b' }}
            axisLine={false}
            tickLine={false}
            label={{ value: 'Rounds', angle: -90, position: 'insideLeft', fontSize: 11, fill: '#475569' }}
          />
          <Tooltip
            formatter={(value: number, name: string) => {
              if (name === 'Hours to First Review') return [`${value.toFixed(1)}h`, name];
              return [value, name];
            }}
            cursor={{ strokeDasharray: '3 3', stroke: '#475569' }}
            contentStyle={{
              backgroundColor: '#1a1f2e',
              border: '1px solid rgba(255,255,255,0.06)',
              borderRadius: '8px',
              fontSize: '12px',
              color: '#e2e8f0',
              boxShadow: '0 10px 30px rgba(0,0,0,0.4)',
            }}
          />
          <Scatter data={data} fill="#a78bfa" opacity={0.8} />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}

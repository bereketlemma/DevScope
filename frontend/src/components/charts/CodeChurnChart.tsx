import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
} from 'recharts';
import { GitCommitHorizontal } from 'lucide-react';
import type { CodeChurnPoint } from '../../types/api';
import { formatDate } from '../../utils/formatters';

interface Props {
  data: CodeChurnPoint[];
}

export default function CodeChurnChart({ data }: Props) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-card p-8 text-center">
        <GitCommitHorizontal className="w-6 h-6 text-violet-400/40 mx-auto mb-2" />
        <p className="text-sm text-gray-500">No code churn data available</p>
      </div>
    );
  }

  return (
    <div className="glass-card p-5 animate-fade-in">
      <div className="flex items-center gap-2 mb-4">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-violet-500/10 ring-1 ring-violet-500/20">
          <GitCommitHorizontal className="w-4 h-4 text-violet-400" />
        </div>
        <div>
          <h3 className="text-sm font-semibold text-white">Code Churn</h3>
          <p className="text-[11px] text-gray-500">Additions & deletions over time</p>
        </div>
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis dataKey="committed_date" tickFormatter={formatDate} tick={{ fontSize: 11, fill: '#64748b' }} axisLine={{ stroke: '#1e293b' }} tickLine={false} />
          <YAxis tick={{ fontSize: 11, fill: '#64748b' }} axisLine={false} tickLine={false} />
          <Tooltip
            labelFormatter={formatDate}
            formatter={(value: number, name: string) => [`${value.toLocaleString()} lines`, name]}
            contentStyle={{
              backgroundColor: '#1a1f2e',
              border: '1px solid rgba(255,255,255,0.06)',
              borderRadius: '8px',
              fontSize: '12px',
              color: '#e2e8f0',
              boxShadow: '0 10px 30px rgba(0,0,0,0.4)',
            }}
          />
          <Legend wrapperStyle={{ fontSize: '12px', color: '#94a3b8' }} />
          <Bar dataKey="total_additions" name="Additions" fill="#22c55e" radius={[3, 3, 0, 0]} stackId="churn" />
          <Bar dataKey="total_deletions" name="Deletions" fill="#ef4444" radius={[3, 3, 0, 0]} stackId="churn" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import type { PRLatencyPoint } from '../../types/api';

interface Props {
  data: PRLatencyPoint[];
}

export default function PRLatencyChart({ data }: Props) {
  return (
    <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        PR Merge Latency (hours)
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
          <XAxis dataKey="created_date" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Area
            type="monotone"
            dataKey="median_hours_to_merge"
            name="Median"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.15}
            strokeWidth={2}
          />
          <Area
            type="monotone"
            dataKey="p95_hours_to_merge"
            name="p95"
            stroke="#ef4444"
            fill="#ef4444"
            fillOpacity={0.08}
            strokeWidth={1.5}
            strokeDasharray="4 4"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

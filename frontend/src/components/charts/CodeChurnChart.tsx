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
import type { CodeChurnPoint } from '../../types/api';

interface Props {
  data: CodeChurnPoint[];
}

export default function CodeChurnChart({ data }: Props) {
  return (
    <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Code Churn
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
          <XAxis dataKey="committed_date" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip />
          <Legend />
          <Bar dataKey="total_additions" name="Additions" fill="#22c55e" stackId="churn" />
          <Bar dataKey="total_deletions" name="Deletions" fill="#ef4444" stackId="churn" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import type { ReviewCyclePoint } from '../../types/api';

interface Props {
  data: ReviewCyclePoint[];
}

export default function ReviewCycleChart({ data }: Props) {
  return (
    <div className="rounded-lg bg-white dark:bg-gray-800 p-4 shadow-sm">
      <h3 className="mb-3 text-sm font-medium text-gray-700 dark:text-gray-300">
        Review Cycles (rounds vs. time to first review)
      </h3>
      <ResponsiveContainer width="100%" height={280}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
          <XAxis
            dataKey="hours_to_first_review"
            name="Hours to First Review"
            tick={{ fontSize: 11 }}
            label={{ value: 'Hours to First Review', position: 'bottom', fontSize: 11 }}
          />
          <YAxis
            dataKey="review_rounds"
            name="Review Rounds"
            tick={{ fontSize: 11 }}
            label={{ value: 'Rounds', angle: -90, position: 'insideLeft', fontSize: 11 }}
          />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter data={data} fill="#8b5cf6" opacity={0.7} />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}

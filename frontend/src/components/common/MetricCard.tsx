interface MetricCardProps {
  label: string;
  value: string | number;
  subtitle?: string;
  color?: 'green' | 'yellow' | 'red' | 'blue';
}

const colorMap = {
  green: 'border-green-500 bg-green-50 dark:bg-green-900/20',
  yellow: 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20',
  red: 'border-red-500 bg-red-50 dark:bg-red-900/20',
  blue: 'border-brand-500 bg-blue-50 dark:bg-blue-900/20',
};

export default function MetricCard({ label, value, subtitle, color = 'blue' }: MetricCardProps) {
  return (
    <div className={`rounded-lg border-l-4 p-4 ${colorMap[color]}`}>
      <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-gray-900 dark:text-white">{value}</p>
      {subtitle && <p className="mt-1 text-xs text-gray-400">{subtitle}</p>}
    </div>
  );
}

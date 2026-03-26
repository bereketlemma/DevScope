export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center h-64 gap-4">
      <div className="relative">
        <div className="w-10 h-10 rounded-full border-2 border-brand-500/20" />
        <div className="absolute inset-0 w-10 h-10 rounded-full border-2 border-transparent border-t-brand-500 animate-spin" />
      </div>
      <p className="text-sm text-gray-500 animate-pulse">Loading data...</p>
    </div>
  );
}

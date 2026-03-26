import { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useRepos } from '../hooks/useMetrics';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { GitBranch, ArrowRight, Inbox, Search } from 'lucide-react';

export default function Dashboard() {
  const { data: repos, isLoading, error } = useRepos();
  const [search, setSearch] = useState('');

  const filtered = useMemo(
    () =>
      repos?.filter((r) =>
        r.repo_id.toLowerCase().includes(search.toLowerCase())
      ) ?? [],
    [repos, search]
  );

  if (isLoading) return <LoadingSpinner />;
  if (error) {
    return (
      <div className="glass-card p-8 text-center max-w-md mx-auto mt-12">
        <div className="w-12 h-12 rounded-full bg-red-500/10 ring-1 ring-red-500/20 flex items-center justify-center mx-auto mb-4">
          <svg className="w-6 h-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <p className="text-sm font-medium text-white">Failed to load repositories</p>
        <p className="text-xs text-gray-500 mt-1">Check your connection and try again.</p>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Page Header */}
      <div className="page-header">
        <div className="flex flex-wrap items-center gap-2 sm:gap-3 mb-1">
          <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">Dashboard</h1>
          <span className="badge bg-brand-500/15 text-brand-400 ring-1 ring-brand-500/20">
            {repos?.length ?? 0} repos
          </span>
        </div>
        <p className="section-subtitle">Select a repository to explore engineering health metrics.</p>
      </div>

      {/* Search */}
      {repos && repos.length > 0 && (
        <div className="relative mb-5">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search repositories..."
            className="input-field w-full pl-9"
          />
        </div>
      )}

      {/* Repo Grid */}
      <div className="grid gap-3 sm:gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((repo, i) => (
          <Link
            key={repo.repo_id}
            to={`/repo/${encodeURIComponent(repo.repo_id)}`}
            className="glass-card-hover p-5 group block"
            style={{ animationDelay: `${i * 80}ms` }}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-brand-500/10 ring-1 ring-brand-500/20">
                <GitBranch className="w-5 h-5 text-brand-400" />
              </div>
              <ArrowRight className="w-4 h-4 text-gray-600 group-hover:text-brand-400 group-hover:translate-x-0.5 transition-all" />
            </div>
            <h2 className="mt-4 text-sm font-semibold text-white truncate">
              {repo.repo_id}
            </h2>
            <p className="mt-1 text-xs text-gray-500">
              {repo.pr_count.toLocaleString()} pull requests tracked
            </p>
            <div className="mt-3 pt-3 border-t border-white/[0.04]">
              <div className="flex items-center gap-1.5">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse-slow" />
                <span className="text-[11px] text-gray-500">Active</span>
              </div>
            </div>
          </Link>
        ))}

        {filtered.length === 0 && repos && repos.length > 0 && (
          <div className="col-span-full">
            <div className="glass-card p-8 text-center">
              <p className="text-sm text-gray-400">No repositories match "{search}"</p>
            </div>
          </div>
        )}

        {repos?.length === 0 && (
          <div className="col-span-full">
            <div className="glass-card p-12 text-center">
              <div className="w-16 h-16 rounded-2xl bg-brand-500/10 ring-1 ring-brand-500/20 flex items-center justify-center mx-auto mb-4">
                <Inbox className="w-8 h-8 text-brand-400" />
              </div>
              <h3 className="text-base font-semibold text-white">No repositories yet</h3>
              <p className="mt-2 text-sm text-gray-400 max-w-sm mx-auto">
                Trigger an ingestion pipeline to start tracking your engineering metrics.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

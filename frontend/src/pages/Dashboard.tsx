import { Link } from 'react-router-dom';
import { useRepos } from '../hooks/useMetrics';
import LoadingSpinner from '../components/common/LoadingSpinner';

export default function Dashboard() {
  const { data: repos, isLoading, error } = useRepos();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <p className="text-red-500">Failed to load repositories.</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
      <p className="mt-1 text-sm text-gray-500">Select a repository to view engineering metrics.</p>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {repos?.map((repo) => (
          <Link
            key={repo.repo_id}
            to={`/repo/${encodeURIComponent(repo.repo_id)}`}
            className="block rounded-lg bg-white dark:bg-gray-800 p-5 shadow-sm border border-gray-200 dark:border-gray-700 hover:border-brand-500 transition-colors"
          >
            <h2 className="text-base font-semibold text-gray-900 dark:text-white">
              {repo.repo_id}
            </h2>
            <p className="mt-1 text-sm text-gray-500">{repo.pr_count} pull requests tracked</p>
          </Link>
        ))}

        {repos?.length === 0 && (
          <div className="col-span-full text-center text-sm text-gray-400 py-12">
            No repositories ingested yet. Trigger an ingestion to get started.
          </div>
        )}
      </div>
    </div>
  );
}

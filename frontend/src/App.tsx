import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import DashboardLayout from './components/layout/DashboardLayout';
import LoadingSpinner from './components/common/LoadingSpinner';
import ErrorBoundary from './components/common/ErrorBoundary';
import { Home } from 'lucide-react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const RepoDetail = lazy(() => import('./pages/RepoDetail'));
const Anomalies = lazy(() => import('./pages/Anomalies'));

function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-20 animate-fade-in">
      <p className="text-6xl font-bold text-gray-700">404</p>
      <p className="mt-3 text-sm text-gray-400">Page not found</p>
      <Link
        to="/"
        className="mt-6 inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-600/20 text-brand-400 text-sm font-medium hover:bg-brand-600/30 transition-colors"
      >
        <Home className="w-4 h-4" />
        Back to Dashboard
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <BrowserRouter>
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            <Route element={<DashboardLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/repo/:repoId" element={<RepoDetail />} />
              <Route path="/anomalies" element={<Anomalies />} />
              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </Suspense>
      </BrowserRouter>
    </ErrorBoundary>
  );
}

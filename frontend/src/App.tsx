import { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import DashboardLayout from './components/layout/DashboardLayout';
import LoadingSpinner from './components/common/LoadingSpinner';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const RepoDetail = lazy(() => import('./pages/RepoDetail'));
const Anomalies = lazy(() => import('./pages/Anomalies'));

export default function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route element={<DashboardLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="/repo/:repoId" element={<RepoDetail />} />
            <Route path="/anomalies" element={<Anomalies />} />
          </Route>
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}

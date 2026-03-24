import { useQuery } from '@tanstack/react-query';
import {
  fetchRepos,
  fetchPRLatency,
  fetchCodeChurn,
  fetchReviewCycles,
  fetchHealthScore,
  fetchAnomalies,
} from '../api/metrics';

export function useRepos() {
  return useQuery({ queryKey: ['repos'], queryFn: fetchRepos });
}

export function usePRLatency(repoId: string, days = 30) {
  return useQuery({
    queryKey: ['pr-latency', repoId, days],
    queryFn: () => fetchPRLatency(repoId, days),
    enabled: !!repoId,
  });
}

export function useCodeChurn(repoId: string, days = 30) {
  return useQuery({
    queryKey: ['code-churn', repoId, days],
    queryFn: () => fetchCodeChurn(repoId, days),
    enabled: !!repoId,
  });
}

export function useReviewCycles(repoId: string, days = 30) {
  return useQuery({
    queryKey: ['review-cycles', repoId, days],
    queryFn: () => fetchReviewCycles(repoId, days),
    enabled: !!repoId,
  });
}

export function useHealthScore(repoId: string, days = 30) {
  return useQuery({
    queryKey: ['health-score', repoId, days],
    queryFn: () => fetchHealthScore(repoId, days),
    enabled: !!repoId,
  });
}

export function useAnomalies(repoId: string, days = 30, severity?: string) {
  return useQuery({
    queryKey: ['anomalies', repoId, days, severity],
    queryFn: () => fetchAnomalies(repoId, days, severity),
    enabled: !!repoId,
  });
}

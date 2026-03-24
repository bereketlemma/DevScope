import client from './client';
import type {
  ApiResponse,
  RepoSummary,
  PRLatencyPoint,
  CodeChurnPoint,
  ReviewCyclePoint,
  HealthScore,
  Anomaly,
} from '../types/api';

export async function fetchRepos(): Promise<RepoSummary[]> {
  const { data } = await client.get<ApiResponse<RepoSummary[]>>('/metrics/repos');
  return data.data;
}

export async function fetchPRLatency(repoId: string, days = 30): Promise<PRLatencyPoint[]> {
  const { data } = await client.get<ApiResponse<PRLatencyPoint[]>>(
    `/metrics/${repoId}/pr-latency`,
    { params: { days } }
  );
  return data.data;
}

export async function fetchCodeChurn(repoId: string, days = 30): Promise<CodeChurnPoint[]> {
  const { data } = await client.get<ApiResponse<CodeChurnPoint[]>>(
    `/metrics/${repoId}/code-churn`,
    { params: { days } }
  );
  return data.data;
}

export async function fetchReviewCycles(repoId: string, days = 30): Promise<ReviewCyclePoint[]> {
  const { data } = await client.get<ApiResponse<ReviewCyclePoint[]>>(
    `/metrics/${repoId}/review-cycles`,
    { params: { days } }
  );
  return data.data;
}

export async function fetchHealthScore(repoId: string, days = 30): Promise<HealthScore> {
  const { data } = await client.get<ApiResponse<HealthScore>>(
    `/metrics/${repoId}/health`,
    { params: { days } }
  );
  return data.data;
}

export async function fetchAnomalies(
  repoId: string,
  days = 30,
  severity?: string
): Promise<Anomaly[]> {
  const { data } = await client.get<ApiResponse<Anomaly[]>>(
    `/anomalies/${repoId}`,
    { params: { days, severity } }
  );
  return data.data;
}

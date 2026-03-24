/** API response envelope */
export interface ApiResponse<T> {
  data: T;
  meta?: {
    repo_id?: string;
    window_days?: number;
    total?: number;
    detection_method?: string;
  };
}

/** Repository summary from BigQuery */
export interface RepoSummary {
  repo_id: string;
  pr_count: number;
}

/** PR latency data point */
export interface PRLatencyPoint {
  created_date: string;
  median_hours_to_merge: number | null;
  p95_hours_to_merge: number | null;
  pr_count: number;
}

/** Code churn data point */
export interface CodeChurnPoint {
  committed_date: string;
  total_additions: number;
  total_deletions: number;
  net_churn: number;
  commit_count: number;
}

/** Review cycle data point */
export interface ReviewCyclePoint {
  created_date: string;
  number: number;
  review_rounds: number;
  first_review_at: string | null;
  hours_to_first_review: number | null;
}

/** Health score response */
export interface HealthScore {
  health_score: number;
  breakdown: {
    pr_latency: number;
    code_churn_stability: number;
    review_coverage: number;
    deployment_frequency: number;
  };
  repo_id: string;
  window_days: number;
}

/** Anomaly record */
export interface Anomaly {
  repo_id: string;
  metric_date: string;
  metric_name: string;
  metric_value: number;
  expected_value: number;
  confidence: number;
  severity: 'MEDIUM' | 'HIGH' | 'CRITICAL';
  anomaly_type: string;
  z_score?: number;
}

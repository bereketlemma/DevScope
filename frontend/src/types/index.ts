export interface User {
  id: number
  github_id: number
  username: string
  email: string
  avatar_url: string
  created_at: string
  updated_at: string
}

export interface Repository {
  id: number
  github_id: number
  owner: string
  name: string
  full_name: string
  url: string
  description?: string
  stars: number
  watchers: number
  forks: number
  language?: string
  is_fork: boolean
  created_at: string
  updated_at: string
  last_synced_at?: string
}

export interface Metric {
  repository_id: number
  pr_latency_days?: number
  pr_review_time_hours?: number
  commit_frequency_daily?: number
  pr_acceptance_rate?: number
}

export interface DailyMetric {
  date: string
  metric_name: string
  value: number
  avg_value: number
  median_value: number
  p95_value: number
}

export interface Anomaly {
  id: number
  repository_id: number
  metric_name: string
  detected_value: number
  z_score: number
  threshold: number
  description?: string
  created_at: string
}

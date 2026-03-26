# DevScope — Version Roadmap

## v1.0 — Core Platform (Current)

**Status: Complete and deployed**

### What's built
- **Ingestion service** — GitHub REST API client with rate-limit handling, pagination, webhook receiver with HMAC signature verification. Deployed on Cloud Run.
- **Event streaming** — Cloud Pub/Sub with dead-letter queue for fault-tolerant message delivery between ingestion and processing layers.
- **Stream processing** — Apache Beam pipeline (Dataflow) transforms raw GitHub events, routes by type (PR/commit/review), validates schemas, and writes to BigQuery.
- **Analytics store** — BigQuery with 4 partitioned and clustered tables: `pull_requests`, `commits`, `reviews`, `daily_metrics`. Sub-second query performance.
- **Anomaly detection** — Vertex AI Isolation Forest model trained on engineered time-series features (lags, rolling stats, z-scores, trends). Z-score statistical fallback with severity classification (MEDIUM >2σ, HIGH >3σ, CRITICAL >4σ).
- **API service** — FastAPI on Cloud Run. Parameterized BigQuery queries, health score computation, anomaly detection endpoint.
- **Dashboard** — React 18 / TypeScript (strict) with dark theme, glassmorphism design, Recharts visualizations. Multi-repo support, time-range selector, search/filter, mobile responsive.
- **CI/CD** — GitHub Actions (lint, test, type-check). Manual deploy via Cloud Build + Cloud Run.
- **Testing** — 17 unit tests passing across API, ingestion, and ML modules.

### Metrics tracked
- PR merge latency (median + p95)
- Code churn (additions, deletions, net)
- Review cycles (rounds per PR, time to first review)
- Deployment frequency (merges/day)
- Health score (weighted composite 0–100)

### Tech stack
| Layer | Technology |
|---|---|
| Ingestion | Python 3.11+, GitHub REST API, httpx |
| Streaming | Google Cloud Pub/Sub |
| Processing | Apache Beam → Cloud Dataflow |
| Storage | Google BigQuery (partitioned + clustered) |
| ML | Vertex AI, scikit-learn (Isolation Forest) |
| API | FastAPI, Cloud Run |
| Frontend | React 18, TypeScript, Vite, Tailwind, Recharts |
| Deployment | Docker, Cloud Build, Cloud Run, GitHub Actions |

### Live URLs
| Service | URL |
|---|---|
| Dashboard | https://devscope-frontend-965448962417.us-central1.run.app |
| API Docs | https://devscope-api-965448962417.us-central1.run.app/docs |
| Ingestion | https://devscope-ingestion-965448962417.us-central1.run.app |

---

## v2.0 — Authentication, Teams, and Advanced Analytics (Planned)

### Authentication and authorization
- GitHub OAuth2 login flow (register OAuth app, handle callback)
- JWT access tokens (15-min expiry) + refresh tokens (7-day)
- Role-based access control: Owner, Admin, Viewer
- Protected routes — redirect unauthenticated users to login
- Token refresh with auto-renewal before expiry
- User profiles with avatar, connected repos, preferences

### Team and organization support
- Organization-level dashboards aggregating all repos
- Team management — invite members, assign roles
- Per-developer breakdowns within repos
- Developer comparison view (velocity, review load, churn)
- Team health score (aggregate of individual repo scores)

### Advanced metrics
- **DORA metrics** — deployment frequency, lead time for changes, change failure rate, mean time to recovery
- **Bus factor** — knowledge concentration per file/directory
- **Review load balance** — distribution of review assignments across team
- **Rework ratio** — percentage of changes that revert or fix recent commits
- **Cycle time** — end-to-end time from first commit to production deploy
- **Sprint velocity** — story points or PR throughput per sprint

### Enhanced anomaly detection
- Deploy Vertex AI endpoint for real-time online prediction
- Multi-metric correlation (detect when latency + churn spike together)
- Anomaly acknowledgment and resolution workflow
- Slack/email notifications for CRITICAL anomalies
- Custom threshold configuration per repo
- Scheduled retraining pipeline (weekly)

### Dashboard enhancements
- Developer detail page — individual contributor metrics
- Comparison mode — side-by-side repo or developer comparison
- Custom date ranges with calendar picker
- Export charts as PNG/PDF
- Dashboard embedding (iframe for team wikis)
- Real-time updates via WebSocket

### Infrastructure upgrades
- Automated CD pipeline via GitHub Actions + Cloud Build
- Staging environment (separate Cloud Run services)
- Infrastructure as Code (Terraform for GCP resources)
- Cloud Dataflow execution with autoscaling
- Cost monitoring dashboard
- API rate limiting and usage tracking

---

## v3.0 — Enterprise Features (Future)

### Multi-tenant architecture
- Separate data isolation per organization
- Custom domains per tenant
- SSO integration (SAML, OIDC)

### Integrations
- Jira/Linear integration (link PRs to tickets)
- Slack bot for anomaly alerts and daily summaries
- GitHub App (instead of personal access tokens)
- PagerDuty integration for CRITICAL alerts

### Advanced ML
- Forecasting — predict merge latency and churn trends
- Recommendation engine — suggest optimal reviewers
- Natural language summaries of weekly engineering health
- Custom model training per organization

### Compliance and audit
- Audit log of all user actions
- Data retention policies
- GDPR data export/deletion
- SOC 2 compliance controls

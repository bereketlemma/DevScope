# Architecture Decision Records

## ADR-001: Use PostgreSQL + BigQuery Split

**Status:** Accepted

**Context:**  
Need to separate operational data (user sessions, sync jobs) from analytical data (PR events, metrics).

**Decision:**  
- PostgreSQL for application state (OLTP)
- BigQuery for analytics (OLAP)

**Consequences:**  
✅ Optimized query patterns  
✅ BigQuery scales for analytics  
⚠️ Need to sync data consistently

---

## ADR-002: Async FastAPI with SQLAlchemy 2.0

**Status:** Accepted

**Context:**  
Need high concurrency for API + background jobs.

**Decision:**  
- FastAPI with async/await
- SQLAlchemy 2.0 with asyncpg driver
- Connection pooling

**Consequences:**  
✅ Better resource utilization  
✅ Handles concurrent syncs  
⚠️ Debugging async code is harder

---

## ADR-003: Celery for Background Jobs

**Status:** Accepted

**Context:**  
GitHub syncs can be long-running and need retry logic.

**Decision:**  
Use Celery with Redis broker for async tasks.

**Consequences:**  
✅ Decoupled sync from API  
✅ Built-in retries and monitoring  
⚠️ Need Redis instance

---

## ADR-004: Z-Score for Anomaly Detection

**Status:** Accepted

**Context:**  
Need simple but effective anomaly detection without ML.

**Decision:**  
Calculate mean/std dev over 30-day window, flag if $ |z| > 3 $.

**Consequences:**  
✅ Simple to understand and implement  
✅ Baseline for future ML models  
⚠️ May miss subtle patterns

---

## ADR-005: JWT for Stateless Auth

**Status:** Accepted

**Context:**  
Need lightweight auth without session management.

**Decision:**  
GitHub OAuth2 → JWT (HS256) stored in localStorage.

**Consequences:**  
✅ Stateless API  
✅ Works with frontend  
⚠️ Token revocation requires blacklist

---

## ADR-006: React 18 + TypeScript Strict

**Status:** Accepted

**Context:**  
Need type-safe frontend with modern best practices.

**Decision:**  
React 18, TypeScript strict mode, Vite, Tailwind CSS.

**Consequences:**  
✅ Catch errors at dev time  
✅ Excellent DX with Vite  
⚠️ Stricter compilation

---

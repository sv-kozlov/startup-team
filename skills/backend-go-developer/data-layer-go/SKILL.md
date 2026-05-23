---
name: data-layer-go
description: Use when designing or changing the data access layer of a Go service — SQL/NoSQL choice, transactions, indices, query plans, forward-compatible migrations, repository shape, connection pool sizing.
family: code
profile_level: Senior+
---

# Data Layer — Go

## Purpose

Make the data layer correct under concurrency, fast under expected load, and safe to migrate without downtime. Treat schema changes as code: reviewed, reversible, deployed independently of application releases.

## Use When

- Designing the storage of a new aggregate or read model.
- Adding indices, partitioning, or changing query shape under load.
- Writing migrations or reviewing migration safety.
- Investigating slow queries or lock contention.
- Choosing between SQL, document store, key-value, and search engine.

## Do Not Use When

- The discussion is event production after a state change → `event-driven-integration`.
- The discussion is the database cluster operation (HA, backups) → handoff to `devops-sre`.
- The discussion is analytical store / warehouse design → handoff to `data-engineer`.

## Inputs

- Access patterns: read/write ratio, query shapes, latency budget.
- Consistency requirements per operation.
- Existing storage and its current pain points (slow queries, lock waits, migration outages).
- Volume and growth projection.

## Workflow

1. State access patterns before storage choice. SQL by default for transactional data. Document/KV/search only with a named reason.
2. Define the repository shape: small, intention-revealing methods (`GetByID`, `ListByUser`, `Save`), not generic CRUD reflectors.
3. Open transactions at the use-case boundary, not in the repository. The service decides "this is one unit of work".
4. Use parameterized queries always. No string concatenation in SQL.
5. Read the query plan (`EXPLAIN ANALYZE`) for any non-trivial query before merging. Indices are a deliberate decision.
6. Bound connection pools by upstream pressure. The pool plus replicas plus PgBouncer plus app instances is one sizing problem.
7. Migrations are forward-compatible: expand → migrate data → contract. Never drop a column the running app reads.
8. Every migration is reversible or has a documented one-way rationale.
9. Soft-delete only when audit/compliance requires it. Otherwise hard-delete and let the event log carry history.
10. Capture slow queries (`pg_stat_statements`, slow log) and review weekly.

## Outputs

- Schema with named indices and a migration history.
- Repository code with explicit transaction boundaries.
- Query plans archived for hot paths.
- Connection pool sizing note tied to load.
- Migration runbook: expand/migrate/contract steps with rollback.

## Named Patterns

### Good — Transaction at use-case boundary
```go
// service layer
func (s *OrderService) Place(ctx context.Context, in PlaceInput) error {
    return s.tx.WithTx(ctx, func(ctx context.Context) error {
        if err := s.orders.Save(ctx, in.Order); err != nil { return err }
        if err := s.outbox.Insert(ctx, in.Event); err != nil { return err }
        return nil
    })
}
```
The repository methods are transaction-aware via context; the service owns the boundary.

### Bad — Transactions inside the repository
```go
func (r *Repo) Save(ctx context.Context, o Order) error {
    tx, _ := r.db.BeginTx(ctx, nil)
    // ... 200 lines ...
    return tx.Commit()
}
```
Composability lost. Two repository calls become two transactions. Outbox publish escapes the unit of work.

### Good — Expand → migrate → contract migration
1. Migration A: add `currency` column nullable, deploy.
2. Backfill data in batches with rate control.
3. Migration B: add NOT NULL constraint, deploy.
4. Migration C: drop the old column once no app reads it.
Each step is a separate deploy; rollback at any step is safe.

### Bad — Single migration with destructive change
One migration renames a column and the same release reads the new name. A rollback brings the old code back; the old code reads the renamed column and crashes.

### Good — Indices from query plan
```sql
EXPLAIN ANALYZE SELECT * FROM orders
WHERE user_id = $1 AND created_at > $2
ORDER BY created_at DESC LIMIT 50;
-- → Seq Scan: bad
CREATE INDEX CONCURRENTLY orders_user_created_idx
    ON orders (user_id, created_at DESC);
-- → Index Scan: good
```
The index name reflects the columns; created concurrently to avoid table lock.

### Bad — "Indices fix everything"
Every column gets an index. Write throughput drops. Storage doubles. The plan still uses sequential scan for the actual query.

### Good — N+1 detection and fix
```go
// Before:
for _, id := range ids {
    o, _ := repo.GetByID(ctx, id) // N round trips
    ...
}
// After:
os, _ := repo.GetByIDs(ctx, ids) // 1 round trip
```
Batch reads when the access pattern is "many by IDs".

### Bad — Loop of `GetByID`
Tests pass on 5 items; production at 5,000 takes 10 seconds.

### Good — Pool sized to upstream
```
maxOpenConns = min(replicaCapacity / appInstances, expectedConcurrency × safetyFactor)
```
Documented in code with the calculation. Adjusted when topology changes.

### Bad — `MaxOpenConns = 1000`
"To be safe". Pool exhaustion moves from app to database; database OOMs.

### Good — Parameterized query
```go
const q = `SELECT id, total FROM orders WHERE user_id = $1`
rows, err := db.QueryContext(ctx, q, userID)
```

### Bad — String-built SQL
```go
q := fmt.Sprintf("SELECT * FROM orders WHERE user_id = '%s'", userID)
```
SQL injection. Plan cache misses.

### Good — Cursor-based scan for backfills
```go
// process in pages of 1000, cursor on (id) primary key
for {
    rows, _ := db.QueryContext(ctx, q, lastID, 1000)
    // ... apply ...
    if pageSize < 1000 { break }
}
```

### Bad — `SELECT * FROM big_table` in code
Memory blows up; replication lag spikes; cluster paged.

## Boundaries

- Owns the service's data access code and migration content.
- Does not own DB cluster, HA, backups, restore drill → `devops-sre`.
- Does not own warehouse / lake design for the same data → `data-engineer`.
- Does not own cross-service data ownership across bounded contexts → `system-architect`.

## Sources

### Priority 1 — Engine and protocol canon
- PostgreSQL documentation — https://www.postgresql.org/docs/
- `database/sql` package — https://pkg.go.dev/database/sql
- `pgx` — https://github.com/jackc/pgx
- MongoDB documentation — https://www.mongodb.com/docs/
- Redis documentation — https://redis.io/docs/

### Priority 2 — Design orientation
- Use The Index, Luke — https://use-the-index-luke.com/
- Martin Kleppmann: Designing Data-Intensive Applications — book reference.
- PostgreSQL Wiki: Don't Do This — https://wiki.postgresql.org/wiki/Don%27t_Do_This

### Priority 3 — Background
- Brandur Leach: postgres-for-the-wire engineering blog posts — https://brandur.org/
- The PG Mate blog (Citus, Crunchy Data) — https://www.crunchydata.com/blog

## Handoff

- Cluster operation, replication, backups → `devops-sre`.
- Warehouse/lake schema for the same data → `data-engineer`.
- Cross-service data ownership and bounded context fit → `system-architect`.
- Outbox/event production after data changes → `event-driven-integration`.

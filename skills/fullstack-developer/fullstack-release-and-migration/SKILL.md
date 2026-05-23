---
name: fullstack-release-and-migration
description: Use when releasing a web feature that requires a database schema change, a coordinated frontend + backend deploy, a feature flag rollout, or a safe rollback plan. Covers expand/migrate/contract migration pattern, feature flags, blue-green and rolling deploy coordination, and the sequence that lets both stacks ship without downtime.
family: method
profile_level: Senior+
---

# Fullstack Release and Migration

## Purpose

Ship a fullstack feature so the database schema and the application code on both ends can be deployed in safe, reversible steps. Prevent the class of incidents where a deploy is rolled back but the schema change cannot be.

## Use When

- Releasing a feature that adds, renames, or removes a database column or table.
- Coordinating a deploy where the frontend and backend must be backward compatible during the rollout window.
- Introducing a feature flag to decouple code delivery from feature activation.
- Planning a rollback: if deploy fails, what is the recovery path?
- Deciding the deploy sequence for a schema-heavy feature.

## Do Not Use When

- The task is designing the data schema → `fullstack-data-flow`.
- The task is the CI/CD pipeline setup → handoff to `devops-sre`.
- The task is the observability of the deploy → `fullstack-observability`.
- The task is infrastructure-level blue-green setup → handoff to `devops-sre`.

## Inputs

- Feature design output: API contract, data schema change, UI state map.
- Current DB schema and any constraints that block the migration.
- Deploy environment: can frontend and backend deploy independently? Are there rolling restarts?
- Rollback requirements: how long does the old code need to run alongside the new schema?

## Workflow

1. **Classify the schema change.** Additive (add nullable column / new table) = safe to deploy first. Destructive (drop column, rename, change type) = requires expand/migrate/contract.
2. **Plan the expand/migrate/contract sequence for destructive changes:**
   - **Expand**: add new column/table with no constraints that break old code. Deploy the new schema. Old code still works.
   - **Migrate**: deploy code that writes to both old and new columns. Backfill existing rows in the background.
   - **Contract**: once all data is migrated and no old code reads the old column, deploy the removal. Add constraints.
3. **Decide the feature flag approach.** If the feature must ship before activation: wrap the new UI path and the new endpoint behind a flag. The flag is evaluated at runtime, not at compile time.
4. **Define the deploy sequence:**
   - Backend schema migration first (expand step).
   - Backend code deploy (writes new column, reads old+new).
   - Frontend deploy (new UI, calls new endpoint, behind flag).
   - Flag enablement: 1% → 10% → 50% → 100%.
   - Cleanup: remove flag, deploy the contract step, remove old column.
5. **Write the rollback plan.** For each deploy step: how do you revert? What is the state of the database if you roll back step N?
6. **Verify backward compatibility at the API level.** During the rollout window, old frontend + new backend and new frontend + old backend both work. Test with MSW handlers for the old and new contract shapes.

## Outputs

- Migration plan: expand/migrate/contract steps with SQL snippets.
- Deploy sequence document with dependency arrows between steps.
- Feature flag wrapper in the codebase.
- Rollback plan per deploy step.
- Backfill script with batch size and throttle settings.
- API backward compatibility checklist.

## Named Patterns

### Good — Expand/migrate/contract in three deploys
```sql
-- Deploy 1 (expand): add nullable column, old code unaffected
ALTER TABLE orders ADD COLUMN currency_code VARCHAR(3);

-- Deploy 2: code writes to both old (amount) and new (currency_code)
-- Backfill (background job, batched):
UPDATE orders SET currency_code = 'RUB' WHERE currency_code IS NULL LIMIT 5000;

-- Deploy 3 (contract): all rows have currency_code, remove old column
ALTER TABLE orders DROP COLUMN legacy_currency;
```
Each step is independently reversible. No deploy exposes incomplete data.

### Bad — Destructive migration in one deploy
```sql
ALTER TABLE orders
  DROP COLUMN amount,
  ADD COLUMN amount_cents INTEGER NOT NULL DEFAULT 0;
-- Rollback: impossible. The column is gone and old code cannot restart.
```

### Good — Feature flag at the UI and API boundary
```typescript
// Backend: expose new endpoint only when flag is active
router.get('/v1/orders/v2/:id', (req, res) => {
  if (!flags.isEnabled('order-v2', req.user.id)) {
    return res.status(404).json({ code: 'NOT_FOUND' });
  }
  return orderControllerV2.getById(req, res);
});

// Frontend: same flag controls which component renders
const OrderDetail = ({ id }: { id: string }) => {
  const isV2 = useFlag('order-v2');
  return isV2 ? <OrderDetailV2 id={id} /> : <OrderDetailV1 id={id} />;
};
```
Feature is in production before it is visible to users. Rollback = flip the flag.

### Bad — Feature behind a deploy flag
```
// "Feature flag" = comment out the new route in code
// Deploy = uncomment + redeploy
// Rollback = git revert + redeploy
// Zero-downtime deploy window: none
```

### Good — Backward-compatible API during rolling deploy
```typescript
// New backend: responds to both old and new request shapes
const createOrder = (body: CreateOrderV1 | CreateOrderV2) => {
  const items = 'lineItems' in body ? body.lineItems : body.items; // v1 uses items, v2 uses lineItems
  return orderService.create(items);
};
```
During the rolling deploy window, old frontend (using `items`) and new frontend (using `lineItems`) both work. No coordination is required between frontend and backend deploy timing.

### Bad — New contract breaks old clients
```typescript
// Backend deploys, expects lineItems only. Old frontend sends items.
// 400 Bad Request for all users until frontend deploy completes.
```

### Good — Batched backfill with throttle
```typescript
// Background job: migrate in small batches to avoid locking the table
const backfillCurrencyCode = async () => {
  let processed = 0;
  while (true) {
    const rows = await db('orders')
      .whereNull('currency_code')
      .limit(1000)
      .update({ currency_code: 'RUB' });
    processed += rows;
    if (rows === 0) break;
    await sleep(200); // 200ms pause between batches
  }
  logger.info('backfill complete', { processed });
};
```
No table lock. The migration runs in the background while production traffic continues.

### Bad — Full-table update in a migration file
```sql
-- Migration file, runs in a transaction:
UPDATE orders SET currency_code = 'RUB'; -- 10M rows, locks the table for 5 minutes
```

## Boundaries

- Owns the release sequence, migration strategy, and feature flag decisions for a feature.
- Does not own CI/CD pipeline configuration and infrastructure → `devops-sre`.
- Does not own the data schema design → `fullstack-data-flow`.
- Does not own organization-wide feature flag platform → `tech-lead` / `devops-sre`.
- Does not own the deploy orchestration (Kubernetes rolling update, canary routing) → `devops-sre`.

## Sources

### Priority 1 — Migration and safety canon
- PostgreSQL Documentation — https://www.postgresql.org/docs/
- OpenAPI Specification 3.1 (backward compatibility rules) — https://spec.openapis.org/oas/v3.1.0

### Priority 2 — Deployment patterns
- martinfowler.com on feature toggles — https://martinfowler.com/articles/feature-toggles.html
- martinfowler.com on expand/contract — https://martinfowler.com/bliki/ParallelChange.html
- The Twelve-Factor App — https://12factor.net/
- Google SRE Book — https://sre.google/sre-book/table-of-contents/

### Priority 3 — Pattern orientation
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar
- microservices.io patterns — https://microservices.io/patterns/

## Handoff

- CI/CD pipeline, infrastructure-level blue-green/canary → `devops-sre`.
- Data schema design → `fullstack-data-flow`.
- Feature flag platform choice and configuration management → `tech-lead` / `devops-sre`.
- API contract evolution policy → `api-contract-design`.
- QA regression plan for the release → `qa-engineer`.

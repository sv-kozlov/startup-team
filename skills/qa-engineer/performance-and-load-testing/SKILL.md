---
name: performance-and-load-testing
description: Use when designing or executing a load test, validating NFR targets (latency, throughput, error rate), analyzing percentile results, or localizing performance bottlenecks across service layers. Does not own infrastructure provisioning or architecture decisions.
family: method
profile_level: Senior+
---

# Performance and Load Testing

## Purpose

Validate that the system meets its non-functional requirements under expected and peak load, before that load
is seen in production. Produce reproducible evidence that NFR targets (latency p95/p99, throughput RPS,
error rate) are met or identify where they are not and which layer is the bottleneck.

## Use When

- A new service or feature is expected to serve significant load.
- NFR targets (latency, throughput, error rate) are defined and need verification.
- A performance regression is suspected after a code or infrastructure change.
- Capacity planning evidence is needed before a traffic migration or launch.
- Investigating slow response times reported by monitoring or users.

## Do Not Use When

- Functional correctness is the goal -> use `test-design-and-coverage` or `api-testing`.
- Infrastructure provisioning for the performance environment is needed -> `devops-sre`.
- Performance bottleneck is in the database cluster configuration -> `devops-sre` or the relevant developer.
- Security load testing (DDoS simulation) -> `security-engineer`.

## Inputs

- NFR targets: p50/p95/p99 latency budgets, target throughput (RPS), acceptable error rate.
- Traffic model: expected concurrent users, ramp-up time, peak duration, off-peak baseline.
- System architecture: entry points, service dependencies, caches, databases.
- Performance environment spec: hardware, scaling settings, data volume.
- Baseline measurements from previous runs (if available).

## Workflow

1. Define the performance test objective. One of: baseline measurement, NFR validation, regression check,
   or capacity ceiling discovery. The objective determines the load shape and success criteria.

2. Define load shapes:
   - Ramp-up (load test): gradually increase users to target level; observe where degradation starts.
   - Steady-state (soak test): hold target load for an extended period (30-60 min); detect memory leaks,
     connection pool exhaustion, and degradation over time.
   - Spike test: sudden peak well above expected load; observe recovery time.
   - Stress test: increase beyond capacity ceiling to find the breaking point.

3. Identify the critical user journeys to load-test. Do not load-test everything: focus on the
   paths with the highest expected volume and the strictest latency requirements.

4. Write the load test scripts. Use tool-appropriate virtual user (VU) scripts:
   ```
   # k6 structural pattern (JavaScript DSL)
   import http from 'k6/http';
   import { check, sleep } from 'k6';

   export const options = {
     stages: [
       { duration: '2m', target: 100 },   // ramp up
       { duration: '5m', target: 100 },   // hold
       { duration: '1m', target: 0 },     // ramp down
     ],
     thresholds: {
       http_req_duration: ['p95<300'],    // NFR: p95 < 300ms
       http_req_failed: ['rate<0.01'],   // error rate < 1%
     },
   };

   export default function () {
     const res = http.post('https://api.example.com/orders', JSON.stringify(payload), params);
     check(res, { 'status 201': (r) => r.status === 201 });
     sleep(1);
   }
   ```

5. Prepare test data proportionate to load. Pre-seeded data must reflect production data volume.
   Generating data inside the load test loop creates artificial slowness unrelated to the product.

6. Run the test in the performance environment. Monitor in parallel: CPU, memory, DB connections,
   network I/O, GC pause times, external service call latencies. Correlate tool-reported latency
   with server-side metrics.

7. Analyze results using percentiles, not averages. p95 and p99 reveal tail latency that the
   average hides. Plot over time: a rising p99 during a soak test indicates resource leak.

8. Localize bottlenecks. If NFRs are not met, determine the layer:
   - Application: CPU-bound code, inefficient queries, unoptimized serialization.
   - Database: slow queries, connection pool exhaustion, lock contention.
   - Network: external API latency, DNS resolution.
   - Infrastructure: under-provisioned memory, disk I/O saturation.
   Report the bottleneck with evidence (metrics, query plans, logs), not a hypothesis.

## Outputs

- Performance test plan: objectives, load shapes, NFR targets, environment spec.
- Load test scripts (k6, JMeter, or equivalent).
- Performance test report: p50/p95/p99 results, throughput, error rate, comparison to NFR.
- Bottleneck localization notes with supporting evidence.
- Pass/fail verdict against NFR targets.
- Recommendations for optimization or capacity increase (if NFRs not met).

## Named Patterns

### Good — NFR-linked thresholds in the test script

```javascript
// k6 thresholds linked to the NFR document
export const options = {
  thresholds: {
    http_req_duration: ['p95<300', 'p99<500'],  // from NFR-PERF-01
    http_req_failed: ['rate<0.01'],              // from NFR-PERF-02
  },
};
```

The test fails automatically if NFRs are not met. No manual result interpretation.

### Bad — Load test without thresholds

The test runs, produces charts, and a human decides if it "looks OK." Different team members
interpret the same chart differently. There is no reproducible pass/fail verdict.

### Good — Percentile analysis over average

```
Test results for POST /orders (500 VU, 5 min steady):
  p50: 120ms    <- typical experience
  p95: 285ms    <- NFR target: < 300ms -> PASS
  p99: 1,240ms  <- long tail: investigate
  max: 4,500ms  <- isolated spikes: connection pool timeout
  
Average: 145ms  <- misleading; hides the 1.24s tail
```

The p99 and max reveal a pool exhaustion pattern not visible in the average.

### Bad — Reporting only the average

"Average response time is 145ms, well within the 300ms target." The p99 tail at 1.24 seconds
is not reported. 1% of users experience 4-second responses. Support tickets follow.

### Good — Soak test catching resource leak

```
Soak test: 200 VU for 60 minutes
t=0:   p95 = 180ms, memory = 512MB
t=20m: p95 = 195ms, memory = 720MB
t=40m: p95 = 310ms, memory = 950MB  <- NFR breach starts
t=60m: p95 = 450ms, memory = 1.1GB  <- OOM warning

Finding: memory leak in connection pool; connections not released after 10-minute inactivity.
```

### Bad — Load test without soak phase

Five-minute ramp-up looks fine. Memory leak shows up at 30 minutes in production.
Incident at peak traffic the following week.

### Good — Bottleneck localized to DB query

```
Performance finding: POST /reports p95 = 2.4s (NFR: 500ms)

Evidence:
  - App CPU: 15% during test (not CPU-bound)
  - DB slow query log: SELECT on reports table: avg 1.8s, 45% of total time
  - EXPLAIN ANALYZE: sequential scan on reports (user_id) for table with 2M rows
  
Root cause: missing index on (user_id, created_at)
Recommendation: CREATE INDEX CONCURRENTLY reports_user_created_idx ON reports(user_id, created_at DESC)
Estimated impact: query plan changes to index scan; expected p95 < 200ms (validated in dry run)
```

### Bad — Performance report with no root cause

"The API is slow. We need more hardware." No query analysis, no CPU profiling, no layer
localization. Hardware added; performance unchanged. The bottleneck was a missing index.

### Good — Pre-seeded test data at production scale

```
Performance environment data preparation:
  - users: 500,000 (matches production)
  - orders per user: avg 12 (matches production distribution)
  - total orders table rows: ~6,000,000
  
Reason: query plan with 500 rows (dev database) uses different join strategy than with 6M rows.
        Index scan vs sequential scan crossover point is at approximately 200K rows.
```

### Bad — Performance test against empty database

Tests pass with 1,000 records. Query uses full table scan in production with 5 million records.
Performance degrades 100x at production scale.

## Boundaries

- Owns load test design, execution, result analysis, and bottleneck localization.
- Does not own infrastructure provisioning for the performance environment -> `devops-sre`.
- Does not own database cluster tuning or index creation -> `developer` or `devops-sre`.
- Does not own architecture decisions to address performance issues -> `tech-lead` / `system-architect`.
- Does not own security load testing (DDoS simulation) -> `security-engineer`.

## Sources

### Priority 1 — Tools and NFR standards

- Grafana k6 documentation — https://k6.io/docs/
- Apache JMeter User Manual — https://jmeter.apache.org/usermanual/
- ISO/IEC 25010: Performance efficiency quality characteristic — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- ISTQB Advanced Level Test Analyst: Non-functional testing — https://www.istqb.org/certifications/advanced-level-test-analyst

### Priority 2 — Orientation

- Google SRE Book: Service Level Objectives chapter — https://sre.google/sre-book/service-level-objectives/
- Brendan Gregg: USE Method — https://www.brendangregg.com/usemethod.html
- Prometheus Best Practices — https://prometheus.io/docs/practices/
- Gatling documentation — https://docs.gatling.io/

### Priority 3 — Background

- ThoughtWorks Technology Radar (performance testing) — https://www.thoughtworks.com/radar
- Continuous Delivery (Humble, Farley): NFR testing chapter — book reference

## Handoff

- Infrastructure provisioning for performance environment -> `devops-sre`.
- Database query optimization and index creation -> `developer` with bottleneck evidence.
- Architecture-level performance decisions (caching strategy, service decomposition) -> `system-architect` / `tech-lead`.
- CI/CD integration of performance tests -> `ci-cd-test-integration`.
- Security load test scenarios -> `security-engineer`.

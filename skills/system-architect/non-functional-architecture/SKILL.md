---
name: non-functional-architecture
description: Use when defining and owning the NFR catalog at the architectural level — setting measurable performance, reliability, scalability, availability, security, observability, and compatibility targets; making trade-offs explicit; and tying each target to components, flows, and verification approaches. Not for running load tests, operating infrastructure, or defining product KPIs.
family: method
profile_level: Senior+
---

# Non-Functional Architecture

## Purpose

Set non-functional properties of the architecture as measurable, traceable constraints, and own the trade-offs between them. Produce an NFR catalog that QA can verify, DevOps/SRE can instrument, and engineering can design to — without treating "high performance" as a specification.

## Use When

- A system, domain, or significant change needs an NFR catalog tied to architecture.
- Performance, reliability, scalability, availability, security, observability, or compatibility targets must be set with measurable values.
- NFR trade-offs — latency vs consistency, availability vs cost, throughput vs ordering guarantee — must be made explicit and recorded.
- NFRs must be decomposed to components or flows and linked to architectural mechanisms.
- A QA or DevOps/SRE team needs architecture-level NFR definitions to set up verification and instrumentation.
- Regulatory or contractual SLA obligations must be translated into internal SLOs and error budget rules.

## Do Not Use When

- The task is running load, stress, chaos, or security tests → handoff to `qa-engineer` / `devops-sre`.
- The task is infrastructure tuning, autoscaling policy, or runtime SLO operations → handoff to `devops-sre`.
- The task is defining product success KPIs or business OKRs → handoff to `product-manager`.
- The task is full security threat modeling and vulnerability management → handoff to `security-engineer`.
- The task is choosing an integration pattern to meet an NFR → `integration-architecture`.

## Inputs

- Product or domain goal, criticality level, and failure-consequence classification.
- Usage profile: concurrent users, peak RPS, data volume, growth projections.
- Operational data: current latency percentiles, throughput, error rates, incident history.
- Regulatory and contractual SLA obligations.
- Current capacity, known scaling limits, and debt evidence.

## Workflow

1. **Identify applicable NFR categories.** Use ISO/IEC 25010 quality model as the checklist: performance efficiency (time behavior, capacity, resource utilization), reliability (maturity, fault tolerance, recoverability, availability), security (confidentiality, integrity, authenticity, non-repudiation), maintainability, portability, compatibility, usability. Select categories relevant to the system.
2. **Set measurable targets per category and per component or flow.** Avoid adjectives. Specify: metric name, measurement point, percentile or aggregate, threshold, and measurement method.
   ```
   NFR-03: Checkout API
   Metric: p99 response time at gateway ingress
   Target: ≤ 300ms under 500 RPS sustained
   Measurement: load test baseline + production RED dashboard
   ```
3. **Identify trade-offs between NFRs.** Document trade-off decisions explicitly. Common pairs: latency vs consistency (strong consistency adds synchronous coordination cost); availability vs cost (multi-AZ redundancy doubles infrastructure cost); throughput vs ordering (Kafka partition-level ordering limits parallel scaling).
4. **Tie NFRs to architectural mechanisms.** Each NFR target must link to a concrete architectural choice: caching strategy, partitioning approach, redundancy model, circuit breaker, bulkhead, read replica, eventual consistency model. If no mechanism is nominated, the NFR is aspirational, not architectural.
5. **Define verification approach with QA and DevOps/SRE.** For each target: who verifies (QA with load test, DevOps/SRE with production monitoring), what tool, and at which stage (pre-release, production canary, quarterly review).
6. **Set error budgets and SLO boundaries.** Translate external SLA (e.g., 99.9% monthly uptime = 43.8 min downtime allowed) into internal SLO (99.95% to leave error budget headroom) and error budget policy (freeze releases when >50% budget consumed in one week).
7. **Record NFR ADRs.** Each significant trade-off decision gets an ADR entry. Mark targets that require product or business confirmation before locking.

## Outputs

- NFR catalog: target, scope (system / component / flow), mechanism, verification approach.
- NFR trade-off matrix with explicit trade-off decisions and rationale.
- SLO and error budget definitions for critical paths.
- NFR ADRs for significant trade-off choices.
- Handoff items for `qa-engineer` (verification plan), `devops-sre` (instrumentation and alerting), `security-and-observability-by-design` (security and observability NFRs).

## Named Patterns

### Good — Measurable NFR with mechanism
```
NFR-07: Inventory read API
Target: p99 ≤ 50ms at 2,000 RPS
Mechanism: Redis cache with 10s TTL on product availability; cache miss falls through to Postgres replica.
Trade-off: Data staleness up to 10s is acceptable for availability display; not acceptable for cart reservation.
Verification: k6 load test, Prometheus p99 dashboard, SLO alert at ≥ 60ms.
```

### Bad — Aspirational NFR without mechanism
```
NFR-07: Inventory API must be fast and highly available.
```
No metric, no percentile, no mechanism, no verification method. Engineering cannot design to it; QA cannot verify it.

### Good — Explicit CAP/PACELC trade-off in ADR
```
ADR-019: Inventory availability trade-off
Decision: Prefer AP (availability + partition tolerance) over CP for product catalog reads.
Consequence: Cache may serve stale data during Postgres failover (up to 10s staleness accepted by Product).
Revisit trigger: If stale data causes inventory oversell incidents exceeding 3 per quarter.
```

### Bad — Implicit consistency assumption
System documentation says "high availability." Engineers assume strong consistency. Operations team configures read replicas with async replication. Cart service reads stale inventory. Oversell incidents begin. No ADR captures the trade-off.

### Good — SLO with error budget policy
```
SLO: 99.9% monthly availability on /api/checkout
Error budget: 43.8 min/month
Policy: If 50% of monthly error budget is consumed in 7 days → freeze feature releases,
        prioritize reliability work until budget recovers.
```

### Bad — SLA commitment without internal SLO
Contract promises 99.9%. No internal SLO is defined. Operations team discovers the commitment only during an incident post-mortem.

## Boundaries

- Does not run load, stress, chaos, or security testing → `qa-engineer` / `devops-sre`.
- Does not own infrastructure tuning, autoscaling configuration, or runtime incident response → `devops-sre`.
- Does not own product KPIs, business OKRs, or commercial SLA negotiation → `product-manager`.
- Does not own the full security threat model or vulnerability management → `security-engineer`.

## Sources

### Priority 1 — Canonical References
- ISO/IEC 25010 — Product Quality Model: https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- Google SRE Book — Service Level Objectives: https://sre.google/sre-book/service-level-objectives/
- Google SRE Workbook — SLO Implementation and Error Budgets: https://sre.google/workbook/implementing-slos/
- AWS Well-Architected Reliability Pillar: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html

### Priority 2 — Practitioner Guidance
- Microsoft Azure Well-Architected Framework — Reliability and Performance: https://learn.microsoft.com/azure/well-architected/
- Martin Kleppmann — Designing Data-Intensive Applications (consistency and availability trade-offs): https://dataintensive.net/
- PACELC theorem — extended discussion: https://cs.uwaterloo.ca/~tozsu/courses/CS848/W17/presentations/PACELC.pdf

### Priority 3 — Supplementary
- InfoQ — SRE and SLO practices: https://www.infoq.com/sre/
- ThoughtWorks Tech Radar — fitness functions for architecture: https://www.thoughtworks.com/radar/techniques/fitness-function-driven-development

## Handoff

- Verification plan execution (load test, security test, chaos test) → `qa-engineer` / `devops-sre`.
- Observability instrumentation and alerting for NFR targets → `devops-sre` and `security-and-observability-by-design`.
- Security-specific NFR targets (encryption strength, auth latency, audit retention) → `security-and-observability-by-design`.
- Recording NFR trade-off decisions → `architecture-decision-records`.
- Integration pattern selection to meet specific NFR targets → `integration-architecture`.

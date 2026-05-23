---
name: non-functional-requirements
description: Use when identifying, formulating, or reviewing non-functional requirements — performance, reliability, availability, security, audit, observability, scalability, maintainability, or compliance — as measurable constraints that architecture, engineering, QA, and operations can act on.
family: method
profile_level: Senior+
---

# Non-Functional Requirements

## Purpose

Make quality attributes explicit, measurable, and scoped so that architecture, engineering, QA, and SRE can decide how to satisfy them without guessing. Vague quality expectations ("must be fast", "must be secure") are not requirements; they are wishes. This skill converts wishes into SLO-shaped, verifiable constraints — and routes ownership of meeting them to the correct role.

## Use When

- A feature has visible performance, reliability, security, or compliance risks that are not yet stated as requirements.
- An NFR exists in prose form ("high performance", "must be secure") and must be made testable.
- Architecture, QA, or SRE needs a quality-attribute checklist before design or test planning begins.
- A change affects an SLO-sensitive path and the existing NFR set must be reviewed for impact.
- Security, audit, data-retention, or observability obligations exist but have not been formalized.

## Do Not Use When

- The task is making architecture decisions to meet the NFRs — hand off to `system-architect`.
- The task is writing the security review or penetration test plan — hand off to Security.
- The task is implementing monitoring or alerting — hand off to `devops-sre`.
- The task is designing QA test plans — hand off to `qa-engineer`.
- The task is functional behavior specification — use `functional-specification`.

## Inputs

- Feature scope and criticality: user-facing or internal; transactional or read-heavy.
- User volume: expected concurrent users, peak load, traffic growth projections.
- Business criticality: revenue impact of downtime, SLA commitments to customers.
- Data sensitivity: PII, financial, healthcare, regulated data classes.
- Existing architecture: infrastructure, hosting model, adjacent service SLAs.
- Regulatory or contractual obligations: GDPR, PCI-DSS, SOC 2, industry-specific.

## Workflow

1. List the relevant ISO 25010 quality attribute categories for this feature: Performance Efficiency, Reliability, Security, Maintainability, Compatibility, Portability, Usability, Functional Suitability. Select only the attributes with genuine risk for this context.
2. For each selected attribute, draft a measurable constraint. Apply the SLO template: "[metric] of [scope] must be [threshold] under [conditions] measured by [method]". Avoid subjective qualifiers.
3. Scope each NFR: endpoint, user segment, data class, operation type, or traffic percentile. An NFR applied to the whole system is usually too broad to act on.
4. For performance: specify latency (p95/p99 preferred over average), throughput (requests/sec or messages/sec), and the load profile at which these hold (normal load, 3× peak).
5. For reliability and availability: specify uptime target, recovery time objective (RTO), recovery point objective (RPO), graceful degradation behavior, and failure isolation requirements.
6. For security: specify authentication/authorization model, data classification and encryption at rest/transit, audit log requirements (who, what, when, from where), rate limiting, and known threat model assumptions. Do not write a security spec — route to Security.
7. For observability: specify mandatory log events, trace coverage, and metric names that support incident diagnosis. Route implementation to `devops-sre`.
8. For compliance: name the regulatory framework, the relevant articles, and the system obligation. Route legal/regulatory interpretation to the compliance function.
9. Mark NFRs that cannot be made measurable as open risks with an owner assigned.
10. Produce the NFR specification and hand off to `system-architect` for architecture decisions, `qa-engineer` for test plan, and `devops-sre` for implementation.

## Outputs

- NFR specification: attribute, measurable constraint, scope, measurement method, and derivation rationale.
- Quality attribute checklist (ISO 25010 categories with status: specified / deferred / not applicable).
- Open NFR risk register: items not yet measurable, owner, and unblock path.
- Handoff list: which NFRs require architecture decision, QA test design, or SRE implementation.

## Named Patterns

### Good — Measurable performance NFR
```
NFR-P01: Latency
Scope: POST /v1/orders (order creation, authenticated user)
Constraint: p95 response time < 300 ms under normal load (500 concurrent users)
            p99 response time < 1000 ms under peak load (2000 concurrent users)
Measurement: synthetic load test in staging, Prometheus histogram
Derivation: customer research shows >1s latency causes 20% cart abandonment.
```
Threshold, scope, load profile, measurement method, and business rationale — all present.

### Bad — Vague performance wish
```
The API must be fast and handle high load.
```
"Fast" and "high load" are undefined. Engineering cannot design for it; QA cannot test it; SRE cannot alert on it.

### Good — Availability NFR with RTO/RPO
```
NFR-A01: Availability
Scope: Order creation and retrieval paths
Uptime: 99.9% measured monthly (≤43 min downtime/month)
RTO: < 5 minutes (time to restore degraded → full service)
RPO: 0 (no committed orders lost; event log is the source of truth)
Degradation behavior: on downstream payment gateway timeout (>3s),
  order moves to status Pending; user shown "payment processing" message;
  background retry runs every 30s for up to 10 minutes.
```
Operations and architecture can plan for this; QA can test the degradation path.

### Bad — Uptime target without RTO/RPO
"99.9% uptime." No recovery strategy, no RPO, no degradation behavior. Incident response improvises.

### Good — Security NFR (scope-limited)
```
NFR-S01: Authentication
Scope: All write endpoints in the Order API
Constraint: Requests without a valid JWT token (RS256, issued by Auth Service) must be rejected with HTTP 401.
Constraint: Token must contain user_id, tenant_id, and role claims; order ownership checked at application level.
Audit: every authentication failure logged with timestamp, IP, user-agent, and attempted endpoint.
Handoff: token validation implementation → Engineering; audit log schema → system-analyst (see NFR-S02).
```
Scope is bounded; audit obligation is explicit; handoff is named.

### Bad — "Must be secure"
No scope, no authentication model, no audit requirement. Every team interprets "secure" differently.

### Good — Observability NFR
```
NFR-O01: Traceability
Scope: All order state transitions
Mandatory log events: order_created, order_confirmed, order_cancelled (each with order_id, user_id, timestamp, initiating_actor)
Trace: distributed trace span required for all cross-service calls in the order creation flow
Metrics: orders_created_total (counter), order_creation_latency_seconds (histogram), order_failure_total (counter by error_code)
Handoff: metric naming and alerting threshold → devops-sre.
```
Engineering knows what to emit; SRE knows what to monitor; QA knows what to verify in logs.

### Bad — Observability as afterthought
No log events specified. After launch, on-call team cannot diagnose incidents without reading code.

## Boundaries

- Owns: formulation of NFR constraints as measurable requirements, quality attribute scoping, open-risk identification.
- Does not own: architecture decisions to meet NFRs — that is `system-architect`.
- Does not own: security review, penetration testing, threat modeling — route to Security.
- Does not own: monitoring implementation, alerting, on-call — that is `devops-sre`.
- Does not own: QA test plan for NFR validation — that is `qa-engineer`.
- Does not own: regulatory legal interpretation — route to Compliance.

## Sources

### Priority 1 — Standards
- ISO/IEC 25010 Software Quality Model — https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
- IEEE/ISO/IEC 29148:2018, section on non-functional requirements — https://standards.ieee.org/content/ieee-standards/en/standard/29148-2018.html
- Karl Wiegers, Joy Beatty: Software Requirements, 3rd ed. — book reference (quality attribute chapters)

### Priority 2 — Practice
- Google SRE Book, SLO chapter — https://sre.google/sre-book/service-level-objectives/
- OWASP Security Requirements — https://owasp.org/www-project-application-security-verification-standard/
- NIST SP 800-53 Security Controls — https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final

### Priority 3 — Background
- Len Bass, Paul Clements, Rick Kazman: Software Architecture in Practice — book reference (quality attribute scenarios)
- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar

## Handoff

- Architecture decisions to satisfy NFRs → `system-architect`.
- Monitoring, alerting, and SLO implementation → `devops-sre`.
- NFR test plan and validation strategy → `qa-engineer`.
- Security review, threat model, penetration test → Security team.
- Regulatory compliance interpretation → Compliance function.

---
name: security-and-observability-by-design
description: Use when embedding security and observability as first-class architectural properties — defining trust boundaries, AuthN/AuthZ at the architectural level, audit logging requirements, encryption and isolation rules, and structured logs/metrics/traces architecture across components and integrations. Not for full security governance, threat modeling execution, or SRE operations.
family: method
profile_level: Senior+
---

# Security and Observability by Design

## Purpose

Embed security and observability into the architecture so they are structural properties, not afterthought overlays. Produce a security-by-design brief (trust boundaries, AuthN/AuthZ, audit, encryption, isolation) and an observability-by-design brief (logs, metrics, traces, correlation) that engineering and DevOps/SRE can implement against — and that security engineers can validate without redesigning the system.

## Use When

- Trust boundaries, authentication, authorization, audit logging, encryption, or isolation must be defined at the architectural level before implementation begins.
- Logs, metrics, and traces architecture must be designed across components and integrations — not added after go-live.
- A change introduces new component boundaries, external integrations, or data classification zones with security or observability implications.
- An architectural risk affects confidentiality, integrity, availability, or operational visibility.
- NFR catalog includes security or observability targets that need architectural mechanisms assigned.

## Do Not Use When

- The task is full threat modeling execution (STRIDE, PASTA) or vulnerability scoring → handoff to `security-engineer`.
- The task is implementing observability: deploying collectors, configuring dashboards, writing alert rules → handoff to `devops-sre`.
- The task is a security audit, penetration test, or attestation → handoff to `security-engineer`.
- The task is incident response or on-call SLO management → handoff to `devops-sre`.
- The task is writing detailed API security specs or auth flow sequence diagrams → handoff to `system-analyst`.

## Inputs

- Component and integration map from `component-and-service-decomposition` and `integration-architecture`.
- Data classification: which data is PII, PCI-DSS, or regulated; where it lives; who accesses it.
- Existing AuthN/AuthZ patterns: OAuth2, OIDC, RBAC, ABAC, SSO, mTLS topology.
- Regulatory constraints: GDPR, PCI-DSS, SOC 2, HIPAA, or equivalent.
- Current observability stack and gaps: what is instrumented, what is missing, what correlation exists.
- Threat surface assumptions and known incidents from previous post-mortems.

## Workflow

1. **Map trust boundaries.** Draw zones where trust is explicit: external clients, internal services, internal trusted services, admin plane, data stores. Every boundary crossing must have an explicit trust assertion — do not default to implicit trust inside the perimeter.
2. **Define AuthN/AuthZ per boundary.** For each boundary crossing: Who authenticates? By what mechanism (OIDC token, mTLS, API key)? What authorization model applies (RBAC, ABAC, OPA policy)? What is the token lifetime and revocation path?
3. **Define audit logging requirements.** Which operations must be auditable (identity, time, action, resource, outcome)? At which layer (API gateway, service, database)? What retention period? Where does the audit trail land and who owns it?
4. **Define encryption requirements.** Data in transit: TLS version minimum, cipher policy, mTLS where service identity is required. Data at rest: which stores require encryption, key management approach (KMS, HSM), rotation policy.
5. **Design observability architecture.** Structured logs: required fields (service, trace_id, span_id, user_id if applicable, error_code). Metrics: RED method per service (Rate, Errors, Duration), USE for infrastructure (Utilization, Saturation, Errors). Distributed traces: propagation header standard (W3C Trace Context), sampling strategy, retention horizon.
6. **Tie security and observability to NFR catalog and ADRs.** Security targets (e.g., "all API calls authenticated") and observability targets (e.g., "p99 trace coverage ≥ 95%") become NFR entries. Each gets an ADR when the mechanism involves a significant architectural choice.
7. **Hand off detailed implementation.** Architecture defines the properties; implementation goes to engineering and DevOps/SRE. Threat modeling execution goes to `security-engineer`. Observability platform operation goes to `devops-sre`.

## Outputs

- Trust boundary map with zone definitions and crossing rules.
- Security-by-design brief: AuthN/AuthZ mechanisms per boundary, audit requirements, encryption rules, isolation model.
- Observability-by-design brief: structured log schema, metric taxonomy (RED/USE), trace propagation standard, correlation IDs, sampling policy, retention.
- Security and observability ADRs.
- Handoff items for `security-engineer` (threat modeling, audit), `devops-sre` (platform implementation), engineering (instrumentation pattern).

## Named Patterns

### Good — Defense-in-depth trust boundary model
```
Zone 1 (External): API Gateway — validates JWT, enforces rate limit, terminates TLS.
Zone 2 (Internal services): mTLS between services — service identity verified via SPIFFE/SPIRE.
Zone 3 (Data stores): Service accounts with least privilege — no direct external access.
Zone 4 (Admin plane): Separate network segment, MFA required, audit trail to SIEM.
```
Each zone crossing has an explicit trust mechanism. Compromise of one zone does not grant access to others.

### Bad — Implicit internal trust ("inside the firewall is safe")
All internal service calls use HTTP without authentication. A compromised internal service can call any other service with any payload. No audit trail. Lateral movement is trivial.

### Good — Observability with correlation across components
```
// Every log entry carries W3C Trace Context
{
  "service": "order-api",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "user_id": "u-9923",
  "action": "create_order",
  "outcome": "success",
  "duration_ms": 142,
  "timestamp": "2026-05-23T10:15:30Z"
}
```
Trace ID links this log entry to spans across all services. Incident investigation follows a single thread.

### Bad — Unstructured logs without correlation
```
INFO  2026-05-23 10:15:30 Order created successfully
```
No trace ID, no user identity, no service label, no duration. Correlating this entry with a downstream failure requires manual text search across multiple log files.

### Good — Authorization decision at the service boundary
RBAC policy evaluated at the service entry point using OPA: request carries JWT with roles claim; OPA policy file defines which roles can call which endpoints. Policy is version-controlled and auditable. Service does not re-implement authorization logic per endpoint.

### Bad — Authorization logic scattered across service
Each endpoint has its own `if user.role == "admin"` check. Roles are hardcoded strings. No central policy. Adding a new role requires touching 30 files. A missed check creates an escalation path.

## Boundaries

- Does not own threat modeling execution, vulnerability scoring, security audit, or attestation → `security-engineer`.
- Does not own observability platform operation: collector deployment, dashboard configuration, alert routing → `devops-sre`.
- Does not own incident response, on-call rotation, or SRE error budgets → `devops-sre`.
- Does not write detailed auth flow sequence diagrams or API security specifications → `system-analyst`.

## Sources

### Priority 1 — Canonical References
- OWASP Application Security Verification Standard (ASVS): https://owasp.org/www-project-application-security-verification-standard/
- OWASP Cheat Sheet Series — Authentication, Authorization, Logging and Monitoring: https://cheatsheetseries.owasp.org/
- NIST SP 800-160 Vol. 1 — Systems Security Engineering: https://csrc.nist.gov/publications/detail/sp/800-160/vol-1/final
- OpenTelemetry — Observability primer and specification: https://opentelemetry.io/docs/concepts/observability-primer/
- W3C Trace Context standard: https://www.w3.org/TR/trace-context/

### Priority 2 — Practitioner Guidance
- Google SRE Book — Monitoring Distributed Systems: https://sre.google/sre-book/monitoring-distributed-systems/
- SPIFFE/SPIRE — workload identity for zero-trust: https://spiffe.io/
- OPA (Open Policy Agent) — policy-as-code for authorization: https://www.openpolicyagent.org/docs/latest/
- AWS Security Pillar — Well-Architected Framework: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html

### Priority 3 — Supplementary
- STRIDE threat modeling overview: https://learn.microsoft.com/azure/security/develop/threat-modeling-tool-threats
- Prometheus RED method — https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture/
- InfoQ — observability and security-by-design articles: https://www.infoq.com/security/

## Handoff

- Threat modeling execution, penetration test scope, vulnerability review → `security-engineer`.
- Observability platform deployment and alert configuration → `devops-sre`.
- Auth flow and API security specification → `system-analyst`.
- Encryption and key management implementation → engineering + `devops-sre`.
- Security and observability NFR targets → `non-functional-architecture`.

---
name: shared-requirements-analysis
description: Use when needs, requests, constraints, or stakeholder inputs must be transformed into structured requirements — classified by type, checked for clarity and testability, traced to their source, and routed to the role that owns each requirement class — without merging business analysis and system analysis ownership.
---

# Shared Requirements Analysis

## Purpose

Transform vague needs, change requests, regulations, or stakeholder inputs into structured requirements that are unambiguous, testable, traceable, and scoped — and route each requirement class to the role that owns it. Requirements analysis is the method; ownership of the outputs is distributed across roles by class. The method ensures that the same need is not interpreted differently by business, product, system, and QA roles, and that no requirement advances without an identified owner and a traceability link to its source.

## Use When

- A feature request, process change, integration need, or regulatory obligation has arrived and must be translated into structured requirements before design or implementation begins.
- Requirements are described in natural language and are vague, conflicting, overlapping, or missing key conditions.
- Business requirements, user requirements, functional requirements, system requirements, and non-functional requirements exist as an undifferentiated mix and must be separated by class and owner.
- Requirements from multiple sources conflict or overlap and the conflicts have not been resolved.
- An existing requirement is challenged as out of scope, and the team needs to trace it to its origin to decide whether to keep, change, or remove it.
- A requirement handoff to a downstream role (System Analyst, QA, Engineering) is imminent and the requirements are not yet in a state that the receiving role can use.

## Do Not Use When

- The task is product strategy or discovery — deciding what to build and why → Product Manager owns discovery and opportunity framing; this skill structures what has been decided, not what to decide.
- The task is architecture design or technology selection → System Architect owns technology and architecture decisions; requirements analysis provides the "what" and constraints, not the "how."
- The task is QA test strategy design or regression scope selection → QA Engineer owns test strategy; requirements are inputs to test strategy, not the test strategy itself.
- The task is BI / data pipeline implementation or DWH schema design → Data/BI or Product Analyst owns those; reporting requirements are inputs.
- Requirements are complete and testable; the task is authoring specifications or acceptance criteria → use `functional-specification` (System Analyst) or `shared-acceptance-criteria`.

## Inputs

- The originating need: goal, problem statement, business objective, user story draft, change request, defect report, regulatory text, or stakeholder verbal description.
- Existing documentation: prior requirements, specifications, process models, rule catalogs, decision logs.
- Stakeholder context: who requested it, who is affected, who approves, and what success looks like.
- Known constraints: technical, regulatory, contractual, organizational, and timeline.
- Role boundaries: which role owns which requirement class for this product and team context.

## Workflow

1. **Identify the underlying need or business objective.** Before classifying requirements, answer: what problem does this solve, whose problem is it, and what outcome does success produce? Requirements that are not anchored to a problem or objective are solutions masquerading as requirements. If the need cannot be stated, stop and elicit it first.

2. **Classify requirement candidates by type.** Apply the ISO/IEC/IEEE 29148 requirement type taxonomy:
   - *Business requirements*: goals, objectives, and desired outcomes at organization or business-unit level. Owner: Business Analyst.
   - *Stakeholder requirements*: what specific stakeholder groups need from the solution. Owner: Business Analyst.
   - *Solution requirements — functional*: what the solution must do to satisfy stakeholder and business requirements. Owner: System Analyst.
   - *Solution requirements — non-functional*: performance, availability, security, maintainability, and other quality constraints. Owner: System Analyst.
   - *Transition requirements*: what is needed to move from the current state to the target state (data migration, training, legacy cutover). Owner: depends on type; typically Business Analyst or Project Manager.
   Avoid mixing types in one requirement statement. A statement that combines a business goal and a system behavior is two requirements, not one.

3. **Normalize requirement wording.** Apply the EARS (Easy Approach to Requirements Syntax) patterns or equivalent:
   - *Ubiquitous*: "The system shall…" — always active.
   - *Event-driven*: "When [trigger], the system shall [response]."
   - *Unwanted behavior*: "If [unwanted condition], the system shall [protective action]."
   - *State-driven*: "While [state], the system shall [behavior]."
   - *Optional feature*: "Where [feature is included], the system shall [behavior]."
   Replace vague verbs ("support", "handle", "manage") with verifiable behavior. Replace passive voice with an active subject.

4. **Check each requirement against quality criteria.** Apply the SMART-R checklist:
   - *Specific*: one condition or behavior per requirement statement.
   - *Measurable*: a test can verify it pass or fail.
   - *Agreed*: a named stakeholder has confirmed the requirement.
   - *Realistic*: achievable within the known constraints.
   - *Traceable*: linked to a source (upstream requirement, business rule, policy, decision).
   Flag any requirement that fails one criterion as a defect. Do not advance defective requirements.

5. **Identify conflicts and overlaps.** Compare requirements from different sources: do they contradict each other, duplicate each other, or leave boundary conditions undefined? For each conflict: record both versions, name the resolution owner, and mark the requirement as blocked until resolved. For each duplication: merge or cross-reference; do not maintain two authoritative statements of the same requirement.

6. **Establish traceability.** For every requirement, record: the source (policy reference, stakeholder decision record, upstream requirement ID, decision log entry), and the downstream artifacts that derive from it (acceptance criteria IDs, test case references, specification section). Traceability without a source is a guess; traceability without a downstream link is an orphan.

7. **Route non-owned requirement classes.** Route functional and non-functional requirements to System Analyst. Route measurement requirements (metric definitions, tracking needs, analytical validation) to Product Analyst or the metric owner. Route transition requirements to the appropriate owner (Business Analyst for business-side transition, System Analyst for system migration, Project Manager for delivery-side transition). Create handoff blocks, not internal notes.

## Outputs

- Structured requirements list: each requirement with ID, type, normalized statement, source, owner, status (draft / validated / deferred / rejected), and traceability link.
- Conflict and overlap log: each conflict with both versions, resolution owner, and deadline.
- Traceability matrix: requirement ID, source, owner, and downstream artifact references.
- Gap and open-question log: requirements with missing information, unresolved source, or undefined scope.
- Handoff tasks: one per requirement class routed to another role, with expected artifact and acceptance criteria.

## Role Modes

### Business Analyst

Owns the business and stakeholder requirements tier: eliciting business objectives, stakeholder needs, and constraints from business owners, then normalizing them into structured requirements using domain vocabulary. Validates business requirements with the accountable business owner before handoff. Routes functional and non-functional requirements to System Analyst as handoffs; routes measurement requirements to Product Analyst. Does not author system specifications, API contracts, or acceptance criteria for system behavior — those are handoff outputs from System Analyst.

## Boundaries

- Does not merge business analysis and system analysis ownership. Business requirements and functional requirements are distinct classes with distinct owners; maintaining this separation is non-negotiable.
- Does not decide product priority, roadmap sequencing, or architectural approach → Product Manager decides priority; System Architect and Tech Lead decide architecture. Requirements analysis provides input; it does not make those decisions.
- Does not author QA test strategies or regression suites → QA Engineer derives test plans from requirements; the requirements are inputs, not the test plan.
- Does not treat stakeholder wording as final requirements without normalization → stakeholder language is the raw input; the normalized requirement is the output. Copying stakeholder wording as-is propagates ambiguity into specification and test work.
- Does not advance requirements with open conflicts → a requirement with an unresolved source conflict is not ready for specification or development.

## Named Patterns

### Good — Normalized functional requirement
```
REQ-088 [Functional — System Analyst]
Type: Solution requirement — functional
Statement: When a customer submits an order containing an out-of-stock item,
  the system shall reject the submission and return error code ITEM_OUT_OF_STOCK
  with the list of out-of-stock item identifiers.
Source: Business Rule BR-033 (validated 2025-05-20, Finance Controller).
         Business Requirement BR-REQ-012.
Status: Validated.
Downstream: SYS-114 (specification), AC-088 (acceptance criteria), TC-312 (test case).
```
Type and owner explicit. Statement is event-driven (EARS pattern), behavior is verifiable. Traceability to source and downstream complete.

### Bad — Mixed-type compound requirement
"The system should provide a user-friendly checkout experience with fast payment processing that complies with PCI DSS and handles all edge cases including out-of-stock, payment failures, and network errors."
Five requirements (UX quality, performance, compliance, and two error scenarios) in one statement. No type, no owner, no traceability. Unverifiable as written.

### Good — Conflict resolution record
```
Conflict REQ-044a vs REQ-044b:
REQ-044a (Business Analyst draft from Finance): "The discount applies only to orders >= 5 000 RUB."
REQ-044b (Business Analyst draft from Marketing): "The discount applies to all B2B orders."
Conflict: threshold vs universal application for B2B.
Resolution owner: Head of Product (decision needed by 2025-05-30).
Status: BLOCKED — do not advance either version to specification.
```
Both versions recorded. Resolution owner named. Status blocks downstream work until resolved.

### Bad — Silent conflict resolution
Analyst picks one version and writes the specification. Marketing discovers the error during UAT. "You never told us you changed it." Rework at the specification and test level.

### Good — Traceability matrix excerpt
```
| Req ID  | Type              | Source              | Owner          | Spec     | AC      |
|---------|---|---|---|---|---|
| REQ-088 | Functional        | BR-033, BR-REQ-012  | System Analyst | SYS-114  | AC-088  |
| REQ-089 | Non-functional    | NFR-007 (SLA)       | System Analyst | SYS-115  | —       |
| REQ-090 | Business          | PM Decision 2025-05 | BA             | —        | AC-090  |
| REQ-091 | Transition        | Project Charter     | Project Mgr    | —        | —       |
```
Every requirement has a source, an owner, and at least one downstream artifact (or an explicit absence with reason).

### Bad — Requirements list without traceability
Spreadsheet with 120 requirements: ID, description, status. No type, no owner, no source, no downstream link. When any requirement is questioned in UAT, the team cannot explain its origin.

### Good — Handoff task from requirements analysis
```
To: System Analyst
Task: Specify functional behavior for REQ-088 (out-of-stock rejection).
Context: Business rule BR-033 validated. Business requirement BR-REQ-012 approved.
Inputs: REQ-088 (normalized statement), BR-033 rule catalog entry, order state machine.
Expected artifact: Functional specification SYS-114 section covering out-of-stock rejection,
  including API error shape and state transition.
Acceptance criteria: SYS-114 covers REQ-088 completely; error code ITEM_OUT_OF_STOCK
  is defined in the API error taxonomy.
Deadline: 2025-06-05.
```
The receiving role knows exactly what it receives, what it must produce, and how to verify it.

### Bad — Informal handoff
"Here's the requirements doc — can you spec it out?" No explicit scope, no acceptance criteria, no deadline. System Analyst produces a spec that misses several requirements; the gap is discovered at code review.

### Good — Requirement with testability gap flagged
```
REQ-095 [DRAFT — testability defect]
Statement: "The payment page should load quickly."
Defect: "Quickly" is not measurable. Cannot write a pass/fail test.
Fix needed: Define load time threshold (e.g., "The payment page shall load within 2 seconds
  under 95th-percentile load conditions as defined in NFR-012").
Owner for fix: Product Manager (acceptable threshold) → System Analyst (NFR formalization).
Status: BLOCKED.
```
The defect is named, the fix is concrete, and the owner for each fix step is explicit.

### Bad — Untestable requirement advanced to specification
"The system should provide a good user experience." Passes into the specification without normalization. QA writes no test case. Feature releases with undefined acceptance conditions.

## Sources

### Priority 1 — Method canon

- ISO/IEC/IEEE 29148:2018 — Systems and software engineering — Life cycle processes — Requirements engineering — https://standards.ieee.org/ieee/29148/6937/ (canonical standard; defines requirement types, quality attributes, and traceability)
- IIBA BABOK Guide v3 — Requirements Analysis and Design Definition knowledge area — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/ (business analysis requirements methodology)
- IREB CPRE Foundation Level — Requirements Engineering framework — https://www.ireb.org/en/cpre/foundation-level/ (structured requirements engineering method; classification, quality criteria, elicitation, documentation)
- Karl Wiegers and Joy Beatty, "Software Requirements" (Microsoft Press, 3rd ed.) — comprehensive practitioner reference on requirements classification, writing, review, and traceability

### Priority 2 — Orientation

- Alistair Cockburn, "Writing Effective Use Cases" (Addison-Wesley, 2000) — use case structure as a requirements formalization technique
- Gojko Adzic, "Specification by Example" (Manning, 2011) — living documentation approach; acceptance tests as the specification; bridges requirements and test work
- Lauesen, S. — EARS: Easy Approach to Requirements Syntax — cited in IREB training materials; requirement wording normalization using five syntactic patterns

### Priority 3 — Background

- Wikipedia — Requirements engineering — https://en.wikipedia.org/wiki/Requirements_engineering
- James Robertson and Suzanne Robertson, "Mastering the Requirements Process" (Addison-Wesley, 3rd ed.) — requirements process and template reference; useful for full project lifecycle requirements governance

## Handoff

- Classified and validated business and stakeholder requirements → hand off to System Analyst for functional specification.
- Functional and non-functional requirement candidates → hand off to System Analyst as a typed, normalized list with traceability.
- Measurement and reporting requirement candidates → hand off to Product Analyst or metric owner.
- Transition requirement candidates → hand off to Business Analyst (business-side), System Analyst (system migration), or Project Manager (delivery-side), depending on type.
- Requirements with unresolved conflicts → do not advance; create a decision task for the named resolution owner.
- Complete, validated requirements set with traceability → hand off to QA for test strategy derivation; QA receives requirements as inputs, not as a test plan.

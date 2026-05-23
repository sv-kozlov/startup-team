---
name: shared-documentation-management
description: Use when a role artifact — requirements, specification, process description, rule catalog, decision log, glossary, analysis memo, or product document — must be created, structured, updated, versioned, or made handoff-ready for a specific audience and decision context.
---

# Shared Documentation Management

## Purpose

Keep role-owned artifacts clear, traceable, current, and usable by the next owner or decision-maker. Documentation management is not document production for its own sake — it is the discipline of ensuring that every artifact has a stated purpose, a known audience, an identified owner, a link to its source decisions, and an update path. Artifacts without these properties degrade into stale reference material that blocks rather than enables downstream work.

## Use When

- Documentation is missing before a handoff and the receiving role cannot proceed without explicit context, scope, or decision records.
- An existing artifact is stale or ambiguous and is actively causing misalignment between roles.
- A role needs to structure content that will be reviewed, signed off, or used by multiple stakeholders with different needs.
- A change decision has been made but no artifact records why — resulting in the same question being raised repeatedly.
- A glossary, decision log, or traceability link is absent, causing different roles to use different definitions for the same term.
- A documentation set needs to be audited before a major release, handoff, or compliance review.
- A new team member or stakeholder must onboard using existing artifacts; the artifacts are not self-sufficient.

## Do Not Use When

- The task is authoring customer-facing public documentation, user manuals, or legal content → technical writers, legal, or operations own those; this skill produces internal team-facing artifacts.
- The task is product roadmap communication or executive-level strategy narrative → Product Manager owns that communication.
- The task is BI governance documentation (metric catalogue, data lineage, DWH documentation) → Data/BI or Product Analyst owns that.
- The task is architecture documentation (ADRs, C4 diagrams, system context diagrams) → System Architect or System Analyst owns those in their respective skills.
- The task is turning a documentation gap into new scope decisions — if writing the document reveals an undecided requirement, stop, surface the open question, and route to the owning role before proceeding.

## Inputs

- The purpose and audience of the artifact: who reads it, what decision it supports, and what action it enables.
- Source context: decisions already made, requirements already approved, rules already validated, diagrams already produced.
- The current state of the artifact: missing, stale, fragmented, or present but not handoff-ready.
- Adjacent artifacts that the document references or is referenced by (traceability chain).
- Known constraints: format requirements, tool conventions, publication channel, and review/approval path.

## Workflow

1. **State purpose, audience, and decision context.** Before writing or restructuring, answer: what decision does this document support? Who reads it and what action do they take after reading? An artifact without a stated purpose drifts into completeness theater — growing longer without becoming more useful.

2. **Apply the Diátaxis document type model.** Classify the artifact into one of four types and apply the corresponding structure:
   - *Tutorial*: learning-oriented, step-by-step, outcome is skill acquisition. Rare in product IT teams.
   - *How-to guide*: task-oriented, goal is completing a specific task. Example: "How to add a new payment method to the integration spec."
   - *Explanation / concept*: understanding-oriented, no immediate task. Example: "Why we use cursor pagination in this API."
   - *Reference*: information-oriented, consulted not read linearly. Example: rule catalog, glossary, API field descriptions.
   Mixing types in one artifact produces documents that serve no audience well.

3. **Structure content by scope, not by completeness.** Use sections that match what the reader needs: goal / scope / out of scope, definitions, the substantive content (requirements, rules, process steps, decisions, scenarios), assumptions and constraints, open questions, traceability links, and revision history. Do not pad sections to look thorough — a short accurate document is preferable to a long ambiguous one.

4. **Separate owned content from adjacent-role content.** Write what this role owns; link to or reference what another role owns. Copying another role's artifact inline creates a maintenance problem: the copy drifts from the source. Use cross-references with a stable identifier (document ID + section), not a copy.

5. **Add traceability and change context.** Every requirement or rule statement should trace to its source (stakeholder decision, policy reference, upstream requirement ID). Every non-trivial change to a document should have a dated change note: what changed, why, and who approved. Documents without traceability cannot be maintained under change.

6. **Apply a review and approval path.** Identify who reviews and who approves the artifact before it is used downstream. "Done" means the artifact has passed its review gate and the reviewer is recorded. Artifacts that are passed informally (no review record) create disputes later.

7. **Produce an update plan or handoff brief.** State how the artifact will be kept current: what triggers an update, who owns the update, and where the living version is stored. An artifact with no update plan is a future stale document.

## Outputs

- Structured documentation artifact: requirements document, specification, process description, rule catalog, decision log, glossary, analysis memo, or product document — with stated purpose, audience, scope, and traceability.
- Glossary or decision log: canonical term definitions and decision records with rationale and date.
- Traceability and change notes: links from artifact statements to source decisions and a revision history.
- Handoff-ready documentation brief: a summary that gives the receiving role everything it needs to proceed without re-discovering context.
- Update plan: trigger, owner, and storage location for the living version.

## Role Modes

### Business Analyst

Owns business-facing documentation: business requirements documents, process descriptions, business rule catalogs, glossaries, decision notes, and business-side change context documents. Structures these for audiences that include Product Manager, System Analyst, UX/UI, QA, and business stakeholders. Applies traceability from requirements back to business decisions and policy references. Does not author system specifications, API documentation, or technical design records — those go to System Analyst.

### Product Owner

Owns sprint-level and backlog-level documentation: story maps, backlog structure, acceptance criteria records, sprint goals, and product-level decision logs. Ensures that the backlog state is legible to the delivery team without requiring verbal explanation. Does not author requirements documents or process descriptions (Business Analyst), does not author product strategy narratives (Product Manager), and does not author system specifications (System Analyst).

### Product Manager

Owns product-level documentation: PRDs, product briefs, opportunity assessments, hypothesis records, metric trees, outcome roadmap explanations, and stakeholder alignment documents. Structures these so that Product Owner, System Analyst, UX/UI, and Engineering can derive their respective work without asking for repeated clarification. Does not author backlog or sprint documentation (Product Owner), system specifications (System Analyst), or delivery governance documents (Project Manager).

### Project Manager

Owns delivery governance documentation: project plans, milestone records, risk and issue logs, decision escalation records, status reports, dependency maps, and release coordination documents. Structures these for leadership, steering committees, and cross-team coordination. Does not author product strategy documents (Product Manager), system specifications (System Analyst), or business requirements documents (Business Analyst).

## Boundaries

- Does not publish customer-facing, legal, or operational content without review by the accountable content owner.
- Does not replace technical writing, user documentation, or BI governance documentation — those are distinct specializations with their own owners.
- Does not turn documentation cleanup into new scope decisions. If a documentation gap reveals an undecided requirement, surface it as an open question and route to the owning role.
- Does not produce living documentation from code (API references, auto-generated specs) — those are generated by Engineering tools and owned by the Engineering role.

## Named Patterns

### Good — Diátaxis-typed artifact
```
Artifact: Business Rules Reference — Payment Discount Engine
Type: Reference (consulted, not read linearly)
Audience: System Analyst (spec input), QA (test case input), Finance Controller (rule validation)
Scope: Rules BR-041 to BR-055 as validated 2025-05-15.
Out of scope: Implementation logic, API error handling, UI copy.
Structure: Rule ID | Type | Statement | Examples | Source | Validated by | Date
```
Audience, type, scope, and structure stated before content. Each reader knows whether this artifact answers their question.

### Bad — Omnibus requirements document
A 120-page Word document titled "Requirements" containing: business goals, user stories, process diagrams, API fields, test scenarios, UI mockup descriptions, and a glossary — all in narrative prose without section ownership or cross-references. Nobody reads it fully; every role extracts a different subset; updates are not synchronized.

### Good — Traceability chain
```
REQ-088: "The system must prevent order submission when the cart contains an out-of-stock item."
Source: Business Decision BRD-22 (2025-04-10, Product Manager approval).
Upstream: Business Rule BR-033 "An order may only contain items with inventory > 0."
Downstream: System Specification SYS-114, Acceptance Criteria AC-088, Test Case TC-312.
```
Trace from business decision through requirement to test. Any change to BRD-22 identifies every downstream artifact to update.

### Bad — Orphaned requirement
"The system must prevent order submission for out-of-stock items." No source reference. Challenged in UAT by a stakeholder who says "we never agreed to that." No evidence either way; the team debates from memory.

### Good — Decision log entry
```
DEC-031: Selected cursor-based pagination for order list API (2025-05-20).
Rationale: offset pagination degrades at scale (see ADR-018 by System Architect).
Approver: Product Manager. Contributors: System Analyst, Backend Lead.
Impact: Frontend must implement cursor-based navigation; affects UX flow for order history.
```
Decision recorded with rationale, approver, and downstream impact. Not re-opened at the next planning session.

### Bad — Decision by meeting memory
Architecture decision made in a stand-up. No record. Three months later, new team member implements offset pagination because "the spec didn't say otherwise." Tech debt traced back to an undocumented meeting.

### Good — Update trigger defined
```
This document is updated when: (a) a new business rule is validated, (b) an existing rule
is changed by Finance Controller, (c) a system specification change traces back to a rule
that differs from this catalog. Owner: Business Analyst. Living version: Confluence BA space,
page "Payment Discount Rules v{N}".
```
Update trigger, owner, and storage location explicit. Anyone who finds a discrepancy knows who to contact and where the source of truth is.

### Bad — Document without update plan
Requirements document published as v1.0 at project start. System changes approved in later sprints. Document never updated. By release, specification and implementation have diverged; which is correct is unknown.

### Good — Audience-scoped document with explicit exclusions
```
Document: Business Requirements — Discount Engine v1.2
Audience: System Analyst (spec input), QA (UAT scope), Finance Controller (rule validation).
Out of scope for this document: API error shapes (see SYS-114), UI copy (see UX spec DS-22),
  test automation plan (QA-owned).
Each reader section: Section 2 for Finance Controller, Section 3 for System Analyst,
  Section 4 for QA.
```
Audience is explicit. Each reader section is identified. Adjacent artifacts are referenced, not duplicated.

### Bad — One document for all audiences
A single "requirements" document serves business stakeholders, system analysts, QA, and engineering simultaneously. Each audience must read the whole document to find their relevant section. The document is simultaneously too detailed for business stakeholders and too vague for engineering.

## Sources

### Priority 1 — Method canon

- Daniele Procida, Diátaxis documentation framework — https://diataxis.fr/ (four-type model: tutorial, how-to, explanation, reference; the canonical framework for structuring technical documentation by audience need)
- ISO/IEC/IEEE 26515:2018 — Systems and software engineering — Developing information for users in an agile environment — https://standards.ieee.org/ieee/26515/6488/ (documentation practices in iterative delivery)
- ISO/IEC/IEEE 29148:2018 — Requirements engineering — https://standards.ieee.org/ieee/29148/6937/ (traceability and completeness criteria for requirements documentation)
- arc42 documentation framework — https://arc42.org/overview (template for architecture documentation; useful as a reference for section structure in system documentation)

### Priority 2 — Orientation

- Write the Docs — Documentation guide — https://www.writethedocs.org/guide/ (practitioner community guidance on documentation structure and practices)
- C4 model for software architecture — https://c4model.com/ (visual documentation model; orientation for structure of system-level artifacts)
- Atlassian — Confluence documentation best practices — https://www.atlassian.com/software/confluence/guides (practical guidance on page templates and documentation organization in team wikis)

### Priority 3 — Background

- IIBA BABOK Guide v3 — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/ (documentation tasks in business analysis: maintain requirements, prepare transition requirements)
- Wikipedia — Technical documentation — https://en.wikipedia.org/wiki/Technical_documentation

## Handoff

- When documentation review reveals an undecided requirement → surface as open question, route to the owning role (Business Analyst, Product Manager, or System Analyst) before proceeding.
- When an artifact needs a system specification elaboration not owned by this role → hand off to System Analyst with a link to the source artifact.
- When a completed artifact is ready for review and approval → route to the named reviewer and record the review outcome.
- When a documentation set is ready for downstream use → produce a handoff brief summarizing what changed, what the receiving role needs to know, and where the living version is stored.
- When the scope of the documentation task exceeds the current role's ownership boundary → stop and hand off rather than writing content that belongs to another role.

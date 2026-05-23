---
name: shared-business-rules
description: Use when business rules, decision logic, eligibility conditions, calculations, approval flows, validation constraints, or policy exceptions must be extracted from natural language, spreadsheets, legacy code, or stakeholder description and made explicit, testable, and ready for formalization or handoff.
---

# Shared Business Rules

## Purpose

Make implicit rules explicit — extracting them from policies, stakeholder statements, spreadsheets, and legacy behavior so they can be validated by a business owner, formalized into a system specification, and tested. A business rule states what is always true in the domain: a constraint, a calculation, a derivation, an eligibility condition, or an approval requirement. Rules are distinct from process steps (when to do something) and from implementation choices (how to do something technically).

## Use When

- Decision logic, eligibility, approval flows, calculations, or validation constraints are hidden in stakeholder language, policy documents, spreadsheets, or legacy code behavior.
- A requirement references a rule by name ("apply the standard discount") without stating the rule explicitly.
- Two sources describe the same rule differently, or rules conflict with each other and nobody has a single authoritative version.
- A decision table, rule catalog, or DMN-oriented brief is needed before system specification or test design begins.
- A rule change request arrives and the team needs to understand the current rule, its exceptions, its downstream implications, and the validation path.
- A calculation, derivation, or threshold must be stated as a formula with named variables, not as a narrative.

## Do Not Use When

- The task is legal interpretation of a regulation without an accountable business owner present → escalate to the business-side owner; do not interpret law independently.
- The task is implementing rules in a rules engine or workflow system → that is an engineering task; Business Analyst or System Analyst provides the rule spec, Engineering implements it.
- The task is designing the data model or API that enforces the rule → `data-modeling` or `shared-api-contract-design`; the rule spec feeds those, but ownership stays with the respective technical role.
- The task is deciding product policy (what the rules should be, not what they are) → Product Manager owns policy framing; Business Analyst structures what is approved.

## Inputs

- Policy documents, regulations, process notes, meeting notes, or existing specifications.
- Stakeholder verbal or written explanations and worked examples.
- Spreadsheets, configuration files, or legacy code containing embedded rule logic.
- Known terms, states, thresholds, actors, and systems involved.
- Counterexamples and known exceptions provided by business owners.

## Workflow

1. **Extract candidate rules using structured reading.** Read source material and mark every statement that constrains, derives, or decides — not statements that describe process steps or technical implementation. Use the sentence test: does the statement remain true regardless of process sequence? If yes, it is a rule candidate.

2. **Classify each rule by type.** Apply the OMG SBVR rule type taxonomy:
   - *Structural rule (constraint)*: something that must always hold (e.g., "An order amount must be greater than zero").
   - *Operative rule (behavioral)*: something the system must enforce (e.g., "A payment must not be approved if the account balance is insufficient").
   - *Derivation rule*: a calculated or derived fact (e.g., "Net amount equals gross amount minus applicable discounts").
   - *Decision rule*: determines an outcome from conditions (e.g., "If loyalty tier is Gold and order amount exceeds 10 000 RUB, apply 15% discount").
   - *Eligibility / qualification rule*: conditions for an entity to participate (e.g., "Only verified merchants may initiate payouts").

3. **Normalize wording.** Rewrite each rule in a single declarative sentence using domain vocabulary. Remove modal ambiguity: "should" → "must" or "may". Separate compound conditions (rule chains with AND/OR) into atomic rules. Assign a unique rule ID (e.g., `BR-014`).

4. **Attach examples and counterexamples.** For each rule, record at least one positive example (the rule fires / applies) and one negative example (the rule does not apply). For boundary conditions, record the boundary value explicitly. These become the basis for acceptance criteria.

5. **Identify conflicts, gaps, and priorities.** Check whether rules contradict each other, overlap, or leave condition combinations undefined. When two rules conflict, record the conflict as an open question with the business owner listed as decision owner. When a combination is undefined, flag it as a gap.

6. **Build the rule catalog or decision table.** For simple rule sets: a rule catalog with ID, type, statement, examples, exceptions, source, and owner. For complex multi-condition decision logic: a DMN-style decision table with condition columns and outcome columns. The format must be machine-checkable: no narrative in condition cells.

7. **Validate with the business owner.** Present the rule catalog or decision table to the owner who can confirm, reject, or qualify each rule. Record the validation date and version. Rules without business-owner validation are not ready for system specification.

8. **Hand off to the owning formalization role.** Validated rules go to System Analyst for formalization into system behavior specifications; rules affecting analytics go to the metric owner for measurement definitions; rules requiring workflow engine configuration go to Engineering with the rule spec as input.

## Outputs

- Rule catalog: each entry has ID, type, normalized statement, examples, counterexamples, exceptions, source reference, owner, and validation status.
- Decision table or DMN-oriented brief: condition columns, outcome columns, and rule priority where order matters.
- Conflict and gap log: unresolved contradictions and undefined condition combinations with a named decision owner.
- Handoff notes: which validated rules go to System Analyst, which to metric owner, which to Engineering.

## Role Modes

### Business Analyst

Owns the full business rule extraction and validation cycle. Sources rules from policy documents, stakeholder interviews, process notes, and legacy behavior. Uses domain vocabulary; confirms rule wording with business owners. Authors the rule catalog and decision tables as primary artifacts. Validates rules with the accountable business owner before handoff. Does not implement rules in systems, define system validation logic, or author API/data model specifications — those go to System Analyst as a handoff.

## Boundaries

- Does not provide legal interpretation of regulation without an accountable business owner as the validating party.
- Does not own implementation of rules in rules engines, workflow systems, or application code → Engineering owns the implementation.
- Does not own the data model or API contract that enforces the rule → System Analyst owns those in `data-modeling` and `shared-api-contract-design`.
- Does not decide what business policies should be → Product Manager frames policy direction; Business Analyst structures what has been approved by the accountable owner.
- Does not produce test cases or regression suites → QA Engineer derives test cases from the rule catalog; the rule catalog is the input, not the test plan.

## Named Patterns

### Good — Normalized atomic rule
```
BR-041 [Derivation]
Net invoice amount = gross amount – sum of applicable line discounts – order-level discount.
Variables: gross_amount (decimal, > 0), line_discount_i (decimal, >= 0), order_discount (decimal, >= 0).
Example: gross 10 000, line discount 500, order discount 1 000 → net 8 500.
Counterexample: gross 10 000, no discounts → net 10 000.
Source: Finance Policy v3.2, section 4.1. Owner: Finance Controller.
```
One rule, one ID, one type, formula with named variables, explicit examples. System Analyst can derive validation logic directly.

### Bad — Rule embedded in process narrative
```
After the manager reviews the invoice, the system should apply the relevant discounts
according to the applicable policy and calculate the final amount.
```
Three rules hidden in one sentence: who reviews, which discounts, which policy. "Relevant" and "applicable" are unresolved references. System Analyst cannot derive validation logic; QA cannot write a test case.

### Good — Decision table for multi-condition logic
```
| Loyalty Tier | Order Amount   | Discount |
|---|---|---|
| Gold         | >= 10 000 RUB  | 15%      |
| Gold         | < 10 000 RUB   | 5%       |
| Silver       | >= 10 000 RUB  | 8%       |
| Silver       | < 10 000 RUB   | 2%       |
| Bronze / None| any            | 0%       |
```
All condition combinations explicit; no undefined cells; boundary values stated. DMN-ready.

### Bad — Narrative multi-condition rule
```
Gold members get 15% off big orders. Silver members get less. Others don't get anything special
unless there's a promotion running.
```
"Big orders" undefined. "Less" is relative. "Unless there's a promotion" introduces an uncaptured exception class. Cannot be formalized without re-interviewing the business owner.

### Good — Conflict log entry
```
Conflict BR-041 vs BR-052:
BR-041 (Finance Policy v3.2) states order-level discount applies after line discounts.
BR-052 (Promotions Policy v1.4) states promotional discount applies before line discounts.
For orders with both a line discount and a promotion: application sequence is undefined.
Decision owner: Finance Controller + Promotions Manager. Due: 2025-06-10.
```
Named rules, source versions, defined conflict, named decision owner. The conflict does not become an assumption.

### Bad — Silent assumption
The analyst picks one interpretation (line discounts first, then promotions) and writes the spec without recording the conflict. Testing reveals the error when the promotions team runs UAT.

### Good — Validated rule with version
```
BR-041 v1.1. Validated by: Finance Controller (Anna K.). Date: 2025-05-15.
Change from v1.0: boundary changed from 5 000 RUB to 10 000 RUB per Finance Policy v3.2.
```
Validation event recorded; change history traceable.

### Bad — Unvalidated rule in specification
Rule catalog delivered to System Analyst as a draft without a record of business-owner review. System Analyst specifies behavior; developer implements. Business owner in UAT says the rule is wrong. Rework at the most expensive phase.

### Good — Compound rule separated into atomic rules
```
Original (compound): "Approved and active verified merchants with positive balance can initiate payouts."
Separated:
  BR-061 [Eligibility]: A merchant must have status = VERIFIED to initiate a payout.
  BR-062 [Eligibility]: A merchant must have status = ACTIVE to initiate a payout.
  BR-063 [Constraint]: A payout may only be initiated when merchant balance > 0.
  Combination: all three must hold simultaneously.
```
Three atomic rules, each independently testable. System Analyst can derive three separate validation checks.

### Bad — Compound rule kept as one statement
"Approved and active verified merchants with positive balance can initiate payouts."
Three conditions merged. System Analyst implements a single compound check. QA writes one test case. When the activation rule changes independently of the balance rule, the compound statement must be re-analyzed from scratch.

## Sources

### Priority 1 — Method canon

- OMG Semantics of Business Vocabulary and Business Rules (SBVR) v1.5 — https://www.omg.org/spec/SBVR/1.5/ (canonical rule type taxonomy: structural rule, operative rule, definitional rule, behavioral rule)
- OMG Decision Model and Notation (DMN) v1.4 — https://www.omg.org/spec/DMN/1.4/ (decision table structure, FEEL expression language, DRD notation)
- Ronald G. Ross, "Business Rule Concepts: Getting to the Point of Knowledge" (Business Rule Solutions, 5th ed.) — foundational text on rule classification, normalization, and rule catalogs
- IIBA BABOK Guide v3, Chapter 10: Business Rules Analysis technique — https://www.iiba.org/career-resources/a-business-analysis-professionals-foundation-for-success/babok/

### Priority 2 — Orientation

- Drools DMN Engine documentation — https://docs.drools.org/latest/drools-docs/docs-website/drools/DMN/index.html (practical DMN decision table and DRD reference)
- Decision Management Community — DMN by Example — https://dmcommunity.org/challenge/ (worked examples of decision tables and DRDs)
- Bruce Silver, "DMN Method and Style" (Cody-Cassidy Press, 2nd ed.) — practical guide to decision modeling with DMN notation

### Priority 3 — Background

- Object Management Group — Business Motivation Model (BMM) — https://www.omg.org/spec/BMM/ (situates business rules within business strategy and policy context)
- Wikipedia — Business rules approach — https://en.wikipedia.org/wiki/Business_rules_approach

## Handoff

- Validated rule catalog → System Analyst for formalization into `functional-specification` or `data-modeling`.
- Rules with metric or calculation implications → metric owner or Product Analyst.
- Rules requiring workflow engine or rules engine configuration → Engineering with the validated rule spec.
- Unresolved conflicts → return to the business owner decision-maker; do not advance to specification with open conflicts.
- When rules surface regulatory constraints that need legal interpretation → escalate to the accountable business owner; halt formalization until interpretation is confirmed.

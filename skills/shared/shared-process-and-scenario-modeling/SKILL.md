---
name: shared-process-and-scenario-modeling
description: Use when AS IS or TO BE work flows, user or system scenarios, actor interactions, handoff sequences, exception paths, or state transitions must be captured in a structured notation — BPMN, UML use case, UML sequence, UML state machine, or equivalent — to support requirements, specification, design, or test work.
---

# Shared Process and Scenario Modeling

## Purpose

Produce structured representations of how work flows, how users interact with systems, how systems interact with each other, and how exceptions are handled — in a notation precise enough for the next role to derive specifications, design decisions, or test cases from it. Modeling is not an end in itself; a model is ready when it answers the specific question it was created to answer and enables the next decision or handoff.

## Use When

- A change depends on understanding the current business process (AS IS) before the target process (TO BE) can be specified.
- Actors, systems, handoff points, exception paths, or decision branches in a process are not yet explicit and will cause misalignment between roles.
- A use case, user journey, system scenario, integration sequence, or entity state life cycle must be described before implementation begins.
- Two roles have different mental models of the same process and a shared diagram is needed to resolve the discrepancy.
- BPMN-style swim-lane diagrams, UML use case diagrams, sequence diagrams, or state machine diagrams are needed as inputs for specification, design, or test work.
- An exception path or compensating transaction is known to exist but has not been captured in any existing artifact.
- A process or scenario review has revealed inconsistencies that require the diagram to be refactored or extended.

## Do Not Use When

- The task is organization-wide business process governance, BPM platform configuration, or enterprise process architecture → Process Analyst or Enterprise Architect owns those; this skill produces targeted modeling artifacts for delivery team use.
- The task is UX visual design, wireframes, or interaction prototyping → UX/UI Designer owns those; process and scenario models are inputs to UX, not substitutes for it.
- The task is implementation design of algorithms, data structures, or internal component behavior → System Architect or Engineering owns those; this skill models observable flows, not internal implementation.
- The task is deployment pipeline or infrastructure flow → DevOps/SRE owns those.
- The model is growing indefinitely without answering the question it was created to answer → scope the model to the minimal granularity needed; do not model for completeness.

## Inputs

- The question the model must answer: which decision, specification gap, or design input triggered the modeling task?
- Process descriptions, user journey notes, requirements, policies, incident reports, or stakeholder-provided examples.
- Known actors, systems, triggers, inputs, outputs, decisions, exceptions, and handoffs.
- Existing models, diagrams, or specs that the new model must align with or extend.
- Target notation and tool conventions (BPMN 2.0, UML, or structured text for rapid capture).

## Workflow

1. **Define the modeling scope.** State: the starting trigger, the ending outcome, the actors and systems in scope, and what is explicitly out of scope. An unbounded model grows to include everything and answers nothing. The scope statement is part of the artifact.

2. **Capture the primary path (happy path) first.** Model the sequence of events, decisions, and handoffs that occur when everything works as intended. Name each step with a verb phrase in domain language. Identify the system or actor responsible for each step. Use the correct notation element: BPMN task (rectangle with rounded corners) for a unit of work, gateway (diamond) for a decision or fork, intermediate event (circle) for a signal or timer, pool/lane for a process owner boundary.

3. **Add alternative and exception paths.** For each gateway: model all named branches, including "payment fails," "approval rejected," "timeout," and "data invalid." An unmodeled exception is a specification gap. Model exception handling paths explicitly: compensation transactions, rollback sequences, error notifications, and escalation paths.

4. **Separate business process, user interaction, and system behavior views.** Use swim-lane boundaries to distinguish process owners. Business Analyst owns the inter-role business process view (BPMN with pools and lanes reflecting organizational roles). System Analyst owns the system scenario view (UML use case for functional scope; UML sequence for system-to-system interaction; UML state machine for entity life cycle). UX/UI Designer owns the user-interaction view; they receive the scenario as input and produce wireframes and prototypes as output.

5. **Review for completeness against a checklist.** Every model must have: at least one start event and one end event; no dangling flows (every arrow has a target); all gateways converging (no unmerged forks); all exception paths named and handled; all actors/systems in scope labeled; boundary with the out-of-scope world marked. Apply the checklist before handing off the model.

6. **Validate with the artifact's primary consumer.** Before the model is used as a specification or design input, review it with the consuming role (System Analyst, QA, UX/UI) to confirm it answers their question. Capture any changes as a revision note on the model.

7. **Produce the minimal set of diagrams that serves the next decision.** Do not produce diagrams for every possible view if only one is needed. State which decision each diagram enables; omit diagrams that do not contribute to a current decision.

## Outputs

- AS IS and/or TO BE process model: BPMN 2.0 swim-lane diagram with actors, systems, decisions, handoffs, and exception paths.
- Scenario or use-case brief: UML use case diagram or structured scenario description with preconditions, primary path, alternative paths, and postconditions.
- Sequence diagram: UML-style interaction diagram showing system-to-system or actor-to-system message flow and ordering.
- State machine: UML state diagram for entities with a significant life cycle (order, payment, document, session).
- Exception and compensation path notes: explicit handling for each named exception.
- Modeling scope statement: trigger, outcome, in-scope actors/systems, and out-of-scope boundaries.

## Role Modes

### Business Analyst

Owns the AS IS / TO BE business process view: inter-role workflows, actor responsibilities, organizational handoffs, business decision points, business exception paths, and process constraints. Uses BPMN swim-lane diagrams with pools representing organizational roles or teams. Does not model system-internal behavior, API call sequences, or entity state machines — those go to System Analyst. Does not produce wireframes or UX flows — those go to UX/UI Designer. Business process models are the primary input for System Analyst's system scenario work.

## Boundaries

- Does not own organization-wide business process governance, BPM platform configuration, or enterprise process architecture → Process Analyst or Enterprise Architect owns those.
- Does not own UX visual design, wireframe production, or user interaction prototyping → UX/UI Designer owns those; process and scenario models are inputs to UX work, not substitutes.
- Does not own architecture or implementation design → System Architect and Engineering own internal component behavior; this skill models observable flows.
- Does not produce deployment pipeline or infrastructure flow diagrams → DevOps/SRE owns those.

## Named Patterns

### Good — BPMN 2.0 swim-lane structure
```
Pool: Payment Process
  Lane: Customer
    [Start Event: Customer submits payment] → [Task: Submit payment form]
  Lane: Payment Service
    → [Task: Validate payment data]
    → [Gateway (XOR): Data valid?]
      YES → [Task: Charge payment provider]
           → [Gateway (XOR): Charge successful?]
             YES → [Task: Send confirmation] → [End Event: Payment complete]
             NO  → [Task: Record failure] → [End Event: Payment failed]
      NO  → [Task: Return validation error] → [End Event: Payment rejected]
```
All paths named. Exception paths (data invalid, charge failed) modeled explicitly. No dangling flows.

### Bad — Sequence described as prose
"The customer submits the form, then we validate it, and if everything is fine, we charge the provider and send a confirmation. If something goes wrong, we handle it appropriately."
"Handle it appropriately" is not a model. Two exception paths are undefined. QA cannot derive test cases from this.

### Good — Modeling scope statement
```
Scope: Payment submission flow from Customer Submit to payment record created in Order Service.
In scope: Customer, Frontend, Payment Service, Order Service.
Out of scope: Fraud detection (separate flow), refund process (separate flow), notification delivery (async event).
Start event: Customer clicks "Pay now".
End events: (1) Payment record created; (2) Payment rejected with error code; (3) Payment failed — provider error.
```
The model has exactly three defined outcomes. Out-of-scope items are named, not silently omitted.

### Bad — Infinite model scope
The analyst models the entire order lifecycle from registration through fulfillment, refunds, and archiving in one BPMN diagram. The diagram has 80+ tasks and 30+ gateways. No one can read it. QA cannot derive test cases. Subsequent updates break the model for unrelated reasons.

### Good — UML state machine for an entity life cycle
```
Order State Machine:
[Initial] → DRAFT (created)
DRAFT → SUBMITTED (customer confirms)
SUBMITTED → PAYMENT_PENDING (payment initiated)
PAYMENT_PENDING → CONFIRMED (payment successful)
PAYMENT_PENDING → PAYMENT_FAILED (payment rejected)
PAYMENT_FAILED → DRAFT (customer retries) | CANCELLED (timeout > 30 min)
CONFIRMED → PROCESSING (warehouse picks up)
PROCESSING → SHIPPED (carrier assigned)
SHIPPED → DELIVERED (delivery confirmed)
DELIVERED → CLOSED (post-delivery window expires)
Any state except CLOSED → CANCELLED (admin action with reason)
```
Every named state, every named transition, every terminal state. System Analyst can derive API contract states and QA can derive test coverage from this.

### Bad — State machine in narrative
"Orders can be in various states depending on what has happened. Payment states are handled by the payment system." No enumeration of states, no enumeration of transitions, no terminal states. System Analyst cannot derive the state field for the API contract.

### Good — Separation of views
Business Analyst produces: BPMN process diagram (business role swim lanes, 3 pools, 12 tasks).
System Analyst produces separately: UML sequence diagram (system-to-system calls, 4 participants, 8 messages).
UX/UI Designer produces separately: wireframe flow (7 screens, 3 error states).
Each artifact answers a different question and is owned by a different role.

### Bad — Mixed-view diagram
Single diagram showing BPMN tasks, UI mockup thumbnails, API call arrows, and database table references in the same diagram. No role can maintain it; updates require simultaneous coordination of BA, SA, and UX.

### Good — Model validated with a completeness checklist before handoff
```
Pre-handoff checklist for BPMN diagram:
[PASS] Exactly one Start Event and at least one named End Event per pool.
[PASS] All XOR gateways have all branches named and all branches converge.
[PASS] All exception paths are named and have an explicit handling step.
[PASS] All pools and lanes are labeled with role or system names.
[PASS] Scope statement present: trigger, outcome, in-scope actors, out-of-scope items.
[PASS] Model reviewed with System Analyst: confirmed as input for SYS-114.
```
No dangling flows, no unnamed branches, no implicit exceptions. The receiving role can derive test cases directly.

### Bad — Model handed off without completeness check
Analyst sends a BPMN diagram with an unmerged fork, two unnamed exception paths, and no scope statement. System Analyst cannot tell what the diagram covers or whether it is finished. Ambiguity propagates into the specification.

## Sources

### Priority 1 — Method canon

- OMG Business Process Model and Notation (BPMN) 2.0.2 — https://www.omg.org/spec/BPMN/2.0.2/ (normative specification; defines all BPMN elements, semantics, and notations)
- OMG Unified Modeling Language (UML) 2.5.1 — https://www.omg.org/spec/UML/2.5.1/ (normative specification for use case, sequence, state machine, and activity diagrams)
- Bruce Silver, "BPMN Method and Style" (Cody-Cassidy Press, 2nd ed., 2011) — practical methodology for BPMN modeling with explicit style rules; the most widely cited practitioner guide for BPMN

### Priority 2 — Orientation

- BPMN Quick Guide — Modeling best practices — https://www.bpmnquickguide.com/quickguide/bpmn-quick-guide/bpmn-modeling-best-practices.html (practitioner checklist for BPMN diagram quality)
- OMG Case Management Model and Notation (CMMN) 1.1 — https://www.omg.org/spec/CMMN/1.1/ (orientation for knowledge-intensive, non-sequential process modeling)
- Martin Fowler, "UML Distilled" (Addison-Wesley, 4th ed.) — concise reference on how to use UML diagrams practically in delivery teams

### Priority 3 — Background

- Wikipedia — Business process modeling — https://en.wikipedia.org/wiki/Business_process_modeling
- Wikipedia — Use case — https://en.wikipedia.org/wiki/Use_case

## Handoff

- AS IS process model complete → hand off to Product Manager (for TO BE framing) and Business Analyst (for gap analysis and rule extraction).
- AS IS / TO BE process model validated → hand off to System Analyst for system scenario modeling and use-case elaboration.
- System scenario and sequence diagrams complete → hand off to UX/UI Designer (user interaction flows) and QA (test scenario derivation).
- State machine complete → hand off to System Analyst for inclusion in API contract and functional specification.
- When model scope expands to cover organization-wide processes → flag as out of scope for this skill; hand off to Process Analyst or Enterprise Architect.

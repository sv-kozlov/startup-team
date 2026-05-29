# User Stories and Metrics Guidance

## User Stories

Default format:

```markdown
As a [user type],
I want to [action],
So that [benefit].
```

Use job stories when context and motivation matter more than persona:

```markdown
When [situation],
I want to [motivation],
So I can [expected outcome].
```

## Acceptance Criteria

Prefer `Given / When / Then`:

```markdown
- Given [context], when [action], then [expected result].
- Given [edge case], when [action], then [safe/system response].
```

Good criteria are:

- testable;
- specific;
- user-visible or system-verifiable;
- independent from implementation details;
- explicit about errors, empty states, permissions, and limits.

## INVEST Check

Stories should be:

- Independent;
- Negotiable;
- Valuable;
- Estimable;
- Small;
- Testable.

If a story is too broad, split it by workflow step, user role, platform, permission, or release phase.

## Priorities

- **P0 / Must-have**: required for MVP value or compliance.
- **P1 / Should-have**: important but can follow MVP.
- **P2 / Nice-to-have**: useful future enhancement.

## Metrics Selection

Choose metrics that connect to the product goal. Avoid vanity metrics unless they inform a decision.

### Common Metric Types

- Adoption: users who start using the feature.
- Activation: users who reach the first valuable outcome.
- Engagement: frequency or depth of use.
- Retention: users who return after initial use.
- Task success: completion rate, time to complete, error rate.
- Satisfaction: CSAT, NPS, qualitative feedback.
- Business impact: revenue, conversion, cost reduction, support reduction.
- Performance: latency, availability, throughput, quality scores.

### Frameworks

Use **HEART** for UX-heavy features:

- Happiness;
- Engagement;
- Adoption;
- Retention;
- Task Success.

Use **AARRR** for growth funnels:

- Acquisition;
- Activation;
- Retention;
- Revenue;
- Referral.

Use **OKRs** for strategic initiatives:

- Objective: qualitative direction;
- Key Results: 2-5 measurable outcomes.

Use a **North Star Metric** when one metric clearly represents delivered value.

## Metric Definition Template

```markdown
**Metric:** [name]
**Definition:** [exact calculation]
**Baseline:** [current value or TBD]
**Target:** [target value]
**Measurement:** [event, dashboard, query, survey, or manual review]
**Window:** [daily, weekly, monthly, launch + 30 days]
```

## AI Feature Metrics

For AI-powered features, consider:

- task completion rate;
- answer accuracy;
- citation accuracy;
- hallucination rate;
- human override rate;
- unsafe output rate;
- latency;
- cost per request;
- fallback rate;
- user satisfaction after AI interaction.

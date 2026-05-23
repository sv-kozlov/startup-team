---
name: analytics-communication-and-storytelling
description: Use when analytical findings must influence a product decision through a structured memo, experiment readout, executive narrative, or recommendation document. Triggers when raw analysis needs to become an artifact that drives a specific action by a specific audience.
family: advanced
profile_level: Senior+
---

# Analytics Communication and Storytelling

## Purpose

Turn analytical evidence into decision-ready artifacts — concise memos, experiment readouts, and executive narratives — so stakeholders act on the right conclusion with accurate confidence in what the data does and does not say.

## Use When

- Writing an analytical memo, executive summary, or product recommendation based on completed analysis.
- Structuring an experiment readout for a ship / iterate / rollback decision.
- Turning messy, preliminary, or multi-source findings into a clear decision-oriented document.
- Explaining analytical limitations, data caveats, or confidence levels to non-analyst audiences.
- Adapting the depth and framing of a finding to different audiences (product team, engineering, leadership, finance).

## Do Not Use When

- The underlying analysis has not been completed and validated → complete the analysis first using the appropriate skill.
- The task requires producing charts, dashboards, or BI reports → `sql-and-data-analysis`.
- The final decision ownership belongs to the Product Manager; this skill produces the recommendation, not the decision.
- The task requires presenting strategy, roadmap, or portfolio trade-offs → `product-manager`.

## Inputs

- Completed analysis: question, findings, metrics, charts or tables.
- Decision options the audience is weighing.
- Audience: role, context, prior knowledge, and action they need to take.
- Known caveats, data limitations, and confidence level.
- Deadline and format constraints.

## Workflow

1. **Start with the decision, not the data.** Write the bottom-line recommendation in the first sentence. The audience should know what you think before reading the evidence.

2. **Structure with the So What — Because — Therefore pattern.**
   - So What: the recommendation or conclusion.
   - Because: the key evidence (2–4 findings that are sufficient; not all findings).
   - Therefore: the next action and owner.

3. **Select only the evidence that supports the decision.** Every chart and number included should change the reader's belief or confidence. If removing a chart would not change the recommendation, cut it.

4. **State confidence level and limitations explicitly.**
   Do not hide uncertainty. Use clear language:
   - "This is directional; underpowered for a formal decision."
   - "Observational; causal claim would require an experiment."
   - "Based on 3 weeks of data; seasonality not yet controlled."

5. **Adapt to the audience.**
   - Product team: mechanism, metric detail, segment breakdown, next analytical step.
   - Leadership / executive: business impact, risk, and recommended action — minimal methodology.
   - Engineering: data quality notes, query logic, instrumentation requirements.
   - Finance: unit economics impact, assumptions, sensitivity range.

6. **End with clear next actions.** State who does what by when. Handoffs are named roles, not vague "follow-up needed."

7. **Avoid the data dump.** A document that presents all data without a conclusion is not an analytical artifact — it is a backup for the author. The reader's job is not to do the analysis again.

## Outputs

- Analytical memo (structured: recommendation → evidence → limitations → next actions)
- Experiment readout (SRM check, effect size, CI, guardrail table, recommendation)
- Executive summary (1-page: decision context, finding, impact, risk, action)
- Recommendation and next-action list with named owners

## Named Patterns

**Good: bottom-line-up-front memo**
```
## Recommendation
Ship the new checkout flow to 100%. Experiment shows +4pp conversion (95% CI: +2pp–+6pp),
guardrails stable, SRM clean.

## Evidence
- Primary: checkout_conversion_rate: +4.0pp absolute, p = 0.002 (n = 12 000/variant, 14 days).
- Guardrail: checkout_latency_p99 = 620ms (below 800ms threshold). No regression.
- Guardrail: payment_failure_rate = 1.8% (baseline 1.9%). Stable.

## Limitations
- Effect measured on mobile web; desktop not yet in experiment. Separate rollout recommended.
- Holiday week overlap (Dec 22–28): seasonal spike may inflate AOV in both arms equally.

## Next Actions
- PM: approve production rollout by [date].
- Engineering: full rollout in [date] deployment.
- Analyst: monitor primary + guardrails for 7 days post-rollout.
```

**Bad: data dump without conclusion**
```
## Results
Control conversion: 10.2%. Treatment conversion: 14.2%. P-value: 0.002.
Average order value control: $48. Treatment: $47. Session duration control: 4m 12s. Treatment: 4m 08s.
Latency p99 control: 615ms. Treatment: 622ms.
[14 additional tables with no interpretation or recommendation]
```
Reader must reconstruct the conclusion. High cognitive load; different stakeholders draw different conclusions.

**Good: explicit confidence and limitation**
```
This analysis is observational and cannot establish causation. The correlation between
feature X adoption and D30 retention (+12pp) is consistent with our hypothesis,
but alternative explanations (selection bias: users who adopt feature X are already
more engaged) have not been ruled out. Causal validation requires an A/B test.
```

**Bad: implied causality from correlation**
```
Users who use feature X have 12pp higher D30 retention. Feature X drives retention.
We should prioritize feature X adoption.
```
No acknowledgment that this is observational; selection bias not mentioned; causal claim unwarranted.

**Good: audience-adapted depth**
Leadership version: "The checkout experiment adds estimated $180K/month incremental revenue with low execution risk. Recommend full rollout."
Product team version: same memo plus segment breakdown, methodology notes, and next analytical steps.

**Bad: one version for all audiences**
Dense statistical methodology shared in an executive meeting; decision-makers disengage. Or stripped-down summary shared with the product team; engineers can't validate the data logic.

**Good: pre-registered before-and-after framing**
"We defined success before the experiment launched: primary significant AND guardrails stable AND SRM clean. All three conditions met. Recommendation: ship."

**Bad: HARKing (Hypothesizing After Results are Known)**
"After seeing the results, we noticed that female users in the 25–34 cohort show a 9pp lift. Let's call this the primary finding." — This is a false positive discovered through multiple comparisons.

## Boundaries

- Does not own the final ship / launch / cancel decision → `product-manager`.
- Does not produce dashboards or recurring BI reports → `sql-and-data-analysis`.
- Does not overstate certainty or hide data limitations in the artifact.
- Does not replace the analysis itself; produces the communication layer on top of completed analysis.

## Sources

**Priority 1 — canonical**
- Kohavi, R. et al., Trustworthy Online Controlled Experiments (Cambridge, 2020): https://www.exp-platform.com/Documents/2013-02-CACM.pdf
- Tableau, Data Storytelling Guide: https://www.tableau.com/learn/articles/data-storytelling
- Cole Nussbaumer Knaflic, Storytelling with Data: https://www.storytellingwithdata.com/

**Priority 2 — practitioner**
- Microsoft Power BI Data Storytelling: https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-storytelling
- Andrew Chen, How to write analytical memos: https://andrewchen.com/
- Lenny Rachitsky, Writing effective product analysis: https://www.lennysnewsletter.com/

**Priority 3 — supplementary**
- Barbara Minto, The Pyramid Principle (BLUF narrative structure).
- Crystal Widjaja on analytical communication at Gojek: https://www.reforge.com/artifacts/

## Handoff

```
To: product-manager
Task: Review the analytical memo and make the ship / iterate / rollback decision.
Context: Memo complete with recommendation, evidence, limitations, and next actions.
Inputs: Analytical memo or experiment readout (attached).
Expected artifact: Go/no-go decision logged with rationale.
Acceptance criteria: Decision references the stated limitations and confidence level.
```

```
To: engineering
Task: Review the data-quality notes and confirm the instrumentation issues are understood.
Context: Memo identified [specific tracking gap]; engineering needs to assess fix timeline.
Inputs: Data-quality section of the memo; affected event specs.
Expected artifact: Confirmation of root cause and fix timeline.
Acceptance criteria: Fix timeline confirmed or escalated to data-engineer.
```

---
name: data-and-reporting-requirements
description: Use when defining business meaning, audience, questions, terms, calculations, filters, grain, and acceptance needs for reports, metrics, dashboards, exports, or operational data use.
---

# Data and Reporting Requirements

## Purpose

Define what business users need to know from data and reports without taking ownership of BI implementation, data pipelines, or metric governance.

## Use When

- A report, export, dashboard, or metric request lacks business definition.
- Calculations, filters, grain, dimensions, or audience are unclear.
- Data/BI or Product Analyst needs business context.

## Inputs

- Reporting request, business question, audience, decisions, examples, existing reports, and terms.
- Source-system context, data constraints, and known metric owners.
- Acceptance expectations.

## Workflow

1. Identify audience, decision, cadence, and business question.
2. Define terms, entities, grain, filters, dimensions, calculations, and exclusions in business language.
3. Capture examples, edge cases, privacy or compliance constraints, and acceptance checks.
4. Separate business definition from data modeling, dashboard design, and pipeline implementation.
5. Hand off metric methodology to Product Analyst and BI implementation to Data/BI.

## Outputs

- Reporting requirements brief.
- Business definitions and calculation intent.
- Acceptance examples and open questions.
- Handoff notes for Data/BI or Product Analyst.

## Boundaries

- Does not own dashboard implementation or DWH modeling.
- Does not own product metric methodology unless assigned by Product Analyst.
- Does not define data pipeline or source integration design.

## Sources

- IIBA BABOK key concepts and techniques: https://www.iiba.org/knowledgehub/business-analysis-body-of-knowledge-babok-guide/key-concepts/
- IEEE/ISO/IEC 29148 requirements engineering standard: https://standards.ieee.org/content/ieee-standards/en/standard/29148-2018.html

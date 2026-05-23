---
name: ci-cd-test-integration
description: Use when wiring test suites into a CI/CD pipeline — designing test stages, configuring parallel execution, setting flakiness budgets, defining test gates, and integrating test reporting (Allure or equivalent). QA owns test stage logic; DevOps/SRE owns the CI/CD platform.
family: method
profile_level: Senior+
---

# CI/CD Test Integration

## Purpose

Make automated tests a reliable gate in the delivery pipeline: fast enough to not block developers,
stable enough to trust, and informative enough to diagnose failures without manual log diving.
A test pipeline that is slow, flaky, or opaque is worse than no pipeline because it trains the team to ignore it.

## Use When

- Adding automated tests to a CI pipeline for the first time.
- Restructuring a slow or unreliable test pipeline.
- Setting a flakiness budget and enforcement policy for the test suite.
- Designing parallel execution for a large test suite.
- Integrating test reporting tools (Allure, JUnit XML, or equivalent) into CI.
- Defining which test gate blocks a merge vs blocks a deployment.

## Do Not Use When

- Designing the test automation framework code -> `test-automation-framework`.
- Designing which tests to run -> `test-design-and-coverage`.
- CI/CD platform infrastructure setup (runner provisioning, secrets management) -> `devops-sre`.

## Inputs

- Current test suite structure and execution time profile.
- CI/CD toolchain (GitHub Actions, GitLab CI, Jenkins, or equivalent).
- Test categories and their target environments.
- Current flakiness rate per test or suite.
- NFR for pipeline execution time (e.g., PR check must complete in under 10 minutes).

## Workflow

1. Map test categories to pipeline stages. Not all tests run on every event:
   - On every commit/PR: fast unit and component tests, API smoke tests.
   - On merge to main: full API test suite, integration tests, smoke e2e.
   - Nightly or pre-release: full regression, performance tests, extended e2e.
   Separating fast gates from slow gates keeps the PR feedback loop responsive.

2. Design parallel execution. Identify tests that can run concurrently (no shared mutable state).
   Shard large suites across multiple runners. Set a target wall-clock time for each stage.

3. Define the flakiness budget. Measure current flakiness rate per test (flaky failures / total runs
   over a rolling 30-day window). Set a budget:
   - Suite-level: flakiness rate must be below 1%.
   - Individual test: a test with > 5% flakiness rate must be quarantined until fixed.
   Quarantine means: move to a non-blocking stage, create a fix ticket, set SLA for resolution.

4. Set test gate policy:
   - Blocking gate: failure prevents merge or deployment. Only for fast, stable suites.
   - Non-blocking gate (informational): failure is reported but does not block. For slow or
     exploratory suites, or for suites with known instability being addressed.
   - Required gate: must pass before deployment to production (full regression, smoke).

5. Integrate test reporting. Configure the CI job to produce JUnit XML or Allure results.
   Publish the report as a CI artifact. For Allure: configure history (trend charts) and
   categories (failed, broken, passed, skipped).

6. Configure retry policy carefully. One retry on failure is acceptable for transient
   environment issues. More than one retry masks real instability. Retries must be logged
   and counted toward flakiness metrics, not hidden.

7. Configure test environment access in CI. Tests that need a running service use:
   - Docker Compose for local dependencies (DB, message broker, mock services).
   - Shared integration environment for external dependencies (with isolation per test run).
   Never test against production from CI.

8. Review the pipeline execution time monthly. If the PR check exceeds 10 minutes, identify
   the slowest stage and optimize: parallelize, move slow tests to nightly, or drop redundant tests.

## Outputs

- CI pipeline configuration file with test stages (YAML for GitHub Actions, GitLab CI, etc.).
- Flakiness tracking report: per-test failure rate, quarantine list, fix status.
- Test gate policy document: which gates block what events.
- Allure or JUnit XML report integration configuration.
- Parallel execution plan: sharding strategy and target execution times per stage.

## Named Patterns

### Good — Staged pipeline with fast gate first

```yaml
# GitHub Actions example (structural pattern)
jobs:
  fast-tests:
    name: Unit and API smoke
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run unit and API smoke tests
        run: pytest tests/unit tests/api/smoke -x --timeout=60
        # target: < 3 minutes

  integration-tests:
    name: Integration suite
    needs: fast-tests          # only run if fast-tests pass
    runs-on: ubuntu-latest
    steps:
      - name: Run integration tests
        run: pytest tests/integration --timeout=120
        # target: < 8 minutes
```

Fast tests give developers a 3-minute feedback signal. Integration runs only on green fast gate.

### Bad — All tests in one job, no stages

```yaml
steps:
  - run: pytest tests/  # 45-minute run on every PR commit
```

Developers wait 45 minutes for feedback. They stop pushing small commits. Branch drift
increases. The pipeline becomes a bottleneck, not a quality gate.

### Good — Flakiness budget enforcement with quarantine

```yaml
# .github/workflows/nightly-flakiness-check.yml
steps:
  - name: Run suite 10 times and report flakiness
    run: |
      for i in $(seq 1 10); do pytest tests/regression --json-report; done
      python scripts/flakiness_report.py  # flags tests > 5% failure rate
  - name: Fail if any test exceeds flakiness budget
    run: python scripts/check_flakiness_budget.py --budget 0.05
```

Tests exceeding the budget are quarantined automatically and a fix ticket is created.

### Bad — Retrying failures silently

```yaml
steps:
  - run: pytest tests/ --retries 3  # retry up to 3 times without logging
```

A test that fails 3 times and then passes on the 4th retry is counted as "green."
Flakiness is hidden. The team ships broken tests that occasionally fail in production-adjacent scenarios.

### Good — Test reporting with history

```yaml
# GitLab CI example
test:
  script:
    - pytest tests/ --alluredir=allure-results
  artifacts:
    when: always
    paths:
      - allure-results/
    expire_in: 30 days

pages:
  script:
    - allure generate allure-results --clean -o public
  artifacts:
    paths:
      - public
```

Every CI run produces an Allure report with trend history. QA can see which tests have been
failing for 3 consecutive runs vs a one-off failure.

### Bad — Test output as plain text in CI log

No artifact. Failures require scrolling through thousands of lines of log output. Trend
analysis is impossible. Post-incident coverage analysis takes hours.

### Good — Docker Compose for isolated dependencies in CI

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    ports:
      - "5432:5432"
  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

Each CI run gets a fresh, isolated Postgres and Redis. Tests do not interfere with each other.
No shared staging database used for CI runs.

### Bad — Tests pointing to shared staging database in CI

Two developers open PRs simultaneously. Both run integration tests against the same staging DB.
Test data conflicts cause random failures. Both blame "the environment." Root cause is shared state.

### Good — Non-blocking gate for exploratory-adjacent suites

```yaml
extended-regression:
  continue-on-error: true   # does not block the deployment
  steps:
    - run: pytest tests/extended --timeout=300
  # Failure is reported in the PR comment but does not block merge
```

The suite is informational while being stabilized. Failures are visible and tracked without
blocking the team.

### Bad — No gate distinction

Every test stage is blocking. A single flaky e2e test in the extended regression blocks all
deployments. The team starts skipping or commenting out tests to unblock the pipeline.

## Boundaries

- Owns test stage design, parallel execution, flakiness budgets, test gate policy, and reporting integration.
- Does not own CI/CD platform setup (runners, secrets, infra) -> `devops-sre`.
- Does not own test automation framework code -> `test-automation-framework`.
- Does not own which tests to include in the suite -> `test-design-and-coverage`.

## Sources

### Priority 1 — CI/CD documentation and testing standards

- GitHub Actions documentation — https://docs.github.com/en/actions
- GitLab CI/CD documentation — https://docs.gitlab.com/ee/ci/
- Allure Framework documentation — https://allurereport.org/docs/
- ISTQB Advanced Level Test Automation Engineer Syllabus (pipeline section) — https://www.istqb.org/certifications/advanced-test-automation-engineer

### Priority 2 — Orientation

- Martin Fowler: Continuous Integration — https://martinfowler.com/articles/continuousIntegration.html
- Continuous Delivery (Humble, Farley): Test stages and deployment pipeline — book reference
- Google Testing Blog: Testing in CI — https://testing.googleblog.com/

### Priority 3 — Background

- ThoughtWorks Technology Radar — https://www.thoughtworks.com/radar
- Software Engineering at Google: Continuous Integration chapter — https://abseil.io/resources/swe-book

## Handoff

- CI/CD platform provisioning, runner setup, secrets management -> `devops-sre`.
- Test automation framework restructuring (code changes) -> `test-automation-framework`.
- Which test scenarios belong in which stage -> `test-strategy-and-planning` + `test-design-and-coverage`.
- Performance test pipeline integration -> `performance-and-load-testing`.

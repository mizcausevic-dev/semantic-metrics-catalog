# Why We Built This

**semantic-metrics-catalog** comes from a familiar analytics failure mode: the
business can repeat a metric name with confidence long after the underlying
definition has started to drift. Revenue, finance, support, and product teams
all believe they are discussing the same KPI while quietly carrying different
assumptions about grain, freshness, exclusions, or ownership. That ambiguity is
expensive for humans, and it is even worse for AI systems that only see
fragments of the context.

Existing tools help, but most of them stop short of the real operator problem.
Dashboards show the number, not the full contract behind it. dbt models and BI
semantic layers hold important logic, but that logic often stays buried inside
engineering artifacts that non-engineering teams rarely inspect. Documentation
pages help until they age out. The missing layer is a governed publication
surface that treats metrics like durable interfaces instead of private
implementation details.

We built **semantic-metrics-catalog** to make that interface visible. The repo
is intentionally opinionated: every metric carries an owner, a contract version,
a freshness posture, a top risk, and policy flags that explain whether the
definition is stable enough for board decks, finance workflows, or AI retrieval.
The goal is not just better metadata. The goal is to reduce the number of times
an organization discovers too late that the same KPI meant different things in
different rooms.

The design philosophy is straightforward:

- **operator-friendly** so analytics, RevOps, and BI leads can review drift fast
- **contract-first** so the metric definition is more visible than the chart
- **AI-legible** so retrieval systems have structured definitions to ground on
- **lightweight** enough to fit alongside real warehouses, semantic layers, and
  dashboard stacks without pretending to replace them

The sample data leans into real pressure points: revenue coverage, retention,
support SLAs, product usage, and onboarding velocity. Those are the metrics that
usually matter to senior operators and executives, and they are also the ones
most likely to get miscommunicated once they spread across decks, dashboards,
and copilots.

Next on the roadmap is deeper lineage modeling, semantic diff history, and
warehouse-aware validation so the catalog can show not only what the metric
means, but how much trust the underlying pipeline still deserves.

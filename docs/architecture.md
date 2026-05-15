# Semantic Metrics Catalog Architecture

## Intent

This repo makes metric definitions behave like governed contracts instead of
loosely documented dashboard labels.

It packages three surfaces together:

- a human-readable catalog for metrics, formulas, and ownership
- a contract board for semantic drift, policy flags, and freshness issues
- a machine-readable `DataCatalog` export for AI and retrieval systems

## Flow

1. `app/data/sample_metrics_catalog.yml` stores the source-of-truth contract set.
2. `app/services/semantic_service.py` loads metrics, computes owner lanes, and
   derives contract posture summaries.
3. `app/main.py` exposes:
   - HTML overview, catalog, contracts, owners, and docs pages
   - JSON APIs for metrics, owners, and contract review
   - structured JSON-LD export
4. `app/render.py` generates the visual proof pages and static screenshot scenes.
5. `scripts/render_readme_assets.py` captures repo-owned HTML scenes into PNG
   screenshots for the README.

## Core surfaces

- `/`
  - Overview of metric count, flagged contracts, freshness breaches, and policy pressure
- `/catalog`
  - Metric catalog with formula contracts, owners, tiers, and dimensions
- `/contracts`
  - Review board for contract status, top risk, and policy flags
- `/owners`
  - Ownership lanes showing accountability distribution and focus metrics
- `/docs`
  - API summary and sample payload
- `/api/catalog`
  - Full catalog payload
- `/api/contracts`
  - Contract review payload
- `/api/owners`
  - Ownership-lane payload
- `/semantic/catalog.jsonld`
  - Machine-readable semantic export

## Why this matters

Analytics systems usually fail semantically before they fail technically. Teams
reuse metric names, executive decks carry stale meanings forward, and AI systems
guess from surface context instead of canonical definitions.

This repo makes those problems legible by attaching:

- explicit owner lanes
- contract versions
- freshness posture
- policy flags
- formula visibility

to every metric published through the catalog.

## Validation

- `py -3.11 -m unittest discover -s tests`
- `py -3.11 scripts\run_demo.py`
- `py -3.11 scripts\smoke_check.py`
- `py -3.11 scripts\render_readme_assets.py`

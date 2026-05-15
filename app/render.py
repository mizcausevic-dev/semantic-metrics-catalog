from __future__ import annotations

from html import escape
from pathlib import Path

from app.services.semantic_service import build_service

service = build_service()


def shell(title: str, eyebrow: str, body: str, current: str) -> str:
    summary = service.summary()
    nav = [
        ("/", "Overview", "overview"),
        ("/catalog", "Catalog", "catalog"),
        ("/contracts", "Contracts", "contracts"),
        ("/owners", "Owners", "owners"),
        ("/docs", "Docs", "docs"),
    ]
    nav_links = "".join(
        f'<a class="nav-link {"active" if key == current else ""}" href="{href}">{label}</a>'
        for href, label, key in nav
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)}</title>
    <style>
      :root {{
        color-scheme: dark;
        --bg: #06101b;
        --panel: #091728;
        --panel-2: #0e1e33;
        --line: rgba(255,255,255,0.08);
        --text: #edf4ff;
        --muted: #92a7c7;
        --blue: #76c8ff;
        --indigo: #6b79ff;
        --green: #48d59b;
        --amber: #f5c16b;
        --red: #ff7f92;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Inter, "Segoe UI", system-ui, sans-serif;
        background:
          radial-gradient(circle at top left, rgba(118,200,255,0.14), transparent 24%),
          linear-gradient(180deg, #03070c 0%, var(--bg) 100%);
        color: var(--text);
      }}
      a {{ color: inherit; text-decoration: none; }}
      .wrap {{ max-width: 1360px; margin: 0 auto; padding: 28px; }}
      .topbar {{
        display: flex; justify-content: space-between; align-items: center; gap: 18px;
        padding: 20px 0 16px; border-bottom: 1px solid var(--line);
      }}
      .brand strong {{ display: block; font-size: 14px; }}
      .brand span {{
        display: block; margin-top: 4px; color: var(--blue); font-size: 10px;
        letter-spacing: .2em; text-transform: uppercase;
      }}
      .status {{
        display: inline-flex; align-items: center; gap: 10px; padding: 10px 14px;
        border-radius: 999px; border: 1px solid rgba(118,200,255,0.15);
        background: rgba(118,200,255,0.07); color: #d8ebff; font-size: 11px;
        text-transform: uppercase; letter-spacing: .16em; font-weight: 800;
      }}
      .dot {{ width: 8px; height: 8px; border-radius: 999px; background: var(--blue); box-shadow: 0 0 12px rgba(118,200,255,0.85); }}
      .hero {{
        margin-top: 24px; padding: 28px; border: 1px solid var(--line); border-radius: 28px;
        background: linear-gradient(180deg, rgba(9,23,40,0.97), rgba(6,16,28,0.96));
        box-shadow: 0 24px 54px rgba(0,0,0,0.26);
      }}
      .eyebrow {{
        color: var(--blue); font-size: 11px; letter-spacing: .28em; text-transform: uppercase;
        font-weight: 800; margin-bottom: 16px;
      }}
      h1 {{
        margin: 0; font-size: clamp(40px, 5vw, 72px); line-height: .94;
        font-family: Georgia, "Times New Roman", serif; letter-spacing: -.05em;
      }}
      .hero p {{
        margin: 14px 0 0; max-width: 900px; color: var(--muted); font-size: 18px; line-height: 1.56;
      }}
      .hero-strip {{
        display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 14px; margin-top: 24px;
      }}
      .hero-kpi {{
        padding: 16px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.03);
      }}
      .hero-kpi .label, .section-kicker, .micro {{
        color: #7388a6; font-size: 10px; letter-spacing: .16em; text-transform: uppercase; font-weight: 800;
      }}
      .hero-kpi .value {{ margin-top: 8px; font-size: 30px; font-weight: 900; }}
      .callout {{
        margin-top: 18px; padding: 18px 20px; border-radius: 18px; background: rgba(0,0,0,0.18);
        border: 1px solid rgba(255,255,255,0.06);
      }}
      .callout strong {{
        display: block; color: var(--amber); font-size: 10px; letter-spacing: .18em; text-transform: uppercase;
        margin-bottom: 8px;
      }}
      .nav-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; }}
      .nav-link {{
        padding: 10px 14px; border-radius: 999px; border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03); color: #b1c1d8; font-size: 11px; font-weight: 800;
        text-transform: uppercase; letter-spacing: .12em;
      }}
      .nav-link.active {{ color: var(--amber); border-color: rgba(245,193,107,0.18); background: rgba(245,193,107,0.08); }}
      .section {{
        margin-top: 24px; border-radius: 26px; border: 1px solid var(--line);
        background: var(--panel); overflow: hidden; box-shadow: 0 18px 44px rgba(0,0,0,0.22);
      }}
      .section-head {{ padding: 22px 24px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
      .section-head h2 {{ margin: 8px 0 0; font-family: Georgia, "Times New Roman", serif; font-size: 26px; letter-spacing: -.03em; }}
      .section-head p {{ margin: 10px 0 0; color: var(--muted); font-size: 15px; line-height: 1.55; max-width: 920px; }}
      .section-body {{ padding: 24px; }}
      .grid-4, .grid-3, .grid-2 {{ display: grid; gap: 18px; }}
      .grid-4 {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
      .grid-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .grid-2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .card {{
        border-radius: 20px; padding: 18px; border: 1px solid rgba(255,255,255,0.06);
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(0,0,0,0.08));
      }}
      .card .value {{ margin-top: 10px; font-size: 34px; font-weight: 900; }}
      .card p {{ margin: 10px 0 0; color: var(--muted); font-size: 14px; line-height: 1.45; }}
      table {{ width: 100%; border-collapse: collapse; }}
      th, td {{ text-align: left; padding: 14px 12px; border-bottom: 1px solid rgba(255,255,255,0.06); vertical-align: top; }}
      th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: .12em; }}
      td {{ font-size: 14px; color: var(--text); }}
      .tag {{
        display: inline-flex; align-items: center; justify-content: center; padding: 7px 10px;
        border-radius: 999px; font-size: 10px; font-weight: 900; text-transform: uppercase; letter-spacing: .14em;
      }}
      .healthy {{ color: var(--green); background: rgba(72,213,155,0.12); border: 1px solid rgba(72,213,155,0.12); }}
      .watch {{ color: var(--amber); background: rgba(245,193,107,0.12); border: 1px solid rgba(245,193,107,0.12); }}
      .breached {{ color: var(--red); background: rgba(255,127,146,0.12); border: 1px solid rgba(255,127,146,0.12); }}
      .pill-stack {{ display: flex; flex-wrap: wrap; gap: 8px; }}
      .pill {{
        display: inline-flex; padding: 7px 10px; border-radius: 999px; background: rgba(118,200,255,0.09);
        color: var(--blue); font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .12em;
      }}
      .code {{
        border-radius: 22px; border: 1px solid rgba(255,255,255,0.08); background: rgba(2,7,14,0.88); overflow: hidden;
      }}
      .code-head {{ padding: 16px 18px; border-bottom: 1px solid rgba(255,255,255,0.08); display: flex; justify-content: space-between; align-items: center; }}
      .lights {{ display: flex; gap: 8px; }}
      .lights i {{ width: 11px; height: 11px; border-radius: 999px; display: block; }}
      .lights i:nth-child(1) {{ background: rgba(255,127,146,0.55); }}
      .lights i:nth-child(2) {{ background: rgba(245,193,107,0.55); }}
      .lights i:nth-child(3) {{ background: rgba(72,213,155,0.55); }}
      pre {{ margin: 0; padding: 18px; color: #d9e8fb; font-size: 13px; line-height: 1.56; white-space: pre-wrap; overflow: auto; font-family: "Cascadia Code", Consolas, monospace; }}
      .footer {{ display: flex; flex-wrap: wrap; gap: 18px; margin: 18px 0 8px; color: #7388a6; font-size: 10px; text-transform: uppercase; letter-spacing: .16em; }}
      .footer strong {{ color: #c1d0e3; }}
      @media (max-width: 1080px) {{
        .hero-strip, .grid-4, .grid-3, .grid-2 {{ grid-template-columns: 1fr; }}
        .topbar {{ flex-direction: column; align-items: flex-start; }}
      }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="topbar">
        <div class="brand">
          <strong>Semantic Metrics Catalog</strong>
          <span>{eyebrow}</span>
        </div>
        <div class="status"><span class="dot"></span>Metric contract registry live</div>
      </div>
      <section class="hero">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{escape(title)}</h1>
        <p>Governed metric definitions, owner lanes, freshness expectations, and AI-readable semantic contracts in one catalog surface.</p>
        <div class="hero-strip">
          <div class="hero-kpi"><div class="label">Metrics</div><div class="value">{summary["metricCount"]}</div></div>
          <div class="hero-kpi"><div class="label">Owners</div><div class="value">{summary["ownerCount"]}</div></div>
          <div class="hero-kpi"><div class="label">Flagged contracts</div><div class="value">{summary["flaggedMetricCount"]}</div></div>
          <div class="hero-kpi"><div class="label">Freshness breaches</div><div class="value">{summary["freshnessBreaches"]}</div></div>
          <div class="hero-kpi"><div class="label">Policy flags</div><div class="value">{summary["policyFlagCount"]}</div></div>
        </div>
        <div class="callout"><strong>Lead recommendation</strong>{escape(summary["leadRecommendation"])}</div>
        <div class="nav-row">{nav_links}</div>
      </section>
      {body}
      <div class="footer">
        <span><strong>Discipline:</strong> metric governance</span>
        <span><strong>Focus:</strong> contracts / freshness / ownership / semantic reuse</span>
        <span><strong>Surface:</strong> operator-friendly / AI-legible / analytics-safe</span>
      </div>
    </div>
  </body>
</html>"""


def tone(status: str) -> str:
    return status if status in {"healthy", "watch", "breached"} else "healthy"


def render_overview() -> str:
    data = service.catalog()
    metrics = data["metrics"]
    board_rows = "".join(
        f"""
        <tr>
          <td><strong>{escape(metric["label"])}</strong><div class="micro">{escape(metric["name"])}</div></td>
          <td>{escape(metric["owner"])}</td>
          <td>{escape(metric["domain"])}</td>
          <td><span class="tag {tone(metric["contract_status"])}">{escape(metric["contract_status"])}</span></td>
          <td><span class="tag {tone("watch" if metric["freshness_status"] != "within_sla" else "healthy")}">{escape(metric["freshness_status"])}</span></td>
          <td>{escape(metric["top_risk"])}</td>
        </tr>
        """
        for metric in metrics[:5]
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Control-plane summary</div>
          <h2>Metric definitions should feel like contracts, not oral tradition.</h2>
          <p>This repo turns analytics definitions into a governed catalog with contract status, freshness posture, owner accountability, and semantic output that AI systems can cite more safely.</p>
        </div>
        <div class="section-body">
          <div class="grid-4">
            <div class="card"><div class="micro">Certified metrics</div><div class="value">{len([m for m in metrics if m["tier"] == "certified"])}</div><p>Metrics approved for board, finance, or shared operating reviews.</p></div>
            <div class="card"><div class="micro">Watchlist metrics</div><div class="value">{len([m for m in metrics if m["contract_status"] == "watch"])}</div><p>Definitions drifting through partial ownership or contract ambiguity.</p></div>
            <div class="card"><div class="micro">Breached contracts</div><div class="value">{len([m for m in metrics if m["contract_status"] == "breached"])}</div><p>Metrics with real governance or freshness issues that should not travel unqualified.</p></div>
            <div class="card"><div class="micro">Distinct domains</div><div class="value">{data["stats"]["domainCount"]}</div><p>Coverage across revenue, lifecycle, support, finance, and product analytics lanes.</p></div>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Review board</div>
          <h2>The riskiest metric contracts stay visible at a glance.</h2>
          <p>Board-level definitions, pipeline math, and support efficiency KPIs often look stable right until logic drift or stale data makes them unreliable.</p>
        </div>
        <div class="section-body">
          <table>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Owner</th>
                <th>Domain</th>
                <th>Contract</th>
                <th>Freshness</th>
                <th>Top risk</th>
              </tr>
            </thead>
            <tbody>{board_rows}</tbody>
          </table>
        </div>
      </section>
    """
    return shell(
        "Control-plane summary for governed metric definitions.",
        "semantic metrics catalog",
        body,
        "overview",
    )


def render_catalog() -> str:
    metrics = service.catalog()["metrics"]
    cards = "".join(
        f"""
        <div class="card">
          <div class="micro">{escape(metric["domain"])} · {escape(metric["tier"])}</div>
          <h3 style="margin:10px 0 0;font-size:22px;">{escape(metric["label"])}</h3>
          <p>{escape(metric["description"])}</p>
          <div class="pill-stack" style="margin-top:14px;">
            <span class="pill">{escape(metric["owner"])}</span>
            <span class="pill">v{escape(metric["contract_version"])}</span>
            <span class="pill">{escape(metric["grain"])}</span>
          </div>
          <div class="code" style="margin-top:16px;">
            <div class="code-head"><span class="micro">Formula contract</span><div class="lights"><i></i><i></i><i></i></div></div>
            <pre>{escape(metric["formula_sql"])}</pre>
          </div>
        </div>
        """
        for metric in metrics
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Metric catalog</div>
          <h2>Each metric is published with the contract humans and machines actually need.</h2>
          <p>The point is not just to name the metric. It is to expose owner, grain, dependencies, formula, consumer pressure, and policy flags clearly enough that downstream teams can reuse it safely.</p>
        </div>
        <div class="section-body">
          <div class="grid-2">{cards}</div>
        </div>
      </section>
    """
    return shell(
        "Catalog lane for formulas, owners, and metric contracts.",
        "catalog lane",
        body,
        "catalog",
    )


def render_contracts() -> str:
    contracts = service.contract_board()
    rows = "".join(
        f"""
        <tr>
          <td><strong>{escape(row["label"])}</strong><div class="micro">{escape(row["name"])}</div></td>
          <td>{escape(row["owner"])}</td>
          <td><span class="tag {tone(row["contractStatus"])}">{escape(row["contractStatus"])}</span></td>
          <td>{escape(row["topRisk"])}</td>
          <td><div class="pill-stack">{"".join(f'<span class="pill">{escape(flag)}</span>' for flag in row["policyFlags"]) or '<span class="pill">none</span>'}</div></td>
        </tr>
        """
        for row in contracts
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Contract board</div>
          <h2>Governance drift should be inspectable before it reaches an executive dashboard.</h2>
          <p>This board surfaces the metrics most likely to cause semantic confusion because their contract state, freshness posture, or policy flags have started to drift.</p>
        </div>
        <div class="section-body">
          <table>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Owner</th>
                <th>Status</th>
                <th>Top risk</th>
                <th>Policy flags</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
      </section>
    """
    return shell(
        "Contract review queue for metric drift and semantic risk.",
        "contract board",
        body,
        "contracts",
    )


def render_owners() -> str:
    owners = service.owner_lanes()
    cards = "".join(
        f"""
        <div class="card">
          <div class="micro">Owner lane</div>
          <h3 style="margin:10px 0 0;font-size:24px;">{escape(owner["owner"])}</h3>
          <p>Metrics: {owner["metricCount"]} · Flagged: {owner["flaggedMetrics"]} · Freshness breaches: {owner["freshnessBreaches"]}</p>
          <div class="pill-stack" style="margin-top:14px;">
            {"".join(f'<span class="pill">{escape(domain)}</span>' for domain in owner["domains"])}
          </div>
          <p style="margin-top:14px;"><strong>Focus metric:</strong> {escape(owner["focusMetric"])}</p>
        </div>
        """
        for owner in owners
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Owner lanes</div>
          <h2>Semantic accountability becomes real when ownership pressure is visible.</h2>
          <p>Most analytics ambiguity does not start in SQL. It starts when a metric belongs to everyone and no one, or when freshness and certification expectations are never assigned clearly.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">{cards}</div>
        </div>
      </section>
    """
    return shell(
        "Owner lanes for metric accountability and semantic stewardship.",
        "ownership lane",
        body,
        "owners",
    )


def render_api_summary() -> str:
    payload = service.api_payload()
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">API summary</div>
          <h2>A lightweight route surface for catalogs, owners, and contract posture.</h2>
          <p>The service exposes a small but useful contract surface for operator tooling, analytics governance checks, and AI-readable semantic retrieval.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">
            <div class="card"><div class="micro">GET /api/catalog</div><div class="value" style="font-size:22px;">Catalog graph</div><p>Returns metrics, owners, stats, and catalog metadata in one payload.</p></div>
            <div class="card"><div class="micro">GET /api/contracts</div><div class="value" style="font-size:22px;">Contract board</div><p>Surfaces contract status, top risks, and policy flags for review workflows.</p></div>
            <div class="card"><div class="micro">GET /semantic/catalog.jsonld</div><div class="value" style="font-size:22px;">AI-readable export</div><p>Publishes the catalog as structured JSON-LD for machine consumption.</p></div>
          </div>
          <div class="code" style="margin-top:18px;">
            <div class="code-head"><span class="micro">Sample payload</span><div class="lights"><i></i><i></i><i></i></div></div>
            <pre>{escape(str(payload))}</pre>
          </div>
        </div>
      </section>
    """
    return shell(
        "API surface for governed metrics and semantic contracts.",
        "api surface",
        body,
        "docs",
    )


def write_static_proof_pages(screenshot_dir: Path) -> list[Path]:
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    pages = {
        "01-overview.html": render_overview(),
        "02-catalog-lane.html": render_catalog(),
        "03-contract-board.html": render_contracts(),
        "04-api-summary.html": render_api_summary(),
    }
    written = []
    for name, content in pages.items():
        page = screenshot_dir / name
        page.write_text(content, encoding="utf-8")
        written.append(page)
    return written

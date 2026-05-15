from __future__ import annotations

from html import escape
from pathlib import Path

from app.services.semantic_service import build_service

service = build_service()


def classify_freshness(status: str) -> str:
    return "overdue" if status != "within_sla" else "within_sla"


def badge(label: str, tone: str) -> str:
    return f'<span class="badge {tone}">{escape(label.replace("_", " "))}</span>'


def mini_bar(value: int, total: int, tone: str = "blue") -> str:
    width = 0 if total == 0 else max(10, round((value / total) * 100))
    return (
        '<div class="mini-bar-track">'
        f'<div class="mini-bar-fill {tone}" style="width:{width}%"></div>'
        "</div>"
    )


def top_shell(title: str, subtitle: str, current: str, body: str) -> str:
    summary = service.summary()
    nav = [
        ("/", "System Overview", "overview"),
        ("/catalog", "Registry Catalog", "catalog"),
        ("/contracts", "Contract Board", "contracts"),
        ("/owners", "Ownership Areas", "owners"),
        ("/docs", "API / Integration", "docs"),
    ]
    nav_links = "".join(
        f'<a class="sidebar-link {"active" if key == current else ""}" href="{href}">{label}</a>'
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
        --bg: #f6f8fb;
        --panel: #ffffff;
        --panel-alt: #f8fafc;
        --line: #dbe3ee;
        --line-strong: #cdd8e5;
        --ink: #0f172a;
        --muted: #64748b;
        --soft: #94a3b8;
        --brand: #2563eb;
        --brand-dark: #1d4ed8;
        --brand-soft: #eaf2ff;
        --green: #15803d;
        --green-soft: #dcfce7;
        --amber: #b45309;
        --amber-soft: #fef3c7;
        --red: #b91c1c;
        --red-soft: #fee2e2;
        --shadow: 0 20px 40px rgba(15, 23, 42, 0.06);
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Inter, "Segoe UI", system-ui, sans-serif;
        color: var(--ink);
        background:
          radial-gradient(circle at top left, rgba(37,99,235,0.08), transparent 22%),
          radial-gradient(circle at bottom right, rgba(148,163,184,0.12), transparent 18%),
          linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
      }}
      body::before {{
        content: "";
        position: fixed;
        inset: 0;
        background-image: radial-gradient(rgba(148,163,184,0.16) 1px, transparent 1px);
        background-size: 28px 28px;
        mask-image: linear-gradient(180deg, rgba(0,0,0,0.18), transparent 68%);
        pointer-events: none;
      }}
      a {{ color: inherit; text-decoration: none; }}
      .app {{
        max-width: 1600px;
        margin: 0 auto;
        min-height: 100vh;
        display: grid;
        grid-template-columns: 248px minmax(0, 1fr);
      }}
      .sidebar {{
        position: sticky;
        top: 0;
        align-self: start;
        height: 100vh;
        border-right: 1px solid var(--line);
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(18px);
        padding: 24px 0;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}
      .sidebar-top {{ padding: 0 22px; }}
      .mark {{
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        background: var(--ink);
        color: white;
        font-weight: 900;
        letter-spacing: -.03em;
      }}
      .brand-block {{
        display: flex;
        gap: 14px;
        align-items: center;
        margin-bottom: 28px;
      }}
      .brand-block strong {{
        display: block;
        font-size: 17px;
        font-weight: 800;
        letter-spacing: -.03em;
      }}
      .brand-block span {{
        display: block;
        margin-top: 4px;
        color: var(--soft);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .14em;
        text-transform: uppercase;
      }}
      .sidebar-kicker {{
        padding: 0 22px;
        margin-bottom: 12px;
        color: var(--soft);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .16em;
        text-transform: uppercase;
      }}
      .sidebar-link {{
        display: block;
        padding: 14px 22px;
        font-size: 13px;
        font-weight: 700;
        color: var(--muted);
        border-right: 2px solid transparent;
        transition: 160ms ease;
      }}
      .sidebar-link.active {{
        color: var(--brand);
        border-right-color: var(--brand);
        background: var(--brand-soft);
      }}
      .sidebar-link:hover {{
        color: var(--ink);
        background: #f8fafc;
      }}
      .sidebar-card {{
        margin: 0 22px;
        border: 1px solid var(--line);
        background: var(--panel-alt);
        padding: 16px;
      }}
      .sidebar-card .tiny {{
        color: var(--soft);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
      }}
      .sidebar-card .link {{
        margin-top: 10px;
        display: inline-flex;
        gap: 6px;
        color: var(--ink);
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
      }}
      .main {{
        min-width: 0;
        padding: 0 34px 34px;
      }}
      .topbar {{
        position: sticky;
        top: 0;
        z-index: 2;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        padding: 22px 0 18px;
        background: linear-gradient(180deg, rgba(246,248,251,0.94), rgba(246,248,251,0.82));
        backdrop-filter: blur(14px);
        border-bottom: 1px solid var(--line);
      }}
      .status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border: 1px solid var(--line);
        background: white;
        color: var(--muted);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
      }}
      .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: #22c55e;
        box-shadow: 0 0 0 5px rgba(34,197,94,0.12);
      }}
      .topbar-meta {{
        display: flex;
        gap: 18px;
        align-items: center;
      }}
      .meta-box {{
        background: white;
        border: 1px solid var(--line);
        padding: 10px 12px;
        min-width: 156px;
      }}
      .meta-box span {{
        display: block;
        color: var(--soft);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .14em;
        text-transform: uppercase;
      }}
      .meta-box strong {{
        display: block;
        margin-top: 6px;
        font-size: 12px;
        font-weight: 800;
        color: var(--ink);
      }}
      .hero {{
        margin-top: 30px;
        border: 1px solid var(--line);
        background: white;
        box-shadow: var(--shadow);
        overflow: hidden;
      }}
      .hero-grid {{
        display: grid;
        grid-template-columns: minmax(0, 1.35fr) 340px;
      }}
      .hero-copy {{
        padding: 34px 34px 28px;
      }}
      .eyebrow {{
        color: var(--brand);
        font-size: 11px;
        font-weight: 900;
        letter-spacing: .26em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 16px 0 0;
        font-size: clamp(44px, 5vw, 74px);
        line-height: .92;
        font-family: Georgia, "Times New Roman", serif;
        letter-spacing: -.055em;
      }}
      .hero-copy p {{
        margin: 16px 0 0;
        max-width: 780px;
        color: var(--muted);
        font-size: 18px;
        line-height: 1.6;
        font-weight: 500;
      }}
      .hero-aside {{
        border-left: 1px solid var(--line);
        background: linear-gradient(180deg, #f8fbff 0%, #f8fafc 100%);
        padding: 28px;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }}
      .hero-aside h3 {{
        margin: 0;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: .16em;
        text-transform: uppercase;
        color: var(--soft);
      }}
      .hero-aside .callout {{
        border: 1px solid var(--line);
        background: white;
        padding: 18px;
      }}
      .hero-aside .callout strong {{
        display: block;
        color: var(--ink);
        font-size: 13px;
        line-height: 1.45;
      }}
      .hero-aside .callout p {{
        margin: 10px 0 0;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.55;
      }}
      .hero-kpis {{
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0;
        border-top: 1px solid var(--line);
      }}
      .hero-kpi {{
        padding: 18px 22px 20px;
        border-right: 1px solid var(--line);
      }}
      .hero-kpi:last-child {{ border-right: 0; }}
      .label, .section-kicker, .micro {{
        color: var(--soft);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .16em;
        text-transform: uppercase;
      }}
      .hero-kpi .value {{
        margin-top: 8px;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: -.04em;
      }}
      .nav-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 18px;
      }}
      .nav-pill {{
        padding: 10px 14px;
        border: 1px solid var(--line);
        background: white;
        color: var(--muted);
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .12em;
      }}
      .nav-pill.active {{
        color: var(--brand);
        border-color: #bfdbfe;
        background: var(--brand-soft);
      }}
      .section {{
        margin-top: 28px;
        border: 1px solid var(--line);
        background: white;
        box-shadow: var(--shadow);
      }}
      .section-head {{
        padding: 26px 28px 18px;
        border-bottom: 1px solid var(--line);
      }}
      .section-head h2 {{
        margin: 10px 0 0;
        font-size: 28px;
        font-family: Georgia, "Times New Roman", serif;
        letter-spacing: -.04em;
      }}
      .section-head p {{
        margin: 12px 0 0;
        max-width: 920px;
        color: var(--muted);
        font-size: 15px;
        line-height: 1.6;
      }}
      .section-body {{ padding: 28px; }}
      .grid-4, .grid-3, .grid-2 {{
        display: grid;
        gap: 20px;
      }}
      .grid-4 {{ grid-template-columns: repeat(4, minmax(0, 1fr)); }}
      .grid-3 {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .grid-2 {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .stat-card, .card {{
        border: 1px solid var(--line);
        background: white;
        padding: 22px;
      }}
      .stat-card .value, .card .value {{
        margin-top: 12px;
        font-size: 36px;
        font-weight: 900;
        letter-spacing: -.04em;
      }}
      .stat-card p, .card p {{
        margin: 10px 0 0;
        color: var(--muted);
        font-size: 14px;
        line-height: 1.55;
      }}
      .editorial {{
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        gap: 20px;
      }}
      .table-shell {{
        border: 1px solid var(--line);
        background: white;
        overflow: hidden;
      }}
      .toolbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        padding: 16px 18px;
        border-bottom: 1px solid var(--line);
        background: var(--panel-alt);
      }}
      .searchbar {{
        min-width: 360px;
        padding: 12px 14px;
        border: 1px solid var(--line);
        background: white;
        color: var(--muted);
        font-size: 13px;
        font-weight: 600;
      }}
      .toolbar-actions {{
        display: flex;
        gap: 10px;
      }}
      .chip {{
        padding: 10px 12px;
        border: 1px solid var(--line);
        background: white;
        color: var(--muted);
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .12em;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        text-align: left;
        padding: 16px 14px;
        border-bottom: 1px solid #ecf1f6;
        vertical-align: top;
      }}
      th {{
        background: #fbfdff;
        color: var(--soft);
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: .14em;
      }}
      td {{
        font-size: 13px;
        line-height: 1.5;
        color: var(--ink);
      }}
      .metric-name {{
        font-size: 14px;
        font-weight: 800;
      }}
      .metric-slug {{
        margin-top: 5px;
        color: var(--soft);
        font-size: 11px;
        font-family: "Cascadia Code", Consolas, monospace;
      }}
      .badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 7px 10px;
        border: 1px solid transparent;
        border-radius: 2px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: .12em;
        text-transform: uppercase;
      }}
      .healthy, .within_sla {{
        color: var(--green);
        background: var(--green-soft);
        border-color: #bbf7d0;
      }}
      .watch {{
        color: var(--amber);
        background: var(--amber-soft);
        border-color: #fde68a;
      }}
      .breached, .overdue {{
        color: var(--red);
        background: var(--red-soft);
        border-color: #fecaca;
      }}
      .panel {{
        border: 1px solid var(--line);
        background: white;
        padding: 24px;
      }}
      .panel h3 {{
        margin: 0;
        font-size: 20px;
        letter-spacing: -.03em;
      }}
      .panel-list {{
        margin-top: 18px;
        display: grid;
        gap: 14px;
      }}
      .row-item {{
        padding: 14px 0;
        border-top: 1px solid #edf2f7;
      }}
      .row-item:first-child {{ border-top: 0; padding-top: 0; }}
      .row-item strong {{
        display: block;
        font-size: 14px;
      }}
      .row-item span {{
        display: block;
        margin-top: 6px;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.5;
      }}
      .pill-stack {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }}
      .pill {{
        display: inline-flex;
        align-items: center;
        padding: 7px 10px;
        border: 1px solid #d8e4f4;
        background: #f5f9ff;
        color: var(--brand);
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .12em;
      }}
      .code {{
        border: 1px solid #0f172a;
        background: #0f172a;
        color: #dbeafe;
        overflow: hidden;
      }}
      .code-head {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 16px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
      }}
      .lights {{
        display: flex;
        gap: 8px;
      }}
      .lights i {{
        width: 10px;
        height: 10px;
        border-radius: 999px;
        display: block;
      }}
      .lights i:nth-child(1) {{ background: rgba(248,113,113,0.8); }}
      .lights i:nth-child(2) {{ background: rgba(251,191,36,0.8); }}
      .lights i:nth-child(3) {{ background: rgba(74,222,128,0.8); }}
      pre {{
        margin: 0;
        padding: 18px;
        white-space: pre-wrap;
        overflow: auto;
        font-family: "Cascadia Code", Consolas, monospace;
        font-size: 12px;
        line-height: 1.6;
      }}
      .mini-bar-track {{
        margin-top: 8px;
        height: 8px;
        background: #e5edf7;
      }}
      .mini-bar-fill {{
        height: 100%;
      }}
      .mini-bar-fill.blue {{ background: linear-gradient(90deg, var(--brand), #60a5fa); }}
      .mini-bar-fill.amber {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
      .mini-bar-fill.red {{ background: linear-gradient(90deg, #ef4444, #f87171); }}
      .bar-row {{
        margin-top: 18px;
        display: grid;
        gap: 14px;
      }}
      .bar-label {{
        display: flex;
        justify-content: space-between;
        gap: 12px;
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
      }}
      .footer {{
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        margin: 18px 0 8px;
        color: var(--soft);
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: .14em;
      }}
      .footer strong {{ color: var(--ink); }}
      @media (max-width: 1260px) {{
        .app {{ grid-template-columns: 1fr; }}
        .sidebar {{ display: none; }}
        .hero-grid, .hero-kpis, .grid-4, .grid-3, .grid-2, .editorial {{
          grid-template-columns: 1fr;
        }}
        .topbar {{
          position: static;
          flex-direction: column;
          align-items: flex-start;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="app">
      <aside class="sidebar">
        <div>
          <div class="sidebar-top">
            <div class="brand-block">
              <div class="mark">SM</div>
              <div>
                <strong>Semantic Metrics</strong>
                <span>Registry // v2.4.1-stable</span>
              </div>
            </div>
          </div>
          <div class="sidebar-kicker">Workspace</div>
          {nav_links}
        </div>
        <div class="sidebar-card">
          <div class="tiny">Source: mizcausevic-dev</div>
          <a class="link" href="https://github.com/mizcausevic-dev/semantic-metrics-catalog">GitHub Repository</a>
        </div>
      </aside>
      <main class="main">
        <div class="topbar">
          <div class="status-pill"><span class="status-dot"></span>Posture: stable metric governance</div>
          <div class="topbar-meta">
            <div class="meta-box"><span>Flagged metrics</span><strong>{summary["flaggedMetricCount"]} under review</strong></div>
            <div class="meta-box"><span>Freshness drift</span><strong>{summary["freshnessBreaches"]} breach lane</strong></div>
            <div class="meta-box"><span>Owner coverage</span><strong>{summary["ownerCount"]} stewardship lanes</strong></div>
          </div>
        </div>
        <section class="hero">
          <div class="hero-grid">
            <div class="hero-copy">
              <div class="eyebrow">{escape(current.replace("-", " "))}</div>
              <h1>{escape(title)}</h1>
              <p>{escape(subtitle)}</p>
              <div class="nav-row">
                {"".join(f'<a class="nav-pill {"active" if key == current else ""}" href="{href}">{label}</a>' for href, label, key in nav)}
              </div>
            </div>
            <div class="hero-aside">
              <h3>Lead Recommendation</h3>
              <div class="callout">
                <strong>{escape(summary["leadRecommendation"])}</strong>
                <p>Make metrics portable enough for operators, executives, and AI systems to reuse the same contract without reinterpreting it.</p>
              </div>
            </div>
          </div>
          <div class="hero-kpis">
            <div class="hero-kpi"><div class="label">Metrics</div><div class="value">{summary["metricCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Owners</div><div class="value">{summary["ownerCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Flagged</div><div class="value">{summary["flaggedMetricCount"]}</div></div>
            <div class="hero-kpi"><div class="label">Freshness breaches</div><div class="value">{summary["freshnessBreaches"]}</div></div>
            <div class="hero-kpi"><div class="label">Policy flags</div><div class="value">{summary["policyFlagCount"]}</div></div>
          </div>
        </section>
        {body}
        <div class="footer">
          <span><strong>Discipline:</strong> metric governance</span>
          <span><strong>Focus:</strong> contracts / freshness / semantic reuse</span>
          <span><strong>Surface:</strong> operator-friendly / AI-legible / analytics-safe</span>
        </div>
      </main>
    </div>
  </body>
</html>"""


def render_overview() -> str:
    data = service.catalog()
    metrics = data["metrics"]
    healthy = len([m for m in metrics if m["contract_status"] == "healthy"])
    watch = len([m for m in metrics if m["contract_status"] == "watch"])
    breached = len([m for m in metrics if m["contract_status"] == "breached"])
    recent_rows = "".join(
        f"""
        <div class="row-item">
          <strong>{escape(metric["label"])}</strong>
          <span>{escape(metric["owner"])} · v{escape(metric["contract_version"])} · {escape(metric["top_risk"])}</span>
        </div>
        """
        for metric in sorted(metrics, key=lambda item: item["contract_version"], reverse=True)[:4]
    )
    domain_rows = []
    domains = sorted({metric["domain"] for metric in metrics})
    for domain in domains:
        count = len([m for m in metrics if m["domain"] == domain])
        tone = "red" if domain == "support" else "amber" if domain in {"finance", "lifecycle"} else "blue"
        domain_rows.append(
            f"""
            <div>
              <div class="bar-label"><span>{escape(domain)}</span><span>{count} metrics</span></div>
              {mini_bar(count, len(metrics), tone)}
            </div>
            """
        )

    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Metric governance analytics</div>
          <h2>Definitions only become trustworthy when their contracts stay inspectable.</h2>
          <p>This surface highlights contract coverage, freshness pressure, and the specific metrics most likely to drift away from board-safe or AI-safe reuse.</p>
        </div>
        <div class="section-body">
          <div class="grid-4">
            <div class="stat-card"><div class="label">Healthy contracts</div><div class="value">{healthy}</div><p>Definitions operating with clear ownership and clean freshness posture.</p></div>
            <div class="stat-card"><div class="label">Watchlist metrics</div><div class="value">{watch}</div><p>Contracts carrying ambiguity, definition drift, or policy review pressure.</p></div>
            <div class="stat-card"><div class="label">Breached contracts</div><div class="value">{breached}</div><p>Metrics currently unsafe to reuse without qualification.</p></div>
            <div class="stat-card"><div class="label">Domain coverage</div><div class="value">{data["stats"]["domainCount"]}</div><p>Revenue, finance, product, support, and lifecycle lanes under one registry.</p></div>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">System posture</div>
          <h2>Recent contract movement and domain pressure in one view.</h2>
          <p>The strongest version of this repo is not just a list of metrics. It behaves like an operator dashboard for semantic reliability.</p>
        </div>
        <div class="section-body">
          <div class="editorial">
            <div class="panel">
              <div class="label">Recent changes</div>
              <div class="panel-list">{recent_rows}</div>
            </div>
            <div class="panel">
              <div class="label">Governance maturity</div>
              <h3 style="margin-top:10px;">All Tier 1 metrics are registered, but support and finance still carry the most contract pressure.</h3>
              <div class="bar-row">{"".join(domain_rows)}</div>
            </div>
          </div>
        </div>
      </section>
    """
    return top_shell(
        "Metric governance should feel operational, not ceremonial.",
        "Governed metric definitions, owner lanes, freshness expectations, and AI-readable semantic contracts in one catalog surface.",
        "overview",
        body,
    )


def render_catalog() -> str:
    metrics = service.catalog()["metrics"]
    rows = "".join(
        f"""
        <tr>
          <td><div class="metric-name">{escape(metric["label"])}</div><div class="metric-slug">{escape(metric["name"])}</div></td>
          <td>{escape(metric["owner"])}</td>
          <td>{badge(metric["freshness_status"], classify_freshness(metric["freshness_status"]))}</td>
          <td>{badge(metric["contract_status"], metric["contract_status"])}</td>
          <td>{escape(metric["tier"])}</td>
        </tr>
        """
        for metric in metrics
    )
    spotlight = metrics[1]
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Registry catalog</div>
          <h2>Searchable metric inventory with the details downstream systems actually need.</h2>
          <p>The catalog becomes more useful when the table is readable at a glance and the semantic contract is close enough to inspect without leaving the page.</p>
        </div>
        <div class="section-body">
          <div class="table-shell">
            <div class="toolbar">
              <div class="searchbar">Search catalog by metric name, owner, or identifier...</div>
              <div class="toolbar-actions">
                <div class="chip">Filter</div>
                <div class="chip">Sort</div>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Metric identification</th>
                  <th>Owner lane</th>
                  <th>Freshness</th>
                  <th>Contract status</th>
                  <th>Tier</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
          <div class="grid-2" style="margin-top:20px;">
            <div class="panel">
              <div class="label">Metric spotlight</div>
              <h3 style="margin-top:10px;">{escape(spotlight["label"])}</h3>
              <p>{escape(spotlight["description"])}</p>
              <div class="pill-stack" style="margin-top:16px;">
                <span class="pill">{escape(spotlight["owner"])}</span>
                <span class="pill">v{escape(spotlight["contract_version"])}</span>
                <span class="pill">{escape(spotlight["grain"])}</span>
              </div>
            </div>
            <div class="code">
              <div class="code-head"><span class="label" style="color:#93c5fd;">Formula contract</span><div class="lights"><i></i><i></i><i></i></div></div>
              <pre>{escape(spotlight["formula_sql"])}</pre>
            </div>
          </div>
        </div>
      </section>
    """
    return top_shell(
        "Metric contracts, owner lanes, and freshness signals laid out as a readable registry.",
        "Governed metric definitions, owner lanes, freshness expectations, and AI-readable semantic contracts in one catalog surface.",
        "catalog",
        body,
    )


def render_contracts() -> str:
    contracts = service.contract_board()
    cards = "".join(
        f"""
        <div class="card">
          <div class="pill-stack">
            {badge(row["contractStatus"], row["contractStatus"])}
            {badge(row["freshnessStatus"], classify_freshness(row["freshnessStatus"]))}
          </div>
          <h3 style="margin:16px 0 0;font-size:24px;letter-spacing:-.04em;">{escape(row["label"])}</h3>
          <p>{escape(row["topRisk"])}</p>
          <div class="pill-stack" style="margin-top:16px;">
            <span class="pill">{escape(row["owner"])}</span>
            <span class="pill">{escape(row["domain"])}</span>
            <span class="pill">v{escape(row["contractVersion"])}</span>
          </div>
          <div class="pill-stack" style="margin-top:12px;">
            {"".join(f'<span class="pill">{escape(flag)}</span>' for flag in row["policyFlags"]) or '<span class="pill">none</span>'}
          </div>
        </div>
        """
        for row in contracts
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">Contract board</div>
          <h2>Governance risk deserves its own queue, not a footnote under a chart.</h2>
          <p>These are the definitions most likely to break executive trust, BI reuse, or AI grounding because their freshness, contract state, or policy posture has started to drift.</p>
        </div>
        <div class="section-body">
          <div class="grid-2">{cards}</div>
        </div>
      </section>
    """
    return top_shell(
        "Review queue for drift, freshness pressure, and semantic risk.",
        "Governed metric definitions, owner lanes, freshness expectations, and AI-readable semantic contracts in one catalog surface.",
        "contracts",
        body,
    )


def render_owners() -> str:
    owners = service.owner_lanes()
    total = max(owner["metricCount"] for owner in owners)
    cards = "".join(
        f"""
        <div class="card">
          <div class="label">Owner lane</div>
          <h3 style="margin:10px 0 0;font-size:24px;letter-spacing:-.04em;">{escape(owner["owner"])}</h3>
          <p>{owner["metricCount"]} metrics · {owner["flaggedMetrics"]} flagged · {owner["freshnessBreaches"]} freshness breaches</p>
          {mini_bar(owner["metricCount"], total, "blue")}
          <div class="pill-stack" style="margin-top:16px;">
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
          <div class="section-kicker">Ownership areas</div>
          <h2>Semantic accountability becomes real when stewardship pressure is visible.</h2>
          <p>Owner lanes make it clear which teams are carrying the governance load and which metrics deserve immediate semantic cleanup.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">{cards}</div>
        </div>
      </section>
    """
    return top_shell(
        "Ownership lanes for metric stewardship and accountability.",
        "Governed metric definitions, owner lanes, freshness expectations, and AI-readable semantic contracts in one catalog surface.",
        "owners",
        body,
    )


def render_api_summary() -> str:
    payload = service.api_payload()
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="section-kicker">API / integration</div>
          <h2>Lightweight route surface for catalog retrieval, contract review, and semantic publishing.</h2>
          <p>The API should feel usable by analytics tooling and AI retrieval systems without turning into another giant platform abstraction.</p>
        </div>
        <div class="section-body">
          <div class="grid-3">
            <div class="card"><div class="label">GET /api/catalog</div><div class="value" style="font-size:22px;">Registry graph</div><p>Returns metrics, owner lanes, and summary stats together.</p></div>
            <div class="card"><div class="label">GET /api/contracts</div><div class="value" style="font-size:22px;">Review queue</div><p>Surfaces the riskiest contract lanes with policy flags intact.</p></div>
            <div class="card"><div class="label">GET /semantic/catalog.jsonld</div><div class="value" style="font-size:22px;">AI-readable export</div><p>Publishes a machine-friendly semantic surface without losing business context.</p></div>
          </div>
          <div class="grid-2" style="margin-top:20px;">
            <div class="code">
              <div class="code-head"><span class="label" style="color:#93c5fd;">Sample payload</span><div class="lights"><i></i><i></i><i></i></div></div>
              <pre>{escape(str(payload))}</pre>
            </div>
            <div class="panel">
              <div class="label">Design intent</div>
              <div class="panel-list">
                <div class="row-item"><strong>Catalog-first</strong><span>Definitions should be easy to read long before someone opens a warehouse query.</span></div>
                <div class="row-item"><strong>Contract-aware</strong><span>Status, freshness, ownership, and policy posture travel with the metric.</span></div>
                <div class="row-item"><strong>AI-legible</strong><span>The semantic export is structured enough for retrieval systems to cite instead of improvise.</span></div>
              </div>
            </div>
          </div>
        </div>
      </section>
    """
    return top_shell(
        "API reference for governed metrics and semantic publishing.",
        "Governed metric definitions, owner lanes, freshness expectations, and AI-readable semantic contracts in one catalog surface.",
        "docs",
        body,
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

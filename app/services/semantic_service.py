from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class SemanticMetricsCatalogService:
    source_path: Path

    def load(self) -> dict[str, Any]:
        return yaml.safe_load(self.source_path.read_text(encoding="utf-8"))

    def catalog(self) -> dict[str, Any]:
        data = self.load()
        metrics = sorted(data["metrics"], key=lambda metric: metric["label"])
        owners = self.owner_lanes(metrics)
        flagged = [metric for metric in metrics if metric["contract_status"] != "healthy"]
        freshness_breaches = [
            metric for metric in metrics if metric["freshness_status"] != "within_sla"
        ]
        policy_flags = sum(len(metric.get("policy_flags", [])) for metric in metrics)
        return {
            "catalog": data["catalog"],
            "metrics": metrics,
            "owners": owners,
            "stats": {
                "metricCount": len(metrics),
                "ownerCount": len(owners),
                "domainCount": len({metric["domain"] for metric in metrics}),
                "flaggedMetricCount": len(flagged),
                "freshnessBreaches": len(freshness_breaches),
                "policyFlagCount": policy_flags,
            },
        }

    def metric(self, name: str) -> dict[str, Any] | None:
        return next(
            (metric for metric in self.catalog()["metrics"] if metric["name"] == name),
            None,
        )

    def contract_board(self) -> list[dict[str, Any]]:
        board = []
        for metric in self.catalog()["metrics"]:
            board.append(
                {
                    "name": metric["name"],
                    "label": metric["label"],
                    "owner": metric["owner"],
                    "domain": metric["domain"],
                    "contractStatus": metric["contract_status"],
                    "freshnessStatus": metric["freshness_status"],
                    "contractVersion": metric["contract_version"],
                    "topRisk": metric["top_risk"],
                    "policyFlags": metric.get("policy_flags", []),
                    "consumerCount": len(metric.get("consumers", [])),
                }
            )
        severity_rank = {"breached": 0, "watch": 1, "healthy": 2}
        return sorted(
            board,
            key=lambda row: (
                severity_rank.get(row["contractStatus"], 3),
                row["label"],
            ),
        )

    def owner_lanes(self, metrics: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        metrics = metrics or self.catalog()["metrics"]
        lanes = []
        for owner in sorted({metric["owner"] for metric in metrics}):
            owned = [metric for metric in metrics if metric["owner"] == owner]
            lanes.append(
                {
                    "owner": owner,
                    "metricCount": len(owned),
                    "flaggedMetrics": len(
                        [metric for metric in owned if metric["contract_status"] != "healthy"]
                    ),
                    "freshnessBreaches": len(
                        [metric for metric in owned if metric["freshness_status"] != "within_sla"]
                    ),
                    "domains": sorted({metric["domain"] for metric in owned}),
                    "focusMetric": max(
                        owned,
                        key=lambda metric: (
                            metric["contract_status"] != "healthy",
                            metric["freshness_status"] != "within_sla",
                            len(metric.get("policy_flags", [])),
                        ),
                    )["label"],
                }
            )
        return lanes

    def summary(self) -> dict[str, Any]:
        data = self.catalog()
        return {
            "catalogName": data["catalog"]["name"],
            "metricCount": data["stats"]["metricCount"],
            "ownerCount": data["stats"]["ownerCount"],
            "flaggedMetricCount": data["stats"]["flaggedMetricCount"],
            "freshnessBreaches": data["stats"]["freshnessBreaches"],
            "policyFlagCount": data["stats"]["policyFlagCount"],
            "leadRecommendation": (
                "Treat metric definitions like contracts: surface ownership gaps, "
                "freshness drift, and policy exceptions before dashboards turn into "
                "executive folklore."
            ),
        }

    def catalog_jsonld(self) -> dict[str, Any]:
        data = self.catalog()
        catalog = data["catalog"]
        return {
            "@context": "https://schema.org",
            "@type": "DataCatalog",
            "name": catalog["name"],
            "description": catalog["description"],
            "keywords": catalog["tags"],
            "creator": {"@type": "Organization", "name": catalog["owner"]},
            "dataset": [
                {
                    "@type": "Dataset",
                    "name": metric["label"],
                    "identifier": metric["name"],
                    "description": metric["description"],
                    "keywords": [
                        metric["domain"],
                        metric["tier"],
                        metric["contract_status"],
                    ],
                    "measurementTechnique": metric["formula_sql"],
                    "variableMeasured": [
                        {"@type": "PropertyValue", "name": dimension}
                        for dimension in metric.get("dimensions", [])
                    ],
                    "maintainer": {"@type": "Organization", "name": metric["owner"]},
                }
                for metric in data["metrics"]
            ],
        }

    def api_payload(self) -> dict[str, Any]:
        data = self.catalog()
        return {
            "dashboard": self.summary(),
            "contractBoard": self.contract_board()[:3],
            "owners": self.owner_lanes()[:3],
            "catalogJsonLdUrl": f"{data['catalog']['publication_url']}/semantic/catalog.jsonld",
        }


def build_service(root: Path | None = None) -> SemanticMetricsCatalogService:
    base = root or Path(__file__).resolve().parents[2]
    return SemanticMetricsCatalogService(base / "app" / "data" / "sample_metrics_catalog.yml")

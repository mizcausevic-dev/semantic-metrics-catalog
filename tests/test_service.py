from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.semantic_service import build_service


class SemanticMetricsCatalogTests(unittest.TestCase):
    def test_summary_counts(self) -> None:
        summary = build_service().summary()
        self.assertEqual(summary["metricCount"], 5)
        self.assertEqual(summary["ownerCount"], 5)
        self.assertEqual(summary["flaggedMetricCount"], 3)

    def test_contract_board_prioritizes_breached(self) -> None:
        board = build_service().contract_board()
        self.assertEqual(board[0]["name"], "first_response_sla_attainment")
        self.assertEqual(board[0]["contractStatus"], "breached")

    def test_api_routes(self) -> None:
        client = TestClient(app)
        response = client.get("/api/metrics/pipeline_coverage_ratio")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["owner"], "Revenue Systems")


if __name__ == "__main__":
    unittest.main()

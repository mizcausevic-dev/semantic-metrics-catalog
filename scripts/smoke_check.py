from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from app.main import app


def main() -> None:
    client = TestClient(app)
    for route in [
        "/",
        "/catalog",
        "/contracts",
        "/owners",
        "/docs",
        "/api/dashboard/summary",
        "/api/contracts",
        "/semantic/catalog.jsonld",
    ]:
        response = client.get(route)
        response.raise_for_status()
    print("smoke-ok")


if __name__ == "__main__":
    main()

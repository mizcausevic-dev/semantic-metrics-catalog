from __future__ import annotations

import json
import os

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import (
    render_api_summary,
    render_catalog,
    render_contracts,
    render_overview,
    render_owners,
)
from app.services.semantic_service import build_service

app = FastAPI(
    title="Semantic Metrics Catalog",
    version="0.1.0",
    description=(
        "Governed metric catalog for semantic contracts, ownership, freshness "
        "expectations, and AI-readable analytics definitions."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/catalog", response_class=HTMLResponse)
def catalog_page() -> str:
    return render_catalog()


@app.get("/contracts", response_class=HTMLResponse)
def contracts_page() -> str:
    return render_contracts()


@app.get("/owners", response_class=HTMLResponse)
def owners_page() -> str:
    return render_owners()


@app.get("/docs", response_class=HTMLResponse)
def docs_page() -> str:
    return render_api_summary()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/catalog")
def api_catalog() -> dict:
    return service.catalog()


@app.get("/api/metrics")
def api_metrics() -> list[dict]:
    return service.catalog()["metrics"]


@app.get("/api/metrics/{metric_name}")
def api_metric(metric_name: str) -> dict:
    metric = service.metric(metric_name)
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@app.get("/api/contracts")
def api_contracts() -> list[dict]:
    return service.contract_board()


@app.get("/api/owners")
def api_owners() -> list[dict]:
    return service.owner_lanes()


@app.get("/api/sample")
def api_sample() -> dict:
    return service.api_payload()


@app.get("/semantic/catalog.jsonld")
def semantic_catalog() -> JSONResponse:
    return JSONResponse(service.catalog_jsonld())


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "4994"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)

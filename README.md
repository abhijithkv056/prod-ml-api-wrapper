## Transaction Fraud Model API

Production-style FastAPI service for a dummy fraud model, with:
- async API handlers
- strict Pydantic validation
- structured error responses
- Prometheus metrics (`/metrics`)
- Grafana provisioning via Docker Compose

## Project Structure

```text
q2-ml-model-api/
├─ app/
│  ├─ api/
│  │  ├─ health.py                   # /health endpoint
│  │  ├─ metrics.py                  # /metrics endpoint
│  │  └─ predict.py                  # /predict and /predict/batch endpoints
│  ├─ core/
│  │  └─ errors.py                   # exception handler registration
│  ├─ models/
│  │  └─ transactions.py             # Request/response and transaction schemas
│  ├─ monitoring/
│  │  ├─ metrics.py                  # Prometheus counters/histograms
│  │  ├─ middleware.py               # HTTP latency + volume middleware
│  │  └─ grafana/
│  │     ├─ dashboards/
│  │     │  └─ fraud-api-overview.json
│  │     └─ provisioning/
│  │        ├─ dashboards/dashboards.yml
│  │        └─ datasources/prometheus.yml
│  ├─ services/
│  │  └─ fraud_model.py              # Dummy model inference logic
│  └─ main.py                        # App wiring/composition root
├─ docker-compose.yml
├─ Dockerfile
├─ prometheus.yml
└─ README.md
```

## API Endpoints

- `POST /predict` - single transaction prediction
- `POST /predict/batch` - batch prediction (max 100)
- `GET /health` - health endpoint
- `GET /metrics` - Prometheus metrics endpoint

## Design Choices

- **FastAPI + Pydantic**: chosen for concise API development, strong request validation, and clear schema-driven contracts.
- **Separated layers**: routing (`app/api`), schema models (`app/models`), model logic (`app/services`), monitoring primitives (`app/monitoring`), and error registration (`app/core`) are split for maintainability.
- **Composition root in `app/main.py`**: `main.py` only wires middleware, exception handlers, and routers, while endpoint and handler logic live in dedicated modules.
- **Structured errors**: validation, model, and server failures return consistent JSON shapes to simplify client-side handling.
- **Built-in observability**: request count and latency metrics are captured via middleware and exposed through `/metrics`, with Prometheus/Grafana support for quick monitoring.

## Model Logic

The dummy model is rule-based:
- if `transaction_amount` is a whole odd number -> `0.85` (high fraud probability)
- else -> `0.15` (low fraud probability)

## Assumptions Made

`odd/even` is evaluated only for whole-number amounts (for example, `101.00` is treated as odd, while `101.01` is not). 
This rule is intentionally simplistic and only used as dummy logic for the assignment.
Batch inference is limited to at most 100 transactions per request, as required.

## Run Locally

1) Install dependencies:

```bash
uv sync
```

2) Start API:

```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3) Test:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"transaction\":{\"transaction_amount\":101.00,\"merchant_id\":\"m_123\",\"transaction_time\":\"2026-05-01T10:00:00Z\",\"user_location\":{\"latitude\":12.9,\"longitude\":77.6}}}"
```

## Run with Docker Compose

```bash
docker compose up -d --build
```

Services:
- API: <http://localhost:8000>
- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000> (`admin` / `admin`)

Grafana auto-loads:
- Prometheus datasource
- `Fraud API Overview` dashboard

## Monitoring Metrics

- `http_requests_total{method,path,status}` - request volume
- `http_request_duration_seconds{method,path}` - request latency histogram

## Validation and Error Handling

- Payload schemas are defined in `app/models/transactions.py`
- Unknown fields are rejected (`extra="forbid"`)
- Validation errors return consistent `422` JSON payloads
- Model inference failures return `503` with `model_error`
- Unhandled exceptions return `500` with `internal_error`
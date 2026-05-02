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
│  │  └─ predict.py                  # /predict and /predict/batch endpoints
│  ├─ models/
│  │  └─ transactions.py             # Request/response and transaction schemas
│  ├─ monitoring/
│  │  ├─ metrics.py                  # Prometheus counters/histograms + /metrics router
│  │  ├─ middleware.py               # HTTP latency + volume middleware
│  │  └─ grafana/
│  │     ├─ dashboards/
│  │     │  └─ fraud-api-overview.json
│  │     └─ provisioning/
│  │        ├─ dashboards/dashboards.yml
│  │        └─ datasources/prometheus.yml
│  ├─ services/
│  │  └─ fraud_model.py              # Dummy model inference logic
│  └─ main.py                        # App factory and wiring
├─ main.py                           # Entrypoint shim (imports app.main:app)
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

## Model Logic

The dummy model is rule-based:
- if `transaction_amount` is a whole odd number -> `0.85` (high fraud probability)
- else -> `0.15` (low fraud probability)

## Run Locally

1) Install dependencies:

```bash
uv sync
```

2) Start API:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

3) Test:

```bash
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
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
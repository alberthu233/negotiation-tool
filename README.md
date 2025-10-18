# negotiation-tool

Simple, deterministic negotiation microservice for a voice agent. Exposes a single POST endpoint to compute the next agent offer under a strict ceiling.

## API

- **POST `/negotiate`**
  - Body:
    ```json
    {"driver_price": 2000, "price_margin": 2500, "agent_price": 1800}
    ```
  - Returns:
    ```json
    {"next_agent_price": 1899.5}
    ```
  - Auth: optional header `X-API-Key: <API_KEY>` (if `API_KEY` is set in env).

- **GET `/health`** → `{ "ok": true }`

### Safety
The service never returns a value ≥ `price_margin` (strictly below).

## Run locally

Install deps and run uvicorn:

```
uvicorn app.main:app --reload
```

## Docker

```
docker build -t negotiation-tool .
docker run -p 8080:8080 -e API_KEY=supersecret negotiation-tool
```

## cURL example

```
curl -X POST http://localhost:8080/negotiate \
  -H "Content-Type: application/json" -H "X-API-Key: supersecret" \
  -d '{"driver_price":2100,"price_margin":2200,"agent_price":1900}'
```

## Core logic

Deterministic, rule-based negotiation with a strict ceiling:
- Hard ceiling: `cap = price_margin - epsilon` (final deal is strictly below `price_margin`).
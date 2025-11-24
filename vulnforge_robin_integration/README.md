# VulnForge Robin Integration

Production-ready integration service that ingests Robin dark-web/OSINT findings into the VulnForge platform. The service normalizes Robin output, encrypts sensitive snippets, enriches findings via legal APIs, scores risk, and exposes a review-friendly API + dashboard.

## Features
- Docker-compose stack (API, Celery worker, broker, DB, Robin placeholder)
- Directory watcher **and** webhook ingest paths
- Canonical Pydantic schema with AES-GCM encrypted snippets
- Async enrichment stubs (HIBP, Shodan, Censys, Passive DNS)
- Configurable scoring & deduplication
- FastAPI REST interface, reviewer dashboard, Prometheus metrics
- Celery + SQLAlchemy persistence with Alembic-ready models
- Comprehensive pytest suite & demo script

## Quick Start
```bash
cd vulnforge_robin_integration
cp .env.example .env   # update secrets & API keys
docker-compose up --build
```

Once running:
- Drop sample Robin outputs into `./samples/inbox` or call `POST /ingest`
- Celery worker enriches & scores items automatically
- Visit `http://localhost:8080` for the dashboard

## Local Demo
```bash
./demo.sh
```
Demo copies sample files into the watched directory and exercises the webhook, showing ingestion logs and dashboard entries.

## Testing
```bash
pip install -r requirements.txt
pytest
```

## Security Notes
- No offensive automation is included (no exploit execution, scanning, or credential attacks).
- Raw data encrypted at rest (AES-GCM); reviewer password required to decrypt.
- Robin container is network-isolated; communication occurs via mounted volume only.


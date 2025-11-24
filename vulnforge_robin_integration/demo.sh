#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export COMPOSE_PROJECT_NAME=vulnforge_robin_demo

if [ ! -f "$ROOT_DIR/.env" ]; then
  echo "[!] Please copy .env.example to .env and set secrets before running demo.sh"
  exit 1
fi

mkdir -p "$ROOT_DIR/samples/inbox"
mkdir -p "$ROOT_DIR/data"

echo "[+] Starting docker-compose stack..."
docker-compose -f "$ROOT_DIR/docker-compose.yml" up -d --build

echo "[+] Seeding sample Robin files..."
cp "$ROOT_DIR/samples/example-report.md" "$ROOT_DIR/samples/inbox/report-demo.md"

echo "[+] Waiting for services to stabilize..."
sleep 10

echo "[+] Sending webhook ingest example..."
curl -s -X POST http://localhost:8080/ingest \
  -H "Content-Type: application/json" \
  -d '{"source":"webhook","payload":{"target":"example.com","leak_type":"credentials","raw":"demo raw snippet","structured_fields":{"email":"demo@example.com"}}}' \
  | jq .

echo "[+] Visit http://localhost:8080 to review items. Press Ctrl+C to stop stack."


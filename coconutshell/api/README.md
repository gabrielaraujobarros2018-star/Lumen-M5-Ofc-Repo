# Tiny Lumen API (Pure Java)

Lightweight HTTP API for Lumen OS. Endpoints:
- GET /status → {"status": "alive", "os": "Lumen"}
- GET /metrics → {"cpu": "50%", "mem": "75%"}

## Build & Run
1. chmod +x build.sh
2. ./build.sh
Server: http://localhost:8080

Java 11+ required. No deps.
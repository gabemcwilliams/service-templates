# Loki Configuration

This directory holds the configuration for Grafana Loki, the log aggregation system.

- `loki-config.yaml`: Full configuration with S3 storage backend and mTLS support.

Key features:
- Logs stored in MinIO via S3-compatible API.
- TLS secured with mutual authentication (client certs required).
- Works in tandem with Promtail or Alloy as log shippers.

Accessible internally at `https://loki.internal:3100`.

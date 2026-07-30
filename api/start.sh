#!/bin/sh
set -eu

CERT_FILE="${SSL_CERTFILE:-/tls/tls.crt}"
KEY_FILE="${SSL_KEYFILE:-/tls/tls.key}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8443}"

if [ ! -f "$CERT_FILE" ]; then
  echo "Missing TLS certificate file: $CERT_FILE" >&2
  exit 1
fi

if [ ! -f "$KEY_FILE" ]; then
  echo "Missing TLS private key file: $KEY_FILE" >&2
  exit 1
fi

exec uvicorn main:app \
  --host "$HOST" \
  --port "$PORT" \
  --ssl-keyfile "$KEY_FILE" \
  --ssl-certfile "$CERT_FILE"

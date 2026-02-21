#!/bin/sh
set -e

# Ensure upload directory exists and is writable
mkdir -p "${UPLOAD_DIR:-/app/uploads}"
chown -R 0:0 "${UPLOAD_DIR:-/app/uploads}" || true
chmod -R a+rw "${UPLOAD_DIR:-/app/uploads}" || true

exec "$@"

#!/bin/bash
# Reset the NocoDB database locally (not in Docker)
set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="$PROJECT_ROOT/nocodb"

echo "[reset_local_db.sh] Copying $DATA_DIR/noco.db.bak to $DATA_DIR/noco.db ..."
cp "$DATA_DIR/noco.db.bak" "$DATA_DIR/noco.db"
chmod 777 "$DATA_DIR/noco.db"
echo "[reset_local_db.sh] Done."
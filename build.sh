#!/usr/bin/env bash
set -o errexit

uv sync --frozen && uv cache prune --ci
python scripts/download_model.py
# python app/manage.py collectstatic --no-input

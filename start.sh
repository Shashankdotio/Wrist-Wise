#!/bin/sh
# Entrypoint script for starting the Flask app with Gunicorn/UvicornWorker
WORKERS=${WORKERS:-$(expr $(nproc) \* 2 + 1)}

exec gunicorn backend_server:app --workers $WORKERS --bind 0.0.0.0:8000

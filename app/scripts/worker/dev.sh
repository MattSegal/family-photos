#!/bin/bash
set -e
watchmedo \
auto-restart \
    --directory /app/photos/ \
    --recursive \
    --pattern '*.py' \
    -- ./manage.py qcluster

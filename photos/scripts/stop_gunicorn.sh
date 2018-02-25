#!/bin/bash
echo "Attempting to stop gunicorn"
killall -v gunicorn || true
echo "Attempting to stop celery"
killall -v celery || true

#!/bin/bash
echo "Attempting to stop gunicorn"
 killall -v gunicorn || true

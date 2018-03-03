#!/bin/bash
echo "Attempting to stop gunicorn"
ps auxww | grep 'gunicorn' | awk '{print $2}' | xargs kill
echo "Attempting to stop celery"
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill

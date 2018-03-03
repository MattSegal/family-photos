#!/bin/bash
echo "Stopping gunicorn if running"
pids="$(pgrep --exact gunicorn)"
if [[ "$pids" != "" ]]
then
  printf "$pids" | xargs kill
fi

echo "Stopping celery working if running"
pids=$(pgrep --full 'celery worker')
if [[ "$pids" != "" ]]
then
  printf "$pids" | xargs kill
fi

echo "Checking for gunicorn"
echo "$(ps auxww | grep 'gunicorn')"

echo "Checking for celery worker"
echo "$(ps auxww | grep 'celery worker')"

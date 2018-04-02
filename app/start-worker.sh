#!/bin/bash
BROKER="redis://$CELERY_HOST:6379"
celery worker \
	--broker $BROKER \
	--app photos \
	# --logfile /var/log/celery.log
	--loglevel info

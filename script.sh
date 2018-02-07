#!/bin/bash
oc rsh django-psql-persistent-11-trcdn /bin/bash << EOF
	python manage.py command server com2x3
EOF
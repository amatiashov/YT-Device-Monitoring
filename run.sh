#!/bin/bash

exec gunicorn --bind=0.0.0.0:8080 --workers=1 wsgi:app

#!/bin/bash
set -e

gunicorn app.wsgi:application -w 3 --bind 0.0.0.0:8000
#!/usr/bin/env bash
cd todo_list; gunicorn todo_list.wsgi:application --bind 0.0.0.0:8000 --workers 3 &
nginx -g "daemon off;"

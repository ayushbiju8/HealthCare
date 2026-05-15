#!/bin/bash
./venv/bin/django-admin startproject core .
./venv/bin/python manage.py startapp users
./venv/bin/python manage.py startapp records
./venv/bin/python manage.py startapp metrics
./venv/bin/python manage.py startapp fitness
./venv/bin/python manage.py startapp reminders
./venv/bin/python manage.py startapp ai_logs
./venv/bin/python manage.py startapp integrations

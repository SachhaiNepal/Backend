SHELL=/bin/bash
PYTHON=venv/bin/python

make-migrations:
	$(PYTHON) makemigrations $(APP)

migrate:
	$(PYTHON) django-admin migrate

serve:
	$(PYTHON) manage.py runserver

createsuperuser:
	$(PYTHON) manage.py createsuperuser

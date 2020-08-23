SHELL=/bin/bash
PYTHON=venv/bin/python3.8
PIP=venv/bin/pip3.8

virtual-env:
	python3.8 -m venv venv

install:
	$(PIP) install -r requirements.txt

make-migrations:
	$(PYTHON) manage.py makemigrations $(APP)

migrate:
	$(PYTHON) manage.py migrate

serve:
	$(PYTHON) manage.py runserver

createsuperuser:
	$(PYTHON) manage.py createsuperuser

clean-db:
	rm -rf db.sqlite3

clean-migrations:
	rm -rf branch/migrations

clean-db-with-migration: clean-db clean-migrations

clean-env:
	rm -rf venv

clean: clean-db clean-env clean-migrations

build:
	$(PYTHON) manage.py makemigrations
	$(PYTHON) manage.py migrate

shell:
	$(PYTHON) manage.py shell

SHELL=/bin/bash
PYTHON=venv/bin/python3.8
PIP=venv/bin/pip3.8

create-env:
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
	$(PYTHON) manage.py migrate

shell:
	$(PYTHON) manage.py shell

collect-static:
	$(PYTHON) manage.py collectstatic

get-token:
	$(PYTHON) manage.py  drf_create_token $(USER)

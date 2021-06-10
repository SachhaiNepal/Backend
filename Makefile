include .env
SHELL=/bin/bash
ADMIN_EMAIL := admin@test.com
ADMIN_USERNAME := admin
ADMIN_PASSWORD := admin

create-env:
	python3.8 -m venv venv

install:
	$(PIP) install -r requirements.txt

make-migrations:
	$(PYTHON) manage.py makemigrations $(APP)

migrate:
	$(PYTHON) manage.py migrate

serve:
	$(PYTHON) manage.py runserver $(BASE_URL)

createsuperuser:
	$(PYTHON) manage.py createsuperuser


create-admin:
	DJANGO_SUPERUSER_PASSWORD=$(ADMIN_PASSWORD) $(PYTHON) manage.py createsuperuser --username $(ADMIN_USERNAME) --email $(ADMIN_EMAIL) --noinput

clean-db:
	rm -rf db.sqlite3

clean-migrations:
	rm -rf accounts/migrations
	rm -rf branch/migrations
	rm -rf multimedia/migrations
	rm -rf article/migrations
	rm -rf location/migrations
	rm -rf event/migrations
	rm -rf advertise/migrations
	rm -rf utilities/migrations

load-fresh-migrations:
	make clean-migrations
	make make-migrations APP=location
	make migrate
	make make-migrations APP=accounts
	make make-migrations APP=branch
	make migrate
	make make-migrations APP=advertise
	make make-migrations APP=article
	make make-migrations APP=event
	make make-migrations APP=multimedia
	make make-migrations APP=utilities
	make migrate

super-fresh: clean-db-with-migration load-fresh-migrations create-admin serve

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

isort:
	isort .

black:
	black .

lint:
	black .
	isort .

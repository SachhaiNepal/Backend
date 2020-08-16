make-migrations:
	DJANGO_SETTINGS_MODULE=backend.settings django-admin makemigrations $(APP)

migrate:
	DJANGO_SETTINGS_MODULE=backend.settings django-admin migrate

serve:
	DJANGO_SETTINGS_MODULE=backend.settings django-admin runserver

run:
	@python manage.py runserver 0.0.0.0:8000

migrate:
	@python manage.py migrate --run-syncdb

loaddata:
	@python manage.py loaddata command.json
#	@python manage.py loaddata apptype.json

crontab_remove:
	@python manage.py crontab remove

crontab_add:
	@python manage.py crontab add

superuser:
	@python manage.py createsuperuser

#run-celery-worker:
#	@celery -A django_graph worker -l info

#run-celery-beat:
#	@celery -A django_graph beat -l info

#run-redis:
#	redis-server --daemonize yes
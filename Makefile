run:
	python3 manage.py runserver
redis:
	docker container rm anismile_redis
	docker run --name anismile_redis -d -p 6379:6379 redis
redis-stop:
	docker stop anismile_redis
celery:
	celery -A config worker --loglevel=INFO
celery-beat:
	celery -A config beat --loglevel=INFO
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser

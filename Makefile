run:
	python3 manage.py runserver
redis:
	docker run --name anismile_redis -d -p 6379:6379 redis
redis-stop:
	docker stop anismile_redis
celery:
	celery -A config worker --loglevel=INFO
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

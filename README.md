# AniSlime (Final Hackaton Makers)
>AniSlime API - is api for a web application built using the Django REST framework. This web application is made for watching anime and discussing it. You can test this [API Documents](http://34.89.235.149/api/v1/swagger/) here.

## Developers
- Adil (ovaomnis)
- Sayan (ASayan#$)
- Iskhak (1sabro)

## Technologies used in project
- Django REST
- PostgreSQL
- Celery
- Redis


### To test our project
cloning project:
```
git clone https://github.com/ovaomnis/anislime.git
```

to start
installation and dependencies:
```
pip3 install -r requirements.txt
```
create virtual environment:
```
python -m venv <you_env_name>
```
activate virtual evnironment:
>if you using windows:
>>```
>><you_env_name>\Scripts\activate
>>```
>if you using linux:
>>```
>>. <you_env_name>/bin/activate
>>```
running the server: 
```
python3 manage.py runserver
```
running the celery: 
```
celery -A config worker --loglevel=INFO
```
running the celery beat: 
```
celery -A config beat --loglevel=INFO
```

## API Allows
- **Register**
- **Start watching your favorite series**
- **Add to favorites**
- **Subscribe to Title and receive messages when new episodes are released**

---------------

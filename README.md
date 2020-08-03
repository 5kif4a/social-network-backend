## Social Network Back-end API - [Django 3](https://www.djangoproject.com/)
### Client realization with React [here](https://github.com/5kif4a/social-network-frontend)   
### Installation 
**[Python]() 3.7+ required**  
Default DBMS: **SQLite 3**  
Using other DBMS you can find [here](https://docs.djangoproject.com/en/3.0/ref/databases/)    
Download source code:
```
$ git clone https://github.com/5kif4a/social-network-backend.git
$ cd project_folder
```
Create virtual environment:
```
$ python -m venv venv
```
Activate venv:
```
$ source venv/bin/activate
```
Install requirements:
```
$ pip install -r requirements.txt
```
Create .env file in root of the project folder:
```
$ touch .env
```
Environment variables:
```
# On develepment DEBUG=1, on production DEBUG=0
DEBUG=1
SECRET_KEY=your_secret_key
```
Migrate database:
```
$ python manage.py makemigrations
$ python manage.py migrate
```
Create superuser:
```
$ python manage.py createsuperuser
```
Run Django App server:
```
$ python manage.py runserver
```
**Django deployment see [here](https://docs.djangoproject.com/en/3.0/howto/deployment/)**
### Used Libraries
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django-CORS-Headers](https://github.com/adamchainz/django-cors-headers)  
- [djoser](https://djoser.readthedocs.io/en/latest/getting_started.html)  
- [SimpleJWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt)  
- [python-dotenv](https://github.com/theskumar/python-dotenv)
    

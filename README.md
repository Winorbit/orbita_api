# Winterorbit API

#### requirements

  - Docker
  - docker-compose
  - OPTIONAL: for runing in Python virtual env - Python 3.7+ & pipenv
# How to run

  In Docker
```sh
$ sudo docker-comppose up --build
```
In Python virtual env - 
```sh
$ pipenv shell  
$ pipenv install   
$ python manage.py runserver
```  
`$ pipenv install --dev` команда установит все зависим, необходимые для разработки, и те, которые вы указали в аргументе –dev


#### Configuration

Service configuring via .env-file 

# Winterorbit API

#### requirements

  - Docker
  - docker-compose
  - OPTIONAL: for runing in Python virtual env - Python 3.7+ & pipenv

# How to run

In Docker
```sh
$ sudo docker-compose up --build
```
In Python virtual env - 
```sh
$ pipenv shell  
$ pipenv install   
$ python manage.py runserver
```  
команда установит все зависим, необходимые для разработки, и те, которые вы указали в аргументе –dev  
`$ pipenv install --dev`  

### TEST

```sh
$ pipenv shell  
$ pipenv sync   
$ python manage.py test api.tests
```



#### Configuration

Service configuring via .env-file 

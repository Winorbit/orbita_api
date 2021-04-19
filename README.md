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
команда установит все зависимости, необходимые для разработки, и те, которые вы указали в аргументе –dev  
`$ pipenv install --dev`  

### TEST

``` 
$ make test

OR

$ pipenv shell  
$ pipenv sync   
$ python manage.py test api.tests
```


### APPLY FIXTURE
In case of empty database you can apply fixtures to add some test data

``` 
$ python manage.py apply_fixtures <env>
example:
$ python manage.py apply_fixtures dev

```


#### Configuration

Service configuring via .env-file 

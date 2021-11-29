# rent-house-rating-api
## install project dependencies
```
pip install requirements.txt
```
## create table schemas in database
```
python manage.py makemigrations
python manage.py migrate
```
## insert initial data
```
python manage.py execute sqls
```
## API test
```
python manage.py test
```